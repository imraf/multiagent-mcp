import sys
from unittest.mock import MagicMock, patch

# Mock mcp.server.fastmcp before importing main
mcp_mock = MagicMock()
# Setup decorators to return the function unmodified
def decorator(*args, **kwargs):
    def wrapper(func):
        return func
    return wrapper

mcp_instance = mcp_mock.FastMCP.return_value
mcp_instance.resource.side_effect = decorator
mcp_instance.prompt.side_effect = decorator
mcp_instance.tool.side_effect = decorator

sys.modules["mcp.server.fastmcp"] = mcp_mock

from mcp_server.main import load_plugins, get_invoice_pdf

def test_load_plugins():
    mcp = MagicMock()
    with patch("importlib.metadata.entry_points") as mock_eps:
        # Mock entry points behavior
        mock_ep = MagicMock()
        mock_ep.name = "test_plugin"
        mock_ep.load.return_value = MagicMock()
        
        # Structure for Python 3.10+ select()
        mock_eps_result = MagicMock()
        mock_eps_result.select.return_value = [mock_ep]
        mock_eps.return_value = mock_eps_result
        
        load_plugins(mcp)
        
        mock_ep.load.return_value.assert_called_once_with(mcp)

def test_get_invoice_pdf():
    # Helper to test the resource function logic
    # We need to mock resource_provider in main.py or just the underlying service call
    with patch("mcp_server.main.resource_provider") as mock_provider:
        mock_provider.get_resource.return_value.text = "PDF CONTENT"
        
        result = get_invoice_pdf("inv_1")
        assert result == "PDF CONTENT"
        
        # Test not found
        mock_provider.get_resource.return_value = None
        try:
            get_invoice_pdf("inv_2")
            assert False
        except ValueError:
            pass
