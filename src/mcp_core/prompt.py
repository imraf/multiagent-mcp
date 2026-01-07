from typing import Any

import jinja2
from pydantic import BaseModel, Field


class PromptArgument(BaseModel):
    """Definition of an argument for a prompt."""

    name: str = Field(..., description="Name of the argument")
    description: str | None = Field(None, description="Description of the argument")
    required: bool = Field(True, description="Whether the argument is required")


class Prompt(BaseModel):
    """
    Represents an MCP Prompt.
    Prompts are reusable templates for LLM interactions.
    """

    name: str = Field(..., description="Unique name of the prompt")
    description: str | None = Field(None, description="Description of what the prompt does")
    arguments: list[PromptArgument] = Field(
        default_factory=list, description="List of arguments the prompt accepts"
    )
    template: str = Field(..., description="Jinja2 template string")


class PromptManager:
    """
    Manages prompt registration and rendering using Jinja2.
    """

    def __init__(self):
        self._prompts: dict[str, Prompt] = {}
        self._jinja_env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            autoescape=jinja2.select_autoescape(
                ["html", "xml"]
            ),  # Default safe, though mostly text
        )

    def register_prompt(self, prompt: Prompt):
        """Register a new prompt."""
        self._prompts[prompt.name] = prompt

    def get_prompt(self, name: str) -> Prompt | None:
        """Retrieve a prompt by name."""
        return self._prompts.get(name)

    def list_prompts(self) -> list[Prompt]:
        """List all registered prompts."""
        return list(self._prompts.values())

    def render_prompt(self, name: str, arguments: dict[str, Any] = None) -> str:
        """
        Render a prompt with the given arguments.
        Raises ValueError if prompt not found or arguments missing.
        """
        prompt = self.get_prompt(name)
        if not prompt:
            raise ValueError(f"Prompt '{name}' not found")

        arguments = arguments or {}

        # Validate required arguments
        for arg in prompt.arguments:
            if arg.required and arg.name not in arguments:
                raise ValueError(f"Missing required argument: {arg.name}")

        # Render template
        template = self._jinja_env.from_string(prompt.template)
        return template.render(**arguments)
