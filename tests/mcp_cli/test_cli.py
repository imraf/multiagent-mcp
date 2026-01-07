from unittest.mock import patch

from typer.testing import CliRunner

from mcp_cli.main import app
from mcp_core.models import Customer, Invoice, InvoiceItem, InvoiceStatus

runner = CliRunner()


@patch("mcp_cli.main.client")
def test_cli_new_invoice(mock_client):
    # Setup mock
    mock_invoice = Invoice(
        id="inv_1",
        customer_id="cust1",
        items=[InvoiceItem(description="Item1", quantity=2, unit_price=50.0)],
        status=InvoiceStatus.DRAFT,
        total_amount=100.0,
        invoice_number=None
    )
    mock_client.create_invoice.return_value = mock_invoice

    # Since the client is mocked in the CLI file logic (or rather the class is used directly),
    # this tests the CLI wrapper.
    result = runner.invoke(app, ["new", "cust1", "Item1", "2", "50.0"])

    assert result.exit_code == 0
    assert "Creating invoice for customer cust1" in result.stdout
    assert "Invoice Created" in result.stdout
    assert "$100.00" in result.stdout


@patch("mcp_cli.main.client")
def test_cli_add_customer(mock_client):
    mock_customer = Customer(
        id="cust_1",
        name="NewCustomer",
        email="new@example.com"
    )
    mock_client.register_customer.return_value = mock_customer

    result = runner.invoke(app, ["customer-add", "NewCustomer", "new@example.com"])
    assert result.exit_code == 0
    assert "Customer added" in result.stdout
    assert "NewCustomer" in result.stdout

@patch("mcp_cli.main.client")
def test_cli_list_invoices(mock_client):
    mock_invoice = Invoice(
        id="inv_1",
        customer_id="cust1",
        items=[InvoiceItem(description="Test Item", quantity=1, unit_price=100.0)],
        status=InvoiceStatus.SENT
    )
    mock_client.list_invoices.return_value = [mock_invoice]

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Invoices (All)" in result.stdout
    assert "inv_1" in result.stdout
    assert "$100.00" in result.stdout

@patch("mcp_cli.main.client")
def test_cli_list_invoices_filter(mock_client):
    mock_invoice = Invoice(
        id="inv_2",
        customer_id="cust1",
        items=[],
        status=InvoiceStatus.DRAFT,
        total_amount=50.0
    )
    mock_client.list_invoices.return_value = [mock_invoice]

    result = runner.invoke(app, ["list", "--status", "draft"])
    assert result.exit_code == 0
    assert "Invoices (draft)" in result.stdout
    assert "draft" in result.stdout

