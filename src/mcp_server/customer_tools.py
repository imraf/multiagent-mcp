from mcp.server.fastmcp import FastMCP

from mcp_core.json_repository import JsonFileRepository
from mcp_core.models import Customer
from mcp_customer.service import CustomerService

# Initialize services
customer_repo = JsonFileRepository(Customer, "data/customers.json")
customer_service = CustomerService(customer_repo)


def register_customer_tools(mcp: FastMCP) -> None:
    """
    Registers customer-related tools with the MCP server.
    """

    @mcp.tool()
    def register_customer(
        name: str, email: str, vat_id: str | None = None, address: str | None = None
    ) -> str:
        """
        Register a new customer.

        Args:
            name: Full name or company name.
            email: Contact email address.
            vat_id: VAT ID if applicable.
            address: Billing address.

        Returns:
            JSON string representation of the created customer.
        """
        customer = customer_service.add(name=name, email=email, vat_id=vat_id, address=address)
        return str(customer.model_dump_json())
