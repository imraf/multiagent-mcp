import pytest
from unittest.mock import Mock
from mcp_customer.service import CustomerService
from mcp_customer.tools import create_register_customer_tool, create_update_customer_tool
from mcp_core.models import Customer


@pytest.fixture
def mock_service():
    return Mock(spec=CustomerService)


def test_register_customer_tool(mock_service):
    tool = create_register_customer_tool(mock_service)

    # Check schema
    assert "name" in tool.input_schema["properties"]
    assert "email" in tool.input_schema["properties"]

    # Mock return
    customer = Customer(id="c1", name="Test", email="t@e.com", vat_id=None, address=None)
    mock_service.add.return_value = customer

    # Execute
    result = tool.handler(name="Test", email="t@e.com")

    # Verify
    assert result["id"] == "c1"
    mock_service.add.assert_called_with(name="Test", email="t@e.com", vat_id=None, address=None)


def test_update_customer_tool(mock_service):
    tool = create_update_customer_tool(mock_service)

    # Check schema
    assert "customer_id" in tool.input_schema["properties"]
    assert "name" in tool.input_schema["properties"]

    # Mock return
    customer = Customer(id="c1", name="New", email="t@e.com", vat_id=None, address=None)
    mock_service.update.return_value = customer

    # Execute
    result = tool.handler(customer_id="c1", name="New")

    # Verify
    assert result["name"] == "New"
    mock_service.update.assert_called_with(
        customer_id="c1", name="New", email=None, vat_id=None, address=None
    )
