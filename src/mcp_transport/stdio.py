import asyncio
import json
import sys
from collections.abc import Awaitable, Callable
from typing import Any

from .base import Transport


class StdioTransport(Transport):
    """Standard Input/Output transport implementation."""

    def __init__(self) -> None:
        self._handler: Callable[[Any], Awaitable[None]] | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    async def start(self) -> None:
        """Start reading from stdin."""
        self._loop = asyncio.get_running_loop()
        try:
            reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(reader)
            await self._loop.connect_read_pipe(lambda: protocol, sys.stdin)

            # Start a background task to read lines
            asyncio.create_task(self._read_loop(reader))
        except RuntimeError:
            # Handle case where loop is not running or stdin is not compatible
            pass

    async def close(self) -> None:
        """Close the transport."""
        # Standard streams don't typically need explicit closing in this context,
        # but we might want to cancel the read loop if we tracked it.
        pass

    async def send(self, message: Any) -> None:
        """Send a JSON-RPC message to stdout."""
        json_str = json.dumps(message)
        sys.stdout.write(json_str + "\n")
        sys.stdout.flush()

    def set_handler(self, handler: Callable[[Any], Awaitable[None]]) -> None:
        """Set the handler for incoming messages."""
        self._handler = handler

    async def _read_loop(self, reader: asyncio.StreamReader) -> None:
        """Continuously read lines from stdin."""
        while True:
            line = await reader.readline()
            if not line:
                break

            await self._handle_line(line)

    async def _handle_line(self, line: bytes) -> None:
        """Process a single line of input."""
        if not self._handler:
            return

        try:
            message = json.loads(line.decode().strip())
            await self._handler(message)
        except json.JSONDecodeError:
            # Log error or ignore malformed JSON
            pass
        except Exception:
            # Log unexpected errors
            pass
