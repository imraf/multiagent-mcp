from decimal import Decimal

import pytest

from mcp_core.invoice_service import InvoiceService
from mcp_core.models import Invoice, InvoiceItem, InvoiceStatus
from mcp_core.repository import Repository


class InMemoryRepository(Repository[Invoice]):
    def __init__(self):
        self.data: dict[str, Invoice] = {}

    def get(self, id: str) -> Invoice | None:
        return self.data.get(id)

    def list(self) -> list[Invoice]:
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


def test_update_draft(invoice_service):
    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    inv = invoice_service.create_draft("c1", items)

    # Update logic
    inv.customer_id = "c2"
    updated = invoice_service.update_draft(inv)
    assert updated.customer_id == "c2"

    # Fail if not found
    inv_fake = Invoice(id="fake", customer_id="c", items=[])
    with pytest.raises(ValueError, match="not found"):
        invoice_service.update_draft(inv_fake)

    # Fail if not DRAFT (update the stored one to SENT)
    inv.status = InvoiceStatus.SENT
    invoice_service.repository.save(inv)

    with pytest.raises(ValueError, match="Only draft invoices can be modified"):
        invoice_service.update_draft(inv)

    # Fail if implicitly changing status
    inv.status = InvoiceStatus.DRAFT  # Reset
    invoice_service.repository.save(inv)

    inv_modified = inv.model_copy()
    inv_modified.status = InvoiceStatus.SENT
    with pytest.raises(ValueError, match="Use specific transition methods"):
        invoice_service.update_draft(inv_modified)


def test_mark_paid_errors(invoice_service):
    with pytest.raises(ValueError, match="not found"):
        invoice_service.mark_paid("fake")

    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    inv = invoice_service.create_draft("c1", items)

    with pytest.raises(ValueError, match="must be in SENT state"):
        invoice_service.mark_paid(inv.id)


def test_cancel_invoice(invoice_service):
    with pytest.raises(ValueError, match="not found"):
        invoice_service.cancel_invoice("fake")

    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    inv = invoice_service.create_draft("c1", items)

    cancelled = invoice_service.cancel_invoice(inv.id)
    assert cancelled.status == InvoiceStatus.CANCELLED


def test_list_invoices(invoice_service):
    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    invoice_service.create_draft("c1", items)
    invoice_service.create_draft("c2", items)

    assert len(invoice_service.list_invoices()) == 2  # noqa: PLR2004


def test_get_invoice(invoice_service):
    assert invoice_service.get_invoice("fake") is None

    items = [InvoiceItem(description="Item", quantity=1, unit_price=Decimal("100"))]
    inv = invoice_service.create_draft("c1", items)
    assert invoice_service.get_invoice(inv.id).id == inv.id


def test_finalize_error_not_found(invoice_service):
    with pytest.raises(ValueError, match="not found"):
        invoice_service.finalize_invoice("fake")
