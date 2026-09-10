---
name: readme-expert
description: >
  Create or repair a README grounded in what the codebase actually contains.
  Use when a README is being written, has gone stale, has drifted into
  open-source-template shape (What is X / Why X / Features), duplicates an
  inventory that lives elsewhere, or names files, commands and versions that do
  not exist. Classifies the repository's role first — contract, CLI, library,
  client, installer, workspace root — because one template serves none of them.
  Every claim is verified against the tree and every command is executed before
  it ships.
---

# README Expert

A README is a **router**, not a manual and not a pitch. It answers one question
for one reader: *what is this, and where do I go next?* Everything else is a
link.

The failure this skill exists to prevent is not an ugly README. It is a
**confident document describing something untrue**, because a reader reasons
from it. In KSPD a README documenting four schemas with no files and a package
layout removed two schema versions earlier sent two issues chasing evidence that
did not exist; they stayed open six days and the reporters were reasoning
correctly from a document that lied.

Every anti-pattern named here is one a Khaos repository actually shipped.

## Route

| Situation | Go to |
| --- | --- |
| No README, or it needs a full rewrite | §1 Create |
| README exists; is it still true? | §2 Verify |
| A section is wrong or missing | §1, from Step 2, scoped to that section |
| An inventory here duplicates one elsewhere | §3 Gate |

---

## §1 Create

### Step 1 — Classify the role. Do not skip this.

The role decides the shape. Get it wrong and every later choice is wrong.

| Role | Reader arrives to… | Lead with |
| --- | --- | --- |
| **Contract / spec** (KSPD) | implement against it, or check what a field means | the inventory: what an artifact contains, which schema governs what |
| **CLI / engine** (khaos-tools) | run a command | install, then the three commands that matter |
| **Library** (`kspdprotocol`, khaotik-ui) | import it | the import path, the version to pin, the entry points |
| **Client / app** (khaos-app, khaos-tui) | run it locally | how to run it, and what it talks to |
| **Installer / packaging** (khaos-foundation) | ship or debug a build | the release lane and where artifacts land |
| **Workspace root** (khaos.machine) | find the right submodule | the component map, nothing else |
| **Service** (khaosstorage, khaosd) | call it or operate it | the endpoint, auth, and the two calls that matter |

A repo with two roles has two audiences. Say so in one line and route, rather
than interleaving.

**A repo whose readers are all engineers implementing against it does not get a
benefits section.** Adoption copy belongs on the product site.

### Step 2 — Scan before writing

Load `knowledge/foundation/codebase-scanner.md`.

Extract facts from files, never from memory or from the previous README:

- the module path and the version a consumer pins (`go.mod`, `Package.swift`,
  `package.json`, `Cargo.toml`)
- the commands that exist (`justfile`, `Makefile`, `package.json` scripts)
- the entry points a consumer imports or invokes
- what an artifact actually contains, enumerated from a real one

Everything gathered here is a claim you must defend in Step 4.

### Step 3 — Draft to the shape

Load `knowledge/application/template-library.md` for the role's template.

**Required, in order:**

1. **One line**: what this is and who it is for. Not what it aspires to be.
2. **Status that changes the reader's next move** — the version to pin, whether
   it is proprietary, whether it is stable. Only if it changes something.
3. **The role's lead content** from Step 1.
4. **Where to go next** — canonical documents, linked, not summarised.

**Forbidden unless the role genuinely calls for it:**

- `## What is X?` → `## Why X?` → `## Overview`: three sections saying the same
  thing. This is the template's signature.
- A features or benefits list in an engineering repo.
- Badges a reader does not act on.
- An inventory that also exists canonically — **link to it** (§3).
- The same content twice. Two sections with the same heading is the tell.
- Emoji headings, taglines, contribution boilerplate nobody follows.
- Time or effort estimates. They are unverifiable and they age badly.

**Length:** over roughly 150 lines, something belongs elsewhere. The test is not
*is this true* but *does a reader need this here, rather than one link away*.

### Step 4 — Verify every claim

Load `knowledge/foundation/validation-checklist.md` for the layers, and
`knowledge/application/script-executor.md` before running anything.

Non-negotiable, and the reason this skill exists:

1. **Existence** — every file, directory, command and symbol named must exist.
2. **Accuracy** — every quoted signature, field name and version must match the
   source exactly. Copy it; do not retype it.
3. **Execution** — every command shown must run **as written**. KSPD's README
   carried an `ajv` invocation that could not work because it lacked the plugin
   flag `info.json`'s `date-time` format requires.
