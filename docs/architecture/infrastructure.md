# Infrastructure Module (`mcp_infra`)

The `mcp_infra` module provides cross-cutting concerns that support the entire application.

## Configuration

We use `pydantic-settings` for robust configuration management. Settings are read from environment variables and `.env` files.

## Logging

Structured logging is implemented using `structlog`. This ensures logs are machine-readable and contain context-rich information, which is crucial for debugging distributed systems.

## Exception Handling

A centralized exception handling mechanism ensures that errors are reported consistently across different transport layers.
