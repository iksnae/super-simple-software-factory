# Update the Roster

Add or retune agents. **Which file you edit is a scope decision**, and there are
three, resolved by `extends:` in this order:

```
config/base.yaml            WHAT runs      stock workflows, limits, paths
config/rosters/*.yaml       WHO runs it    model staffing per agent
<repo>/sssf.config.yaml     AGAINST WHAT   that repo's commands and overrides
```

Merges are **by name**: an override naming `builder` edits the builder and leaves
the other agents alone. `just config layers <repo>` prints the resolution order
for any repo. Field-by-field spec: `docs/CONFIG.md`. Models, providers, auth, and
harnesses: `docs/MODELS.md`.

Retune a roster when the change is about *staffing*. Put it in the repo's config
when it is about *that repo*.

## Retune model or thinking

```yaml
agents:
  - name: builder
    model: openrouter/google/gemini-3.6-flash
    thinking: high                   # was medium
```

Models resolve through pi's live catalog — `pi --list-models`. If the catalog
lists what your roster names, you are done; there is no `models.json` to edit,
and editing it to "add" a model the catalog already has just duplicates it with
prices that drift.

Thinking levels are the harness's reasoning effort: `off | minimal | low |
medium | high | xhigh | max`. It only bites on models registered as reasoning-capable.

**A model change means a fresh session.** `agent_map.json` records the model each
harness session was created with. When a joined run (`--adw-id`) finds the
config's model no longer matches, that agent starts a **new** session rather than
resuming — never a bad resume. Thinking changes do not invalidate a session;
model changes do. Expect that agent to lose its accumulated context window on the
first run after the change.

## Recolor an agent's lane

```yaml
    color: "#22d3ee"      # hex; the starter roster ships violet/cyan/amber/green
```

Cosmetic and safe mid-project: the color rides the `agent_start` event and the
`agent_sessions` row, so the visualizer picks it up on the next run without
touching past sessions.

## Retune tools

The harness builtins are `read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`.
The last three are off in bare pi, so an agent that does not name them shells out
through `bash` to search and list.

Set the floor in `defaults`, then narrow per agent:

```yaml
defaults:
  tools: [read, bash, edit, write, grep, find, ls]

agents:
  - name: reviewer
    tools: [read, grep, find, ls, bash, write]   # an explicit list wins
```

**Resolution:** the agent's own list wins, else it inherits `defaults.tools`,
else `None` meaning all tools. An empty list is not "all tools"; it is a
tool-less agent, and it will stall.

Narrow by role, not by reflex:

- Any agent that must produce a `context_handoff/` artifact needs **`write`** —
  without it, it falls back to a `bash` heredoc to create the file the gate checks for.
- Recon agents should get the full read surface (`read`, `grep`, `find`, `ls`) —
  cheaper and more legible in the trace than the equivalent `bash` calls.

**Extension tools count against the allowlist.** Once an agent has a `tools` list,
a tool registered by one of its `harness_engineering` extensions is dropped unless
it is named there. Nothing errors: the extension loads, the run passes, the tool
is simply never offered.

## Set what an agent may CHANGE

`tools:` is a capability list and cannot make "this agent changes nothing" true —
`bash` runs anything (including `git checkout`, which one builder used to discard
the very check it was about to be judged by) and `write` reaches any path.

The boundary is `writes:`, enforced in code after every agent call:

```yaml
  - name: reviewer
    writes: []                       # read-only with respect to the REPO
  - name: planner
    writes: ["docs/specs/**"]        # only these paths
  - name: builder
    # key omitted = unrestricted
```

| `writes:` | Means |
|---|---|
| omitted / `None` | unrestricted |
| `[]` | read-only — may write nothing in the repo |
| `[...]` | only these paths |

`defaults.protected_files` names paths **no** agent may touch unless it names
them itself.

How it is enforced: the working tree's change-set is fingerprinted before the
agent runs and compared afterwards. Comparing change-sets rather than watching
for writes is what catches reversion — a path that was dirty before and clean
after has been *reverted*, and a reversion is a modification. The session runtime
under `data_dir` is gitignored and always writable, so a read-only agent is
read-only with respect to the repo, never mute.

A breach is **not** a gate violation. Gates are for work an agent can be asked to
redo; a breach cannot be corrected by re-prompting, because the write already
happened. It fails the phase and names every offending path.

## Set what an agent may READ

`writes:` bounds changes; `env:` bounds what the agent process receives from the
engineer's shell.

```yaml
defaults:
  env:
    deny:  ["*_KEY", "*_SECRET", "*_TOKEN", "*_PASSWORD", "*_CREDENTIALS"]
    allow: []
```

`allow` is an exception to `deny`, checked first. Defaults and per-agent
policies union, so an agent adding one `allow` keeps every roster `deny`.
Withheld names — never values — are printed on the phase and traced as
`env_withheld` on `agent_start`.

The shipped `allow` is empty because pi authenticates from
`~/.pi/agent/auth.json`, not the environment. Add an entry only when an agent's
own TOOLS need one (a private registry token for `npm ci`), and prefer the
repo's config over the shared roster.

It filters the environment and nothing else: an agent with `bash` can still read
`~/.pi/agent/auth.json` or a shell rc. Full spec: `docs/CONFIG.md`.

## Add harness extensions

```yaml
    harness_engineering:
      - config/harness/subagents.ts
```

Entries are extension **file paths**, applied to that agent only. Adding a
tool-registering extension is a two-part edit — the path here, *and* the tool name
it registers in that agent's `tools:` list. Skip the second half and it fails
silently.

## Add a new agent

Three steps, all required — skipping any one fails validation at startup, before
anything spawns:

1. **Prompts.** Create `config/prompts/{name}/system.md` (Purpose + Instructions —
   the static identity, nothing else) and `user.md` (an h3 per incoming datum:
   `{{prompt}}`, `{{previous_envelope}}`, `{{context_handoff_dir}}`, then the
   task, then a `## Report` section showing the exact output JSON). Copy an
   existing pair as the shape.
2. **Roster entry.** Name, purpose, prompt refs, plus anything differing from
   `defaults`.
3. **An envelope type.** Every agent step parses against a concrete type
   registered in `engine.ENVELOPES`. If none of the existing ones fits, add one —
   `update_modules.md`. The `## Report` section must show exactly that JSON.

Then name the agent as a step's `owner:` in a workflow.

## Rules that do not bend

- Workflows name **agents**, never models. Swapping a model is a config edit and
  touches no Python.
- One agent, one prompt, one purpose. If an entry needs two purposes, it is two agents.
- Envelope types never appear in config as definitions — they live in code, and a
  workflow only names one.

## Before you ship it

```bash
sf doctor --repo <target>     # every roster model resolves, every binary exists
sf check --repo <target>      # every workflow still validates against the roster
```

`doctor` confirms models resolve in the catalog. It does **not** confirm the
provider will authenticate — a roster naming a direct provider can pass green and
fail mid-run on a 401. Confirm auth separately when you add one.
