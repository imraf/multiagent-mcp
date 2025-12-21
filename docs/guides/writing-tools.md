# Writing Tools

Tools are the capabilities you expose to the LLM.

## Creating a New Tool

To create a new tool, define a function and decorate it with `@tool`.

```python
from mcp_server.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b
```

## Registering the Tool

Once defined, the tool needs to be registered with the server instance so it can be exposed via the MCP protocol.

(Refer to `src/mcp_server/tools.py` for more examples.)
