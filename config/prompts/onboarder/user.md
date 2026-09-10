# Configure This Repo For The Factory

## Variables

### prompt

Optional context from the operator. It does NOT define your task — your task is
fixed and stated below. It may be empty, or a single vague word, and that
changes nothing about what you produce. Use it only if it names something
specific worth honouring (a platform, a constraint, a check to include or leave
out).

{{prompt}}

### previous_envelope

{{previous_envelope}}

### context_handoff_dir

{{context_handoff_dir}}

## Task

Answer one question: **what must this repo's `sssf.config.yaml` contain for the
factory to build in it and verify the result?**

That is the whole scope. You are not reviewing the code, judging the
architecture, summarising the product, or suggesting improvements. You are
determining configuration.

Four questions decide it, in order:

1. **What makes the tree runnable?** Installs, fetches, code generation — the
   commands that must succeed before anything can be built or tested. These
   become `prepare:`. If nothing is needed, say so; an empty `prepare:` is a
   correct answer for a repo with no dependency step.
2. **What does this project run to decide the code is good?** Tests, type
   checks, builds, linters. These become `quality: checks:`. Take them from what
   the repo STATES — its guidance files, CI workflows, task runner, package
   scripts — not from what is conventional for the stack.
3. **Which of those is fast and load-bearing enough to re-run after every
   builder repair?** That set is the `test` group. The rest is `full`.
4. **What is stated but cannot be a check here, and why?** Anything needing
   credentials, a network service, a device, a desktop application, or assets
   absent from the repo. Also anything that currently fails for reasons that
   predate this work.

Read the repo's own account of itself to answer them: `AGENTS.md`, `CLAUDE.md`,
`CONTRIBUTING`, `README`, `.github/workflows`, `justfile`/`Makefile`,
`package.json` scripts, and every manifest INCLUDING those below the root.

Then write two files and emit your `Report` JSON. **Both are short. Length here
is a defect, not thoroughness** — a real run produced 257 lines of notes for an
answer that is forty lines of YAML.

- `<context_handoff_dir>/proposed-checks.yaml` — the deliverable. A
  ready-to-paste `prepare:` and `quality:` block obeying the command contract in
  your system prompt. **One comment line per entry**, carrying the `file:line`
  that states it. Not a paragraph, not an essay on the trade-off. The exception
  is a check you are deliberately parking, which gets one extra line saying what
  would let it in.

- `<context_handoff_dir>/onboarding-notes.md` — **at most 30 lines**, in three
  short sections: what this project is architecturally (two or three lines: the
  languages, the shape, where each half lives); what is stated but cannot be a
  check, and why (a line each, two or three of them); and what you could not
  determine (a line each). No tables of every command in the repo, no history,
  no recommendations beyond the config.

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
