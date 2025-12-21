#!/bin/bash

# Orchestration Script for Multi-Agent MCP Project
# Usage: ./orchestrate.sh

CODER_BIN="/opt/homebrew/bin/gemini"
REPO_ROOT=$(pwd)
WORKTREES_DIR="../worktrees" # Storing worktrees in a sibling directory to keep things clean

# Ensure worktrees directory exists
mkdir -p "$WORKTREES_DIR"

# Function to setup worktree and run agent
# Arguments:
# 1: Agent Name (folder name in docs/agents)
# 2: Branch Name
# 3: Worktree Path (relative to REPO_ROOT/..)
run_agent() {
    local AGENT_NAME=$1
    local BRANCH_NAME=$2
    local WORKTREE_PATH=$3
    local AGENT_DIR="$REPO_ROOT/docs/agents/$AGENT_NAME"
    local LOG_FILE="$AGENT_DIR/agent_execution.log"

    echo "---------------------------------------------------"
    echo "🚀 Launching Agent: $AGENT_NAME"
    echo "   Branch: $BRANCH_NAME"
    echo "   Worktree: $WORKTREE_PATH"
    echo "---------------------------------------------------"

    # 1. Create/Checkout Branch and Worktree
    # Check if branch exists
    if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
        echo "   Branch $BRANCH_NAME already exists."
    else
        echo "   Creating branch $BRANCH_NAME..."
        git branch "$BRANCH_NAME" master
    fi

    # Add Worktree
    # We use --force because sometimes prune doesn't clean up immediately
    echo "   Setting up worktree at $WORKTREE_PATH..."
    git worktree add --force "$WORKTREE_PATH" "$BRANCH_NAME"

    # 2. Prepare Prompt
    # Concatenate PROMPT, SKILLS, and PLAN
    local PROMPT_CONTENT=$(cat "$AGENT_DIR/PROMPT.md" "$AGENT_DIR/SKILLS.md" "$AGENT_DIR/PLAN.md")
    
    # Add a specific instruction to execute the plan
    local FINAL_PROMPT="
You are an autonomous coding agent. 
Here is your identity, skills, and the plan you must execute.
Please implement the tasks described in the PLAN.
Remember to commit your work as specified in the PROMPT.

CONTEXT:
$PROMPT_CONTENT
"

    # 3. Run Agent in Background
    # We cd into the worktree so the agent works in the correct context
    (
        cd "$WORKTREE_PATH" || exit
        echo "   Agent $AGENT_NAME started working in $(pwd)..."
        # Invoke gemini with the prompt
        # Assuming -s is for system/silent and -p is for prompt
        "$CODER_BIN" run "$FINAL_PROMPT" >> "$LOG_FILE" 2>&1
        echo "   ✅ Agent $AGENT_NAME finished."
    ) &
    
    # Return the PID of the background process
    return $!
}

# Function to wait for PIDs
wait_for_agents() {
    local pids=("$@")
    echo "⏳ Waiting for agents to complete..."
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    echo "🎉 All agents in this phase have finished."
}

# Function to merge branches
merge_branches() {
    local branches=("$@")
    echo "🔀 Merging branches: ${branches[*]}"
    
    # Ensure we are on master
    git checkout master
    
    for branch in "${branches[@]}"; do
        echo "   Merging $branch..."
        # Using --no-ff to preserve history of the feature branch
        git merge --no-ff --no-edit "$branch" || {
            echo "   ❌ Merge conflict or error merging $branch. Please resolve manually."
            exit 1
        }
    done
    echo "✅ Merge complete."
}

# ==============================================================================
# PHASE 1: Foundation & Core
# ==============================================================================
echo "=============================================================================="
echo "PHASE 1: Foundation & Core"
echo "=============================================================================="

PIDS_PHASE_1=()

# Agent 1: Infrastructure
run_agent "infrastructure" "agent/infrastructure" "$WORKTREES_DIR/mcp-infra"
PIDS_PHASE_1+=($!)

# Agent 2: Core Domain
run_agent "core_domain" "agent/core-domain" "$WORKTREES_DIR/mcp-core"
PIDS_PHASE_1+=($!)

# Wait for Phase 1
wait_for_agents "${PIDS_PHASE_1[@]}"

# Synchronization Point 1
merge_branches "agent/infrastructure" "agent/core-domain"

# Cleanup Worktrees (Optional, but good for hygiene)
git worktree remove "$WORKTREES_DIR/mcp-infra" --force
git worktree remove "$WORKTREES_DIR/mcp-core" --force


# ==============================================================================
# PHASE 2: Business Logic & Transport
# ==============================================================================
echo "=============================================================================="
echo "PHASE 2: Business Logic & Transport"
echo "=============================================================================="

PIDS_PHASE_2=()

# Agent 1: Customer Module
run_agent "customer_module" "agent/customer-module" "$WORKTREES_DIR/mcp-customers"
PIDS_PHASE_2+=($!)

# Agent 2: Invoice Module
run_agent "invoice_module" "agent/invoice-module" "$WORKTREES_DIR/mcp-invoices"
PIDS_PHASE_2+=($!)

# Agent 3: Transport
run_agent "transport" "agent/transport" "$WORKTREES_DIR/mcp-transport"
PIDS_PHASE_2+=($!)

# Wait for Phase 2
wait_for_agents "${PIDS_PHASE_2[@]}"

# Synchronization Point 2
merge_branches "agent/customer-module" "agent/invoice-module" "agent/transport"

# Cleanup Worktrees
git worktree remove "$WORKTREES_DIR/mcp-customers" --force
git worktree remove "$WORKTREES_DIR/mcp-invoices" --force
git worktree remove "$WORKTREES_DIR/mcp-transport" --force


# ==============================================================================
# PHASE 3: Expansion & Clients
# ==============================================================================
echo "=============================================================================="
echo "PHASE 3: Expansion & Clients"
echo "=============================================================================="

PIDS_PHASE_3=()

# Agent 1: Advanced Primitives
run_agent "advanced_primitives" "agent/advanced-primitives" "$WORKTREES_DIR/mcp-primitives"
PIDS_PHASE_3+=($!)

# Agent 2: SDK & CLI
run_agent "sdk_cli" "agent/sdk-cli" "$WORKTREES_DIR/mcp-clients"
PIDS_PHASE_3+=($!)

# Agent 3: Docs & Polish
run_agent "docs_polish" "agent/docs-polish" "$WORKTREES_DIR/mcp-docs"
PIDS_PHASE_3+=($!)

# Wait for Phase 3
wait_for_agents "${PIDS_PHASE_3[@]}"

# Synchronization Point 3
merge_branches "agent/advanced-primitives" "agent/sdk-cli" "agent/docs-polish"

# Cleanup Worktrees
git worktree remove "$WORKTREES_DIR/mcp-primitives" --force
git worktree remove "$WORKTREES_DIR/mcp-clients" --force
git worktree remove "$WORKTREES_DIR/mcp-docs" --force

echo "=============================================================================="
echo "PROJECT IMPLEMENTATION COMPLETE"
echo "=============================================================================="
