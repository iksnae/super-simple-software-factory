---
name: milestone-grinder
description: Run the milestone delivery loop end-to-end — execute the current MILESTONE-<N>-PLAN.md via TDD until DoD passes, write the closeout, draft the next planning artifact, then update ROADMAP.md + CURRENT.md and promote the next planning draft to PLAN. Encodes the operator's working loop: "iterate via TDD until milestone lands and is properly closed out, commit + push often" → "great work, update roadmap + what's in flight + finalize next plan" → repeat. Two modes — stepped (default, pauses between phases for confirmation) and auto (chains phases, halts on TDD exhaustion / validator rejection / max-cycles). Use when the operator says "grind the milestone", "run the milestone loop", "/milestone-grinder", or asks to continue the iterate-close-promote cycle. Do NOT use to start a brand-new milestone with no PLANNING-DRAFT (scope first), to skip closeout writing, or on milestones with `Status: Blocked` in plan frontmatter.
---

# milestone-grinder

The milestone delivery loop, encoded. Most of the platform was
built by running this loop manually — this skill is the deterministic
entry point.

## When to invoke

The operator says any of:

- "grind the milestone" / "run the milestone loop" / "/milestone-grinder"
- "continue to iterate (via TDD) until this milestone lands and is properly closed out, commit + push often"
- "great work! update roadmap, what's in flight, finalize next milestone plan"
- "auto-grind the next N milestones"

Detect the active milestone as the highest-numbered
`docs/MILESTONE-<N>-PLAN.md` that does **not** have a matching
`docs/MILESTONE-<N>-CLOSEOUT.md`. Override only if the operator names
a specific milestone.

## Phase 1 — Deliver

Active milestone: N. Plan: `docs/MILESTONE-N-PLAN.md`.

**Submodule first.** Scope items that touch submodule code land in that
submodule's repository and are pushed there; the root commits the updated
pointer afterwards (`AGENTS.md`). Run the live-agent process check before
branching or committing in any submodule — an occupied one is worked
through `gh api` or an isolated worktree.

**Branch first.** Cut one branch off the latest `main`:
`git fetch origin && git checkout -b claude/m<N>-<theme> origin/main`.
One milestone, one branch, merged to `main` in Phase 3 before N+1 starts.
Never stack on an unmerged branch.

1. **Read the plan.** Confirm `Status` is not `Blocked` and every
   Definition of Done bullet is measurable. If unmeasurable → halt
   and surface the specific bullet; do not guess intent.
2. **For each Primary Scope item (A, B, C, …):**
   1. Write the failing test first.
   2. Implement until the test passes.
   3. Run the full validator catalog for the module touched — see
      `RULES.md` Testing Guidelines and the table in
      `docs/MILESTONE-TEMPLATE.md` — plus any additional validation the
      plan calls for.
   4. Commit with a scope-tagged message: `M<N> <letter>: <one-liner>`
      (e.g. `M12 A:`, `M12 B:`).
   5. **Push.** Every commit, every time. "commit + push often" is
      non-negotiable.
   6. **Append to `docs/MILESTONE-N-TRACKING.md`** — Validation
      Log: commit SHA + validator outcome + one-line summary.
3. **When all DoD bullets pass:**
   - Write `docs/MILESTONE-N-CLOSEOUT.md` against the template:
     `Status` / `Delivered` / `Validation` / `Retrospective` /
     `Validator Notes`.
   - Scaffold `docs/MILESTONE-(N+1)-PLANNING-DRAFT.md` from the
     PLANNING-DRAFT skeleton in
     [`docs/MILESTONE-TEMPLATE.md`](../../../docs/MILESTONE-TEMPLATE.md).
     Populate `Goal` and `Context` from N's retro carry-forward;
     leave other sections for Phase 2.
   - Commit both: `milestone: close N, draft N+1`. Push.

**Stepped mode (default): end here.** Surface to operator. The
follow-up "great work, update roadmap…" enters Phase 2.

**Auto mode: continue to Phase 2 without gate.**

## Phase 2 — Promote

1. **Update `ROADMAP.md`:**
   - Move N from upcoming → completed in "Milestone Outline" with
     a one-sentence summary from the retro and a link to the closeout.
   - Refresh "Current Position" to reflect what N delivered.
   - If N+1 introduces a new theme, add it under "Roadmap Themes".
2. **Update `CURRENT.md`:**
   - Bump **Last updated** to today.
   - Rewrite the `## Focus` section: N is shipped (link its closeout),
     N+1 is what comes next (link its planning draft, about to be
     promoted).
   - Move any milestone-N item out of `## Known open threads`; add any
     carry-forward the retro produced.
