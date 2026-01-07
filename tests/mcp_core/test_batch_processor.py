from decimal import Decimal
from unittest.mock import patch

from mcp_core.batch_processor import BatchInvoiceProcessor, _process_single_invoice_data
from mcp_core.invoice_service import InvoiceService
from mcp_core.models import Invoice, InvoiceStatus


class MockInvoiceService(InvoiceService):
    def __init__(self):
        self.created = []

    def create_draft(self, customer_id, items, tax_rate):
        invoice = Invoice(
            id=f"inv_{len(self.created)}",
            customer_id=customer_id,
            items=items,
            tax_rate=tax_rate,
            status=InvoiceStatus.DRAFT
        )
        self.created.append(invoice)
        return invoice

def test_process_single_invoice_data():
    # Test valid data
    data = {
        "customer_id": "c1",
        "items": [{"description": "Item 1", "quantity": 1, "unit_price": 10.0}],
        "tax_rate": 0.2
    }
    result = _process_single_invoice_data(data)
    assert result["success"] is True
    assert result["customer_id"] == "c1"
    assert len(result["items"]) == 1

    # Test invalid data
    data_bad: dict[str, Any] = {"items": []} # Missing customer_id
    result_bad = _process_single_invoice_data(data_bad)
    assert result_bad["success"] is False
    assert "error" in result_bad

def test_batch_processing():
    service = MockInvoiceService()
    processor = BatchInvoiceProcessor(service, processes=2)

    batch_data = [
        {
            "customer_id": "c1",
            "items": [{"description": "Item 1", "quantity": 1, "unit_price": 10.0}],
            "tax_rate": 0.2
        }
    ]

    # We want to verify the logic connecting pool results to service calls.
    # We can mock Pool.map to return prepared results.
    # This avoids multiprocessing complexity in coverage.

    mock_results = [
        {
            "success": True,
            "customer_id": "c1",
            "items": [],
            "tax_rate": Decimal("0.0")
        },
        {
            "success": False,
            "error": "some error"
        }
    ]

    with patch("multiprocessing.Pool") as MockPool:
        pool_instance = MockPool.return_value
        pool_instance.__enter__.return_value = pool_instance
        pool_instance.map.return_value = mock_results

        invoices = processor.process_batch(batch_data)

        assert len(invoices) == 1
        assert invoices[0].customer_id == "c1"
        # The second result failed, so no invoice created for it.
        assert len(service.created) == 1
