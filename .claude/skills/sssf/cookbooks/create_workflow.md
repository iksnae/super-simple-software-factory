# Create a Workflow

A workflow is a **declared phase graph**, not a script. There is no Python to
write: you add a named entry under `workflows:` and `factory/engine.py` runs it.

Stock workflows live in `config/base.yaml`. A repo may declare its own in its
`sssf.config.yaml` — same shape, merged by name, so a repo can also override a
stock one.

## Step 1 — Design the chain

Answer four questions, in order:

1. **What agents, in what order?** Pick from the roster (`just config rosters`).
   The starter five cover most chains:

| Agent | Use when | `output:` | Typical `gates:` |
|---|---|---|---|
| `scout` | you need to FIND something first — read-only recon | `ScoutOutput` | `artifacts_exist` |
| `planner` | the work needs a plan before code changes | `PlanOutput` | `artifacts_exist`, `files_non_empty` |
| `builder` | code must change | `BuildOutput` | `diff_matches_claims` |
| `reviewer` | the change must be confirmed to BE what was asked for | `ReviewOutput` | `artifacts_exist`, `verdict_consistent` |
| `documenter` | finished work needs a write-up (runs after a `changes` step) | `DocumentOutput` | `artifacts_exist`, `files_non_empty` |
| *(no tester)* | verifying that it RUNS is a `quality` or `verify_loop` step | — | the exit code is the check |
| any agent, generic ask | one-off prompt, no special shape | `GenericOutput` | as needed |

   A new kind of agent needs a roster entry, a prompt pair, and an envelope type
   first — see `update_roster.md` and `update_modules.md`.

   **The suite and the reviewer answer different questions.** "Does it run" is a
   test, and code can ask that. "Is this the thing that was asked for" is a
   review, and only an agent can. A green suite over a feature nobody requested
   is still a failed request, and neither one covers for the other.

2. **Where does code act?** `quality`, `changes`, and `commit` are their own
   steps — never buried inside an agent phase. Running the suite is one of these:
   the command is a named entry under the repo's `quality:` block, so no agent
   rediscovers `bun test` on every run.

3. **Does anything loop?** Use `verify_loop` (checks, then a bounded agent
   repair) or `review_loop` (a verdict, then a bounded agent revision). Do not
   hand-roll a loop; the engine bounds them from `limits:`.

4. **What must each call prove?** Pick gates per step from `engine.GATES`:
   `artifacts_exist`, `files_non_empty`, `json_parses`, `diff_matches_claims`,
   `verdict_consistent`. New reusable gates go in `factory/modules/gates.py` and
   must be registered — `update_modules.md`.

## Step 2 — Declare it

```yaml
workflows:
  plan_build:
    description: Planner then builder. No verification.
    requires: [planner, builder]      # optional; owners are inferred anyway
    pin_baseline: true                # capture HEAD before the first commit
    accept: verified                  # "" = phases only; "verified" = also the verdict
    accept_reason: the suite or the review never came back clean
    steps:
      - step: request
        description: Capture the incoming ask

      - step: agent
        name: plan
        owner: planner
        output: PlanOutput
        gates: [artifacts_exist, files_non_empty]
        description: Turn the request into an implementable plan

      - step: agent
        name: build
        owner: builder
        output: BuildOutput
        previous: plan                # hands the plan envelope forward
        gates: [diff_matches_claims]
        retries: 1                    # extra GATE-correction rounds, same session
        description: Implement the plan exactly

      - step: commit
        name: commit_build
        source: build                 # commits in the builder's own words
        description: Land the code once, in the words of the agent that wrote it
```

### The fields, by step kind

| Step | Requires | Also takes |
|---|---|---|
| `request` | — | `name`, `description` |
| `agent` | `name`, `owner`, `output` | `previous`, `gates`, `retries`, `when` |
| `quality` | `name`, and `checks:` or `group:` | `when` |
| `verify_loop` | `name`, `checks:`/`group:`, `repair:` | `max_attempts`, `when` |
| `review_loop` | `name`, `owner`, `output` | `repair:`, `max_attempts`, `previous`, `gates`, `when` |
| `changes` | `name` | `base:` (default `baseline`), `when` |
| `commit` | `name`, `source` | `when` |
| `group` | `steps:` | `when` |

`repair:` **must be `step: agent`** — the loops hand it straight to the agent
phase without inspecting its kind, so anything else is refused at validation.

### The loops

```yaml
      - step: verify_loop
        name: test
        group: test                   # a named group from the repo's quality: block
        description: Run the suite — a known command, so code runs it
        repair:
          step: agent
          name: fix
          owner: builder
          output: BuildOutput
          gates: [diff_matches_claims]
          retries: 1
          description: Repair what the suite reported, from its verbatim output
```

The loop runs the checks, and on red hands the **verbatim output** to the repair
agent as its previous envelope, bounded by `max_attempts` or `limits.max_fix_loops`.

`review_loop` is the same shape with the verdict first. Omit its `repair:` and it
becomes a single verdict with no revision.

### Conditions

`when:` takes `verified`, `not_verified`, or `revised_and_approved`. Use `group`
to put several steps behind one:

```yaml
      - step: group
        when: verified
        steps:
          - step: commit
            name: commit_build
            source: build
            description: Land the code only now — green suite, approved review
          - step: changes
            name: changes
            description: Capture what this run changed, for the write-up
          - step: agent
            name: document
            owner: documenter
            output: DocumentOutput
            previous: changes
            description: Write up what shipped, from the diff
```

`revised_and_approved` exists for one reason: a revision edited code **after** the
suite last ran, so that green light is stale and must be re-earned before
anything is committed.

## Non-negotiables

- **Every agent step declares `output:`** — an envelope type registered in
  `engine.ENVELOPES`. No untyped handoffs.
- **`previous:` carries the chain** — the named step's envelope lands in the next
  agent's `user.md` as `{{previous_envelope}}`; bulky context travels as
  `context_handoff/` files the envelope references.
- **Step names are unique within a workflow** and are how later steps address
  earlier results (`previous:`, `source:`). Duplicates are refused at validation.
- **The request step comes first**, always.
- **Every step earns a `description`** — one sentence on what it does and why.
  A blank one, or one that merely restates the name, is rejected at construction.
- **A `changes` step measuring `base: baseline` requires `pin_baseline: true`** —
  refused at validation rather than surfacing as an empty ref deep in git
  plumbing after the run has already spent on agents.

## Before you ship it

```bash
sf check --repo <target>                   # validates EVERY workflow, spends nothing
sf explain <name> --repo <target>          # read the chain back; it is derived, not hand-written
sf run <name> "a tiny real request" --repo <target>
just obs phases <adw_id> <repo>
just obs envelopes <adw_id> <repo>         # is the envelope type earning its fields?
```

`sf check` catches everything config can catch — unknown step kinds, unknown
gates or envelopes, a `previous:` naming no earlier step, a quality name that
does not exist, an agent the roster lacks. Run it before every launch of a
workflow you just wrote.
