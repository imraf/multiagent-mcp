import asyncio
from typing import Any, Callable, Awaitable, Optional

from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from uvicorn import Config, Server

from .base import Transport


class SseTransport(Transport):
    """Server-Sent Events transport implementation over HTTP."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        self.host = host
        self.port = port
        self._handler: Optional[Callable[[Any], Awaitable[None]]] = None
        self._app = FastAPI()
        self._server: Optional[Server] = None
        self._message_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()

        self._setup_routes()

    def _setup_routes(self) -> None:
        @self._app.post("/messages")
        async def handle_message(request: Request) -> dict[str, str]:
            if not self._handler:
                return {"status": "error", "message": "No handler set"}

            try:
                data = await request.json()
                await self._handler(data)
                return {"status": "ok"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

        @self._app.get("/events")
        async def sse_endpoint(request: Request) -> EventSourceResponse:
            return EventSourceResponse(self._event_generator(request))

    async def _event_generator(self, request: Request):
        while True:
            if await request.is_disconnected():
                break

            try:
                # Wait for message with timeout to allow checking connection status
                message = await asyncio.wait_for(self._message_queue.get(), timeout=1.0)
                yield {"data": message}
            except asyncio.TimeoutError:
                # Send keepalive comment
                yield {"comment": "keepalive"}

    async def start(self) -> None:
        """Start the HTTP server."""
        config = Config(app=self._app, host=self.host, port=self.port, log_level="error")
        self._server = Server(config=config)
        # Run server in current loop
        await self._server.serve()

    async def close(self) -> None:
        """Close the transport."""
        if self._server:
            self._server.should_exit = True
            # Wait for shutdown? In uvicorn, setting should_exit triggers shutdown sequence.

    async def send(self, message: Any) -> None:
        """Queue message to be sent via SSE."""
        await self._message_queue.put(message)

    def set_handler(self, handler: Callable[[Any], Awaitable[None]]) -> None:
        """Set the handler for incoming messages."""
        self._handler = handler
