---
name: milestone-planner
description: Plan the next batch of milestones — review the history (recent closeouts + carry-forward), the roadmap (themes, the active arc), the vision (`docs/VISION.md`, `ARCHITECTURE.md`), and what is in flight (`CURRENT.md`), take any operator intention as input, then interact with the operator via AskUserQuestion to settle the strategic decisions and draft one or more MILESTONE-<N>-PLANNING-DRAFT.md files (and an optional arc note) that conform to docs/MILESTONE-TEMPLATE.md and are ready for milestone-grinder to promote. The upstream complement to milestone-grinder, which refuses to start a milestone with no PLANNING-DRAFT. Use when the operator says "plan the next milestones", "scope the next arc", "draft the next batch", or wants to turn an intention/roadmap direction into grindable plans. Do NOT use it to execute or promote a plan (use milestone-grinder), to write a delivered milestone's closeout (grinder owns that), or to invent scope with no roadmap/vision/operator signal.
---

# milestone-planner

The upstream half of the milestone loop: turn a vision/roadmap intention
into a **batch of grindable milestone drafts**, with the strategic
decisions settled through `AskUserQuestion` first. The grinder delivers,
closes, and auto-drafts the single next milestone; this skill is the
deliberate, operator-led, plan-a-batch-ahead case.

Hand-off: stops at `MILESTONE-<N>-PLANNING-DRAFT.md` files matching
[`docs/MILESTONE-TEMPLATE.md`](../../../docs/MILESTONE-TEMPLATE.md).
`milestone-grinder` Phase 2 promotes a draft to PLAN. Never promote,
execute, or close here.

## Workflow (summary)

1. **Read the state** — operator intention (primary), recent closeout
   carry-forwards (history), `ROADMAP.md` active arc + themes (direction),
   `docs/VISION.md` + `ARCHITECTURE.md` (vision/constraints),
   `CURRENT.md` (what is in flight). Next number =
   `max(<N> across docs/MILESTONE-<N>-*.md) + 1`.
2. **Synthesize candidates** — for each: goal · the signal it traces to ·
   rough scope class. Drop any with no signal or that duplicate an
   in-flight plan.
3. **Settle decisions via `AskUserQuestion`** — batch theme, size,
   sequencing, scope class per milestone, carry-forward selection, hard
   non-goals. Don't draft until theme/size/sequencing are settled.
4. **Write the drafts** — one PLANNING-DRAFT per milestone, in exact
   template section order, dependency-sequenced, each independently
   shippable, DoD measurable (+ the standing test/check/diff/tracking
   rows). Only genuine delivery-time unknowns stay as `[?]`. Add an arc
   note `docs/<ARC-NAME>.md` if the batch is named.
5. **Self-check** — template-shaped, Status=Draft, measurable DoD, scope
   references real files, no strategic decision buried as `[?]`,
   dependency-ordered. Report each draft + settled decisions to the operator.

## Standing rules

A draft earns its place only if it traces to an operator intention, a
carry-forward item, or a roadmap line — no signal, no milestone. Strategic
scope is the operator's call (surface via `AskUserQuestion`); Open
Questions are for delivery-time unknowns, not deferred decisions. Reject
any candidate that violates the Key Architectural Rules in `RULES.md`
(KSPD paths canonical, khaosd the single backend, onion architecture for
external deps) at planning time.

A milestone whose scope touches submodule code delivers in that
submodule and the root pins the pointer afterwards — `AGENTS.md`,
"Submodule first, pointer second". Name the target repository on every
Primary Scope item.
