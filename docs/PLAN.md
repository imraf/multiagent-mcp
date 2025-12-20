# Implementation Plan: MCP Invoicing System

This comprehensive plan outlines the development of a modular, production-grade Invoicing System based on the Model Context Protocol (MCP) architecture. The project is structured into 6 distinct stages, ensuring a logical progression from foundational infrastructure to a polished, user-ready application.

## Project Overview
**Topic:** Enterprise-Grade Invoicing & Accounting System
**Language:** Python 3.10+
**Architecture:** Model Context Protocol (MCP)
**Key Features:**
- **Robust Customer Management:** CRM-lite capabilities.
- **Invoice Lifecycle Management:** Creation, issuance, tracking, and cancellation.
- **Compliance:** Sequential numbering and configurable VAT calculation.
- **Delivery Simulation:** Mock email delivery system.
- **AI Integration:** Support for both local (Ollama) and proprietary (OpenAI/Anthropic) LLMs.

---

## Stage 1: Basic Infrastructure
**Goal:** Establish a rock-solid foundation with enterprise patterns (Singleton Config, Structured Logging, Typed Exceptions).

### 1.1 Project Structure & Tooling
- Initialize repository with `pyproject.toml` using `uv` or `poetry`.
- Set up strict linting/formatting (`ruff`, `mypy`).
- Create directory structure: `src/`, `tests/`, `docs/`, `config/`.

### 1.2 Configuration Layer
- Implement a type-safe `Config` class using Pydantic Settings.
- Support hierarchical configuration: Environment Variables > `config.yaml` > Defaults.
- **Requirement:** Zero hard-coded values.

### 1.3 Observability (Logging)
- Implement structured JSON logging for machine readability.
- Configure log rotation and dual-sink output (Console + File).
- Add context-aware logging (request IDs).

### 1.4 Exception Handling Strategy
- Define a hierarchy of custom exceptions inheriting from `MCPException`.
- Implement error boundaries and graceful degradation.
- Create standardized error response formats.

### 1.5 Infrastructure Verification
- Unit tests for configuration loading and validation.
- Integration tests for logging sinks.

---

## Stage 2: MCP Server Core
**Goal:** Implement the domain logic, persistence layer, and the first set of MCP Tools.

### 2.1 Domain Modeling
- Define rich Pydantic models with validation logic:
  - `Customer`: Contact info, VAT ID validation.
  - `Invoice`: Line items, tax calculations, status workflow.

### 2.2 Persistence Layer (Repository Pattern)
- Define abstract `Repository` interfaces for loose coupling.
- Implement `JsonFileRepository` for portable, file-based storage.
- Implement optimistic locking for data integrity.

### 2.3 Service Layer
- `CustomerService`: Business logic for client management.
- `InvoiceService`: Complex logic for tax calculation and sequential ID generation.

### 2.4 MCP Tool Implementation
- Implement the `Tool` interface with strict JSON Schema generation.
- **Tools:**
  - `register_customer`: Onboard new clients.
  - `draft_invoice`: Create invoices in draft state.

### 2.5 Core Testing
- Test persistence with mock repositories.
- Property-based testing for financial calculations.

---

## Stage 3: The Three Primitives
**Goal:** Achieve full MCP compliance by implementing Tools, Resources, and Prompts.

### 3.1 Advanced Write Operations (Tools)
- `finalize_invoice`: Lock invoice and assign official number.
- `deliver_invoice`: Trigger mock email delivery.
- `void_invoice`: Handle cancellations with audit trail.

### 3.2 Read Operations (Resources)
- Implement `ResourceProvider` for direct data access.
- **URI Schemes:**
  - `invoice://{id}/pdf`: Virtual PDF representation.
  - `customer://{id}/ledger`: Transaction history.

### 3.3 Context Injection (Prompts)
- Implement a template engine (Jinja2) for dynamic prompts.
- **Templates:**
  - `compose_dunning_email`: Context-aware payment reminders.
  - `financial_summary`: AI-ready summary of outstanding debt.

---

## Stage 4: Communication & Transport
**Goal:** Decouple the application logic from the transport protocol.

### 4.1 Transport Abstraction
- Define `Transport` and `Server` abstract base classes.
- Implement dependency injection for transport selection.

### 4.2 Protocol Implementations
- **StdioTransport:** Standard Input/Output for local CLI/Agent integration.
- **SseTransport:** Server-Sent Events over HTTP (FastAPI/Starlette) for remote access.

### 4.3 Protocol Switching
- Enable transport switching via configuration flags (e.g., `MCP_TRANSPORT=stdio`).

---

## Stage 5: SDK & Client Interfaces
**Goal:** Provide developer-friendly SDKs and user interfaces.

### 5.1 Python SDK
- Build a fluent `InvoicingClient` library.
- Features: Connection management, typed tool calls, resource fetching.

### 5.2 CLI Application
- Develop a rich terminal UI (TUI) using `Typer` and `Rich`.
- Commands: `mcp-invoice new`, `mcp-invoice list --status overdue`.

### 5.3 Web Dashboard (Optional)
- Lightweight Streamlit dashboard for visualizing revenue and invoice status.

---

## Stage 6: Presentation, Documentation & Polish
**Goal:** Prepare the project for public release and professional showcase.

### 6.1 Professional Documentation
- **README.md:**
  - Eye-catching header with project logo/banner.
  - Badges (CI/CD, Python Version, License).
  - "Quick Start" GIF or terminal recording.
- **Docs Site:** Generate static documentation using `MkDocs` + `Material for MkDocs`.
  - API Reference.
  - Architecture Decision Records (ADRs).

### 6.2 Installation Experience
- Create a `Makefile` for common tasks.
- Publishable `pyproject.toml` metadata.
- Dockerfile for containerized deployment.

### 6.3 LLM Integration Guide
- **Local LLM (Ollama):**
  - Guide on running `llama3` or `mistral` locally.
  - Configuration for `MCP_LLM_BACKEND=ollama`.
- **Proprietary APIs:**
  - Setup for `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.
  - Configuration for `MCP_LLM_BACKEND=openai`.

---

## Development Standards
- **Code Quality:** 100% Type coverage (`strict` mode).
- **Testing:** Pytest with >90% coverage.
- **Git Workflow:** Feature branches and Semantic Commit Messages.
- **Modularity:** Strict separation of concerns (Ports and Adapters architecture).
