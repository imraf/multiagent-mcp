from unittest.mock import Mock

import pytest

from mcp_core.models import Customer
from mcp_customer.service import CustomerService


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def service(mock_repo):
    return CustomerService(mock_repo)


def test_add_customer(service, mock_repo):
    # Setup
    mock_repo.save.side_effect = lambda x: x

    # Execute
    result = service.add(name="Test Corp", email="test@example.com")

    # Verify
    assert result.name == "Test Corp"
    assert result.email == "test@example.com"
    mock_repo.save.assert_called_once()


def test_get_customer(service, mock_repo):
    # Setup
    customer = Customer(id="c1", name="Test", email="t@e.com", vat_id=None, address=None)
    mock_repo.get.return_value = customer

    # Execute
    result = service.get("c1")

    # Verify
    assert result == customer
    mock_repo.get.assert_called_with("c1")


def test_update_customer(service, mock_repo):
    # Setup
    customer = Customer(id="c1", name="Old", email="old@e.com", vat_id=None, address=None)
    mock_repo.get.return_value = customer
    mock_repo.save.side_effect = lambda x: x

    # Execute
    result = service.update("c1", name="New")

    # Verify
    assert result.name == "New"
    assert result.email == "old@e.com"  # Unchanged
    mock_repo.save.assert_called_once()


def test_update_missing_customer(service, mock_repo):
    mock_repo.get.return_value = None
    with pytest.raises(ValueError, match="Customer with ID missing not found"):
        service.update("missing", name="New")
