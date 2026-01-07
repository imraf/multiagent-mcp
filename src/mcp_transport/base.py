from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


class Transport(ABC):
    """Abstract base class for transport layer."""

    @abstractmethod
    async def start(self) -> None:
        """Start the transport."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the transport."""
        pass

    @abstractmethod
    async def send(self, message: Any) -> None:
        """Send a message through the transport."""
        pass

    @abstractmethod
    def set_handler(self, handler: Callable[[Any], Awaitable[None]]) -> None:
        """Set the handler for incoming messages."""
        pass


class Server(ABC):
    """Abstract base class for the server."""

    def __init__(self, transport: Transport):
        self.transport = transport

    @abstractmethod
    async def run(self) -> None:
        """Run the server."""
        pass
