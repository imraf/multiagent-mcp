# MCP Architecture – Assignment 8

## Introduction
This assignment focuses on designing and building a modular AI system architecture based on MCP (Model Context Protocol) principles. The goal is to demonstrate understanding of architectural concepts learned in class, with emphasis on modularity, extensibility, and clean separation of concerns.

---

## Project Topic

### Recommended Option: Invoicing System
Build an invoicing/accounting system that includes:
- Customer management  
- Invoice creation, issuance, and tracking  
- Sequential numbering management  
- VAT calculation  
- Invoice delivery  

### Alternative Option
Students may choose a different project, subject to instructor approval, provided it demonstrates all required architectural principles.

---

## The Five Stages

### Stage 1: Basic Infrastructure
**Goal:** Establish foundational infrastructure layers.

**Components:**
- Configuration layer  
- Logging mechanisms  
- Exception handling  
- Project directory structure  
- Basic unit tests  

Students must define infrastructure services required for system expansion.

---

### Stage 2: MCP Server with Tools
**Goal:** Build a basic MCP server with tools.

**Components:**
- Tool definitions with identification and JSON schema  
- Basic business logic  
- Connection to data storage  

Students must design tools with meaningful functionality.

---

### Stage 3: The Three Primitives
**Goal:** Extend the system to support all MCP primitives.

**Components:**
- **Tools (Write):** Actions that modify system state  
- **Resources (Read):** Static and dynamic data access  
- **Prompts:** Templates for guiding model behavior  

Students must integrate all primitives into the system architecture.

---

### Stage 4: Communication Layer
**Goal:** Add a modular communication layer.

**Components:**
- Separation of communication logic  
- Support for at least one protocol (e.g., STDIO, HTTP/SSE)  
- Ability to swap communication layers without code changes  

Students choose the communication method best suited for their project.

---

### Stage 5: SDK and User Interface
**Goal:** Add an SDK and at least one user interface.

**Components:**
- SDK layer for all system operations  
- One or more interfaces (optional but recommended):
  - CLI  
  - Desktop application  
  - Web interface  
  - Other  

Students should focus on good user experience.

---

## Required Architectural Principles
- No hard-coded values; all configuration must come from configuration files  
- Modularity: components must be replaceable without affecting the system  
- Small files (recommended up to 150 lines per file)  
- No duplicated code; use reusable functions and classes  
- Object-Oriented Programming (OOP)  
- Unit tests for every component  
- Proper resource management, locking, and error handling  

---

## Submission

### Submission Structure
- A single repository containing all five stages  
- Separate branch or folder per stage  
- Each stage builds upon the previous one  
- Support for parallel development  

Using **Git Worktrees** is strongly recommended for efficient parallel AI-agent development.

---

### What to Submit
- Source code  
- Unit tests  
- Basic documentation (as per student level)  

---

## Evaluation Criteria
- Demonstration of architectural principles  
- Modularity and separation of layers  
- Code quality and testing  
- Clear progression between stages  

---

## Parallel Development with Git Worktrees

### The Problem: Parallel Work
Modern AI-assisted development often involves multiple agents working simultaneously on the same codebase.

### What Is a Worktree?
A Git Worktree allows multiple working directories linked to the same repository, each on a different branch, sharing history but keeping files isolated.

---

### Pattern: “One Branch per Agent”
Example (recommended by Anthropic):
- Each AI agent works in its own worktree  
- Shared commit history  
- True parallel development  
- Simple Git commands  

---

### Practical Guide

#### Step 1: Create Worktrees
```bash
cd /path/to/project

git worktree add ../project-agent1-feature -b agent1/new-api
git worktree add ../project-agent2-bugfix -b agent2/fix-security
git worktree add ../project-agent3-docs -b agent3/update-readme

git worktree list
```

#### Step 2: Run Agents in Parallel
```bash
# Agent 1
cd ../project-agent1-feature
claude
> Implement OAuth2 authentication for the API

# Agent 2
cd ../project-agent2-bugfix
claude
> Fix the SQL injection vulnerability in user login

# Agent 3
cd ../project-agent3-docs
claude
> Update README with new API documentation
```

#### Step 3: Merge the Work
```bash
cd /path/to/project

git merge agent1/new-api -m "Feature: OAuth2 authentication"
git merge agent2/fix-security -m "Fix: SQL injection vulnerability"

git worktree remove ../project-agent1-feature
git worktree remove ../project-agent2-bugfix
```

---

### Advanced Tips
- Use descriptive branch names (e.g., agent1/feature-oauth)  
- Keep branches in sync using:
```bash
git rebase origin/main
```
- Check for conflicts before merging:
```bash
git merge --no-commit --no-ff
```

---

## Final Note
The primary goal is not just to complete the task, but to internalize correct architectural thinking. A well-structured architecture enables scalable, maintainable, and high-quality systems.

© All rights reserved – Dr. Yair Sagal
