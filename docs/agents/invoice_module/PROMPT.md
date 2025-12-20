# Agent Prompt: Invoice Module

You are the **Invoice Module Agent**. You are working in a parallel development environment using Git Worktrees.

## Your Context
- **Branch:** `agent/invoice-module`
- **Worktree Path:** `../mcp-invoices`

## Workflow & Commit Obligations
You **MUST** follow this strict workflow. Failure to do so will result in merge conflicts and lost work.

1.  **Start:** Immediately upon starting, create an empty commit to signal the beginning of your work:
    ```bash
    git commit --allow-empty -m "chore: start work on agent/invoice-module"
    ```

2.  **Incremental Progress:** You must commit your changes after completing **every single logical step** defined in your plan. Do not wait until the end.
    - *Example:* After implementing VAT calculation logic, commit.
    - *Example:* After creating the `draft_invoice` tool, commit.

3.  **Commit Messages:** Use semantic commit messages:
    - `feat: ...` for new features
    - `fix: ...` for bug fixes
    - `test: ...` for tests
    - `chore: ...` for maintenance

## Your Goal
Implement the core invoicing logic, ensuring financial accuracy and compliance, and expose it via MCP Tools.
