from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_transport.sse import SseTransport
from mcp_transport.stdio import StdioTransport


@pytest.mark.asyncio
async def test_sse_event_generator():
    transport = SseTransport()
    # Mock message queue to yield one message then block (timeout)
    transport._message_queue.put_nowait({"test": 1})

    # We can test the generator directly
    request = MagicMock()
    # Ensure we don't run out of side effects
    request.is_disconnected = AsyncMock(side_effect=[False, False, True, True, True])

    # We patch asyncio.wait_for to return values directly (awaitable)
    with patch("asyncio.wait_for", new_callable=AsyncMock) as mock_wait:
        mock_wait.side_effect = [{"test": 1}, TimeoutError()]

        gen = transport._event_generator(request)

        item1 = await anext(gen)
        assert item1 == {"data": {"test": 1}}

        item2 = await anext(gen)
        assert item2 == {"comment": "keepalive"}

        with pytest.raises(StopAsyncIteration):
            await anext(gen)


@pytest.mark.asyncio
async def test_sse_start_close():
    transport = SseTransport()
    with patch("uvicorn.Server.serve", new_callable=AsyncMock) as mock_serve:
        await transport.start()
        mock_serve.assert_called_once()

    # transport._server is set
    transport._server = MagicMock()
    await transport.close()
    assert transport._server.should_exit is True


@pytest.mark.asyncio
async def test_stdio_read_loop():
    transport = StdioTransport()
    handler = AsyncMock()
    transport.set_handler(handler)

    # Mock reader
    reader = MagicMock()
    reader.readline = AsyncMock(
        side_effect=[
            b'{"jsonrpc": "2.0"}\n',  # Valid
            b"invalid json\n",  # Invalid JSON
            b"",  # EOF
        ]
    )

    await transport._read_loop(reader)

    assert handler.call_count == 1
    args, _ = handler.call_args
    assert args[0] == {"jsonrpc": "2.0"}


@pytest.mark.asyncio
async def test_stdio_start():
    # Mock sys.stdin and asyncio loop
    transport = StdioTransport()

    with patch("asyncio.get_running_loop") as mock_get_loop:
        mock_loop = MagicMock()
        mock_get_loop.return_value = mock_loop
        mock_loop.connect_read_pipe = AsyncMock()

        with patch("sys.stdin"):
            await transport.start()
            mock_loop.connect_read_pipe.assert_called()
