import re
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


class Customer(BaseModel):
    id: str = Field(..., description="Unique identifier for the customer")
    name: str = Field(..., min_length=1, description="Full name or company name")
    email: EmailStr = Field(..., description="Contact email address")
    vat_id: str | None = Field(None, description="VAT ID if applicable")
    address: str | None = Field(None, description="Billing address")
    version: int = Field(default=0, description="Version number for optimistic locking")

    @field_validator("vat_id")
    @classmethod
    def validate_vat_id(cls, v: str | None) -> str | None:
        if v is None:
            return v
        # Basic alphanumeric check for VAT ID, can be expanded for specific country codes
        if not re.match(r"^[A-Z]{2}[A-Z0-9]+$", v):
            raise ValueError(
                "Invalid VAT ID format. Must start with 2 country letters followed by alphanumeric characters."
            )
        return v


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    CANCELLED = "cancelled"


class InvoiceItem(BaseModel):
    description: str = Field(..., min_length=1, description="Item description")
    quantity: int = Field(..., gt=0, description="Quantity of items")
    unit_price: Decimal = Field(..., gt=0, decimal_places=2, description="Price per unit")

    @property
    def total(self) -> Decimal:
        return self.quantity * self.unit_price


class Invoice(BaseModel):
    id: str = Field(..., description="Unique invoice identifier")
    invoice_number: str | None = Field(
        None, description="Official sequential invoice number (assigned when finalized)"
    )
    customer_id: str = Field(..., description="ID of the customer this invoice belongs to")
    items: list[InvoiceItem] = Field(default_factory=list, description="List of invoice items")
    status: InvoiceStatus = Field(
        default=InvoiceStatus.DRAFT, description="Current status of the invoice"
    )
    tax_rate: Decimal = Field(
        default=Decimal("0.0"), ge=0, le=1, description="Tax rate as a decimal (e.g. 0.21 for 21%)"
    )
    version: int = Field(default=0, description="Version number for optimistic locking")

    @property
    def subtotal(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal("0.00"))

    @property
    def tax_amount(self) -> Decimal:
        return self.subtotal * self.tax_rate

    @property
    def total_amount(self) -> Decimal:
        return self.subtotal + self.tax_amount
