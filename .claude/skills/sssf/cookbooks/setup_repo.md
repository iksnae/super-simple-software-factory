# Set Up a Repo

Point the factory at a repository. Nothing is copied into it: the repo gains one
config file and one gitignored data directory, and the machinery stays in the
factory checkout.

## Prerequisites, checked in one command

```bash
sf doctor --repo <target>
```

Reports, in order: `git`, `uv`, and `pi` on PATH; the API key; that
`pi --list-models` returns a catalog; that the config loads; that **every model
the roster names resolves**; and that **every `prepare:` and `quality:` binary
exists**. Fix what it names before spending anything.

**Known gap — it checks one credential.** `doctor` verifies `OPENROUTER_API_KEY`
and that models resolve *in pi's catalog*, which says nothing about whether the
provider will authenticate. A roster staffing a direct provider can pass doctor
green and fail mid-run on a 401, after the planner has already spent. When a
roster names a provider other than OpenRouter, confirm that provider's auth
separately — see `docs/MODELS.md`.

## Write the config

```bash
sf init --repo <target>              # detects the stack, writes sssf.config.yaml
```

`init` reads the repo and writes real commands rather than placeholders:
npm/bun/pnpm/yarn (the lockfile picks the frozen-install form), uv, cargo,
SwiftPM, go, plus `package.json` scripts and `justfile` recipes. It never
overwrites; pass `--force` to replace, `--roster <name>` to extend a roster other
than `default`.

**Read what it inferred, then fix or delete it.** Detection is a starting draft,
not a survey — a check it guessed wrong costs a whole phase every run.

A minimal config is short on purpose:

```yaml
extends: config/rosters/default.yaml

prepare:                      # first phase of every workflow; a failure ABORTS
  install:
    argv: [npm, ci]

quality:
  checks:
    test:
      argv: [npm, test]
      timeout_seconds: 600
  groups:
    test: [test]
    full: [test]
```

Field by field: `docs/CONFIG.md`.

## Validate, spending nothing

```bash
sf check --repo <target>             # resolves config + validates EVERY workflow
just config layers <target>          # which files merged, in what order
sf list --repo <target>              # workflows, agents, checks this repo resolves to
```

`check` is the gate before any spend: it resolves the layered config and
validates every workflow's graph against it — step kinds, gate names, envelope
types, agent names, `previous:` references, and that every named quality check
exists. A green `check` means nothing will fail for a reason config could have
caught.

## Smoke test, still spending nothing

```bash
sf run quality "smoke" --repo <target>
```

Deterministic only — no agent runs. Green means the whole non-agent path works:
config resolved, session minted, `prepare` ran, checks executed, artifacts
landed, the trace recorded. Confirm the trace exists before trusting anything
larger:

```bash
just obs sessions <target>
```

Then, and only then, spend on an agent. `sf run scout "where is X handled"` is
the cheapest real one: read-only, one agent, nothing committed.

## Gitignore

`.sssf/` holds run artifacts and the trace db and must never be committed. `sf
init` does not edit the repo's `.gitignore` — add it yourself:

```
.sssf/
```

## Isolation

A run edits the working tree. If that is not acceptable, give it its own:

```bash
just worktree <branch> <repo>        # git worktree add, printed with the run command
```

That is the isolation tier — a `git worktree`, your call and not a dependency.
There is no VM and no provisioning key.

## What the repo now holds

Exactly two things: `sssf.config.yaml`, tracked; and `.sssf/data/`, gitignored.
Everything else lives in the factory checkout, which is what lets one factory
serve many repos and one fix reach all of them.
