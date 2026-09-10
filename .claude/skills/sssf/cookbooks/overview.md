# Overview

The system map the orchestrator reads on startup — what the factory is, how one
checkout serves many repos, and which cookbook to load next.

## What it is

The factory builds repeatable **agents plus code** workflows. Deterministic
Python owns the phase graph; agents are bounded nodes inside it. Agent proposes,
code disposes.

Your job as orchestrator: **run the system, observe the system, help the
engineer interact with it.** You do not do the work a workflow exists to do.

## Two locations, and the boundary between them

Nothing is stamped into a target repo. One factory checkout is pointed at a repo
with `--repo`.

```
<factory checkout>/                  the shared machinery — one copy, many repos
├── scripts/sf.py                    the one entrypoint
├── factory/
│   ├── cli.py                       run | list | explain | check | doctor | init
│   ├── engine.py                    the workflow interpreter: eight step kinds
│   ├── paths.py                     factory_home vs repo_root — the two-root rule
│   ├── stacks.py                    stack detection, for `sf init`
│   └── modules/                     ALL low-level logic
│       ├── data_types.py            AgentCall, PhaseParams, envelopes, config models
│       ├── agents.py                config load/merge/validate, agent execution
│       ├── runner.py                the Run object: run.phase(...) -> ph.call(...)
│       ├── agent_pi.py              the pi harness   ·   agent_codex.py  the Codex CLI
│       ├── agent_cc.py              Claude Code — stubbed, raises one clear sentence
│       ├── gates.py                 gate(envelope, run) -> GateReport
│       ├── permissions.py           what an agent may CHANGE, enforced after the fact
│       ├── quality.py               run a named check, record it, hand failures back
│       ├── changes.py               git diff vs a resolved base -> envelope
│       └── prompts.py, session.py, tracer.py, console.py, git_helper.py, utils.py
├── config/
│   ├── base.yaml                    WHAT runs: the stock workflows, limits, paths
│   ├── rosters/*.yaml               WHO runs it: model staffing per agent
│   ├── prompts/{agent}/{system,user}.md
│   └── harness/                     pi extensions
└── .claude/skills/sssf/             this skill, and apps/visualizer

<target repo>/                       the repo being worked on
├── sssf.config.yaml                 AGAINST WHAT: your commands, your overrides
└── .sssf/data/                      gitignored runtime
    ├── sssf.db                      the trace — SQLite, WAL
    └── sessions/{adw_id}/
        ├── agent_map.json           agent -> harness session_id + model
        ├── context_handoff/         the one place agents write files for each other
        └── {agent}/{prompts/, raw_output.jsonl, envelope.json}
```

**The target repo holds exactly two things**: its config and its gitignored run
data. Everything else is the factory's.

## The three config layers

Each answers one question, and only the third belongs to the repo.

```
config/base.yaml                WHAT runs      stock workflows, loop bounds, paths
config/rosters/*.yaml           WHO runs it    model staffing per agent
<repo>/sssf.config.yaml         AGAINST WHAT   its commands, its overrides
```

`extends:` chains them, and merges are **by name** — an override naming `builder`
edits the builder and leaves the other agents alone. `just config layers` prints
the resolution order for any repo. Full schema: `docs/CONFIG.md`.

## The phase model

Every run is a sequence of **phases**. Three kinds, three swim lanes:

- **engineer** — the human lane; the request phase (who asked, and for what).
- **agent** — prompt in, typed envelope out, gates verified.
- **code** — deterministic steps that stand alone (prepare, quality, git). Never
  buried inside an agent phase.

**Success must be earned — every phase defaults to `fail`.** A clean exit flips
it to success; agent phases additionally require the envelope to parse and all
gates to come back green. A raise keeps it failed, records an error event, and
aborts the run.

## The eight step kinds

A workflow is a declared graph, not a script. `factory/engine.py` interprets:

| Step | Does |
|---|---|
| `request` | record the incoming ask — the engineer's own phase |
| `agent` | one agent call: typed envelope out, gates verified |
| `quality` | run named deterministic checks |
| `verify_loop` | quality, then an agent repair, bounded — "does it run" |
| `review_loop` | an agent verdict, then an agent revision, bounded — "is it what was asked" |
| `changes` | diff the run against its pinned baseline, for a documenter |
| `commit` | commit the tree in one agent's own words |
| `group` | a nested list of steps, usually behind a `when:` condition |

Ahead of all of them, when the repo's config declares `prepare:`, comes one
phase no workflow asks for: the commands that make the tree runnable at all. It
is not a step kind because it is not a choice — a tree with no dependencies
installed cannot be planned against, built in, or tested. **A failed prepare
aborts**, before any agent spawns and before any money is spent.

## Envelopes

Agents have exactly two output channels: reference files written into
`context_handoff/`, and a **final valid-JSON response** parsed against the
envelope type the step declared. Code persists it as `envelope.json` and injects
it into the next agent's `user.md` via `{{previous_envelope}}`. Bad JSON is never
a restart — the harness re-prompts the *same session, context intact*, bounded.
See `references/handoff.md`.

**The output contract is a synced triad**: the type in `data_types.py` ↔ the
`## Report` JSON example in the agent's `user.md` ↔ `output:` on every step that
names it. Editing one means editing all three.

## Running a workflow

```bash
sf run sdlc "add a /health endpoint" --repo ~/Projects/my-app
sf run plan_build requests/health.md --repo ~/Projects/my-app --adw-id a1b2c3d4
```

The prompt is inline text or a file path. `just` wraps every workflow so the repo
defaults to the directory you are standing in. `--adw-id` is optional on every
workflow: given one, the run joins that session (same dirs, same
`context_handoff/`, agents resume their existing context windows); omitted, a
fresh id is minted and printed.

## When you have finished reading this

You are done with startup. List the workflows (`sf list --repo <target>`) as a
table and **wait for the engineer's request.**

Do not survey anything else — not the trace db, not the config, not past runs,
not the repo tree. You do not yet know what the request is, so anything you
gather now is a guess about what will matter, spent from the context the real
work needs. Every cookbook and reference below is lazy-loaded, one per request,
and that is the whole design.

## Where to go next

| Request | Cookbook |
|---|---|
| Turn a request into the prompt a workflow gets | `how_to_prompt_for_the_eng.md` — **read before every launch** |
| Set the factory up on a repo | `setup_repo.md` |
| Run and monitor a workflow | `how_to_prompt_for_the_eng.md`, then `run_workflow.md` |
| Declare a new workflow | `create_workflow.md` |
| Change an existing workflow's chain | `update_workflow.md` |
| Add or retune an agent | `update_roster.md` |
| Add low-level logic, a gate, or an envelope | `update_modules.md` |

References, loaded when you need the spec: `references/handoff.md` (envelope +
session layout), `references/observability.md` (events, db tables, polling),
`docs/CONFIG.md` (the full config schema), `docs/MODELS.md` (models, auth,
harnesses).