3. **Promote N+1:**
   - Open `docs/MILESTONE-(N+1)-PLANNING-DRAFT.md`. Resolve every
     `[?]` open question and every risk. Write a concrete
     "Primary Scope (Execution Order)" against carry-forward items
     + any new ROADMAP-themes intent.
   - Rename in-place to `docs/MILESTONE-(N+1)-PLAN.md`. Set
     `Status: Ready`.
   - Scaffold an empty `docs/MILESTONE-(N+1)-TRACKING.md`.
4. **Commit and push:** `docs: promote M(N+1) plan; roadmap + CURRENT refreshed` (match the operator's existing message style — see `git log --oneline | grep promote`).

**Then run Phase 3 — Land.** A milestone is not done until it is merged.

## Phase 3 — Land (merge to main)

Full autonomy = the grinder merges its own work. **One milestone, one
branch off the latest `main`, merged before the next milestone starts.**
Never stack a milestone branch on an unmerged one — that is how conflict
cascades start, and this workspace's submodules already move underneath a
long-lived branch.

1. **Open the PR** to `main` (if not already): `gh pr create --base main
   --head claude/m<N>-<theme> --title "M<N>: <theme>" --body "<closeout
   summary>"`.
2. **Wait for required checks**: `gh pr checks <pr> --watch`. Red check →
   fix on the branch, push, re-poll. Never merge red.
3. **Conflicts if `main` moved**: `git fetch origin && git merge
   origin/main`, resolve, `just check && git push`. If the
   conflict is semantic/ambiguous, **halt** with the conflicting files —
   don't guess, don't force.
4. **Merge + delete branch**: `gh pr merge <pr> --squash --delete-branch`
   (squash unless the repo merges with merge-commits).
5. **Sync local main**: `git checkout main && git pull origin main` so
   N+1 branches off the just-landed state.

**Stepped mode: end here** — the milestone is delivered, closed, promoted,
and **on `main`**. The next invocation cuts a fresh branch off `main`
for N+1.

**Auto mode + cycles remaining:** cut N+1's branch off the updated `main`,
then re-enter Phase 1.

## Halt conditions

Halt and return control to the operator on any of:

- **TDD exhaustion** — three consecutive failed implementations on
  the same scope item without making the failing test pass.
- **Validator rejection** — any practice validator hard-fails. With
  `--halt-on-warning`, also halt on soft warnings.
- **Plan ambiguity** — DoD bullet unmeasurable, or Primary Scope
  references a file/symbol that doesn't exist.
- **Broken main** — the touched module fails to build against
  `origin/main` at the start of any phase. Halt; require clean main before resuming.
- **Merge check failure** — a required PR check is red and a fix on the
  branch hasn't turned it green (Phase 3).
- **Unresolvable merge conflict** — `main` moved and the conflict is
  semantic/ambiguous. Surface the conflicting files; never force-merge
  or guess the resolution (Phase 3).
- **Max cycles reached** (auto mode).
- **Manual interrupt** in conversation.

On halt, write the exact pending next step to the conversation so
re-invocation can pick up cleanly. State is fully reconstructable
from disk — no in-memory continuation needed.

## Mode selection

Default to **stepped** unless the operator explicitly says "auto",
"unattended", "overnight", or passes `--auto` / `--max-cycles`.

Auto is for known-tractable plans you don't want to gate. Exploratory
plans ("investigate X") will halt within minutes; stay in stepped.

## Verification (per cycle)

Before declaring a cycle complete, confirm:

- `docs/MILESTONE-N-CLOSEOUT.md` exists; Validation section lists
  every DoD bullet with a green outcome.
- Git log shows incremental scope-tagged commits across Phase 1.
- `ROADMAP.md` reflects N completed, N+1 in flight.
- `CURRENT.md` bumped to today.
- `docs/MILESTONE-(N+1)-PLAN.md` exists, `Status: Ready`, no `[?]`
  markers in Open Questions.

## Failure modes

- **Skipping the closeout** — the loop's state machine depends on
  it. Even a one-paragraph retro counts.
- **Squashing commits** — defeats the "commit + push often" bisect
  property. Many small commits per scope item.
- **Editing ROADMAP.md or CURRENT.md during Phase 1** — those are Phase 2's artifacts. Cross-phase edits
  create merge friction with parallel build threads.
- **Promoting a draft with unresolved `[?]` markers** — Phase 2
  must resolve every open question before the rename. If unresolvable,
  halt.
- **Running auto on an exploratory plan** — auto presumes concrete
  DoD. Stay stepped until the plan is concrete.
