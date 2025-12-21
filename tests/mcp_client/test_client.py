import pytest
from mcp_client.client import InvoicingClient
from mcp_core.models import Invoice


def test_create_invoice_mock():
    client = InvoicingClient()
    invoice = client.create_invoice(
        "cust1", [{"description": "test", "quantity": 1, "unit_price": 10.0}]
    )
    assert invoice.customer_id == "cust1"
    assert len(invoice.items) == 1
    assert invoice.items[0].description == "test"
    assert invoice.total_amount == 10.0


def test_register_customer_mock():
    client = InvoicingClient()
    customer = client.register_customer("Acme Corp", "contact@acme.com")
    assert customer.name == "Acme Corp"
    assert customer.email == "contact@acme.com"
