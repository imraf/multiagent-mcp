import json
import threading
import time
import uuid
from typing import Any

import httpx

from mcp_core.models import Customer, Invoice, InvoiceStatus

__all__ = ["Customer", "Invoice", "InvoiceStatus", "InvoicingClient"]


class InvoicingClient:
    """
    Fluent Python client for the MCP Invoicing System.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=30.0)
        self._pending_requests: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._listening = True
        self._thread = threading.Thread(target=self._listen_sse, daemon=True)
        self._thread.start()
        # Give some time for connection
        time.sleep(0.5)

    def _listen_sse(self) -> None:
        """Background thread to listen for SSE events."""
        retry_count = 0
        while self._listening:
            try:
                with httpx.Client(base_url=self.base_url, timeout=None) as client:  # nosec B113
                    with client.stream("GET", "/events") as response:
                        for line in response.iter_lines():
                            if not self._listening:
                                break
                            if line.startswith("data: "):
                                data_str = line[6:]
                                try:
                                    data = json.loads(data_str)
                                    self._handle_message(data)
                                    retry_count = 0  # Reset retry on success
                                except json.JSONDecodeError:
                                    pass
            except Exception as e:
                if not self._listening:
                    break
                print(f"SSE Connection Error: {e}. Retrying...")
                retry_count += 1
                time.sleep(min(retry_count * 1.0, 10.0))

    def _handle_message(self, message: dict[str, Any]) -> None:
        """Process incoming JSON-RPC message."""
        # Expecting JSON-RPC response
        # {"jsonrpc": "2.0", "result": ..., "id": ...} or error
        req_id = message.get("id")

        # Depending on the server implementation, the ID might be an integer or string.
        # We try to match it as string.
        if req_id is not None:
            req_id_str = str(req_id)
            with self._lock:
                if req_id_str in self._pending_requests:
                    self._pending_requests[req_id_str]["result"] = message
                    self._pending_requests[req_id_str]["event"].set()

    def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Helper to call MCP tools via HTTP POST and wait for SSE response."""
        req_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": req_id,
        }

        event = threading.Event()
        with self._lock:
            self._pending_requests[req_id] = {"event": event, "result": None}

        try:
            response = self.client.post("/messages", json=payload)
            response.raise_for_status()

            # Wait for SSE response
            if not event.wait(timeout=10.0):
                raise TimeoutError(f"Timeout waiting for tool {tool_name}")

            # Safe to read directly as only this thread waits on event,
            # and writer thread (SSE listener) only writes before setting event.
            # But technically cleaner to lock if we want to be purists,
            # however _pending_requests is modified by listener.
            # The dictionary entry itself is shared state.
            # We already hold the reference to the entry (conceptually),
            # but we should lock to read 'result'
            # if we want to be strictly correct, although event.wait acts as memory barrier.
            # But let's check keys again to be safe?
            # Actually, we popped it below.
            # Let's just access it.
            result_message = self._pending_requests[req_id]["result"]

            if "error" in result_message:
                raise RuntimeError(f"Tool error: {result_message['error']}")

            return self._parse_mcp_result(result_message.get("result"))

        finally:
            with self._lock:
                self._pending_requests.pop(req_id, None)

    def _parse_mcp_result(self, result: Any) -> Any:
        """Extract the actual return value from the MCP tool result structure."""
        # FastMCP / MCP SDK usually returns { "content": [ {"type": "text", "text": "..."} ] }
        if isinstance(result, dict) and "content" in result:
            content = result["content"]
            if isinstance(content, list) and len(content) > 0:
                text = content[0].get("text")
                # The tool might return a JSON string (Invoice) or just a string/dict
                # We try to parse it as JSON if it looks like it, otherwise return as is.
                try:
                    if isinstance(text, str) and (text.startswith("{") or text.startswith("[")):
                        return json.loads(text)
                    return text
                except (json.JSONDecodeError, TypeError):
                    return text

        # Fallback if structure is different
        return result

    def close(self) -> None:
        """Stop the SSE listener."""
        self._listening = False
        # Thread will exit on next loop or exception

    def create_invoice(
        self, customer_id: str, items: list[dict[str, Any]], tax_rate: float = 0.0
    ) -> Invoice:
        arguments = {"customer_id": customer_id, "items": items, "tax_rate": tax_rate}
        result_json = self._call_tool("create_draft_invoice", arguments)
        return Invoice.model_validate(result_json)

    def get_invoice(self, invoice_id: str) -> Invoice | None:
        result_json = self._call_tool("get_invoice", {"invoice_id": invoice_id})
        if isinstance(result_json, str) and result_json.startswith("Error"):
            return None
        return Invoice.model_validate(result_json)

    def finalize_invoice(self, invoice_id: str) -> Invoice | None:
        result_json = self._call_tool("finalize_invoice", {"invoice_id": invoice_id})
        return Invoice.model_validate(result_json)

    def register_customer(
        self, name: str, email: str, vat_id: str | None = None, address: str | None = None
    ) -> Customer:
        arguments = {"name": name, "email": email, "vat_id": vat_id, "address": address}
        result_json = self._call_tool("register_customer", arguments)
        return Customer.model_validate(result_json)

    def list_invoices(self, status: InvoiceStatus | None = None) -> list[Invoice]:
        try:
            result_json = self._call_tool(
                "list_invoices", {"status": status.value if status else None}
            )
            return [Invoice.model_validate(item) for item in result_json]
        except RuntimeError:
            # If tool not found
            return []
