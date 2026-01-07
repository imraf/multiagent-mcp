from typing import Any

from pydantic import BaseModel, Field

from mcp_core.tool import Tool
from mcp_customer.service import CustomerService


class RegisterCustomerInput(BaseModel):
    name: str = Field(..., description="Full name or company name")
    email: str = Field(..., description="Contact email address")
    vat_id: str | None = Field(None, description="VAT ID if applicable")
    address: str | None = Field(None, description="Billing address")


def create_register_customer_tool(service: CustomerService) -> Tool:
    def handler(
        name: str, email: str, vat_id: str | None = None, address: str | None = None
    ) -> dict[str, Any]:
        customer = service.add(name=name, email=email, vat_id=vat_id, address=address)
        return customer.model_dump(mode="json")

    return Tool(
        name="register_customer",
        description="Register a new customer",
        input_schema=RegisterCustomerInput.model_json_schema(),
        handler=handler,
    )


class UpdateCustomerInput(BaseModel):
    customer_id: str = Field(..., description="Unique identifier of the customer to update")
    name: str | None = Field(None, description="New full name or company name")
    email: str | None = Field(None, description="New contact email address")
    vat_id: str | None = Field(None, description="New VAT ID")
    address: str | None = Field(None, description="New billing address")


def create_update_customer_tool(service: CustomerService) -> Tool:
    def handler(
        customer_id: str,
        name: str | None = None,
        email: str | None = None,
        vat_id: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any]:
        customer = service.update(
            customer_id=customer_id, name=name, email=email, vat_id=vat_id, address=address
        )
        return customer.model_dump(mode="json")

    return Tool(
        name="update_customer",
        description="Update an existing customer's details",
        input_schema=UpdateCustomerInput.model_json_schema(),
        handler=handler,
    )
