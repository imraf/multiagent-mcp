from typing import List, Optional
from uuid import uuid4
from mcp_core.models import Customer
from mcp_core.repository import Repository


class CustomerService:
    def __init__(self, repository: Repository[Customer]):
        self.repository = repository

    def add(
        self, name: str, email: str, vat_id: Optional[str] = None, address: Optional[str] = None
    ) -> Customer:
        """Add a new customer."""
        customer = Customer(id=str(uuid4()), name=name, email=email, vat_id=vat_id, address=address)
        return self.repository.save(customer)

    def get(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        return self.repository.get(customer_id)

    def list(self) -> List[Customer]:
        """List all customers."""
        return self.repository.list()

    def update(
        self,
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        vat_id: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Customer:
        """Update an existing customer."""
        customer = self.repository.get(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} not found")

        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        if vat_id is not None:
            customer.vat_id = vat_id
        if address is not None:
            customer.address = address

        return self.repository.save(customer)
