# Onboarding Assessment

## Variables

### prompt

{{prompt}}

### previous_envelope

{{previous_envelope}}

### context_handoff_dir

{{context_handoff_dir}}

## Task

Assess this repository and propose its factory config.

1. Read the repo's own account of how it is verified — its guidance files, its CI
   workflows, its task runner, its manifests, including manifests below the root.
2. Write `<context_handoff_dir>/proposed-checks.yaml`: a ready-to-paste
   `prepare:` and `quality:` block, every entry carrying a comment citing the
   `file:line` that states it, and obeying the command contract in your system
   prompt.
3. Write `<context_handoff_dir>/onboarding-notes.md`: what this project is, what
   a root-manifest scan would have missed, which stated commands cannot be
   quality checks and why, and anything you could not determine.

Then emit your `Report` JSON.

## Report

Respond with ONLY valid JSON matching `ScoutOutput` — no prose before or after:

```json
{
  "status": "success",
  "summary": "<one sentence: the stack, and what the manifest scan would have missed>",
  "findings": [
    { "file": "CLAUDE.md:40", "note": "<the command stated here, and why it matters>" }
  ],
  "artifacts": [
    "<context_handoff_dir>/proposed-checks.yaml",
    "<context_handoff_dir>/onboarding-notes.md"
  ],
  "notes_for_next_agent": "<what the operator must decide before this config is merged>"
}
```
