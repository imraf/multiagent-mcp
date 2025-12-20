# Agent Plan: Core Domain

## Identity
- **Branch:** `agent/core-domain`
- **Worktree Path:** `../mcp-core`
- **Phase:** 1 (Foundation & Core)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/core-domain"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 2 - Part 1)

### 2.1 Domain Modeling
- [ ] Define rich Pydantic models with validation logic:
  - [ ] `Customer`: Contact info, VAT ID validation.
  - [ ] `Invoice`: Line items, tax calculations, status workflow.
  - [ ] `InvoiceItem`: Description, quantity, unit price, total.

### 2.2 Persistence Layer (Repository Pattern)
- [ ] Define abstract `Repository` interfaces for loose coupling.
- [ ] Implement `JsonFileRepository` for portable, file-based storage.
- [ ] Implement optimistic locking for data integrity.

### 2.5 Core Testing (Partial)
- [ ] Test persistence with mock repositories.
- [ ] Property-based testing for financial calculations (if applicable at model level).

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
