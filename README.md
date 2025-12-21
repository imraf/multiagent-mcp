# MCP Agent Foundation

[![CI/CD](https://github.com/yourusername/mcp-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/mcp-docs/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A robust, modular infrastructure foundation for building Model Context Protocol (MCP) agents. This project provides the core building blocks—transport layers, service architecture, configuration management, and tool abstractions—required to orchestrate intelligent agents.

## 🚀 Features

- **Core Architecture**: Clean separation of concerns with `mcp_core`, `mcp_infra`, and `mcp_transport`.
- **Transport Layers**: Support for both SSE (Server-Sent Events) and Stdio transports.
- **Service & Tools**: Flexible repository pattern and tool registration system.
- **Configuration**: Pydantic-based settings management.
- **Observability**: Structured logging setup using `structlog`.

## 📦 Modules

- `src/mcp_core`: Core domain logic, repository patterns, and data models.
- `src/mcp_infra`: Infrastructure concerns like configuration and logging.
- `src/mcp_transport`: Transport implementations (SSE, Stdio).
- `src/mcp_server`: Server setup and tool exposure.
- `src/mcp_customer`: Example domain implementation for customer management.

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/mcp-docs.git
cd mcp-docs
pip install -e .
```

### Running the Agent (Example)

You can run the agent using the provided orchestrator script or directly via python:

```bash
# Using the orchestration script
./orchestrate.sh
```

Or run the SSE server example:

```bash
uvicorn src.mcp_server.main:app --reload
```

## 🛠️ Development

### Testing

Run the test suite with `pytest`:

```bash
pytest
```

### Linting

We use `ruff` for linting and formatting:

```bash
ruff check .
```

## 📚 Documentation

For full documentation, including API reference and Architecture Decision Records (ADRs), please visit our [Documentation Site](#).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
