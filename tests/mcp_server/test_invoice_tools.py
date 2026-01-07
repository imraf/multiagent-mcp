import sys
from unittest.mock import MagicMock

# Mock mcp module before importing mcp_server.tools
mcp_mock = MagicMock()
sys.modules["mcp"] = mcp_mock
sys.modules["mcp.server"] = mcp_mock
sys.modules["mcp.server.fastmcp"] = mcp_mock

import json
from decimal import Decimal

import pytest

from mcp_server.tools import register_invoice_tools


# Mock FastMCP
class MockFastMCP:
    def __init__(self):
        self.tools = {}

    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator


@pytest.fixture
def mcp():
    return MockFastMCP()


@pytest.fixture
def mock_invoice_service():
    # We patch the global invoice_service used in tools.py
    # Ideally, tools.py would allow injection, but for this test we mock the import/global
    pass


def test_create_draft_invoice_tool(mcp):
    # Setup
    register_invoice_tools(mcp)
    create_tool = mcp.tools["create_draft_invoice"]

    # Execute
    items = [{"description": "Test Item", "quantity": 1, "unit_price": 100.0}]
    result_json = create_tool(customer_id="cust-1", items=items, tax_rate=0.2)

    # Verify
    result = json.loads(result_json)
    assert result["customer_id"] == "cust-1"
    assert result["status"] == "draft"
    assert len(result["items"]) == 1
    assert result["items"][0]["description"] == "Test Item"
    assert Decimal(result["items"][0]["unit_price"]) == Decimal("100.0")


def test_finalize_invoice_tool(mcp):
    register_invoice_tools(mcp)

    # First create a draft to get a real ID (using the actual service underlying the tool)
    items = [{"description": "Test", "quantity": 1, "unit_price": 10.0}]
    draft_json = mcp.tools["create_draft_invoice"](customer_id="c1", items=items)
    draft = json.loads(draft_json)

    # Finalize
    final_json = mcp.tools["finalize_invoice"](invoice_id=draft["id"])
    final = json.loads(final_json)

    assert final["status"] == "sent"
    assert final["invoice_number"].startswith("INV-")


def test_void_invoice_tool(mcp):
    register_invoice_tools(mcp)

    # Create draft
    items = [{"description": "Test", "quantity": 1, "unit_price": 10.0}]
    draft_json = mcp.tools["create_draft_invoice"](customer_id="c1", items=items)
    draft = json.loads(draft_json)

    # Void
    voided_json = mcp.tools["void_invoice"](invoice_id=draft["id"], reason="Mistake")
    voided = json.loads(voided_json)

    assert voided["status"] == "cancelled"


def test_deliver_invoice_tool(mcp):
    register_invoice_tools(mcp)

    # Create draft
    items = [{"description": "Test", "quantity": 1, "unit_price": 10.0}]
    draft_json = mcp.tools["create_draft_invoice"](customer_id="c1", items=items)
    draft = json.loads(draft_json)

    # Deliver
    result = mcp.tools["deliver_invoice"](invoice_id=draft["id"], method="email")
    assert "delivered via email" in result


def test_list_invoices_tool(mcp):
    register_invoice_tools(mcp)

    # Create two drafts
    items = [{"description": "Test", "quantity": 1, "unit_price": 10.0}]
    mcp.tools["create_draft_invoice"](customer_id="c1", items=items)
    mcp.tools["create_draft_invoice"](customer_id="c2", items=items)

    # List all
    list_json = mcp.tools["list_invoices"]()
    invoices = json.loads(list_json)
    assert len(invoices) >= 2

    # Filter (should be empty if we ask for paid)
    list_paid_json = mcp.tools["list_invoices"](status="paid")
    paid_invoices = json.loads(list_paid_json)
    assert len(paid_invoices) == 0

def test_get_invoice_error(mcp):
    register_invoice_tools(mcp)

    result = mcp.tools["get_invoice"](invoice_id="non-existent")
    assert "Error" in result
    assert "not found" in result

def test_deliver_invoice_error(mcp):
    register_invoice_tools(mcp)

    result = mcp.tools["deliver_invoice"](invoice_id="non-existent")
    assert "Error" in result
    assert "not found" in result

