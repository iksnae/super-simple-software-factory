---
description: Creates a concise engineering implementation plan based on user requirements and saves it to specs directory
argument-hint: [user prompt] [orchestration prompt]
model: sonnet
disallowed-tools: Task, EnterPlanMode
hooks:
  Stop:
    - hooks:
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_new_file.py
            --directory specs
            --extension .md
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py
            --directory specs
            --extension .md
            --contains '## Task Description'
            --contains '## Objective'
            --contains '## Relevant Files'
            --contains '## Step by Step Tasks'
            --contains '## Acceptance Criteria'
            --contains '### Test Planning'
            --contains '## Team Orchestration'
            --contains '### Team Members'
---

# Plan With Team

Create a detailed implementation plan based on the user's requirements provided through the `USER_PROMPT` variable. Analyze the request, think through the implementation approach, and save a comprehensive specification document to `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that can be used as a blueprint for actual development work. Follow the `Instructions` and work through the `Workflow` to create the plan.

## Variables

USER_PROMPT: $1
ORCHESTRATION_PROMPT: $2 - (Optional) Guidance for team assembly, task structure, and execution strategy
PLAN_OUTPUT_DIRECTORY: `specs/`
TEAM_MEMBERS: `.claude/agents/*.md` — the 21 workspace agents, rostered below
GENERAL_PURPOSE_AGENT: `general-purpose` — fallback only, and only with a stated reason

## Team Roster

These are the agents this workspace owns. Assign from this list. Reaching for
`GENERAL_PURPOSE_AGENT` means no role below fits, and the plan must say why.

**Delivery pipeline** — in execution order; skip the phases a task does not need:

| Agent | Assign when |
|---|---|
| `intake` | The request needs framing and its ambiguities listed before anything else |
| `surveyor` | The codebase has not been read yet and later phases would be guessing |
| `product` | What to build and why is not settled — user value, acceptance criteria, scope |
| `designer` | The change has a UI/UX surface that engineering must plan against |
| `architect` | The change is structural or higher-risk and needs a shape before planning |
| `architect-reviewer` | An architecture frame exists and needs a gate verdict |
| `planner` | The request is defined and ready to become a bounded, ordered plan |
| `red-team` | A plan is drafted and needs an adversary before it reaches the gate |
| `plan-reviewer` | The plan needs its buildable / grounded / complete verdict |
| `decomposer` | An approved plan is large enough to slice into parallel packets |
| `builder` | A gate-cleared plan or packet is ready to implement red→green |
| `reviewer` | A build is finished and needs its verdict before a PR opens |

**Research chain** — fan out per angle, then judge and merge:

| Agent | Assign when |
|---|---|
| `research-decomposer` | A research question needs splitting into bounded, non-overlapping angles |
| `web-searcher` | One angle needs a search pass returning deduplicated URLs |
| `content-fetcher` | One source needs its falsifiable claims extracted |
| `adversarial-judge` | One source needs an independent attempt to refute it |
| `synthesizer` | The surviving sources need merging into a single cited report |
| `investigator` | The question crosses between the web and this codebase and needs iteration |
| `local-investigator` | The answer lives in this repository and no web access is needed |

**Interface:**

| Agent | Assign when |
|---|---|
| `chat` | The operator needs grounded Q&A about the workspace rather than work done |
| `onboarder` | A repository here has not been configured for the agents yet |

Assignment rules:

- One role per task. A task needing two roles is two tasks.
- A build task is owned by `builder`; its verdict is owned by `reviewer`. Never
  the same agent for both — the gate is the point.
- Multiple builders are fine and expected for parallel packets. Give each a
  unique name (`builder-cli`, `builder-daemon`) and name `builder` as the type.
- Code changes land in the submodule that owns them, and the root pins the
  pointer afterwards (`AGENTS.md`). A task touching submodule code names that
  repository.

## Instructions

