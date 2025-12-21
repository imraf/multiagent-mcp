import uuid
from typing import List, Optional
from decimal import Decimal
from .models import Invoice, InvoiceStatus, InvoiceItem
from .repository import Repository


class InvoiceService:
    def __init__(self, repository: Repository[Invoice]):
        self.repository = repository

    def create_draft(
        self, customer_id: str, items: List[InvoiceItem], tax_rate: Decimal = Decimal("0.0")
    ) -> Invoice:
        """
        Creates a new invoice in DRAFT status.
        ID generation is handled here.
        """
        invoice_id = str(uuid.uuid4())

        invoice = Invoice(
            id=invoice_id,
            customer_id=customer_id,
            items=items,
            status=InvoiceStatus.DRAFT,
            tax_rate=tax_rate,
            invoice_number=None,
        )
        return self.repository.save(invoice)

    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        return self.repository.get(invoice_id)

    def list_invoices(self) -> List[Invoice]:
        return self.repository.list()

    def update_draft(self, invoice: Invoice) -> Invoice:
        """
        Updates an existing draft invoice.
        Raises ValueError if invoice is not in DRAFT status.
        """
        existing = self.repository.get(invoice.id)
        if not existing:
            raise ValueError(f"Invoice {invoice.id} not found")

        if existing.status != InvoiceStatus.DRAFT:
            raise ValueError("Only draft invoices can be modified")

        # Ensure we are not accidentally changing the status via this method implicitly
        if invoice.status != InvoiceStatus.DRAFT:
            raise ValueError("Use specific transition methods to change invoice status")

        return self.repository.save(invoice)

    def finalize_invoice(self, invoice_id: str) -> Invoice:
        """
        Transitions an invoice from DRAFT to SENT (Issued).
        Assigns a sequential invoice number.
        """
        invoice = self.repository.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if invoice.status != InvoiceStatus.DRAFT:
            raise ValueError(
                f"Invoice must be in DRAFT state to finalize. Current state: {invoice.status}"
            )

        # Assign sequential number
        all_invoices = self.repository.list()
        max_num = 0
        for inv in all_invoices:
            if inv.invoice_number and inv.invoice_number.startswith("INV-"):
                try:
                    num_part = int(inv.invoice_number.split("-")[1])
                    if num_part > max_num:
                        max_num = num_part
                except (ValueError, IndexError):
                    continue

        next_num = max_num + 1
        invoice.invoice_number = f"INV-{next_num:04d}"
        invoice.status = InvoiceStatus.SENT

        return self.repository.save(invoice)

    def mark_paid(self, invoice_id: str) -> Invoice:
        invoice = self.repository.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if invoice.status != InvoiceStatus.SENT:
            raise ValueError(
                f"Invoice must be in SENT state to be marked paid. Current state: {invoice.status}"
            )

        invoice.status = InvoiceStatus.PAID
        return self.repository.save(invoice)

    def cancel_invoice(self, invoice_id: str) -> Invoice:
        invoice = self.repository.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if invoice.status == InvoiceStatus.PAID:
            raise ValueError("Cannot cancel a paid invoice")

        invoice.status = InvoiceStatus.CANCELLED
        return self.repository.save(invoice)
