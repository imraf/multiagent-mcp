from collections.abc import Callable
from typing import Any

from pydantic import BaseModel


class Tool(BaseModel):
    """
    Represents an MCP Tool.
    """

    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., Any]
