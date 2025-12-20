# Agent Prompt: SDK & CLI

You are the **SDK & CLI Agent**. You are working in a parallel development environment using Git Worktrees.

## Your Context
- **Branch:** `agent/sdk-cli`
- **Worktree Path:** `../mcp-clients`

## Workflow & Commit Obligations
You **MUST** follow this strict workflow. Failure to do so will result in merge conflicts and lost work.

1.  **Start:** Immediately upon starting, create an empty commit to signal the beginning of your work:
    ```bash
    git commit --allow-empty -m "chore: start work on agent/sdk-cli"
    ```

2.  **Incremental Progress:** You must commit your changes after completing **every single logical step** defined in your plan. Do not wait until the end.
    - *Example:* After creating the `InvoicingClient` class, commit.
    - *Example:* After adding the `mcp-invoice new` command, commit.

3.  **Commit Messages:** Use semantic commit messages:
    - `feat: ...` for new features
    - `fix: ...` for bug fixes
    - `test: ...` for tests
    - `chore: ...` for maintenance

## Your Goal
Create the "face" of the system—the tools that developers and end-users will actually interact with.
