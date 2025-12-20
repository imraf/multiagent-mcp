# Agent Plan: SDK & CLI

## Identity
- **Branch:** `agent/sdk-cli`
- **Worktree Path:** `../mcp-clients`
- **Phase:** 3 (Expansion & Clients)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/sdk-cli"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 5)

### 5.1 Python SDK
- [ ] Build a fluent `InvoicingClient` library.
- [ ] Features: Connection management, typed tool calls, resource fetching.

### 5.2 CLI Application
- [ ] Develop a rich terminal UI (TUI) using `Typer` and `Rich`.
- [ ] Commands:
  - [ ] `mcp-invoice new`
  - [ ] `mcp-invoice list --status overdue`
  - [ ] `mcp-invoice customer add`

### 5.3 Web Dashboard (Optional)
- [ ] Lightweight Streamlit dashboard for visualizing revenue and invoice status.

### Testing
- [ ] Unit tests for SDK.
- [ ] Integration tests for CLI commands.

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
