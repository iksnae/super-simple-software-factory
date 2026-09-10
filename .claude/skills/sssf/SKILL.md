---
name: sssf
description: Software factory — run and observe repeatable agents+code workflows against any repo from one shared checkout. Use when the user wants to run a workflow (sdlc, plan, build, scout, quality), set the factory up on a repo, add or retune an agent roster, declare a new workflow, or watch a running job. Keywords - sssf, software factory, ADW, agent workflow, sf run, roster, workflow, visualizer.
argument-hint: "[set up a repo | run a workflow | add an agent | declare a workflow | watch a run]"
---

# Software Factory

Reusable combination of **agents plus code**. Deterministic Python owns the phase
graph — sequencing, retries, gates, acceptance; coding agents are bounded nodes
inside it; typed JSON envelopes carry context between them; everything streams
into SQLite as it happens. **Agent proposes, code disposes.**

One factory checkout serves many repositories. The target is passed with
`--repo`, never stamped into the repo.

## Startup

Three steps. Then stop.

1. Read [cookbooks/overview.md](cookbooks/overview.md) — the system map.
2. `sf list --repo <target>` — the workflows, agents, and checks this repo resolves to.
3. Print the workflows as a table — name, chain, one line on when to reach for
   it — and **wait for the engineer's request.**

`sf explain <workflow> --repo <target>` renders any one chain; use it for the
two or three worth showing, not all twelve.

```
| Workflow | Chain | Use when |
|---|---|---|
| scout | engineer -> scout | read-only recon; nothing changes |
| simple_sdlc | plan -> build -> test -> review -> document, 3 commits | the work is real and its shape is not obvious |
```

**Nothing else.** No trace-db queries, no reading the config or the engine, no
repo inventory, no last-runs summary, no diagnosing an old failure, no "current
state" dashboard. None of it was asked for, and it is not free:

- **Volunteered state is guessed state.** An orchestrator that improvised a
  status board queried a `runs` table and a `payload` column — neither exists
  (`sessions`, `payload_json`). The spec that would have said so is
  `references/observability.md`, one lazy read away. Probing to look prepared is
  how you end up confidently wrong in your first message.
- **It spends the context the real task needs**, before you know what the task is.
- **It is stale on arrival.** State printed before the request describes a system
  that the very next run changes.

Everything else — the db schema, the roster, the handoff contract — is
lazy-loaded through the routing table below, when a request actually calls for
it. Reading it early defeats the mechanism.

Two exceptions, both narrow: if the engineer's first message already contains a
request, skip the waiting and route it; and if the target repo has no config
(`sf list` says so), say that in one line instead of the table.

## Orchestrator rules

You run the system, observe the system, and help the user interact with it.
**You do no workflow's work yourself:**

- Never implement, plan, or test in an agent's place — launch the workflow and watch it.
- Never edit files inside `<repo>/.sssf/data/sessions/` — that is the run record.
- Observe by querying `<repo>/.sssf/data/sssf.db` (WAL — reads never block
  writers) **when observing is the task**. This is a capability, not a startup
  step: query it to follow a run you launched or one the engineer asked about,
  never to volunteer a status report nobody requested.
- Report phase status plainly: name, owner, status, error if any.

## Request routing (lazy-load the cookbook, then follow it)

| Request | Cookbook |
|---|---|
| set the factory up on a repo | [cookbooks/setup_repo.md](cookbooks/setup_repo.md) |
| run / monitor a workflow | [cookbooks/how_to_prompt_for_the_eng.md](cookbooks/how_to_prompt_for_the_eng.md) **first**, then [cookbooks/run_workflow.md](cookbooks/run_workflow.md) |
| turn a request into a workflow prompt | [cookbooks/how_to_prompt_for_the_eng.md](cookbooks/how_to_prompt_for_the_eng.md) |
| declare a new workflow | [cookbooks/create_workflow.md](cookbooks/create_workflow.md) |
| change an existing workflow's chain | [cookbooks/update_workflow.md](cookbooks/update_workflow.md) |
| add or retune an agent (model, thinking, tools, prompts) | [cookbooks/update_roster.md](cookbooks/update_roster.md) |
| extend the engine with new low-level logic, a gate, or an envelope | [cookbooks/update_modules.md](cookbooks/update_modules.md) |

