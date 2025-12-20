# Agent Plan: Customer Module

## Identity
- **Branch:** `agent/customer-module`
- **Worktree Path:** `../mcp-customers`
- **Phase:** 2 (Business Logic & Transport)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/customer-module"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 2 - Part 2)

### 2.3 Service Layer (Customer)
- [ ] Implement `CustomerService`: Business logic for client management (add, get, list, update).

### 2.4 MCP Tool Implementation (Customer)
- [ ] Implement the `Tool` interface (if not already in core) or use core interface.
- [ ] Implement `register_customer` tool: Onboard new clients.
- [ ] Ensure strict JSON Schema generation for tools.

### 3.1 Advanced Write Operations (Customer)
- [ ] Implement `update_customer` tool: Modify customer details.

### Testing
- [ ] Unit tests for `CustomerService`.
- [ ] Integration tests for Customer Tools.

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
