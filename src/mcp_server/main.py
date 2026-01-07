import importlib.metadata
import logging
from collections.abc import Iterable
from typing import Any

from mcp.server.fastmcp import FastMCP

from mcp_core.prompt import PromptManager
from mcp_server.customer_tools import register_customer_tools
from mcp_server.invoice_resources import InvoiceResourceProvider
from mcp_server.prompts import register_advanced_prompts

# Import core services and tools
# Note: invoice_service is instantiated in tools.py, reusing it here for consistency
from mcp_server.tools import invoice_service, register_invoice_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP Server
mcp = FastMCP("Invoicing Agent")

# --- 1. Register Tools ---
register_invoice_tools(mcp)
register_customer_tools(mcp)


# --- 2. Register Resources ---
resource_provider = InvoiceResourceProvider(invoice_service)


@mcp.resource("invoice://{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: str) -> str:
    """
    Virtual PDF representation of an invoice.
    """
    res = resource_provider.get_resource(f"invoice://{invoice_id}/pdf")
    if res and res.text:
        return res.text
    # FastMCP resources usually just return content.
    # Raising error might be appropriate if not found.
    raise ValueError(f"Invoice {invoice_id} not found or empty")


# --- 3. Register Prompts ---
# Adapter to bridge mcp_core.prompt.PromptManager with FastMCP
class FastMCPPromptManagerAdapter(PromptManager):
    def __init__(self, mcp_instance: FastMCP) -> None:
        super().__init__()
        self.mcp = mcp_instance

    def register_prompt(self, prompt: Any) -> None:
        """
        Registers a mcp_core.prompt.Prompt with FastMCP.
        """
        # We can't easily dynamically generate the signature for FastMCP to verify arguments
        # so we register a generic handler.
        # Ideally, we would dynamically generate the function with correct signature.

        @self.mcp.prompt(name=prompt.name, description=prompt.description)
        def prompt_handler(**kwargs: Any) -> str:
            # Validate arguments based on prompt.arguments?
            # mcp_core.prompt.Prompt.render should handle jinja rendering
            try:
                result = (
                    prompt.render_prompt(prompt.name, kwargs)
                    if hasattr(prompt, "render_prompt")
                    else prompt.template
                )
                return str(result)
            except Exception as e:
                return f"Error rendering prompt: {e}"

        # Also register in local storage if needed by super class, though likely not used here
        super().register_prompt(prompt)


adapter = FastMCPPromptManagerAdapter(mcp)
register_advanced_prompts(adapter)


# --- 4. Extensibility (Plugins) ---
def load_plugins(mcp_instance: FastMCP) -> None:
    """
    Load plugins from the 'mcp_invoice.plugins' entry point group.
    Each plugin should expose a function that accepts the FastMCP instance.
    """
    group = "mcp_invoice.plugins"
    plugins: Iterable[Any] = []
    try:
        # Python 3.10+
        if hasattr(importlib.metadata, "entry_points"):
            # For Python 3.10+ and modern importlib.metadata
            plugins = importlib.metadata.entry_points(group=group)
        else:
            plugins = []
    except Exception:
        plugins = []

    for entry_point in plugins:
        try:
            register_func = entry_point.load()
            if callable(register_func):
                register_func(mcp_instance)
                logger.info(f"Loaded plugin: {entry_point.name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {entry_point.name}: {e}")


load_plugins(mcp)


if __name__ == "__main__":
    # Run the server (default transport: stdio, or sse via arguments)
    mcp.run()