- **PLANNING ONLY**: Do NOT build, write code, or deploy agents. Your only output is a plan document saved to `PLAN_OUTPUT_DIRECTORY`.
- If no `USER_PROMPT` is provided, stop and ask the user to provide it.
- If `ORCHESTRATION_PROMPT` is provided, use it to guide team composition, task granularity, dependency structure, and parallel/sequential decisions.
- Carefully analyze the user's requirements provided in the USER_PROMPT variable
- Determine the task type (chore|feature|refactor|fix|enhancement) and complexity (simple|medium|complex)
- Think deeply (ultrathink) about the best approach to implement the requested functionality or solve the problem
- Understand the codebase directly without subagents to understand existing patterns and architecture
- Follow the Plan Format below to create a comprehensive implementation plan
- Include all required sections and conditional sections based on task type and complexity
- Generate a descriptive, kebab-case filename based on the main topic of the plan
- Save the complete implementation plan to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`
- Ensure the plan is detailed enough that another developer could follow it to implement the solution
- Include code examples or pseudo-code where appropriate to clarify complex concepts
- Consider edge cases, error handling, and cross-platform (macOS/Linux) concerns
- Understand your role as the team lead. Refer to the `Team Orchestration` section for more details.

### Team Orchestration

As the team lead, you have access to powerful tools for coordinating work across multiple agents. You NEVER write code directly - you orchestrate team members using these tools.

#### Task Management Tools

**TaskCreate** - Create tasks in the shared task list:
```typescript
TaskCreate({
  subject: "Update build script for new binary",
  description: "Add download and signing steps for the new binary. See specs/add-binary-plan.md for details.",
  activeForm: "Updating build script"  // Shows in UI spinner when in_progress
})
// Returns: taskId (e.g., "1")
```

**TaskUpdate** - Update task status, assignment, or dependencies:
```typescript
TaskUpdate({
  taskId: "1",
  status: "in_progress",  // pending -> in_progress -> completed
  owner: "builder-cli"   // Assign to specific team member
})
```

**TaskList** - View all tasks and their status:
```typescript
TaskList({})
// Returns: Array of tasks with id, subject, status, owner, blockedBy
```

**TaskGet** - Get full details of a specific task:
```typescript
TaskGet({ taskId: "1" })
// Returns: Full task including description
```

#### Task Dependencies

Use `addBlockedBy` to create sequential dependencies - blocked tasks cannot start until dependencies complete:

```typescript
// Task 2 depends on Task 1
TaskUpdate({
  taskId: "2",
  addBlockedBy: ["1"]  // Task 2 blocked until Task 1 completes
})

// Task 3 depends on both Task 1 and Task 2
TaskUpdate({
  taskId: "3",
  addBlockedBy: ["1", "2"]
})
```

Dependency chain example:
```
Task 1: Update common.sh utilities  -> no dependencies
Task 2: Update build.sh             -> blockedBy: ["1"]
Task 3: Update build-linux.sh       -> blockedBy: ["1"]
Task 4: Test full pipeline           -> blockedBy: ["2", "3"]
```

#### Owner Assignment

Assign tasks to specific team members for clear accountability:

```typescript
// Assign task to a specific builder
TaskUpdate({
  taskId: "1",
  owner: "builder-cli"
})

// Team members check for their assignments
TaskList({})  // Filter by owner to find assigned work
```

#### Agent Deployment with Task Tool

**Task** - Deploy an agent to do work:
```typescript
Task({
  description: "Update build script",
  prompt: "Update build.sh to include the new binary as specified in Task 1...",
  subagent_type: "builder",
  model: "haiku",  // or "sonnet" for complex work, "haiku" for VERY simple
  run_in_background: false  // true for parallel execution
})
// Returns: agentId (e.g., "a1b2c3")
```

#### Resume Pattern

Store the agentId to continue an agent's work with preserved context:

```typescript
// First deployment - agent works on initial task
Task({
  description: "Update packaging scripts",
  prompt: "Update the macOS packaging scripts...",
  subagent_type: "builder"
})
// Returns: agentId: "abc123"

// Later - resume SAME agent with full context preserved
Task({
  description: "Continue packaging updates",
  prompt: "Now update the Linux packaging scripts...",
  subagent_type: "builder",
  resume: "abc123"  // Continues with previous context
})
```

When to resume vs start fresh:
- **Resume**: Continuing related work, agent needs prior context
- **Fresh**: Unrelated task, clean slate preferred

#### Parallel Execution

Run multiple agents simultaneously with `run_in_background: true`:

```typescript
// Launch multiple agents in parallel
Task({
  description: "Update macOS packaging",
  prompt: "...",
  subagent_type: "builder",
  run_in_background: true
})
// Returns immediately with agentId and output_file path

Task({
  description: "Update Linux packaging",
  prompt: "...",
  subagent_type: "builder",
  run_in_background: true
})
// Both agents now working simultaneously

// Check on progress
TaskOutput({
  task_id: "agentId",
  block: false,  // non-blocking check
  timeout: 5000
})