Deep specs, when needed: [references/handoff.md](references/handoff.md) ·
[references/observability.md](references/observability.md) ·
`docs/CONFIG.md` (the layered config schema) · `docs/MODELS.md` (models, auth, harnesses).

## Hard rules

1. **Validate before running** — `sf check --repo <target>` resolves the config
   and validates every workflow against it, spending nothing. The engine also
   validates the graph it is about to run — step kinds, gate names, envelope
   types, `previous:` references — before the first agent spawns. A workflow
   naming an agent the roster lacks fails at startup, not mid-run.
2. **Typed outputs only** — every agent step declares `output:`, an envelope type
   registered in `factory/engine.py`'s `ENVELOPES`. Parse failures re-prompt the
   **same session** with a correction, context intact, never a restart.
   **The output contract is a synced triad**: (a) the type in
   `factory/modules/data_types.py`, (b) the JSON example in the agent's `user.md`
   `## Report` section, (c) `output:` at every step that names it. These are ONE
   contract — change any one, update all three in the same edit.
3. **Gates validate claims, not guesses** — a gate returns a `GateReport` of
   `{item, ok, note}` checks; failures return to the same session as corrections.
   Gate names in a workflow resolve against `engine.GATES` at validation time.
4. **Four-param rule** — any function with more than 4 parameters takes one
   concrete data type instead (`AgentCall`, `PhaseParams` are the pattern).
5. **One agent, one prompt, one purpose** — identity lives in `system.md`; task
   shape (user prompt + output type) lives at the step that calls it.
6. **Workflows are declared, not written** — a workflow is a named phase graph in
   YAML. There is no per-workflow Python. `describe_chain` renders the resolved
   graph back as a chain, so what you read is what runs and the two cannot drift.
7. **Every phase earns a description** — one sentence on what it does and why,
   never a restatement of its name. It is the only intent the trace, the console,
   and the UI ever show; `commit_plan: "Commit the plan"` is rejected at
   construction, blank is too.
8. **A known command is code, not an agent** — if you can write the invocation
   down (`bun test`, `ruff check`), it is a named entry under `quality:` in the
   target repo's config, run by a `quality` or `verify_loop` step. Agents are for
   the parts that need reading and deciding.
9. **`tools:` is a capability list, `writes:` is the boundary** — `bash` runs
   anything (including `git checkout`) and `write` reaches any path, so a tool
   list can never make "this agent changes nothing" true. `writes:` per agent and
   `protected_files` in defaults are enforced in `factory/modules/permissions.py`
   after every agent call: the working tree is fingerprinted before and after, and
   unauthorized changes fail the phase. The session runtime under `data_dir` is
   always writable — a read-only agent is read-only with respect to the REPO,
   never mute.
10. **Acceptance is separate from phase status** — a `verify_loop` that ran a red
    suite *succeeded* at its job. A workflow declares `accept: verified` when the
    run should only pass if the checks and the review came back clean, so the exit
    code, the session status, and the banner are decided together and cannot
    disagree.

## Scope

`coding_agent: pi` is the default and `codex` is implemented; `claude_code` is
schema-valid and stubbed, and selecting it raises one clear sentence. Models are
resolved through pi's live catalog (`pi --list-models`) — see `docs/MODELS.md`.

The visualizer ships at `apps/visualizer/`: `just obs ui <target>` (the repo is
positional, like every other `obs` recipe; from inside the repo, just `just obs ui`). The
`just obs` sqlite recipes are the headless equivalent and read the same db.
