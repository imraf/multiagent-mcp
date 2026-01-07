from decimal import Decimal

import pytest
from pydantic import ValidationError

from mcp_core.json_repository import JsonFileRepository
from mcp_core.models import Customer, Invoice, InvoiceItem


@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "test_data.json"
    return str(file_path)

@pytest.fixture
def customer_repo(temp_json_file):
    return JsonFileRepository(Customer, temp_json_file)

def test_customer_validation():
    # Valid customer
    customer = Customer(
        id="c1",
        name="Test Corp",
        email="test@example.com",
        vat_id="US123456789"
    )
    assert customer.id == "c1"

    # Invalid email
    with pytest.raises(ValidationError):
        Customer(id="c2", name="Bad Email", email="not-an-email")

    # Invalid VAT format
    with pytest.raises(ValidationError):
        Customer(id="c3", name="Bad VAT", email="ok@example.com", vat_id="123")  # No country code

def test_invoice_calculations():
    item1 = InvoiceItem(description="Item 1", quantity=2, unit_price=Decimal("10.00"))
    item2 = InvoiceItem(description="Item 2", quantity=1, unit_price=Decimal("20.00"))

    invoice = Invoice(
        id="inv1",
        customer_id="c1",
        items=[item1, item2],
        tax_rate=Decimal("0.20")  # 20% tax
    )

    assert item1.total == Decimal("20.00")
    assert item2.total == Decimal("20.00")
    assert invoice.subtotal == Decimal("40.00")
    assert invoice.tax_amount == Decimal("8.00")
    assert invoice.total_amount == Decimal("48.00")

def test_repository_crud(customer_repo):
    customer = Customer(id="c1", name="Test Corp", email="test@example.com")

    # Save (Create)
    saved = customer_repo.save(customer)
    assert saved.version == 1

    # Get
    retrieved = customer_repo.get("c1")
    assert retrieved is not None
    assert retrieved.name == "Test Corp"
    assert retrieved.version == 1

    # Update
    retrieved.name = "Updated Corp"
    updated = customer_repo.save(retrieved)
    assert updated.version == 2

    # Verify update persisted
    final = customer_repo.get("c1")
    assert final.name == "Updated Corp"
    assert final.version == 2

    # List
    all_customers = customer_repo.list()
    assert len(all_customers) == 1
    assert all_customers[0].id == "c1"

    # Delete
    deleted = customer_repo.delete("c1")
    assert deleted is True
    assert customer_repo.get("c1") is None

def test_optimistic_locking(customer_repo):
    customer = Customer(id="lock_test", name="Lock Test", email="lock@test.com")
    customer_repo.save(customer)

    # Simulate two users fetching the same record
    user1_copy = customer_repo.get("lock_test")
    user2_copy = customer_repo.get("lock_test")

    # User 1 updates
    user1_copy.name = "User 1 Update"
    customer_repo.save(user1_copy)

    # User 2 tries to update with stale version
    user2_copy.name = "User 2 Update"
    with pytest.raises(ValueError, match="Optimistic locking failure"):
        customer_repo.save(user2_copy)
