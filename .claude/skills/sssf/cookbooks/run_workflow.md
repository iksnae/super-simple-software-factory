# Run a Workflow

Run a workflow and report on it. **You run and observe — you never step into the
process or do the work yourself.**

## Step 0 — translate the request

**Read [how_to_prompt_for_the_eng.md](how_to_prompt_for_the_eng.md) before you
launch anything.** The prompt you pass is read by every agent in the chain, so it
gets written deliberately: same intent, sharper words, verified paths, and a
stated "done means". That cookbook is the whole procedure; this one starts once
you have the prompt.

## The orchestrator's posture

The workflow is the worker. Your job is to launch it, watch the trace, and tell
the engineer what happened. Do not read the agent's target files and "help", do
not fix the code an agent was supposed to fix, do not edit an envelope. If a run
fails, report the failing phase and its violations — the fix is a config, prompt,
or workflow change, made deliberately, and then a re-run.

## Launch

Which chain to launch is decided in `how_to_prompt_for_the_eng.md`, and the short
version is: **the workflow the engineer named, or else the most complete chain
the work justifies — never a single-agent one.**

```bash
sf list --repo <target>                    # what this repo resolves to
sf explain <workflow> --repo <target>      # the chain, rendered from config
```

Read those from disk every time. Workflows are the engineer's to add and retune,
so a name you remember from a doc is a guess.

```bash
sf run sdlc "add a /health endpoint" --repo ~/Projects/my-app
sf run plan_build requests/health.md --repo ~/Projects/my-app
sf run build "implement the plan" --repo ~/Projects/my-app --adw-id a1b2c3d4
sf run scout "where is auth handled" --repo ~/Projects/my-app --roster frontier
```

The prompt is inline text or a file path. Launch in the background so you can
poll while it works; the `adw_id` is printed on startup — capture it, everything
else keys off it.

From inside the target repo, `just` supplies `--repo` for you: `just sdlc "..."`.

### Listen for the roster

The workflow says *what runs*; the roster says *who runs it*. **If the engineer
references a roster, a config, or a model tier, pass it — do not fall through to
the default.**

```bash
just config rosters                        # every roster, and the model each agent runs
```

They will rarely say `--roster`. Treat any of these as naming one, then resolve
it against what is actually on disk:

| What they say | What it means |
|---|---|
| "run it on the frontier roster" | the roster file whose name matches |
| "use the big models", "the sota roster" | the non-default roster — confirm which if there is more than one |
| "have opus plan this one" | a roster whose planner is that model; if none exists, say so rather than editing the roster mid-request |
| nothing about models at all | the default |

Two things that bite:

- **Never swap rosters on your own.** A different roster is a different cost and
  a different result. If the default's model looks wrong for the work, say so and
  let the engineer choose.
- **Switching rosters mid-session breaks resumption.** `agent_map.json` records
  the model each harness session was created with, so a joined run (`--adw-id`)
  whose roster now names a different model starts that agent **fresh** instead of
  resuming its context window. That is deliberate — a bad resume is worse — but
  it means "plan on frontier, then build on default" costs the builder its
  accumulated context. Say so when you report it.

`--adw-id` is optional on **every** workflow. Given one, the run joins that
session if it exists or creates it pinned to that id: same `sessions/{adw_id}/`
dirs, same `context_handoff/`, envelopes appended, each agent resuming its
existing context window via `agent_map.json`. That is how you chain workflows —
plan under one id, then build under the same id.

## Observe

The trace db is `<repo>/.sssf/data/sssf.db`. It is WAL, so reads never block the
running writers — poll it as often as you like.

```bash
just obs sessions  <repo>            # recent runs: workflow, status, phases, spend
just obs phases    <adw_id> <repo>   # where the run stands, in order, with timings
just obs tail      <adw_id> <repo>   # follow a live run — cursor on rowid
just obs gates     <adw_id> <repo>   # what every gate checked and found
just obs envelopes <adw_id> <repo>   # the typed output each agent produced
just obs costs     <repo>            # spend per agent and per model
just obs artifacts <adw_id> <repo>   # prompts, diffs, and check logs on disk
just obs ui        <repo>            # the visualizer on http://localhost:4600
```

Poll on a cursor: keep the highest `rowid` you have seen and query
`where rowid > ?`. Don't re-read the whole table each pass.

`tool_call` rows carry a real span, so durations come off the columns — see
`references/observability.md` for which fields each event type populates.

The run also narrates to stdout, and every line it prints is written to the db as
a `log` event — terminal and swim lane tell the same story by construction, so
tailing the background process is a valid second view rather than a competing
source of truth.

Files are the raw record if you need more than the db shows:
`<repo>/.sssf/data/sessions/{adw_id}/{agent}/raw_output.jsonl` (the full harness
stream), `envelope.json` (the parsed final response), `prompts/` (exactly what
was sent), and `context_handoff/` (what agents wrote for each other).

## When a run is stuck

A hung agent produces no events at all, so the trace goes quiet rather than red.
Read it in this order:

```bash
just obs phases <adw_id> <repo>      # which phase is still `running`
just obs procs  <repo>               # what that phase is actually running, with pids
```

`processes` rows with `ended_at IS NULL` are the live ones, and `procs` verifies
each recorded command still matches the pid before reporting it live — pids get
recycled. If `procs` shows a harness child but the phase has produced no
`tool_call` events and its `raw_output.jsonl` is empty, the agent never got
started properly. Check that the model resolves and that the provider
authenticates rather than waiting it out.

**Read the raw stream before believing the error.** A harness-level failure can
surface as a parse complaint: a run whose builder died on a provider `401` was
reported as `never produced valid BuildOutput JSON`, and the 401 was visible only
in `raw_output.jsonl` as `stopReason: "error"` with an `errorMessage`. When a
phase fails in seconds with no tool calls, open the raw stream before repeating
the engine's summary to the engineer.

## Report

Tell the engineer, in order: which workflow and which roster you launched (name
the roster whenever it was not the default), which phase is running now (or which
failed), phase statuses in sequence, and for a failure the gate violations or the
error verbatim.

Remember **every phase defaults to `fail`** — a phase showing `fail` may simply
never have completed. Don't dress up a partial run as a success, and don't repeat
an error summary you have not checked against the raw stream.
