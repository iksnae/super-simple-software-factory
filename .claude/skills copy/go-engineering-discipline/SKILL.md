---
name: go-engineering-discipline
description: "Use when implementing or evolving Go code in this workspace and the operator wants the full discipline loaded: a problem statement paired with a solution statement, incremental TDD/BDD, clean architecture, SOLID, and a structural review gate. Orchestrates gherkin-feature-drive (BDD outer loop), writing-tests (TDD inner loop), iteration-plan and effort-pointing (sizing), code-quality-review (structural gate) and incremental-commit-all (landing), and defers to the Go Constitution for standards. Do not use for a single isolated feature file, a test-only task, or a diff review; use the narrower member skill instead."
---

# Go Engineering Discipline

The **umbrella methodology** for Go delivery. It does not restate the detailed
procedures its member skills already own — it sequences them into one loop and
states the principles that hold across all of them. When a step has a
dedicated skill, this skill points there rather than duplicating it.

## Purpose and boundaries

The skill commits to:

- Forcing a **problem statement paired with a solution statement** before any
  code is written
- Driving delivery through **incremental TDD/BDD** — outer BDD loop (behavior
  the work owes), inner TDD loop (units that satisfy it)
- Holding **clean code, clean architecture, and SOLID** as merge gates, not
  aspirations
- Composing — not replacing — its member skills

It does **not** commit to:

- Re-implementing what the member skills do (it delegates)
- "While we're here" scope — every change ties to the stated problem
- Big-bang delivery — work lands in the smallest shippable increments

## Member skills

| Loop / gate | Skill | Owns |
|---|---|---|
| BDD outer loop | [`gherkin-feature-drive`](../gherkin-feature-drive/SKILL.md) | Turning a `.feature` into the minimal code + a verification command that exercises every scenario |
| TDD inner loop | [`writing-tests`](../writing-tests/SKILL.md) | Behavior-first tests, fakes over mocks, interfaces at the seams, deterministic + isolated |
| Iterative rhythm | [`development-loop`](../development-loop/SKILL.md) | plan → implement → review → refactor, applied throughout |
| Sizing the increment | [`iteration-plan`](../iteration-plan/SKILL.md) · [`effort-pointing`](../effort-pointing/SKILL.md) | Breaking the solution into shippable items, pointed by complexity not time |
| Structural gate | [`code-quality-review`](../code-quality-review/SKILL.md) | The maximalist review that blocks correct-but-structurally-worse changes |
| Conservative review | [`pr-review`](../pr-review/SKILL.md) | The default per-PR review when a harsh structural pass is not wanted |
| Coverage gaps | [`unit-test-coverage`](../unit-test-coverage/SKILL.md) | Finding what test-first missed — never the driver of the work |
| TUI surfaces | [`charm-tui`](../charm-tui/SKILL.md) | Charm v2 model contract, components, palette, fallback, Bubble Tea testing |
| Landing the work | [`incremental-commit-all`](../incremental-commit-all/SKILL.md) | Staging meaningful incremental commits until the tree is clean |

## Canonical references

The workspace's own standards govern. Where anything here conflicts with them,
**the constitution wins**.

- [`docs/constitutions/go/CONSTITUTION.md`](../../../docs/constitutions/go/CONSTITUTION.md)
  — the binding Go standard: formatting, naming, packages, error handling,
  concurrency, testing, patterns, gotchas, review.
- [`docs/constitutions/go/AMENDMENT_I.md`](../../../docs/constitutions/go/AMENDMENT_I.md)
  — lint compliance and automated code-quality enforcement.
- [`.claude/docs/CODE-JUDO.md`](../../docs/CODE-JUDO.md) — restructure so whole
  categories of complexity disappear, rather than polishing the shape.
- [`RULES.md`](../../../RULES.md) — architectural invariants, quality gates,
  coverage floors, the 500-line ceiling.
- [`AGENTS.md`](../../../AGENTS.md) — the entrypoint; non-negotiables, and the
  concurrent-agent check before touching any submodule.

## Principles (the standing bar for every increment)

### Clean code

- Names say what, not how. A reader understands intent without the body.
- Small functions, one reason to change. Comment density matches the
  surrounding code — explain *why*, never narrate *what*.
- No dead branches, no speculative generality, no "while we're here."

### Clean architecture

- Dependencies flow **inward**. The core (domain logic) depends on
  interfaces it owns (ports); adapters at the edge depend on the core.
- IO — filesystem, network, DB, clock, randomness, env, process exec —
  lives at the boundary behind an interface, never threaded through the
  core. (This is exactly what makes the `writing-tests` fakes possible.)
- One bounded concern per package/file. New feature logic does not leak
  into a shared path.

### SOLID (stated in Go idiom)

- **S** — one type / one file / one reason to change. (The
  `CAPABILITY-PATTERN.md` shape is the local exemplar.)
- **O** — extend by adding a new implementation of an existing
  interface, not by adding a branch to a switch in shared code.
- **L** — every implementation of an interface honors the same contract;
  fakes used in tests are substitutable for real adapters.
- **I** — small, role-specific interfaces (`io.Reader`-sized), defined
  by the consumer, not fat "manager" interfaces.
- **D** — the core depends on abstractions; concrete adapters are wired
  at the edge. Constructors take interfaces.

## The loop

### Step 0 — Define the problem, pair it with a solution

Before any code, write two short statements (in the work-item body or the PR
description):

- **Problem** — what is broken / missing / costly, in observable terms.
  "Users can't X because Y" — not "we should add Z."
- **Solution** — the smallest change that resolves the problem, named as a
  behavior. This is the contract the increments must satisfy.

