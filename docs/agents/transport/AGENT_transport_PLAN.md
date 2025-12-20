# Agent Plan: Transport

## Identity
- **Branch:** `agent/transport`
- **Worktree Path:** `../mcp-transport`
- **Phase:** 2 (Business Logic & Transport)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/transport"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 4)

### 4.1 Transport Abstraction
- [ ] Define `Transport` abstract base class.
- [ ] Define `Server` abstract base class (or main server class) that accepts a `Transport` strategy.
- [ ] Implement dependency injection for transport selection.

### 4.2 Protocol Implementations
- [ ] **StdioTransport:** Implement Standard Input/Output transport for local CLI/Agent integration (JSON-RPC).
- [ ] **SseTransport:** Implement Server-Sent Events over HTTP (using FastAPI/Starlette) for remote access.

### 4.3 Protocol Switching
- [ ] Enable transport switching via configuration flags (e.g., `MCP_TRANSPORT=stdio`).

### Testing
- [ ] Unit tests for `StdioTransport` (mocking stdin/stdout).
- [ ] Unit tests for `SseTransport` (using test client).

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
