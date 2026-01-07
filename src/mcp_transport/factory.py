import os

from .base import Transport
from .sse import SseTransport
from .stdio import StdioTransport


def get_transport() -> Transport:
    """
    Get the configured transport based on the MCP_TRANSPORT environment variable.
    Defaults to stdio if not specified.
    """
    transport_type = os.environ.get("MCP_TRANSPORT", "stdio").lower()

    if transport_type == "stdio":
        return StdioTransport()
    elif transport_type == "sse":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "8000"))
        return SseTransport(host=host, port=port)
    else:
        raise ValueError(f"Unknown transport type: {transport_type}")
