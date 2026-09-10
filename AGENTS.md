# Working on this repo

You are working **on the factory**, not with it. Two different jobs, two
different documents:

| Job | Read |
|---|---|
| Operate the factory against some target repo | `.claude/skills/sssf/SKILL.md` |
| Change the factory's own code, config, or docs | this file |

If the request is "run sdlc on my app", you want the skill. If it is "add a step
kind", "fix the codex adapter", "why did that run fail" — you are here.

## What this is

A fork of [disler/super-simple-software-factory](https://github.com/disler/super-simple-software-factory).
Its release commit is the **root** of this history, and every change since is a
commit on top, so `git log` reads as the real derivation and
`git diff <root>..HEAD -- <path>` answers "what did we change" for any file.

Three restructurings define the fork, and they are the frame for judging any new
change:

1. **One checkout, many repos.** Nothing is stamped into a target repo. The
   target arrives as `--repo`; the repo owns `sssf.config.yaml` and a gitignored
   `.sssf/data/`, and nothing else.
2. **The target repo owns its commands.** Quality checks are named entries in its
   config, not Python in the engine.
3. **Workflows are declared, not written.** A workflow is a phase graph in YAML,
   interpreted by `factory/engine.py`. There is no per-workflow Python.

A change that reintroduces a second copy of the engine, hardcodes a repo's
toolchain, or adds a Python file per workflow is working against the fork.

## Layout

```
scripts/sf.py             the entrypoint — a uv script, no venv to manage
factory/
  cli.py                  run | list | explain | check | doctor | init
  engine.py               the interpreter: validation, chain rendering, execution
  paths.py                factory_home vs repo_root
  stacks.py               stack detection for `sf init`
  modules/                ALL low-level logic — see cookbooks/update_modules.md
config/
  base.yaml               stock workflows, limits, paths
  rosters/*.yaml          model staffing
  prompts/{agent}/        system.md + user.md
  harness/                pi extensions
docs/                     CONFIG.md (schema), MODELS.md (models/auth), MULTI-PROJECT.md
just/                     the command surface: config.just, obs.just
.claude/skills/sssf/      the operator-facing skill, and apps/visualizer
```

## The two-root rule

`factory_home` and `repo_root` are different directories and confusing them is
the defect this architecture invites. Anything shipped with the factory
(workflows, rosters, prompts, extensions) resolves against `factory_home`;
anything belonging to the work (config, quality commands, `.sssf/data/`, the
files agents touch) resolves against `repo_root`. `factory/paths.py` owns the
distinction — use it rather than `Path.cwd()` or a relative literal.

## Verifying a change

**There is no test suite and no CI.** State that plainly rather than implying
coverage that does not exist. Until there is one, a change is verified by running
the path it rides, and the run is the evidence you cite:

```bash
sf check  --repo <target>                    # config + EVERY workflow, spends nothing
sf doctor --repo <target>                    # binaries, key, model resolution
sf run quality "smoke" --repo <target>       # the deterministic path end to end, $0
sf explain <workflow> --repo <target>        # the chain, derived from config
sf run scout "where is X" --repo <target>    # the cheapest real agent path
just obs phases <adw_id> <repo>              # what actually happened
```

Use a scratch repo or `just worktree`, never a branch you care about.

For the visualizer: `bunx vue-tsc --noEmit` from `apps/visualizer`, then run it
against a real trace — a scratch db with one $0 session will not exercise
anything.

**If you add a test suite, that is a real contribution.** The three highest-value
targets, in the order a defect there is most expensive: `engine.validate`
(everything it catches, an operator otherwise pays for at phase time),
`agents._merge` (merge-by-name across the config layers), and
`permissions.enforce` (the only thing standing between an agent and a path it
was not given).

## Conventions

These are enforced by review, and some by the code itself:

- **Four-param rule.** More than four parameters becomes one concrete data type.
  `AgentCall` and `PhaseParams` are the pattern.
- **Never `print()`.** Modules report through `run.console`, which prints *and*
  traces the same line as a `log` event. A print at a call site makes the
  terminal and the UI disagree.
- **Every phase description earns its place.** One sentence on what and why.
  `PhaseParams` rejects a blank description, and one that merely restates the
  name, at construction.
- **Register what config can name.** A new envelope type or gate is two edits:
  the definition in `modules/`, and the entry in `engine.ENVELOPES` / `engine.GATES`.
  Registration is what turns an unknown name into a validation error listing the
  real options, instead of an `AttributeError` after the run has spent.
- **The output contract is a synced triad.** The type in `data_types.py`, the
  `## Report` JSON in the agent's `user.md`, and `output:` at every step naming
  it. Change one, change all three in the same edit.
- **Comments carry evidence, not intent.** The valuable comments in this codebase
  say what was measured and what broke — "observed as a run that sat idle at 0%
  CPU with an empty raw_output.jsonl". Write those. Delete the ones that restate
  the line below them.

## Documentation rules

The original's main failure was documentation that outran the code, and this
repo's README carries a standing "what is verified, and what is not" section for
exactly that reason. So:

- **Never document a capability that does not run.** If it is designed but not
  built, it goes in `docs/` labelled as design input — `docs/MULTI-PROJECT.md`
  opens with "NOTHING HERE IS IMPLEMENTED" and that is the pattern.
- **Record removals.** If you drop a feature, say so and say why, in the README.
  The skill layer was once removed without that line, and nobody could tell it
  from an intentional decision.
- **One spec, one home.** `docs/CONFIG.md` is the config schema; the cookbooks
  link to it rather than restating it. Two copies of one spec rot apart.
- **Update the verification section when you verify something.** It is the only
  place a reader learns which paths have actually run.

## Lanes

`config/base.yaml` declares `lanes:` — kinds of work, and the floor a model must
clear to do them. `judgement` (planner, reviewer) and `build` (builder) require
200,000 context and reasoning; `mechanical` (scout, documenter) requires 32,000.
Lanes map onto rosters by agent NAME, so a roster needs no edit; an agent may
override with `lane:`.

No shipped roster staffs a local model — that is parked (see `docs/MODELS.md`).
The lanes stand on their own: they exist to check any staffing decision, and
they earned it against hosted models first.

`sf doctor` checks the staffed model against its lane's floor. That is the
difference between "the model resolves" and "the model fits", and it is the
third instance of one gap: a 401 reported as bad JSON, a `403 MODEL_NOT_IN_PLAN`
on a model sitting in the catalog, and a 9B model that could be staffed as the
builder with doctor reporting OK.

The floors are calibrated, not guessed: every model the shipped rosters staff
has at least 272,000 context, so 200,000 passes them all and refuses a 64K local
model from the seats where truncation is silent. A floor is not a promise — a
model above it can still be bad at the work. It is the only part a config file
can check.

## Known gaps

Current as of the skill-and-UI restoration; correct this list when you close one.

- **No tests, no CI.** Everything above.
- **`sf doctor` checks one credential.** It confirms models RESOLVE in pi's
  catalog, never that the provider authenticates. This has already cost a run.
- **Harness errors are misreported as parse failures.** `agent_pi.run` raises only
  on a non-zero exit; a provider error arrives inside the event stream as
  `stopReason: "error"` with an `errorMessage`, and nothing reads it. A 401 was
  reported as "never produced valid BuildOutput JSON" and burned both retries
  re-asking for JSON. Fixing this is small and high-value.
- **A killed run reports $0.** `run.add_usage` is called once, after the harness
  returns, so a run stopped mid-turn loses its whole cost accounting. Measured:
  a scout killed by an outer `timeout` recorded `tokens 0, cost $0.0000` while
  its own raw_output.jsonl carried 331,366 tokens and $0.0076 — `just obs costs`
  showed a free run that was not free. The fix is a fifth name in the harness
  contract (`turn_usage(event)` beside resolve_model / assistant_message_records
  / ToolCallTracker / run) so the event forwarder can record per turn, with the
  final `add_usage` reconciling the difference.
- **The loops and commit phases have never run.** `verify_loop`, `review_loop`,
  and every `commit` step are unexercised.
- **Agents no longer inherit the full environment, but `bash` still reads
  files.** `defaults.env` (see `docs/CONFIG.md`) withholds credential-shaped
  variables — measured at 31 on this machine, with the agent still
  authenticating, because pi reads `~/.pi/agent/auth.json` rather than the
  shell. What remains open is that an agent holding `bash` can read that file,
  or a shell rc, directly. Env scoping raises the cost of an accident; only an
  OS sandbox is a boundary, and `coding_agent: codex --sandbox read-only` is
  still unverified.
- **`coding_agent: claude_code` is a stub.** It raises one clear sentence.
