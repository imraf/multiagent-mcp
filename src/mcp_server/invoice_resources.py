
from mcp_core.invoice_service import InvoiceService
from mcp_core.models import Invoice
from mcp_core.resource import Resource, ResourceProvider


class InvoiceResourceProvider(ResourceProvider):
    """
    Provides invoice-related resources.
    URI schemes:
      - invoice://{id}/pdf: Virtual PDF representation (text/mock)
    """

    def __init__(self, invoice_service: InvoiceService):
        self.invoice_service = invoice_service

    def get_resource(self, uri: str) -> Resource | None:
        if not uri.startswith("invoice://"):
            return None

        # Parse URI: invoice://{id}/pdf
        parts = uri.replace("invoice://", "").split("/")
        if len(parts) != 2 or parts[1] != "pdf":
            return None

        invoice_id = parts[0]
        invoice = self.invoice_service.get_invoice(invoice_id)

        if not invoice:
            return None

        return self._create_pdf_resource(invoice, uri)

    def list_resources(self) -> list[Resource]:
        # For dynamic resources, we might return a list of all invoices
        # or just a template explanation. Here we list all available invoices as resources.
        resources = []
        invoices = self.invoice_service.list_invoices()
        for invoice in invoices:
            uri = f"invoice://{invoice.id}/pdf"
            resources.append(self._create_pdf_resource(invoice, uri))
        return resources

    def _create_pdf_resource(self, invoice: Invoice, uri: str) -> Resource:
        """Helper to create the PDF resource from an invoice."""

        # Virtual PDF content (mocked as text for this primitive)
        content = f"""
INVOICE #{invoice.invoice_number or "DRAFT"}
-----------------------------------
Date: {invoice.id} (Created)
Customer ID: {invoice.customer_id}
Status: {invoice.status.value}

ITEMS:
"""
        for item in invoice.items:
            content += f"- {item.description}: {item.quantity} x {item.unit_price} = {item.total}\n"

        content += f"""
-----------------------------------
Subtotal: {invoice.subtotal}
Tax ({int(invoice.tax_rate * 100)}%): {invoice.tax_amount}
TOTAL: {invoice.total_amount}
"""

        return Resource(
            uri=uri,
            name=f"Invoice PDF {invoice.invoice_number or invoice.id}",
            description="Virtual PDF representation of the invoice",
            mime_type="text/plain",  # Using text/plain for this 'virtual' PDF as per instructions
            text=content,
        )
