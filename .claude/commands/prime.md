---
description: Quick-start agent understanding of the codebase structure
---

# Purpose

Orient quickly in the Khaos Machine workspace — an AI-powered storytelling
platform by Khaos Inc. Screenplay analysis is the foundational toolset; the
platform is designed to grow into broader storytelling capabilities.

## How to read this repo

This file deliberately does **not** restate the workspace's structure,
versions, release graph, or architectural rules. It used to, and every copy
drifted: it still described six submodules and a `khaos-gui` that was archived
in 2026, and quoted component versions several minors behind. Read the
canonical sources instead, then confirm against the live workspace.

| Question | Canonical source |
|----------|------------------|
| What is each component, and is it Built/Designed/Researched? | `docs/VISION.md` |
| How do I build, test, release, and commit? | `AGENTS.md` |
| How does the system fit together (layers, data models, APIs)? | `ARCHITECTURE.md` |
| What does a term mean? | `GLOSSARY.md` |
| Why is it built this way? | `docs/adr/` |
| What are the engineering standards? | `docs/constitutions/go/`, `docs/constitutions/ts/` |

Where any two disagree, `AGENTS.md` wins for process and `docs/VISION.md` wins
for the component map.

## Orient against the live workspace, not a snapshot

Component versions and submodule membership change often enough that any table
written here would be wrong within weeks. Ask the workspace:

```bash
just status    # which submodules are present and clean
just doctor    # required tooling, installed vs dev vs release versions, drift
just --list    # every available recipe, with descriptions
```

`git submodule status` is the authority on what is actually pinned here.

## Steps

1. Read `AGENTS.md` — build/test/commit conventions and architectural rules.
2. Read `docs/VISION.md` — the component map and reality tiers.
3. Run `just doctor` and `just status` to confirm tooling and workspace health.
4. Skim `ARCHITECTURE.md` for the layer the task touches.
5. Locate the code with `git submodule status` plus a search, rather than from
   a remembered path — submodules have been added, renamed, and archived.

## Report

Provide a summary covering:

- **Current state**: what is deployed, what is in flight
- **Architecture**: the layers relevant to the task at hand
- **Open work**: from GitHub issues and `specs/`, not from a list in this file
- **Recommended next steps**: based on the user's task
