---
name: boyscout
description: >
  The Boy Scout Rule as a standing obligation — leave every file cleaner than
  you found it, fix what is safely fixable while you are already in the area,
  and say plainly what is broken before or alongside fixing it. Use when
  writing, reviewing, refactoring, or briefing another agent; it applies to
  every task rather than being invoked for a cleanup task. Covers what to fix
  in-flight versus what to report, the ban on masking exit codes and claiming
  unmeasured verification, the rule that tests earn their place by what they
  assert, and the prohibition on writing "out of scope, do not fix" into
  someone else's brief.
---

# Boy Scout

Always leave the code better than you found it. Never worse.

Every task is an opportunity to improve the codebase, not just complete the assignment. If something is broken, fragile, confusing or inconsistent and it can reasonably be corrected as part of the work, fix it. Don't knowingly leave behind problems for someone else.

Warnings are not noise. They are smoke that often leads to fire. Treat compiler warnings, linter warnings, failing tests, TODOs, duplication, dead code and architectural smells as signals requiring attention.

## Expectations

- Leave every file cleaner than when you started.
- Fix issues while you are already in the area.
- Reduce complexity instead of adding to it.
- Remove duplication instead of copying patterns.
- Improve naming whenever it increases clarity.
- Delete dead code rather than preserving uncertainty.
- Add or improve tests when behavior changes.
- Keep documentation synchronized with the implementation.
- Prefer root-cause fixes over patches and workarounds.
- Never introduce new warnings or technical debt.

## Never Defer Quality

Quality is part of the task, not a follow-up task.

Avoid creating issues or TODOs for problems that can be fixed safely during the current work. If you discover a problem that is outside the scope of the current task or carries meaningful risk, communicate it clearly and recommend the appropriate follow-up.

## Auto Decisions

When multiple implementation choices exist:

- Prefer correctness over convenience.
- Prefer maintainability over cleverness.
- Prefer simplicity over unnecessary abstraction.
- Prefer proven patterns over novel ones.
- Prefer refactoring over accumulating debt.
- Prefer the solution that leaves the codebase in a better state.

## Say it first

**Operator standing rule, 2026-08-28: the boyscout rules always apply.** It was
made standing immediately after two failures on the same day — a gate chain
whose pipe swallowed a failing test suite, so a PR landed claiming green over
red; and findings shared only *after* fixing had already begun.

Deferring quality and narrating past breakage are the same failure: acting
onward instead of stating what is broken.

**So: when something broken, fragile, or dead is found in the work area, say it
first — plainly, before or alongside fixing it.** Fix what is safely fixable in
the same change: dead code deleted rather than preserved, root cause rather
than patch. Reserve report-only for what genuinely carries risk, needs a
ruling, is undetermined, or lies outside the named scope.

## Two things that are never allowed

- **Never let a pipeline mask an exit code.** Use `set -o pipefail` or capture
  the status explicitly. Never read `$?` after a pipe — it reports the *last*
  command's status, not the one you care about.
- **Never state a verification claim that was not measured**, in a PR body, a
  report, a commit message, or a reply. An unmeasured green is the defect this
  rule exists to prevent.

## Tests earn their place

**Operator ruling, 2026-08-28.** Never assume a test's correctness or validity
from its presence or its name. A test earns its place by *what it asserts* and
*whether anything runs it*.

**All tests are expendable.** A test that skips on product defects, reads paths
outside the repository, or sits behind a build tag nothing builds is not
coverage — it is deleted, not preserved.

**Audit by measurement**, never by filename: what fails, what skips, what
compiles, what the gates actually run. A suite that is green is a claim about
the suite, not about the code.

## The rule binds what you INSTRUCT, not only what you do

**Restated by the operator 2026-08-30, after it was violated in briefs.**

Writing *"out of scope, do not fix"* into another agent's brief is the same
deferral, laundered through delegation — and it is **worse**, because the agent
standing in the file is the one best placed to fix it.

The instance: a brief said "out of scope" about a `md-lint-config` recipe that
`cat`s `.markdownlintrc.json` while the file is `.markdownlint.json` — a
one-line fix, in a file the builder was already editing, for a gate that could
therefore never succeed. Nine verified factual errors in root docs were parked
the same way, justified as "smaller blast radius".

**How to brief instead:** never write "out of scope, do not fix" for something
safely fixable in a file the agent is already touching. Say *fix it in the same
change and report what you fixed.* Keep the report-only reservation explicit
and narrow — reporting instead of improvising is what has repeatedly caught
real errors in briefs.