// Wait for completion
TaskOutput({
  task_id: "agentId",
  block: true,  // blocks until done
  timeout: 300000
})
```

#### Orchestration Workflow

1. **Create tasks** with `TaskCreate` for each step in the plan
2. **Set dependencies** with `TaskUpdate` + `addBlockedBy`
3. **Assign owners** with `TaskUpdate` + `owner`
4. **Deploy agents** with `Task` to execute assigned work
5. **Monitor progress** with `TaskList` and `TaskOutput`
6. **Resume agents** with `Task` + `resume` for follow-up work
7. **Mark complete** with `TaskUpdate` + `status: "completed"`

## Workflow

IMPORTANT: **PLANNING ONLY** - Do not execute, build, or deploy. Output is a plan document.

1. Analyze Requirements - Parse the USER_PROMPT to understand the core problem and desired outcome
2. Understand Codebase - Without subagents, directly understand existing patterns, architecture, and relevant files
3. Design Solution - Develop technical approach including architecture decisions and implementation strategy
4. Define Team Members - Use `ORCHESTRATION_PROMPT` (if provided) to guide team composition. Assign from the `Team Roster`; fall back to `GENERAL_PURPOSE_AGENT` only when no role fits, and say why. Document in plan.
5. Define Step by Step Tasks - Use `ORCHESTRATION_PROMPT` (if provided) to guide task granularity and parallel/sequential structure. Write out tasks with IDs, dependencies, assignments. Document in plan.
6. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic
7. Save Plan - Write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md`
8. Save & Report - Follow the `Report` section to write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md` and provide a summary of key components

## Plan Format

- IMPORTANT: Replace <requested content> with the requested content. It's been templated for you to replace. Consider it a micro prompt to replace the requested content.
- IMPORTANT: Anything that's NOT in <requested content> should be written EXACTLY as it appears in the format below.
- IMPORTANT: Follow this EXACT format when creating implementation plans:

```md
# Plan: <task name>

## Task Description
<describe the task in detail based on the prompt>

## Objective
<clearly state what will be accomplished when this plan is complete>

<if task_type is feature or complexity is medium/complex, include these sections:>
## Problem Statement
<clearly define the specific problem or opportunity this task addresses>

## Solution Approach
<describe the proposed solution approach and how it addresses the objective>
</if>

## Relevant Files
Use these files to complete the task:

<list files relevant to the task with bullet points explaining why. Include new files to be created under an h3 'New Files' section if needed>

Key files:
<list the files this task actually touches, each with one line on why, and the
repository each lives in. Verify every path exists before writing it.>

<if complexity is medium/complex, include this section:>
## Implementation Phases
### Phase 1: Foundation
<describe any foundational work needed>

### Phase 2: Core Implementation
<describe the main implementation work>

### Phase 3: Integration & Polish
<describe integration, testing, and final touches>
</if>

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members
<list the team members you'll use to execute the plan>

- Builder
  - Name: <unique name for this builder - this allows you and other team members to reference THIS builder by name. Take note there may be multiple builders, the name make them unique.>
  - Role: <the single role and focus of this builder will play>
  - Agent Type: <the agent name from the `Team Roster` — usually `builder`. Use GENERAL_PURPOSE_AGENT only when no rostered role fits, and state the reason.>
  - Resume: <default true. This lets the agent continue working with the same context. Pass false if you want to start fresh with a new context.>
- <continue with additional team members as needed in the same format as above>

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

<list step by step tasks as h3 headers. Start with foundational work, then core implementation, then validation.>

### 1. <First Task Name>
- **Task ID**: <unique kebab-case identifier, e.g., "update-common-sh">
- **Depends On**: <Task ID(s) this depends on, or "none" if no dependencies>
- **Assigned To**: <team member name from Team Members section>
- **Agent Type**: <agent name from the `Team Roster`; GENERAL_PURPOSE_AGENT only with a stated reason>
- **Parallel**: <true if can run alongside other tasks, false if must be sequential>
- <specific action to complete>
- <specific action to complete>

### 2. <Second Task Name>
- **Task ID**: <unique-id>
- **Depends On**: <previous Task ID, e.g., "update-common-sh">
- **Assigned To**: <team member name>
- **Agent Type**: <agent name from the `Team Roster`; GENERAL_PURPOSE_AGENT only with a stated reason>
- **Parallel**: <true/false>
- <specific action>
- <specific action>

### 3. <Continue Pattern>

### N. <Final Validation Task>
- **Task ID**: validate-all
- **Depends On**: <all previous Task IDs>
- **Assigned To**: <reviewer team member>
- **Agent Type**: `reviewer`
- **Parallel**: false
- Run all validation commands
- Verify acceptance criteria met

<continue with additional tasks as needed. Every Agent Type must be a name from the `Team Roster`.>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the task to be considered complete. include Test Planning section>

## Validation Commands
Execute these commands to validate the task is complete:

<list the commands that actually validate this work, per repository. Take them
from `RULES.md` Testing Guidelines — `just check` for root docs and metadata,
`go test ./...` in a Go module, `npm run build` for khaos-app. Every command
must run as written.>

## Notes
<optional additional context, considerations, or dependencies>
```

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/<filename>.md
Topic: <brief description of what the plan covers>
Key Components:
- <main component 1>
- <main component 2>
- <main component 3>

Team Task List:
- <list of tasks, and owner (concise)>

Team members:
- <list of team members and their roles (concise)>

When you're ready, you can execute the plan in a new agent by running:
/build <replace with path to plan>
```
