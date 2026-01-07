from decimal import Decimal
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_core.batch_processor import BatchInvoiceProcessor
from mcp_core.invoice_service import InvoiceService
from mcp_core.json_repository import JsonFileRepository
from mcp_core.models import Invoice, InvoiceItem

# Initialize services (could be dependency injected or configured externally)
invoice_repo = JsonFileRepository(Invoice, "data/invoices.json")
invoice_service = InvoiceService(invoice_repo)
batch_processor = BatchInvoiceProcessor(invoice_service)


def register_invoice_tools(mcp: FastMCP) -> None:
    """
    Registers invoice-related tools with the MCP server.
    """

    @mcp.tool()
    def create_draft_invoice(
        customer_id: str, items: list[dict[str, Any]], tax_rate: float = 0.0
    ) -> str:
        """
        Creates a new draft invoice.

        Args:
            customer_id: The ID of the customer.
            items: List of items, each with 'description', 'quantity', and 'unit_price'.
            tax_rate: Tax rate as a decimal (e.g., 0.21 for 21%).

        Returns:
            JSON string representation of the created invoice.
        """
        invoice_items = []
        for item in items:
            invoice_items.append(
                InvoiceItem(
                    description=item["description"],
                    quantity=item["quantity"],
                    unit_price=Decimal(str(item["unit_price"])),
                )
            )

        invoice = invoice_service.create_draft(
            customer_id=customer_id, items=invoice_items, tax_rate=Decimal(str(tax_rate))
        )
        return str(invoice.model_dump_json())

    @mcp.tool()
    def batch_create_invoices(batch_data: list[dict[str, Any]]) -> str:
        """
        Creates multiple draft invoices in batch.

        Args:
            batch_data: List of invoice data dictionaries. Each dict should have:
                        - customer_id (str)
                        - items (list of dicts with description, quantity, unit_price)
                        - tax_rate (float, optional)

        Returns:
            JSON string list of created invoices.
        """
        invoices = batch_processor.process_batch(batch_data)
        return str("[" + ",".join(inv.model_dump_json() for inv in invoices) + "]")

    @mcp.tool()
    def finalize_invoice(invoice_id: str) -> str:
        """
        Finalizes a draft invoice, assigning it an official invoice number.
        The invoice status changes from DRAFT to SENT.

        Args:
            invoice_id: The ID of the draft invoice.

        Returns:
            JSON string representation of the finalized invoice.
        """
        invoice = invoice_service.finalize_invoice(invoice_id)
        return str(invoice.model_dump_json())

    @mcp.tool()
    def get_invoice(invoice_id: str) -> str:
        """
        Retrieves an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice.

        Returns:
             JSON string representation of the invoice, or error message if not found.
        """
        invoice = invoice_service.get_invoice(invoice_id)
        if invoice:
            return str(invoice.model_dump_json())
        return f"Error: Invoice {invoice_id} not found"

    @mcp.tool()
    def list_invoices(status: str | None = None) -> str:
        """
        List all invoices, optionally filtered by status.

        Args:
            status: Optional status to filter by (draft, sent, paid, cancelled).

        Returns:
            JSON string representation of the list of invoices.
        """
        invoices = invoice_service.list_invoices()
        if status:
            invoices = [inv for inv in invoices if inv.status.value == status]

        # Serialize list of models
        return str("[" + ",".join(inv.model_dump_json() for inv in invoices) + "]")

    @mcp.tool()
    def deliver_invoice(invoice_id: str, method: str = "email") -> str:
        """
        Simulates delivery of an invoice to the customer.

        Args:
            invoice_id: The ID of the invoice to deliver.
            method: Delivery method (default: "email").

        Returns:
            Success message.
        """
        invoice = invoice_service.get_invoice(invoice_id)
        if not invoice:
            return f"Error: Invoice {invoice_id} not found"

        # In a real system this would send an email.
        # For now, we just log/return success.
        return f"Invoice {invoice.invoice_number or invoice.id} delivered via {method}."

    @mcp.tool()
    def void_invoice(invoice_id: str, reason: str) -> str:
        """
        Cancels (voids) an invoice.

        Args:
            invoice_id: The ID of the invoice to cancel.
            reason: Reason for cancellation.

        Returns:
            JSON string of the cancelled invoice.
        """
        # Logic to append reason to internal notes/audit trail could be added here
        # For now, just change status.
        invoice = invoice_service.cancel_invoice(invoice_id)
        return str(invoice.model_dump_json())