If the problem can't be stated crisply, stop and clarify — do not proceed to
code. A vague problem produces speculative architecture.

### Step 1 — Size the increment

Use [`iteration-plan`](../iteration-plan/SKILL.md) +
[`effort-pointing`](../effort-pointing/SKILL.md) to break the solution into the
smallest shippable items. Each must be deliverable and verifiable on its own.
Order by dependency, not appeal.

### Step 2 — BDD outer loop (behavior owed)

For each increment, express the behavior as scenarios. Where a `.feature` file
exists or is warranted, hand the scenario implementation to
[`gherkin-feature-drive`](../gherkin-feature-drive/SKILL.md) — the scenarios
*are* the spec and the verification command is the proof.

The outer loop answers: *does the system do what the solution promised?*

### Step 3 — TDD inner loop (units that satisfy it)

Drive each unit **red → green → refactor** per
[`writing-tests`](../writing-tests/SKILL.md):

1. **Red** — write the failing test that names the behavior ("does X when Y").
   Extract or confirm the boundary interface the test fakes.
2. **Green** — the minimal code that passes. No more.
3. **Refactor** — apply [`CODE-JUDO.md`](../../docs/CODE-JUDO.md): can a
   branch, helper, or mode disappear entirely? Tests stay green throughout.

Tests are written **first**, never backfilled to satisfy a coverage gate (that
rubber-stamps and over-engineers). Coverage is a side effect of test-first
behavior, not a target —
[`unit-test-coverage`](../unit-test-coverage/SKILL.md) finds what test-first
missed; it does not drive the work.

The floors in [`RULES.md`](../../../RULES.md) are a minimum bar, not the goal:
tools ≥65%, wfl ≥60%, manager ≥70%, tui ≥25%.

### Step 4 — Structural gate

Before the increment is "done," run it past
[`code-quality-review`](../code-quality-review/SKILL.md): behavior correct
**and** no structural regression, no missed code-judo move, no file pushed past
its decomposition boundary, no boundary leak. Correct is necessary but not
sufficient. Use [`pr-review`](../pr-review/SKILL.md) where the conservative
pass is the right one.

`RULES.md` makes two of these concrete: no new file over 500 lines, and all new
code lint-clean against the golangci-lint baseline.

### Step 5 — Land it

Commit in meaningful increments via
[`incremental-commit-all`](../incremental-commit-all/SKILL.md) until the tree
is clean. Each commit maps to one coherent step of the solution.

In this workspace: commit **inside the submodule first**, then record the
pointer at the workspace root — and check the submodule is not occupied by
another agent before touching it (`AGENTS.md`, "Concurrent agents").

Then loop back to Step 1 until the Step 0 solution statement is fully
satisfied.

## Go-specific guardrails

These recur often enough to call out:

- `go.mod` must exist at the build root before any `go build`/`go run`.
- Slice fields that JSON-marshal must be initialized to `[]T{}`, not
  `nil` — `nil` marshals to `null`, not `[]`.
- Every imported package must be used; `gofmt`/`go vet` clean before commit.
- Map iteration is randomized — never let error messages or output depend
  on map order (a recurring source of flaky assertions).
- Constructors take interfaces, return concrete types ("accept
  interfaces, return structs").
- Errors wrap with `%w` and context; the core never depends on
  vendor-specific error types — map them at the adapter edge.

Beyond these, the [Go Constitution](../../../docs/constitutions/go/CONSTITUTION.md)
is binding — no panic in production paths, short receiver names, small
`-er` interfaces, `%w` wrapping, `context.Context` for cancellation,
table-driven deterministic tests, and `jsonx` rather than `encoding/json`
(`RULES.md`).

## Self-check

The increment is complete when:

- [ ] A paired problem/solution statement exists and the change traces
      back to it
- [ ] Behavior is proven by a BDD verification command (where applicable)
- [ ] Every unit was driven test-first (red → green → refactor)
- [ ] Tests are deterministic, isolated, and use fakes — no real
      network/filesystem for core behavior
- [ ] The core depends on interfaces; IO sits at the edge
- [ ] No structural regression survives the structural review bar
- [ ] `gofmt` / `go vet` clean; commits are incremental and meaningful

## Failure modes to avoid

- **Code before a stated problem.** Architecture invented to solve an
  unnamed problem is speculative by definition.
- **Backfilled tests.** Writing tests after the code to hit a coverage
  number is not TDD — it rubber-stamps the implementation.
- **Approving on correctness alone.** Behavior-correct ≠ structurally
  sound. Run the structural review gate.
- **Big-bang delivery.** If the increment can't be stated as one
  shippable, verifiable item, it's too big — split it (Step 1).
- **Duplicating the member skills here.** This skill orchestrates; the
  detail lives in `writing-tests`, `gherkin-feature-drive`, and
  `code-quality-review`. Keep it that way.
- **Following a dead link.** If a reference here does not resolve, that is a
  defect in this file — report it rather than inventing the missing procedure.

## See also

- [`gherkin-feature-drive`](../gherkin-feature-drive/SKILL.md) · [`writing-tests`](../writing-tests/SKILL.md) · [`code-quality-review`](../code-quality-review/SKILL.md)
- [`iteration-plan`](../iteration-plan/SKILL.md) · [`effort-pointing`](../effort-pointing/SKILL.md) · [`incremental-commit-all`](../incremental-commit-all/SKILL.md)
- [`charm-tui`](../charm-tui/SKILL.md) · [`pr-review`](../pr-review/SKILL.md)
- [`docs/constitutions/go/CONSTITUTION.md`](../../../docs/constitutions/go/CONSTITUTION.md) — the binding standard
