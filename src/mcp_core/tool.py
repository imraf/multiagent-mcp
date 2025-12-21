from typing import Any, Callable, Dict, Optional, Type
from pydantic import BaseModel


class Tool(BaseModel):
    """
    Represents an MCP Tool.
    """

    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable[..., Any]
