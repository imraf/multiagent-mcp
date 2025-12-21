#!/bin/bash

# Orchestration Script for Multi-Agent MCP Project
# Usage: ./orchestrate.sh

CODER_BIN="/opt/homebrew/bin/opencode"
REPO_ROOT=$(pwd)
WORKTREES_DIR="../worktrees" # Storing worktrees in a sibling directory to keep things clean
AGENTS_DOC_DIR="$REPO_ROOT/docs/agents"

# Ensure worktrees directory exists
mkdir -p "$WORKTREES_DIR"

# Global array to track active background processes
ACTIVE_PIDS=()

# Function to setup worktree and run agent
# Arguments:
# 1: Agent Name (folder name in docs/agents)
# 2: Branch Name
# 3: Worktree Path (relative to REPO_ROOT/..)
run_agent() {
    local AGENT_NAME=$1
    local BRANCH_NAME=$2
    local WORKTREE_PATH=$3
    local AGENT_DIR="$AGENTS_DOC_DIR/$AGENT_NAME"
    local LOG_FILE="$AGENT_DIR/agent_execution.log"
    local PROGRESS_FILE="$AGENT_DIR/progress.json"

    echo "---------------------------------------------------"
    echo "🚀 Agent: $AGENT_NAME"
    echo "---------------------------------------------------"

    # 0. Check Progress
    if [ -f "$PROGRESS_FILE" ]; then
        # Check if status is completed
        if grep -q '"status": *"completed"' "$PROGRESS_FILE"; then
            echo "   ✅ Agent $AGENT_NAME has already completed its tasks. Skipping."
            return 0
        fi
        echo "   🔄 Found existing progress. Resuming..."
    else
        echo "   🆕 No progress record found. Starting fresh."
        # Initialize progress file
        echo '{ "status": "in-progress", "completed_tasks": [] }' > "$PROGRESS_FILE"
    fi

    # 1. Create/Checkout Branch and Worktree
    # Check if branch exists
    if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
        echo "   Branch $BRANCH_NAME exists."
    else
        echo "   Creating branch $BRANCH_NAME..."
        git branch "$BRANCH_NAME" master
    fi

    # Add Worktree
    # We use --force because sometimes prune doesn't clean up immediately
    echo "   Setting up worktree at $WORKTREE_PATH..."
    git worktree add --force "$WORKTREE_PATH" "$BRANCH_NAME"

    # Copy opencode.json to the worktree
    if [ -f "$REPO_ROOT/opencode.json" ]; then
        echo "   Copying opencode.json to worktree..."
        cp "$REPO_ROOT/opencode.json" "$WORKTREE_PATH/"
    else
        echo "   ⚠️  Warning: opencode.json not found in root. Agent might fail if it depends on it."
    fi

    # 2. Prepare Prompt
    # Concatenate PROMPT, SKILLS, and PLAN
    local PROMPT_CONTENT=$(cat "$AGENT_DIR/PROMPT.md" "$AGENT_DIR/SKILLS.md" "$AGENT_DIR/PLAN.md")
    local CURRENT_PROGRESS=$(cat "$PROGRESS_FILE")
    
    # Add a specific instruction to execute the plan and track progress
    local FINAL_PROMPT="
You are an autonomous coding agent. 
Here is your identity, skills, and the plan you must execute.

CONTEXT:
$PROMPT_CONTENT

IMPORTANT - PROGRESS TRACKING:
You have a progress tracking file at: progress.json
Current content:
$CURRENT_PROGRESS

YOUR INSTRUCTIONS:
1. Analyze the 'completed_tasks' in the progress file.
2. Compare with your PLAN.md to determine the next logical step.
3. Execute the next step(s).
4. CRITICAL: After completing a step, you MUST append it to the 'completed_tasks' list in progress.json.
5. If you have finished ALL tasks in your PLAN, you MUST update the 'status' field in progress.json to 'completed'.

Please proceed with your work.
"

    # 3. Run Agent in Background
    # We cd into the worktree so the agent works in the correct context
    (
        cd "$WORKTREE_PATH" || exit
        
        # Initialize progress file in the worktree if it doesn't exist (or copy from master if we want persistence across runs, 
        # but here we want it in the branch. We'll initialize it with what we know from master/previous runs)
        echo "$CURRENT_PROGRESS" > "progress.json"

        echo "   ▶️  Agent $AGENT_NAME running..."
        # Invoke opencode with the prompt
        "$CODER_BIN" run "$FINAL_PROMPT" >> "agent_execution.log" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Agent $AGENT_NAME finished execution loop."
            # Sync progress back to master/docs for persistence across script runs if needed, 
            # OR just leave it in the branch. The requirement says "write their logs in their own branch".
            # So we leave agent_execution.log in the worktree.
            
            # However, for the script to know if it's done on next run, we might need to sync progress.json back?
            # The user said "Agents should write their logs in their own branch".
            # But the orchestration script checks "$AGENT_DIR/progress.json" (which is in master/docs) to decide whether to skip.
            # If we only write to the branch, the orchestration script won't see it next time unless we merge.
            # But we merge at the end of the phase. So if the script crashes mid-phase, we lose progress info if we don't sync back.
            # Let's assume we sync progress.json back to the docs folder for orchestration tracking, 
            # but keep the heavy logs in the branch.
            
            cp "progress.json" "$AGENT_DIR/progress.json"
        else
            echo "   ❌ Agent $AGENT_NAME failed (exit code $?). Check logs in $WORKTREE_PATH/agent_execution.log."
        fi
    ) &
    
    # Store PID
    ACTIVE_PIDS+=($!)
}

