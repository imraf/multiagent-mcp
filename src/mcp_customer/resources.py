from typing import List, Optional
from mcp_core.resource import ResourceProvider, Resource
from mcp_customer.service import CustomerService
from mcp_core.invoice_service import InvoiceService


class CustomerResourceProvider(ResourceProvider):
    """
    Provides customer-related resources.
    URI schemes:
      - customer://{id}/ledger: Transaction history
    """

    def __init__(self, customer_service: CustomerService, invoice_service: InvoiceService):
        self.customer_service = customer_service
        self.invoice_service = invoice_service

    def get_resource(self, uri: str) -> Optional[Resource]:
        if not uri.startswith("customer://"):
            return None

        # Parse URI: customer://{id}/ledger
        parts = uri.replace("customer://", "").split("/")
        if len(parts) != 2 or parts[1] != "ledger":
            return None

        customer_id = parts[0]
        customer = self.customer_service.get(customer_id)

        if not customer:
            return None

        return self._create_ledger_resource(customer, uri)

    def list_resources(self) -> List[Resource]:
        resources = []
        customers = self.customer_service.list()
        for customer in customers:
            uri = f"customer://{customer.id}/ledger"
            resources.append(self._create_ledger_resource(customer, uri))
        return resources

    def _create_ledger_resource(self, customer, uri: str) -> Resource:
        """Helper to create the ledger resource from a customer."""

        # Get all invoices for this customer to build the ledger
        all_invoices = self.invoice_service.list_invoices()
        customer_invoices = [inv for inv in all_invoices if inv.customer_id == customer.id]

        # Build ledger content
        content = f"""
CUSTOMER LEDGER
-----------------------------------
Customer: {customer.name} ({customer.id})
Email: {customer.email}

TRANSACTIONS:
"""
        total_billed = 0
        for inv in customer_invoices:
            status = inv.status.value.upper()
            date_str = inv.id  # Mocking date with ID for now as per models
            amount = inv.total_amount
            total_billed += amount

            content += (
                f"- {date_str} | Invoice #{inv.invoice_number or 'DRAFT'} | {status} | ${amount}\n"
            )

        content += f"""
-----------------------------------
Total Billed: ${total_billed}
"""

        return Resource(
            uri=uri,
            name=f"Customer Ledger: {customer.name}",
            description="Transaction history for the customer",
            mime_type="text/plain",
            text=content,
        )
