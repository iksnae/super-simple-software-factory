# Map This Repo For The Factory

## Variables

### prompt

Optional context from the operator. It does NOT define your task — your task is
fixed and stated below. It is usually empty, and that changes nothing.

{{prompt}}

### previous_envelope

{{previous_envelope}}

### context_handoff_dir

{{context_handoff_dir}}

## Task

Name this project's shape, and map it to the commands the factory needs.

1. **What shape is it?** Read the manifests and any task runner. Two manifests
   in different languages means one application in two halves — both get checks.
2. **What does that shape imply**, corrected by whatever the repo's own guidance
   file states? A task runner's recipes always win over anything inferred.
3. **Which commands make the tree runnable** (`prepare:`) and **which judge the
   code** (`quality:`)?
4. **Which of the judging commands are fast enough to re-run after every builder
   repair?** That is the `test` group; the rest is `full`.

Stop once you can answer those. If the shape and the guidance file do not settle
something, it is unclear — say so and move on. Chasing it is not this job.

## Output

Two short files, then your `Report` JSON. **Length is a defect here.**

- `<context_handoff_dir>/proposed-checks.yaml` — the deliverable. A
  ready-to-paste `prepare:` and `quality:` block obeying the command contract.
  **One comment line per entry**: where it came from, as a `file:line` if the
  repo states it, or "standard for <shape>" if it comes from the shape.

- `<context_handoff_dir>/onboarding-notes.md` — **at most 20 lines**:
  - **Shape** — two or three lines. The languages, where each half lives, how it
    is run.
  - **Not checkable** — a line each, at most three. What is stated but cannot be
    a check here, and why.
  - **Unclear** — a line each. What you could not settle, and what would settle
    it.

## Report

Respond with ONLY valid JSON matching `ScoutOutput` — no prose before or after:

```json
{
  "status": "success",
  "summary": "<one sentence: the shape, and the commands it maps to>",
  "findings": [
    { "file": "CLAUDE.md:37", "note": "<the command or constraint stated here>" }
  ],
  "artifacts": [
    "<context_handoff_dir>/proposed-checks.yaml",
    "<context_handoff_dir>/onboarding-notes.md"
  ],
  "notes_for_next_agent": "<anything the operator must decide before merging>"
}
```
