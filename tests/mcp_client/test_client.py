from decimal import Decimal
from unittest.mock import MagicMock, patch

from mcp_client.client import InvoicingClient


@patch("mcp_client.client.InvoicingClient._listen_sse")  # Prevent thread start
@patch("mcp_client.client.InvoicingClient._call_tool")
def test_create_invoice_mock(mock_call_tool, mock_listen):
    # Mock return value from _call_tool (simulating decoded JSON)
    mock_call_tool.return_value = {
        "id": "draft_id",
        "customer_id": "cust1",
        "status": "draft",
        "items": [{"description": "test", "quantity": 1, "unit_price": "10.0"}],
        "tax_rate": "0.0",
        "invoice_number": None,
        "version": 0,
    }

    client = InvoicingClient()
    invoice = client.create_invoice(
        "cust1", [{"description": "test", "quantity": 1, "unit_price": 10.0}]
    )

    assert invoice.customer_id == "cust1"
    assert len(invoice.items) == 1
    assert invoice.items[0].description == "test"
    assert invoice.total_amount == Decimal("10.0")


@patch("mcp_client.client.InvoicingClient._listen_sse")
@patch("mcp_client.client.InvoicingClient._call_tool")
def test_register_customer_mock(mock_call_tool, mock_listen):
    mock_call_tool.return_value = {
        "id": "cust_123",
        "name": "Acme Corp",
        "email": "contact@acme.com",
        "vat_id": None,
        "address": None,
        "version": 0,
    }

    client = InvoicingClient()
    customer = client.register_customer("Acme Corp", "contact@acme.com")
    assert customer.name == "Acme Corp"
    assert customer.email == "contact@acme.com"


def test_handle_message():
    """Test that _handle_message updates pending requests correctly."""
    with patch("mcp_client.client.InvoicingClient._listen_sse"):
        client = InvoicingClient()

        # Setup a pending request
        req_id = "test-id"
        event = MagicMock()
        client._pending_requests[req_id] = {"event": event, "result": None}

        # Handle response
        message = {"jsonrpc": "2.0", "id": req_id, "result": {"foo": "bar"}}
        client._handle_message(message)

        # Verify
        assert client._pending_requests[req_id]["result"] == message
        event.set.assert_called_once()


@patch("httpx.Client")
def test_call_tool_success(mock_httpx_cls):
    """Test _call_tool success path."""
    mock_client_instance = mock_httpx_cls.return_value

    # Mock post to succeed
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_client_instance.post.return_value = mock_response

    # We need to simulate the SSE listener receiving the response while _call_tool waits.
    # We can do this by using a side_effect on post that triggers the logic.
    # However, since we are mocking the class,
    # we can just patch InvoicingClient._listen_sse to avoid the thread.

    with patch("mcp_client.client.InvoicingClient._listen_sse"):
        client = InvoicingClient()
        client.client = mock_client_instance  # Ensure we use the mock

        # We need to hook into when `post` is called to simulate the response arriving.
        def side_effect(*args, **kwargs):
            # args[0] is the url path '/messages'
            # json payload has the ID
            payload = kwargs.get("json")
            req_id = payload["id"]

            # Simulate response arrival
            response_message = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": '{"foo": "bar"}'}]},
            }
            client._handle_message(response_message)
            return mock_response

        mock_client_instance.post.side_effect = side_effect

        result = client._call_tool("some_tool", {})
        assert result == {"foo": "bar"}


@patch("httpx.Client")
def test_call_tool_timeout(mock_httpx_cls):
    """Test _call_tool timeout."""
    mock_client_instance = mock_httpx_cls.return_value
    mock_client_instance.post.return_value.raise_for_status.return_value = None

    with patch("mcp_client.client.InvoicingClient._listen_sse"):
        client = InvoicingClient()
        client.client = mock_client_instance

        # We mock threading.Event.wait to return False (timeout)
        with patch("threading.Event.wait", return_value=False):
            try:
                client._call_tool("some_tool", {})
                raise AssertionError("Should have raised TimeoutError")
            except TimeoutError:
                pass


@patch("httpx.Client")
def test_call_tool_api_error(mock_httpx_cls):
    """Test _call_tool when API returns error."""
    mock_client_instance = mock_httpx_cls.return_value

    with patch("mcp_client.client.InvoicingClient._listen_sse"):
        client = InvoicingClient()
        client.client = mock_client_instance

        def side_effect(*args, **kwargs):
            payload = kwargs.get("json")
            req_id = payload["id"]
            response_message = {"jsonrpc": "2.0", "id": req_id, "error": "Something went wrong"}
            client._handle_message(response_message)
            return MagicMock()  # response object

        mock_client_instance.post.side_effect = side_effect

        try:
            client._call_tool("some_tool", {})
            raise AssertionError("Should have raised RuntimeError")
        except RuntimeError as e:
            assert "Something went wrong" in str(e)
