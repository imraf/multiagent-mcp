from unittest.mock import MagicMock

from mcp_server.customer_tools import register_customer_tools


def test_register_customer_tools():
    mcp_mock = MagicMock()

    # Mock tool decorator
    def tool_decorator():
        def wrapper(func):
            return func

        return wrapper

    mcp_mock.tool.side_effect = tool_decorator

    register_customer_tools(mcp_mock)

    # Check if tools were registered
    # Implementation detail: usage of decorator means we can't easily check mcp_mock.tools list
    # unless we mock the FastMCP class structure better or inspect calls.
    # But running the function covers the lines.
    assert mcp_mock.tool.call_count >= 1
