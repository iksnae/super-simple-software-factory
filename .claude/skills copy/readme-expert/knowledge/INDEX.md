# README Expert — knowledge base

`SKILL.md` is the router. These carry the detail it defers to. Load a file when
the step that needs it is reached, not before.

## Files

### `foundation/codebase-scanner.md`

**Extract facts from the tree before writing anything**

Step 2. Detection files in Khaos order (Go first), the justfile as the real source of runnable commands, and Go submodule specifics — subdirectory modules, path-prefixed tags, versions that come from `git tag` rather than a file.

*378 lines.*

### `foundation/validation-checklist.md`

**The five verification layers**

Step 4. Existence, content accuracy, execution validity, link integrity, structure. Each layer says how to check, not just what to check.

*481 lines.*

### `application/template-library.md`

**The README skeleton for each Khaos repository role**

Step 3, after the role is named. Contract, CLI, library, client, installer, workspace root, service — plus what to do when a repo has two roles. Ours, not standard-readme.

*275 lines.*

### `application/script-executor.md`

**Extract and run the commands a README claims**

Step 4, before executing anything. Carries the risk model: read-only runs freely, install/modify needs permission, destructive needs explicit permission.

*604 lines.*

### `application/quality-standards.md`

**The pass/fail conditions before it ships**

Step 4. Nine binary conditions, the order to fix failures in, and what is deliberately *not* a defect for our repositories (no TOC, no badges, no Contributing section, short).

*278 lines.*

## Load order

| Task | Order |
| --- | --- |
| Create or rewrite a README | `codebase-scanner` → `template-library` → `validation-checklist` → `script-executor` → `quality-standards` |
| Verify an existing README | `validation-checklist` → `script-executor` → `quality-standards` |
| Fix one section | `codebase-scanner` (scoped) → `validation-checklist` |

## What changed from the imported version

Recorded so the differences are deliberate rather than drift:

- **Templates are by role, not by language.** A Go CLI and a Go contract
  repository need different READMEs; a Go template serves neither.
- **No quality score.** The imported rubric scored out of ten and called 8.0
  publication-ready. One false claim is the whole failure mode, and a score lets
  a README with one pass on good prose. The standard is binary, per claim.
- **Go first.** The imported scanner led with Python and JavaScript and
  mentioned `go.mod` twice against sixteen for `package.json`.
- **No emoji headings, no time estimates, no token budgets.** The first is house
  style; the last two were unverifiable and already wrong.
- **A gating step.** The imported skill stopped at "the README is now correct".
  A README fixed once does not stay fixed — KSPD's went stale again eight RFCs
  later, inside a day.