4. **Links** — every link resolves.
5. **Figures** — every count and version is re-measured at the moment of writing.

**Classify before executing.** `script-executor.md` carries the risk model:
read-only commands run freely; anything that installs, writes, or is
irreversible needs permission first. Never run a destructive command from a
README to see whether it works.

### Step 5 — Gate what will go stale

A README fixed once does not stay fixed. KSPD's was corrected, then went stale
again eight RFCs later, inside a day.

Go to §3.

---

## §2 Verify

For an existing README, run Step 4 alone and report per layer. Do not rewrite
prose that is still true — a verify pass that turns into a rewrite hides which
claims were actually wrong.

Report as: claim, layer it failed, evidence. Not a score.

---

## §3 Gate

Order of preference, and the order matters:

1. **Link to the canonical source.** A link cannot drift. Almost always right
   for an inventory.
2. **If a copy is unavoidable, gate it** — a check that copy and source agree,
   in the repo's default gate (`just check` in Khaos repos).

Do not invert these. KSPD briefly had a gate requiring `README.md` to list every
schema, which forced the README to carry the copy in order to pass — a gate
enforcing exactly the duplication that had made it go stale twice.

> **A gate that mandates duplication is worse than no gate**, because it makes
> the wrong shape the only passing shape.

This step is what separates a repair from a fix.

---

## Anti-patterns, and what each cost

| Pattern | Why it is wrong |
| --- | --- |
| Two sections with the same heading | Duplicated content that will diverge. One is already wrong. |
| "For Writers / For Developers" benefit lists | Product copy in an engineering repo. Belongs on the marketing site. |
| A file or schema list copied from elsewhere | Guaranteed to drift. Link it or gate it. |
| A command never executed | It will be wrong, and a reader will believe it. |
| `[Add X here]`, "TODO", "Coming soon" | A placeholder shipped is a promise broken. Fill it or cut it. |
| Describing the intended format, not the shipped one | Cost KSPD two issues and six days. |
| A quality score out of ten | Tells nobody what to fix. Report the failing claim instead. |

## Khaos specifics

- What this workspace actually contains: **Go** (khaos-tools,
  khaos-manager, khaos-tui, `kspdprotocol`), **TypeScript/Svelte** (khaos-app,
  khaotik-ui), **Rust** (khaos-app's Tauri shell) and **Bash** (khaos-foundation
  packaging). Scanner and validation guidance leans Go first; the Python
  examples in the knowledge files are illustrative, not the common case.
- The default gate is **`just check`**. If a README claims a command, it should
  be a `just` recipe or a documented raw command that runs.
- **Tag form varies per repo and must be read, never assumed.** Measured
  2026-08-21: most are plain `vX.Y.Z` (khaos-tools `v0.11.1`, khaos-wfl
  `v0.0.102`, khaos-manager `v0.7.1`, khaos-tui `v0.0.53`, khaos-foundation
  `v0.4.79`, khaos-app `v0.1.0`); **KSPD** carries a Go path prefix
  (`go/kspdprotocol/v0.8.0`) because its module sits in a subdirectory;
  **khaosstorage** uses component prefixes (`cli-v0.2.0`, `sdk-v0.1.0`); and
  **khaotik-ui has used both forms** — `lib-0.9.0` through `lib-0.10.1`, then
  `v0.13.2` through `v0.15.0`. A repo whose own history holds two schemes is the
  one that will mislead you. Run `git tag` in the repo; a README quoting the
  wrong form gives a consumer a tag that does not resolve.
  **Note 2026-09-02:** that measurement is left as recorded, but `khaos-wfl` is
  no longer a submodule of this workspace — only its released daemon binary is
  consumed, staged by khaos-foundation.
- Cross-repo claims (khaos-tools' canonical types, khaosd's API) must cite the
  peer repository by path, and must not be restated as though this repo owns
  them.

## Done means

- The role is named and the shape matches it.
- Every claim verified against the tree, not recalled.
- Every command executed as written, after risk classification.
- No duplicated inventory, or a gate that keeps the duplicate honest.
- Nothing a reader does not need *here*.

## Knowledge base

| File | Load when |
| --- | --- |
| `knowledge/foundation/codebase-scanner.md` | Step 2 — extracting facts |
| `knowledge/foundation/validation-checklist.md` | Step 4 — the five layers |
| `knowledge/application/template-library.md` | Step 3 — the role's shape |
| `knowledge/application/script-executor.md` | Step 4 — before executing anything |
| `knowledge/application/quality-standards.md` | Step 4 — what "done" checks |