# Function to wait for PIDs
wait_for_agents() {
    if [ ${#ACTIVE_PIDS[@]} -eq 0 ]; then
        echo "   ℹ️  No active agents to wait for."
        return
    fi

    echo "⏳ Waiting for ${#ACTIVE_PIDS[@]} agents to complete..."
    for pid in "${ACTIVE_PIDS[@]}"; do
        wait "$pid"
    done
    echo "🎉 Phase complete."
    # Reset PIDs for next phase
    ACTIVE_PIDS=()
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

# Agent 1: Infrastructure
run_agent "infrastructure" "agent/infrastructure" "$WORKTREES_DIR/mcp-infra"

# Agent 2: Core Domain
run_agent "core_domain" "agent/core-domain" "$WORKTREES_DIR/mcp-core"

# Wait for Phase 1
wait_for_agents

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

# Agent 1: Customer Module
run_agent "customer_module" "agent/customer-module" "$WORKTREES_DIR/mcp-customers"

# Agent 2: Invoice Module
run_agent "invoice_module" "agent/invoice-module" "$WORKTREES_DIR/mcp-invoices"

# Agent 3: Transport
run_agent "transport" "agent/transport" "$WORKTREES_DIR/mcp-transport"

# Wait for Phase 2
wait_for_agents

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

# Agent 1: Advanced Primitives
run_agent "advanced_primitives" "agent/advanced-primitives" "$WORKTREES_DIR/mcp-primitives"

# Agent 2: SDK & CLI
run_agent "sdk_cli" "agent/sdk-cli" "$WORKTREES_DIR/mcp-clients"

# Agent 3: Docs & Polish
run_agent "docs_polish" "agent/docs-polish" "$WORKTREES_DIR/mcp-docs"

# Wait for Phase 3
wait_for_agents

# Synchronization Point 3
merge_branches "agent/advanced-primitives" "agent/sdk-cli" "agent/docs-polish"

# Cleanup Worktrees
git worktree remove "$WORKTREES_DIR/mcp-primitives" --force
git worktree remove "$WORKTREES_DIR/mcp-clients" --force
git worktree remove "$WORKTREES_DIR/mcp-docs" --force

echo "=============================================================================="
echo "PROJECT IMPLEMENTATION COMPLETE"
echo "=============================================================================="
