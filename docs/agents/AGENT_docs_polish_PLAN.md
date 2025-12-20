# Agent Plan: Docs & Polish

## Identity
- **Branch:** `agent/docs-polish`
- **Worktree Path:** `../mcp-docs`
- **Phase:** 3 (Expansion & Clients)

## Obligatory Workflow
1.  **Initial Commit:** `git commit --allow-empty -m "chore: start work on agent/docs-polish"`
2.  **Incremental Commits:** Commit after every logical step.
3.  **Semantic Messages:** Use `feat:`, `fix:`, `test:`, `docs:`.

## Assigned Tasks (Stage 6)

### 6.1 Professional Documentation
- [ ] **README.md:**
  - [ ] Eye-catching header with project logo/banner.
  - [ ] Badges (CI/CD, Python Version, License).
  - [ ] "Quick Start" GIF or terminal recording.
- [ ] **Docs Site:** Generate static documentation using `MkDocs` + `Material for MkDocs`.
  - [ ] API Reference.
  - [ ] Architecture Decision Records (ADRs).

### 6.2 Installation Experience
- [ ] Create a `Makefile` for common tasks.
- [ ] Ensure `pyproject.toml` metadata is publishable.
- [ ] Create `Dockerfile` for containerized deployment.

### 6.3 LLM Integration Guide
- [ ] **Local LLM (Ollama):** Guide on running `llama3` or `mistral` locally.
- [ ] **Proprietary APIs:** Setup for `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`.

## Definition of Done
- All tasks implemented.
- Documentation is clear, typo-free, and professional.
- Build scripts (Makefile, Dockerfile) work correctly.
