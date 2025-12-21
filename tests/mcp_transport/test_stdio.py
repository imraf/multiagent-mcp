import asyncio
import json
import pytest
from unittest.mock import MagicMock, patch

from mcp_transport.stdio import StdioTransport


@pytest.mark.asyncio
async def test_stdio_transport_send():
    transport = StdioTransport()
    message = {"jsonrpc": "2.0", "method": "test", "params": {}}

    with patch("sys.stdout") as mock_stdout:
        await transport.send(message)

        mock_stdout.write.assert_called_once()
        args, _ = mock_stdout.write.call_args
        assert json.loads(args[0]) == message
        mock_stdout.flush.assert_called_once()


@pytest.mark.asyncio
async def test_stdio_transport_receive():
    transport = StdioTransport()
    mock_handler = MagicMock()

    async def handler(msg):
        mock_handler(msg)

    transport.set_handler(handler)

    input_message = {"jsonrpc": "2.0", "method": "test"}
    input_line = json.dumps(input_message).encode() + b"\n"

    # Mocking asyncio.StreamReader is tricky, but we can test _handle_line directly
    await transport._handle_line(input_line)

    mock_handler.assert_called_once_with(input_message)
