# Implementation Plan: MCP Invoicing System

This plan outlines the development of a modular Invoicing System based on the Model Context Protocol (MCP) architecture. The project is divided into 5 stages as per the assignment requirements.

## Project Overview
**Topic:** Invoicing & Accounting System
**Language:** Python
**Key Features:**
- Customer Management
- Invoice Creation & Tracking
- Sequential Numbering
- VAT Calculation
- Invoice Delivery (Mock)

---

## Stage 1: Basic Infrastructure
**Goal:** Establish the foundational layers (Config, Logging, Exceptions) and project structure.

### 1.1 Project Structure Setup
- Create root directory structure.
- Initialize `pyproject.toml` for dependency management.
- Create `src/` and `tests/` directories.

### 1.2 Configuration Layer
- Implement a `Config` class (Singleton or Dependency Injection).
- Load settings from `config.yaml` or `.env`.
- **Requirement:** No hard-coded values.

### 1.3 Logging Mechanism
- Create a centralized logger wrapper.
- Support different log levels (DEBUG, INFO, ERROR) configurable via file.
- Ensure logs are written to both console and file (rotated).

### 1.4 Exception Handling
- Define a base `MCPException`.
- Define specific exceptions: `ConfigurationError`, `StorageError`, `ValidationError`.
- Implement a global error handler/decorator.

### 1.5 Base Infrastructure Tests
- Unit tests for Config loading.
- Unit tests for Logging (verify output).
- Unit tests for custom Exceptions.

---

## Stage 2: MCP Server with Tools
**Goal:** Implement core business logic, data storage, and basic MCP tools.

### 2.1 Data Models (Domain Layer)
- Define Pydantic models for:
  - `Customer` (id, name, email, address, vat_id)
  - `InvoiceItem` (description, quantity, unit_price, total)
  - `Invoice` (id, customer_id, items, subtotal, tax, total, status, date)

### 2.2 Storage Layer (Persistence)
- Create an abstract `StorageInterface`.
- Implement `JsonFileStorage` (or `SQLiteStorage`) implementing the interface.
- Implement locking mechanisms for concurrent access safety.

### 2.3 Business Logic Services
- `CustomerService`: Add, get, list customers.
- `InvoiceService`: Create invoice, calculate VAT, generate sequential IDs.

### 2.4 MCP Tool Definitions
- Define the `Tool` interface/structure.
- Implement initial tools:
  - `create_customer`: Register a new client.
  - `create_invoice`: Generate a new invoice for a client.
- Ensure tools have JSON Schemas for arguments.

### 2.5 Stage 2 Tests
- Test storage persistence.
- Test service logic (VAT calc, numbering).
- Test tool execution.

---

## Stage 3: The Three Primitives
**Goal:** Expand system to support Tools (Write), Resources (Read), and Prompts.

### 3.1 Advanced Tools (Write)
- `send_invoice`: Mark invoice as sent (mock delivery).
- `cancel_invoice`: Update status to cancelled.
- `update_customer`: Modify customer details.

### 3.2 Resources (Read)
- Implement `Resource` provider logic.
- Define URI schemes (e.g., `invoice://{id}`, `customer://{id}/invoices`).
- Implement resource handlers to fetch data dynamically from storage.

### 3.3 Prompts
- Implement `Prompt` template system.
- Create templates:
  - `compose-invoice-email`: Generates a polite email for an invoice.
  - `analyze-debt`: Summarizes unpaid invoices for a customer.

### 3.4 Stage 3 Tests
- Verify resource URI resolution and data retrieval.
- Verify prompt template rendering with dynamic data.

---

## Stage 4: Communication Layer
**Goal:** Decouple the transport mechanism from the core logic.

### 4.1 Transport Abstraction
- Define a `Transport` abstract base class.
- Define `Server` class that accepts a `Transport` strategy.

### 4.2 STDIO Transport
- Implement `StdioTransport` for standard input/output communication (default for local MCP).
- Handle JSON-RPC message framing.

### 4.3 HTTP/SSE Transport (Optional/Alternative)
- Implement `SseTransport` using a lightweight server (e.g., Starlette/FastAPI) to demonstrate swappability.

### 4.4 Integration
- Ensure the Server can switch transports via configuration without code changes.

---

## Stage 5: SDK and User Interface
**Goal:** Create a client library and a user-facing application.

### 5.1 Client SDK
- Create a Python `InvoicingClient` class.
- Methods to interact with the server:
  - `connect()`
  - `list_tools()`, `call_tool()`
  - `read_resource()`
  - `get_prompt()`

### 5.2 CLI Interface
- Build a command-line tool using `typer` or `argparse`.
- Commands:
  - `invoice new --customer "Acme" --amount 100`
  - `invoice list`
  - `customer add`

### 5.3 Web Interface (Optional)
- Simple Streamlit or HTML dashboard to view invoices.

---

## Development Guidelines
- **Modularity:** Each component (Storage, Logic, Transport) must be in separate modules/packages.
- **File Size:** Keep files under 150 lines. Refactor if necessary.
- **Testing:** `pytest` will be used. Coverage goal > 80%.
- **Git:** Use feature branches/worktrees for each stage or major feature.
