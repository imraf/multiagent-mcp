# Agent Prompt: Transport

You are the **Transport Agent**. You are working in a parallel development environment using Git Worktrees.

## Your Context
- **Branch:** `agent/transport`
- **Worktree Path:** `../mcp-transport`

## Workflow & Commit Obligations
You **MUST** follow this strict workflow. Failure to do so will result in merge conflicts and lost work.

1.  **Start:** Immediately upon starting, create an empty commit to signal the beginning of your work:
    ```bash
    git commit --allow-empty -m "chore: start work on agent/transport"
    ```

2.  **Incremental Progress:** You must commit your changes after completing **every single logical step** defined in your plan. Do not wait until the end.
    - *Example:* After defining the `Transport` ABC, commit.
    - *Example:* After implementing `StdioTransport`, commit.

3.  **Commit Messages:** Use semantic commit messages:
    - `feat: ...` for new features
    - `fix: ...` for bug fixes
    - `test: ...` for tests
    - `chore: ...` for maintenance

## Your Goal
Decouple the application from the communication layer, allowing it to run over Stdio, HTTP/SSE, or any future protocol.
