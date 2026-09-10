# Update a Workflow

Modify an existing chain — add a step, add gates, add a bounded loop. Every edit
is YAML under `workflows:`, either in `config/base.yaml` (stock, all repos) or in
a repo's own `sssf.config.yaml` (that repo only).

**Which file you edit is a scope decision.** A change in `base.yaml` reaches every
repo the factory serves. If the need is one repo's, declare the workflow in that
repo's config — merges are by name, so a repo can override a stock workflow
without forking the rest.

## Add a step

Insert it where it belongs in `steps:`. Pick the right kind: `agent` for a call,
`quality`/`verify_loop` for known commands, `changes`/`commit` for git,
`group` for several steps behind one condition.

```yaml
      - step: agent
        name: scout
        owner: scout
        output: ScoutOutput
        description: Locate the code the request touches
```

Step `name` must be unique within the workflow — that is how `previous:` and
`source:` address earlier results, and duplicates are refused at validation.

`description` is **required**, and a blank one or one that merely restates the
name is rejected at construction. It is the single line of intent the trace, the
console, and the UI show, so write what the step does and why — `"Land the code
only now: green suite, approved review"`, not `"Commit build"`.

Naming an agent no roster provides fails at startup, before anything spawns —
`requires:` is inferred from every `owner:` in the graph, so you cannot forget it.

## Remove a step

Delete it, then **re-thread the chain**: whatever it produced was probably
somebody's `previous:` or a `commit`'s `source:`. Point those at the surviving
upstream step. `sf check` catches a dangling reference; it will not guess the
right replacement.

## Add gates

Gates are named in the step and resolved against `engine.GATES` at validation:

```yaml
        gates: [artifacts_exist, diff_matches_claims]
```

On violations the harness does **not** restart the agent — it sends the violation
list back into the **same session** as a correction (context intact), bounded by
that step's `retries`. Every gate result is traced to `gate_results`. Exhausting
the retries fails the phase.

Gate claims, not guesses: declared artifacts exist and are non-empty, declared
JSON parses, declared changes appear in the diff. Never hardcode counts — express
quantity as a property of the declared list. Plan quality and code taste are not
gateable; that is a reviewer agent or a human. New reusable gates go in
`factory/modules/gates.py` and must be registered — `update_modules.md`.

## Add a bounded loop

Do not hand-roll one. Replace the `quality` step with a `verify_loop` and give it
a repair:

```yaml
      - step: verify_loop
        name: test
        group: test
        max_attempts: 3               # 0 or omitted = limits.max_fix_loops
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

The loop runs the checks; on red it hands their **verbatim output** to the repair
agent as its previous envelope and runs them again. The repair `must` be
`step: agent` — the loops dispatch it without inspecting its kind, so any other
kind is refused at validation rather than dying mid-run on a missing `output:`.

`review_loop` is the same shape with an agent verdict in front, bounded by
`limits.max_revision_loops`.

## Change what acceptance means

```yaml
    accept: verified
    accept_reason: the suite or the review never came back clean
```

`run.finish()` takes the criterion phase statuses cannot express. **A
`verify_loop` that ran a red suite succeeded** — it did its job — so phases alone
would report a green run that never passed its tests, in the db and the UI as
well as the terminal. `accept: verified` makes the exit code, the session status,
and the banner agree.

`verified` means both questions came back clean **where both were asked**: the
checks passed if any ran, and the review approved if one ran. A workflow that
runs only one of them is verified on that one alone.

## Three distinctions worth keeping straight

- **Gate retries vs. JSON retries.** `retries:` buys extra *gate*-correction
  rounds. Malformed final JSON is handled separately and always, bounded by
  `limits.json_fix_attempts`, even on a step with `retries: 0`. Raising one does
  not buy more of the other.
- **Step retries vs. loops.** `retries:` re-attempts one agent step's gate
  corrections in the same session, context intact. A loop repeats a *chain* of
  phases — different agents, new envelopes each pass.
- **A quality step succeeds when it runs and reports correctly.** A failing suite
  does not fail that phase; it fails the *run*, via `accept:`. The runner did its
  job; the code didn't.

## Before you ship it

```bash
sf check --repo <target>              # validates every workflow against this config
sf explain <name> --repo <target>     # the chain, rendered from what you just wrote
```

`explain` is the check that matters after an edit: the chain is **derived** from
config, not hand-written, so what it prints is what will run. If it does not read
the way you intended, the graph is wrong, not the renderer.
