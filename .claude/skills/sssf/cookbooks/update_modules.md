# Update Modules

Extend `factory/` with new low-level logic, a gate, or an envelope type.

## The rule

**ALL low-level logic lives in `factory/modules/`.** `engine.py` is the workflow
interpreter and stays that: it sequences declared steps and decides acceptance.
Anything else — subprocess handling, parsing, retry mechanics, git plumbing,
reusable predicates — goes in a module.

## Where things go

| Module | Owns |
|---|---|
| `data_types.py` | Every Pydantic model: `AgentCall`, `PhaseParams`, `Phase`, `EnvelopeBase` + one envelope type per agent contract, the config models (`AgentConfig`, `SSSFConfig`, `StepConfig`, `WorkflowConfig`), `EventRecord`, `PiRequest`/`PiResult` |
| `agents.py` | config load, `extends:` resolution, merge-by-name, validation, agent execution |
| `runner.py` | the `Run` object; `run.phase(PhaseParams)`; `ph.call(AgentCall)` |
| `agent_pi.py` | the pi harness — `pi -p --mode json`, JSONL stream tailed live, `--session-id` creates-or-continues |
| `agent_codex.py` | the Codex CLI harness, including its OS sandbox |
| `agent_cc.py` | Claude Code — stubbed; raises one clear sentence |
| `gates.py` | validation gates over envelope claims |
| `permissions.py` | what an agent may CHANGE, fingerprinted before and after |
| `quality.py` | run a named check, record it, adapt a failure into an envelope |
| `changes.py` | resolve a base ref, `git diff` into `context_handoff/`, adapt to an envelope |
| `prompts.py` | load system/user prompt refs, render placeholders |
| `session.py` | mint or join `adw_id`, maintain `agent_map.json`, create session dirs |
| `tracer.py` | append JSONL **and** insert every event into `sssf.db` as it happens |
| `console.py` | the terminal narrative — every line also traced as a `log` event |
| `git_helper.py` | branch, status, diff, commit — the plumbing `changes.py` composes |
| `utils.py` | env handling, `resolve_prompt`, ids, timestamps |

Outside `modules/`: `cli.py` (the command surface), `paths.py` (factory_home vs
repo_root), `stacks.py` (detection for `sf init`), `engine.py` (the interpreter).

## Never `print()`

Modules report through `run.console` — never a bare `print()`. Each console
method prints a line **and** writes it to `sssf.db` as a `log` event, both from
one helper, so the terminal narrative and the UI cannot drift. New output means a
new method on `Console`, not a print at the call site.

## The four-param rule

**Any function taking more than 4 parameters gets them converted into a concrete
data type.** `AgentCall` and `PhaseParams` are the pattern — `run.phase()` and
`ph.call()` each take exactly one object.

## Adding an envelope type

Two edits, always together — the type, and its registration:

```python
# factory/modules/data_types.py
class ReviewOutput(EnvelopeBase):
    approved: bool = False
    findings: list[ReviewFinding] = []
    blocking: list[str] = []
```

```python
# factory/engine.py
ENVELOPES: dict[str, type[EnvelopeBase]] = {
    ...
    "ReviewOutput": ReviewOutput,
}
```

**Registration is what makes it nameable from config.** An unregistered type is a
config error at validation with the available names listed — not an
`AttributeError` at phase time, after the run has already spent.

**The output contract is a synced triad — one change means three edits:**

1. The type in `data_types.py` (the enforcer).
2. The agent's `config/prompts/{agent}/user.md` `## Report` section showing
   exactly that JSON (the ask).
3. Every workflow step naming it in `output:` (the binding) — `grep -rn
   "ReviewOutput" config/ factory/` finds them all.

If the type and the Report example drift, the agent produces what the prompt
asked for, the parser rejects what the type expects, and every call burns
correction round-trips before landing — a slow, silent tax.

## Adding a gate

A gate is a callable — `gate(envelope, run) -> GateReport`. Record **one check
per item you look at**; the harness derives the verdict.

```python
# factory/modules/gates.py
def tests_declared_passed(envelope, run) -> GateReport:
    """Verify the envelope's own test claims, after the fact."""
    report = GateReport()
    for failure in envelope.failures:
        report.check(failure.test, False, failure.error)
    report.check("suite", envelope.passed,
                 "all declared tests passed" if envelope.passed
                 else f"{len(envelope.failures)} declared failure(s)")
    return report
```

Then register it, same reason as an envelope:

```python
# factory/engine.py
GATES = {
    ...
    "tests_declared_passed": gates.tests_declared_passed,
}
```

`report.check(item, ok, note)` appends and returns the report, so a single-item
gate is one line: `return GateReport().check(command, ok, f"exit {code}")`.

**Write a note on passing checks too.** The note is the evidence, and it is what
makes a green gate worth reading — `artifacts_exist ✓ 1 checked · plan.md —
exists, 454B` tells you what was verified; a bare ✓ tells you nothing. Notes on
failed checks double as the reason the agent is given, so phrase them as the
problem: `"claimed changed file does not exist"`.

Rules that keep gates honest:

- **Verify claims, never predict.** File names and counts are unknowable before
  the agent finishes; gates check what the envelope declared.
- **Quantity as properties, not counts.** "at least one artifact", "ALL declared
  paths exist" — never `len(artifacts) == 3`.
- **Record checks, don't raise.** The harness feeds the derived violations back
  into the same session as a correction, bounded by the step's `retries`, and
  traces every check to `gate_results.checks_json`.
- **Check every item, even after one fails.** The agent fixes more per correction
  round when it sees every failure at once.
- **Don't gate the ungateable.** Plan quality and code taste are a reviewer
  agent's job, or a human's.

## Adding a step kind

Rare, and a bigger commitment than it looks — it touches four places in
`engine.py`: `_validate_step` (required fields, with a message naming the
workflow and the step), `describe_chain` (how it renders), `_run_steps` (how it
executes), and any recursive walk that must see it (`required_agents`,
`needs_baseline`). A kind that validates but does not render is invisible in the
chain the operator reads before approving a run.

## Before you finish

There is no test suite yet — see the root `AGENTS.md`. Until there is, every
module change is verified by running the path it rides:

```bash
sf check --repo <target>                          # the whole config + every workflow
sf run quality "smoke" --repo <target>            # the deterministic path, $0
sf run scout "where is X handled" --repo <target> # the agent path, one cheap agent
just obs gates <adw_id> <repo>                    # if you touched a gate
```
