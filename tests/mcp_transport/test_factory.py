import os

import pytest

from mcp_transport.factory import get_transport
from mcp_transport.sse import SseTransport
from mcp_transport.stdio import StdioTransport


def test_get_transport_default():
    # Ensure no env var
    if "MCP_TRANSPORT" in os.environ:
        del os.environ["MCP_TRANSPORT"]

    transport = get_transport()
    assert isinstance(transport, StdioTransport)

def test_get_transport_stdio():
    os.environ["MCP_TRANSPORT"] = "stdio"
    transport = get_transport()
    assert isinstance(transport, StdioTransport)
    del os.environ["MCP_TRANSPORT"]

def test_get_transport_sse():
    os.environ["MCP_TRANSPORT"] = "sse"
    os.environ["MCP_HOST"] = "localhost"
    os.environ["MCP_PORT"] = "9090"

    transport = get_transport()
    assert isinstance(transport, SseTransport)
    assert transport.host == "localhost"
    assert transport.port == 9090

    del os.environ["MCP_TRANSPORT"]
    del os.environ["MCP_HOST"]
    del os.environ["MCP_PORT"]

def test_get_transport_unknown():
    os.environ["MCP_TRANSPORT"] = "unknown_transport"
    with pytest.raises(ValueError, match="Unknown transport type"):
        get_transport()
    del os.environ["MCP_TRANSPORT"]
