# Agent Plan: Invoice Module

## Identity
- **Branch:** `agent/invoice-module`
- **Worktree Path:** `../mcp-invoices`
- **Phase:** 2 (Business Logic & Transport)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/invoice-module"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 2 & 3 - Invoice Logic)

### 2.3 Service Layer (Invoice)
- [ ] Implement `InvoiceService`:
  - [ ] Complex logic for tax calculation.
  - [ ] Sequential ID generation.
  - [ ] Status management (Draft -> Issued -> Paid/Cancelled).

### 2.4 MCP Tool Implementation (Invoice)
- [ ] Implement `draft_invoice` tool: Create invoices in draft state.

### 3.1 Advanced Write Operations (Invoice)
- [ ] Implement `finalize_invoice` tool: Lock invoice and assign official number.
- [ ] Implement `deliver_invoice` tool: Trigger mock email delivery.
- [ ] Implement `void_invoice` tool: Handle cancellations with audit trail.

### Testing
- [ ] Unit tests for `InvoiceService` (VAT, numbering).
- [ ] Integration tests for Invoice Tools.

## Definition of Done
- All tasks implemented.
- Tests passing (pytest).
- Code follows project standards (max 150 lines per file, fully typed).
