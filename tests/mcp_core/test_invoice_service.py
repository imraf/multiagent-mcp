import pytest
from decimal import Decimal
from typing import Dict, Any, Optional, List
from mcp_core.models import Invoice, InvoiceStatus, InvoiceItem
from mcp_core.invoice_service import InvoiceService
from mcp_core.repository import Repository


class InMemoryRepository(Repository[Invoice]):
    def __init__(self):
        self.data: Dict[str, Invoice] = {}

    def get(self, id: str) -> Optional[Invoice]:
        return self.data.get(id)

    def list(self) -> List[Invoice]:
        return list(self.data.values())

    def save(self, entity: Invoice) -> Invoice:
        self.data[entity.id] = entity
        return entity

    def delete(self, id: str) -> bool:
        if id in self.data:
            del self.data[id]
            return True
        return False


@pytest.fixture
def invoice_service():
    repo = InMemoryRepository()
    return InvoiceService(repo)


def test_create_draft(invoice_service):
    items = [InvoiceItem(description="Item 1", quantity=2, unit_price=Decimal("10.00"))]
    invoice = invoice_service.create_draft("cust-123", items, tax_rate=Decimal("0.21"))

    assert invoice.status == InvoiceStatus.DRAFT
    assert invoice.customer_id == "cust-123"
    assert len(invoice.items) == 1
    assert invoice.total_amount == Decimal("24.20")  # (2*10) * 1.21


def test_finalize_invoice_numbering(invoice_service):
    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]

    # Create two invoices
    inv1 = invoice_service.create_draft("c1", items)
    inv2 = invoice_service.create_draft("c2", items)

    # Finalize first
    finalized1 = invoice_service.finalize_invoice(inv1.id)
    assert finalized1.status == InvoiceStatus.SENT
    assert finalized1.invoice_number == "INV-0001"

    # Finalize second
    finalized2 = invoice_service.finalize_invoice(inv2.id)
    assert finalized2.status == InvoiceStatus.SENT
    assert finalized2.invoice_number == "INV-0002"


def test_cannot_finalize_invalid_state(invoice_service):
    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    inv = invoice_service.create_draft("c1", items)

    # Finalize moves to SENT
    invoice_service.finalize_invoice(inv.id)

    # Should be SENT now, so mark_paid works
    invoice_service.mark_paid(inv.id)

    # Now it is PAID. Cancelling should fail.
    with pytest.raises(ValueError, match="Cannot cancel a paid invoice"):
        invoice_service.cancel_invoice(inv.id)

    # Trying to finalize again (from PAID) should fail
    with pytest.raises(ValueError, match="must be in DRAFT state"):
        invoice_service.finalize_invoice(inv.id)


def test_financial_calculations():
    item1 = InvoiceItem(description="A", quantity=10, unit_price=Decimal("1.50"))  # 15.00
    item2 = InvoiceItem(description="B", quantity=2, unit_price=Decimal("5.00"))  # 10.00
    # Subtotal 25.00

    invoice = Invoice(id="test", customer_id="c", items=[item1, item2], tax_rate=Decimal("0.20"))

    assert invoice.subtotal == Decimal("25.00")
    assert invoice.tax_amount == Decimal("5.00")
    assert invoice.total_amount == Decimal("30.00")
