# MCP Agent Foundation

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

> **A robust, modular infrastructure foundation for building Model Context Protocol (MCP) agents.**

This project provides the core building blocks—transport layers, service architecture, configuration management, and tool abstractions—required to orchestrate intelligent agents. Designed for scalability and maintainability, it serves as a reference implementation for building production-grade MCP systems.

---

## 🏗️ Architecture Overview

The project is structured around a clean separation of concerns, ensuring that domain logic, infrastructure, and transport layers remain decoupled.

```mermaid
graph TD
    subgraph "Client Layer"
        CLI[CLI (mcp_cli)]
        SDK["CLI (mcp_cli)"]
        SDK["Python SDK (mcp_client)"

    subgraph "Transport Layer (mcp_transport)"
        SSE[SSE Transport]
        Stdio[Stdio Transport]
    end

    subgraph "Server Layer (mcp_server)"
        Tools[Tools Registration]
        Prompts[Prompts Registration]
        Resources[Resources Provider]
    end

    subgraph "Core Domain (mcp_core)"
        Service[Invoice Service]
        Repo[Repository]
        Models[Domain Models]
    end

    subgraph "Infrastructure (mcp_infra)"
        Config[Configuration]
        Log[Structured Logging]
    end

    CLI --> SDK
    SDK --> SSE
    SSE --> Tools
    Stdio --> Tools
    Tools --> Service
    Service --> Repo
    Repo --> Models
    Service --> Log
    Service --> Config
```

---

## 📦 Component Survey

The `src/` directory contains the following modules, each playing a specific role in the system:

### 1. Core Domain (`mcp_core`)
The heart of the application, containing business logic and data models.
- **`models.py`**: Pydantic models defining core entities like `Invoice`, `Customer`, and `InvoiceItem`.
- **`repository.py` & `json_repository.py`**: The Repository pattern implementation. `JsonFileRepository` provides a file-based persistence layer with optimistic locking.
- **`invoice_service.py`**: Encapsulates business rules for invoice management (creation, finalization, status transitions).
- **`prompt.py`**: Manages Jinja2-based prompt templates, allowing for dynamic and reusable LLM prompts.
- **`tool.py` & `resource.py`**: Abstract base classes defining the contract for MCP Tools and Resources.

### 2. Infrastructure (`mcp_infra`)
Handles cross-cutting concerns.
- **`config.py`**: Configuration management using `pydantic-settings`. Supports loading from environment variables (`MCP_*`) and YAML files.
- **`logging.py`**: Sets up structured JSON logging using `structlog`, ensuring observability and machine-readable logs.

### 3. Transport Layer (`mcp_transport`)
Manages communication protocols.
- **`base.py`**: Defines the abstract `Transport` and `Server` interfaces.
- **`sse.py`**: Implements Server-Sent Events (SSE) over HTTP using FastAPI, suitable for web-based clients.
- **`stdio.py`**: Implements Standard Input/Output transport, ideal for local process communication and CLI tools.
- **`factory.py`**: A factory to instantiate the correct transport based on configuration.

### 4. Server Implementation (`mcp_server`)
Connects the domain logic to the MCP protocol.
- **`tools.py`**: Registers domain functions (e.g., `create_draft_invoice`) as MCP Tools.
- **`prompts.py`**: Registers advanced prompts (e.g., `compose_dunning_email`) for LLM usage.
- **`invoice_resources.py`**: Exposes invoice data as MCP Resources (e.g., virtual PDFs).

### 5. Client & CLI (`mcp_client`, `mcp_cli`)
Tools for interacting with the agent.
- **`mcp_client/client.py`**: A fluent Python SDK for programmatically interacting with the agent.
- **`mcp_cli/main.py`**: A Typer-based command-line interface for managing invoices and customers.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **[uv](https://github.com/astral-sh/uv)** (recommended) or `pip`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mcp-docs.git
   cd mcp-docs
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Configuration:**
   The application can be configured via environment variables. Create a `.env` file:
   ```env
   MCP_APP__ENVIRONMENT=development
   MCP_LOGGING__LEVEL=DEBUG
   MCP_TRANSPORT=stdio
   ```

---

## 💻 Usage

### Running the CLI
The CLI allows you to interact with the invoice system directly from your terminal.

```bash
# View help
python src/mcp_cli/main.py --help

# Create a new invoice
python src/mcp_cli/main.py new --customer-id "CUST-123" --description "Consulting Services" --quantity 10 --price 150.0

# List all invoices
python src/mcp_cli/main.py list

# Filter invoices by status
python src/mcp_cli/main.py list --status draft
```

### Running the Server (SSE)
To expose the agent via HTTP/SSE, run the server using `uvicorn`.

```bash
# Start the server (ensure you have an entry point configured)
uvicorn src.mcp_server.main:app --reload
```

---

## 🛠️ Development

### Testing
Run the comprehensive test suite:
```bash
pytest
```

### Linting & Formatting
Maintain code quality with `ruff`:
```bash
ruff check .
ruff format .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
