# Template Library — Khaos repository shapes

**Purpose:** the README skeleton for each repository role. Load after Step 1 has
named the role.

These are ours. They are not standard-readme, and they deliberately omit the
sections that convention supplies by reflex — Features, Motivation, Background,
Contributing, Code of Conduct — because in a private engineering ecosystem those
either do not apply or belong somewhere else.

**Every template is a starting shape, not a form to fill.** A section with
nothing true to say in it is cut, not padded.

## Rules that apply to all templates

1. **Line one states what this is and who it is for.** No tagline.
2. **The reader's next move comes before anything explanatory.** A version to
   pin, a command to run, a document to open.
3. **Inventories are linked, not copied** (SKILL.md §3).
4. **Nothing unverified.** Every path, command and version is checked in Step 4.
5. **Licence footer.** Khaos repositories are proprietary; say so once, at the
   bottom, and link `LICENSE`.
6. **No emoji headings, no badges a reader does not act on, no time estimates.**

---

## Contract / spec

For repositories that define a format others implement — KSPD.

The reader is implementing a producer or consumer. They need the inventory and
the traps, in that order.

```markdown
# NAME — one line saying what it defines

**The contract for X.** What this repository holds: RFCs, schemas, the shared
module, examples. Who consumes it, named.

What is NOT here, and where it lives instead.

    require <module path> <version>

## <Artifact> layout

    <tree of what a real artifact contains, one comment per line>

Link to the canonical inventory. Do not restate it.

### Three things that bite

The traps a consumer hits in the first week. Absence semantics, renames,
anything that is a join rather than a field.

## Where things are decided

| | |
|---|---|
| specs | the normative source |
| schemas | the machine-checkable contract |
| module | the shared vocabulary |
| examples | ground truth, and what validates them |

Which repository is canonical where the two disagree, and what to do about a
divergence.

## Working here

    <the gate command>
    <the two others that matter>

The one non-obvious rule about changing the format.

## Related
## License
```

**Worked example:** this repository's `README.md` (94 lines).

---

## CLI / engine

For repositories whose product is a command — khaos-tools, `khs`.

The reader wants to run something. Install first, then the smallest set of
commands that gets them a result.

```markdown
# NAME — one line

What it does, and the formats or inputs it accepts.

## Install

    <the one command, or the installer link>

## Use

    <the three commands that matter, with real output>

Not every command. Link the full reference.

## How it fits

What it reads and writes, and which contract governs that.

## Working here

    <build, test, gate>

## Related
## License
```

---

## Library

For repositories consumers import — `kspdprotocol`, khaotik-ui.

The reader is about to add a dependency. Import path and version first; if they
have to scroll for those, the README failed.

```markdown
# NAME — one line

    <import path and version to pin>

What it gives you, in three bullets or fewer.

## Entry points

The two or three symbols most consumers actually use, with a real signature
copied from source.

## Compatibility

What a version bump means here, and anything a consumer must review on upgrade.
Breaking changes get named, not implied.

## Working here
## Related
## License
```

**Note on tags:** the form varies per repo — plain `vX.Y.Z` for most, a Go path
prefix where the module sits in a subdirectory (`go/kspdprotocol/v0.8.0`), a
component prefix elsewhere (`cli-v0.2.0`). khaotik-ui's history holds both
`lib-0.10.1` and `v0.15.0`. Read `git tag`; a README quoting the wrong form
gives a consumer a tag that does not resolve.

---

## Client / app

For things a person runs — khaos-app, khaos-tui, the menu bar app.

```markdown
# NAME — one line

What it is, and what it talks to.

## Run it

    <the command, or where the installer puts it>

Prerequisites only if there are real ones. Not "install Node".

## What it talks to

The daemon or service, the port or path, and how to tell it is not connected.

## Working here

    <dev loop, build, test>

## Related
## License
```

---

## Installer / packaging

For release machinery — khaos-foundation.

The reader is shipping or debugging a build, usually under time pressure.

```markdown
# NAME — one line

What it produces, for which platforms.

## Release lane

What triggers a build, what runs, where artifacts land. A list, in order.

## Versioning

The single command that bumps versions, and what desyncs if it is bypassed.

## Debugging a failed build

Where the logs are. The two or three failures that actually happen.

## Related
## License
```

---

## Workspace root

For the repository that pins others — khaos.machine.

The reader is looking for the right submodule. Give them the map and get out of
the way.

```markdown
# NAME

One line on what this workspace is.

## Components

| Submodule | What it is |
|---|---|

## Common tasks

    <init, build, test — the workspace-level recipes only>

Everything else lives in the submodule.

## Related
## License
```

---

## Service

For network-facing components — khaosstorage, khaosd.

```markdown
# NAME — one line

What it serves, and to whom.

## Endpoint and auth

The base URL, how credentials are supplied, where they are stored.

## The two calls that matter

Real requests with real responses.

## Operating it

Health check, where logs are, how to tell it is running.

## Related
## License
```

---

## Choosing when a repo has two roles

Name both in the opening line and route immediately. Do not interleave.

> `khaos-tools` is the parser and analysis engine (CLI) **and** the canonical Go
> types for story data (library). Consumers importing the types want §Entry
> points; everyone else wants §Use.

Two clear routes beat one blended README, which serves neither reader.
