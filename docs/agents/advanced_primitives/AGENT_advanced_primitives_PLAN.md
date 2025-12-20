# Agent Plan: Advanced Primitives

## Identity
- **Branch:** `agent/advanced-primitives`
- **Worktree Path:** `../mcp-primitives`
- **Phase:** 3 (Expansion & Clients)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/advanced-primitives"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 3)

### 3.2 Read Operations (Resources)
- [ ] Implement `ResourceProvider` interface/logic for direct data access.
- [ ] Implement Resource Handlers:
  - [ ] `invoice://{id}/pdf`: Virtual PDF representation (text/mock).
  - [ ] `customer://{id}/ledger`: Transaction history.

### 3.3 Context Injection (Prompts)
- [ ] Implement a template engine (Jinja2) for dynamic prompts.
- [ ] Implement Prompts:
  - [ ] `compose_dunning_email`: Context-aware payment reminders.
  - [ ] `financial_summary`: AI-ready summary of outstanding debt.

### Testing
- [ ] Verify resource URI resolution and data retrieval.
- [ ] Verify prompt template rendering with dynamic data.

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
