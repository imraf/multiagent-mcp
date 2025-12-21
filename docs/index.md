# Welcome to MCP Agent Docs

A robust, modular infrastructure foundation for building Model Context Protocol (MCP) agents.

## Project Goal

This project aims to provide the core building blocks—transport layers, service architecture, configuration management, and tool abstractions—required to orchestrate intelligent agents that adhere to the Model Context Protocol.

## Key Features

- **Core Architecture**: Clean separation of concerns with `mcp_core`, `mcp_infra`, and `mcp_transport`.
- **Transport Layers**: Support for both SSE (Server-Sent Events) and Stdio transports.
- **Service & Tools**: Flexible repository pattern and tool registration system.
- **Configuration**: Pydantic-based settings management.
- **Observability**: Structured logging setup using `structlog`.

## Where to go next?

- **[Getting Started](getting-started/installation.md)**: Learn how to install and run the project.
- **[Architecture](architecture/overview.md)**: Understand the high-level design.
- **[Guides](guides/llm-integration.md)**: Learn how to integrate LLMs and write new tools.
