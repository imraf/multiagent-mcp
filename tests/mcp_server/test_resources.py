import pytest
from unittest.mock import Mock
from decimal import Decimal
from mcp_core.models import Invoice, InvoiceStatus, InvoiceItem, Customer
from mcp_server.invoice_resources import InvoiceResourceProvider
from mcp_customer.resources import CustomerResourceProvider


@pytest.fixture
def mock_invoice_service():
    service = Mock()

    # Mock Invoice
    invoice = Invoice(
        id="inv-123",
        customer_id="cust-123",
        invoice_number="INV-2023-001",
        status=InvoiceStatus.SENT,
        items=[InvoiceItem(description="Service A", quantity=10, unit_price=Decimal("100.00"))],
        tax_rate=Decimal("0.2"),
    )

    service.get_invoice.return_value = invoice
    service.list_invoices.return_value = [invoice]
    return service


@pytest.fixture
def mock_customer_service():
    service = Mock()

    # Mock Customer
    customer = Customer(id="cust-123", name="Acme Corp", email="billing@acme.com")

    service.get.return_value = customer
    service.list.return_value = [customer]
    return service


def test_invoice_pdf_resource_resolution(mock_invoice_service):
    provider = InvoiceResourceProvider(mock_invoice_service)

    # Test valid URI
    resource = provider.get_resource("invoice://inv-123/pdf")
    assert resource is not None
    assert resource.uri == "invoice://inv-123/pdf"
    assert "INV-2023-001" in resource.text
    assert "Service A" in resource.text
    assert "1000.00" in resource.text  # 10 * 100

    # Test invalid URI scheme
    assert provider.get_resource("file://inv-123/pdf") is None

    # Test invalid resource type
    assert provider.get_resource("invoice://inv-123/json") is None

    # Test non-existent invoice
    mock_invoice_service.get_invoice.return_value = None
    assert provider.get_resource("invoice://missing/pdf") is None


def test_invoice_resource_list(mock_invoice_service):
    provider = InvoiceResourceProvider(mock_invoice_service)
    resources = provider.list_resources()

    assert len(resources) == 1
    assert resources[0].uri == "invoice://inv-123/pdf"


def test_customer_ledger_resource_resolution(mock_customer_service, mock_invoice_service):
    provider = CustomerResourceProvider(mock_customer_service, mock_invoice_service)

    # Test valid URI
    resource = provider.get_resource("customer://cust-123/ledger")
    assert resource is not None
    assert resource.uri == "customer://cust-123/ledger"
    assert "Acme Corp" in resource.text
    assert "INV-2023-001" in resource.text
    assert "SENT" in resource.text

    # Test invalid URI
    assert provider.get_resource("customer://cust-123/details") is None

    # Test non-existent customer
    mock_customer_service.get.return_value = None
    assert provider.get_resource("customer://missing/ledger") is None
