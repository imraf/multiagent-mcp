# Agent Orchestration Plan

This document defines the execution order and synchronization points for the multi-agent development process. It serves as the blueprint for the automation script that will drive the implementation.

## 0. Initialization
**Goal:** Prepare the repository for parallel work.
1.  Check if there is a git repository present, otherwise initialize one.
2.  Verify or create the `master` branch with initial `README.md` and `docs/`.
3.  Verify or create the `worktrees/` directory (outside or inside, depending on preference, usually sibling to repo or inside `.git/worktrees` managed by git, but for this project we'll use sibling folders for agents).

---

## Phase 1: Foundation & Core
**Parallel Execution:** Yes
**Dependencies:** None (starts from clean slate)

### Agents
1.  **Infrastructure Agent** (`agent/infrastructure`)
    *   **Task:** Set up project skeleton, `pyproject.toml`, Config, Logging, Exceptions.
    *   **Critical Output:** Directory structure, `src/config.py`, `src/logger.py`.
2.  **Core Domain Agent** (`agent/core-domain`)
    *   **Task:** Define Pydantic models (`Customer`, `Invoice`) and Storage Interfaces.
    *   **Critical Output:** `src/models/`, `src/storage/`.

### Synchronization Point 1
*   **Action:** Merge `agent/infrastructure` and `agent/core-domain` into `master`.
*   **Resolution:** Resolve any directory structure conflicts (though `infrastructure` should take precedence for scaffolding).

---

## Phase 2: Business Logic & Transport
**Parallel Execution:** Yes
**Dependencies:** Phase 1 completed and merged.

### Agents
1.  **Customer Module Agent** (`agent/customer-module`)
    *   **Task:** Implement `CustomerService`, `JsonFileRepository` (Customer), and Customer Tools.
    *   **Input:** Needs `src/models/customer.py` and `src/storage/interface.py` from Phase 1.
2.  **Invoice Module Agent** (`agent/invoice-module`)
    *   **Task:** Implement `InvoiceService`, VAT logic, and Invoice Tools.
    *   **Input:** Needs `src/models/invoice.py` and `src/storage/interface.py` from Phase 1.
3.  **Transport Agent** (`agent/transport`)
    *   **Task:** Implement `Transport` ABC, `StdioTransport`, and `SseTransport`.
    *   **Input:** Needs `src/config.py` and `src/logger.py` from Phase 1.

### Synchronization Point 2
*   **Action:** Merge `agent/customer-module`, `agent/invoice-module`, and `agent/transport` into `master`.
*   **Resolution:** Ensure all services register correctly with the main application entry point (if created).

---

## Phase 3: Expansion & Clients
**Parallel Execution:** Yes
**Dependencies:** Phase 2 completed and merged.

### Agents
1.  **Advanced Primitives Agent** (`agent/advanced-primitives`)
    *   **Task:** Implement Resources (`invoice://`) and Prompts (`compose-email`).
    *   **Input:** Needs full service layer access from Phase 2.
2.  **SDK & CLI Agent** (`agent/sdk-cli`)
    *   **Task:** Build Python Client SDK and Typer CLI.
    *   **Input:** Needs to know the Transport interface and Tool definitions.
3.  **Docs & Polish Agent** (`agent/docs-polish`)
    *   **Task:** Create `README.md`, `Dockerfile`, `Makefile`, and MkDocs site.
    *   **Input:** Can run independently but needs final project structure.

### Synchronization Point 3
*   **Action:** Merge all Phase 3 branches into `master`.
*   **Resolution:** Final integration check.

---

## 4. Finalization
**Goal:** Verify the complete system.
1.  Run full test suite (`pytest`).
2.  Build Docker image.
3.  Verify CLI functionality.
