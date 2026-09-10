"""Detect a repo's stack, so `sf init` writes commands instead of placeholders.

The stamped-copy design shipped `quality.py` as six `echo` placeholders behind a
banner reading "REPLACE THE PLACEHOLDER COMMANDS BELOW". That is honest but it
puts every new repo's first ten minutes into guessing what its own build is
called, and it leaves `prepare:` empty — which is the failure that actually bit
us: a fresh worktree with no dependencies installed, six checks red for reasons
that had nothing to do with the code.

So detection, with three rules that keep it from being magic:

1. **The project's own commands win.** A `justfile` with a `bootstrap` recipe, or
   an `npm` script named `test`, is the repo telling you what it calls things.
   Preferring an inferred `npm ci` over a declared `just bootstrap` would be the
   factory overriding the project about the project.

2. **Lockfile before manifest.** `package.json` says "npm-ish"; `bun.lock`,
   `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json` say which one, and which
   frozen-install flag is correct. Getting this wrong installs a different
   dependency tree than CI does.

3. **Everything emitted is a suggestion, and says so.** Detection is written into
   the config as ordinary commands the operator can read, edit, or delete — never
   applied invisibly at run time. A wrong guess is then a one-line fix in a file
   they already have open, not a mystery.

Detection never runs a command. It reads files.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Command:
    """One suggested command: what to run, and why this one."""

    name: str
    argv: list[str]
    operation: str = "check"
    area: str = "app"
    timeout_seconds: int = 300
    description: str = ""


@dataclass
class Stack:
    """What was found in a repo, and what to put in its config."""

    names: list[str] = field(default_factory=list)      # e.g. ["npm workspaces", "AWS SAM"]
    prepare: list[Command] = field(default_factory=list)
    checks: list[Command] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def detected(self) -> bool:
        return bool(self.prepare or self.checks)


# ── project-declared commands (rule 1) ───────────────────────────────────────

# Recipe names that conventionally mean "install this project's dependencies".
BOOTSTRAP_RECIPES = ("bootstrap", "install", "deps", "setup")

# npm/bun script names worth wiring, mapped to the operation they represent.
SCRIPT_OPERATIONS = {
    "test": "test", "typecheck": "typecheck", "lint": "lint",
    "build": "build", "check": "check",
}


def _just_recipes(root: Path) -> list[str]:
    """Recipe names declared in a justfile, read rather than executed.

    A recipe line starts at column zero and ends at the first colon; that is
    enough to know a name exists without asking `just --list`, which would run
    the file and inherit whatever settings it declares.
    """
    justfile = next((root / name for name in ("justfile", "Justfile", ".justfile")
                     if (root / name).is_file()), None)
    if justfile is None:
        return []
    # Split on the first colon, THEN validate the left side. A single regex over
    # the whole line needed a nested quantifier for the parameter list, and that
    # backtracks catastrophically on a long line with no colon at all — measured
    # as a hang on a 900-line justfile, not a slowdown.
    name = re.compile(r"^[a-zA-Z][\w-]*$")
    recipes = []
    for line in justfile.read_text(errors="replace").splitlines():
        if not line[:1].isalpha() or ":" not in line:
            continue                     # indented body, comment, blank, setting
        head, _, rest = line.partition(":")
        if rest.startswith("="):
            continue                     # `name := value` is an assignment
        candidate = head.split()[0] if head.split() else ""
        if name.match(candidate):
            recipes.append(candidate)
    return recipes


def _package_json(root: Path) -> dict:
    path = root / "package.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text()) or {}
    except (json.JSONDecodeError, OSError):
        return {}


# ── the js/ts family: lockfile decides (rule 2) ──────────────────────────────

# (lockfile, ecosystem label, frozen install argv)
JS_LOCKS = (
    ("bun.lock", "bun", ["bun", "install", "--frozen-lockfile"]),
    ("bun.lockb", "bun", ["bun", "install", "--frozen-lockfile"]),
    ("pnpm-lock.yaml", "pnpm", ["pnpm", "install", "--frozen-lockfile"]),
    ("yarn.lock", "yarn", ["yarn", "install", "--immutable"]),
    ("package-lock.json", "npm", ["npm", "ci"]),
)


def _detect_js(root: Path, stack: Stack) -> None:
    package = _package_json(root)
    if not package:
        return
    runner, install = "npm", ["npm", "install"]
    label = "npm"
    for lockfile, ecosystem, argv in JS_LOCKS:
        if (root / lockfile).is_file():
            runner, install, label = ecosystem, argv, ecosystem
            break
    else:
        stack.notes.append(
            "no lockfile found, so the install is unpinned — CI and this factory "
            "may resolve different dependency trees")

    if package.get("workspaces"):
        label += " workspaces"
        stack.notes.append(
            "workspaces detected: a fresh worktree has none of them linked, which "
            "is exactly what `prepare` is for")
    stack.names.append(label)

    stack.prepare.append(Command(
        name="install", argv=install, operation="install", area="repo",
        timeout_seconds=900, description="Install dependencies from the lockfile"))

    scripts = package.get("scripts") or {}
    for script, operation in SCRIPT_OPERATIONS.items():
        if script not in scripts:
            continue
        # `bun test` and `npm test` are the conventional forms; everything else
        # goes through `run`.
        argv = ([runner, "test"] if script == "test" and runner in ("npm", "bun")
                else [runner, "run", script])
        stack.checks.append(Command(
            name=script, argv=argv, operation=operation,
            timeout_seconds=900 if operation == "test" else 300,
            description=f"package.json script {script!r}"))


# ── other ecosystems ─────────────────────────────────────────────────────────

def _detect_python(root: Path, stack: Stack) -> None:
    if not (root / "pyproject.toml").is_file():
        return
    if (root / "uv.lock").is_file():
        stack.names.append("python (uv)")
        stack.prepare.append(Command(
            name="sync", argv=["uv", "sync"], operation="install", area="repo",
            timeout_seconds=900, description="Sync the locked environment"))
        stack.checks.append(Command(
            name="test", argv=["uv", "run", "pytest", "-q"], operation="test",
            timeout_seconds=900, description="pytest through uv"))
    else:
        stack.names.append("python")
        stack.checks.append(Command(
            name="test", argv=["pytest", "-q"], operation="test",
            timeout_seconds=900, description="pytest"))


def _detect_rust(root: Path, stack: Stack) -> None:
    if not (root / "Cargo.toml").is_file():
        return
    stack.names.append("rust (cargo)")
    stack.prepare.append(Command(
        name="fetch", argv=["cargo", "fetch"], operation="install", area="repo",
        timeout_seconds=900, description="Fetch crates named by Cargo.lock"))
    stack.checks += [
        Command(name="test", argv=["cargo", "test"], operation="test",
                timeout_seconds=1800, description="cargo test"),
        Command(name="clippy", argv=["cargo", "clippy", "--", "-D", "warnings"],
                operation="lint", timeout_seconds=900, description="clippy, warnings denied"),
    ]


def _detect_swift(root: Path, stack: Stack) -> None:
    if not (root / "Package.swift").is_file():
        return
    stack.names.append("swift (SwiftPM)")
    stack.prepare.append(Command(
        name="resolve", argv=["swift", "package", "resolve"], operation="install",
        area="repo", timeout_seconds=900, description="Resolve package dependencies"))
    stack.checks += [
        Command(name="build", argv=["swift", "build"], operation="build",
                timeout_seconds=1800, description="swift build"),
        Command(name="test", argv=["swift", "test"], operation="test",
                timeout_seconds=1800, description="swift test"),
    ]


def _detect_go(root: Path, stack: Stack) -> None:
    if not (root / "go.mod").is_file():
        return
    stack.names.append("go")
    stack.prepare.append(Command(
        name="download", argv=["go", "mod", "download"], operation="install",
        area="repo", timeout_seconds=900, description="Download modules"))
    stack.checks += [
        Command(name="test", argv=["go", "test", "./..."], operation="test",
                timeout_seconds=1800, description="go test ./..."),
        Command(name="vet", argv=["go", "vet", "./..."], operation="lint",
                timeout_seconds=600, description="go vet ./..."),
    ]


# Marker files that say something about a repo without implying a test command.
CONTEXT_MARKERS = (
    ("template.yaml", "AWS SAM"),
    ("samconfig.toml", "AWS SAM"),
    ("Dockerfile", "docker"),
    ("Package.resolved", None),
)

ECOSYSTEMS = (_detect_js, _detect_python, _detect_rust, _detect_swift, _detect_go)

# Where a monorepo conventionally keeps its members. Detection generates commands
# only for the repo ROOT — walking a tree and guessing which member is "the" app
# would be inventing an answer — but a manifest below the root is always worth
# SAYING.
MEMBER_DIRS = ("apps", "packages", "services", "libs", "crates", "modules")

MANIFESTS = ("package.json", "pyproject.toml", "Cargo.toml", "Package.swift", "go.mod")

# Never descended into: build output, dependency trees, and vendored source. A
# manifest in any of them belongs to somebody else's project.
SKIP_DIRS = {
    "node_modules", ".git", "target", "dist", "build", "vendor", ".venv", "venv",
    "__pycache__", ".sssf", "Pods", ".build", "DerivedData", ".next", "out",
}

# The invocation that runs a nested manifest FROM THE ROOT, which is the only
# place a check ever runs. Each takes no shell, so `cd x && y` is not available
# and these flags are the argv-native equivalent.
NESTED_INVOCATION = {
    "Cargo.toml": "[cargo, test, --manifest-path, {path}]",
    "go.mod": "[go, test, ./...]        # run from {dir}, or use a go.work",
    "package.json": "[npm, --prefix, {dir}, test]",
    "Package.swift": "[swift, test, --package-path, {dir}]",
    "pyproject.toml": "[uv, run, --directory, {dir}, pytest, -q]",
}


def _member_manifests(root: Path) -> list[str]:
    """Every manifest below the root, to two levels. Paths, repo-relative.

    Two levels because that covers both shapes seen in the wild: a sibling
    component at the top (`src-tauri/Cargo.toml`) and a conventional monorepo
    member (`packages/api/package.json`). Deeper than that and the hits are
    fixtures and examples rather than the project.

    This used to scan MEMBER_DIRS only, and only when the root had no manifest
    at all. Measured consequence: a Tauri app with package.json at the root and
    Cargo.toml in src-tauri/ was reported as `detected: npm` with no mention of
    Rust anywhere — half the application invisible, and silently, because the
    scan was gated on having found nothing. A repo that is polyglot is exactly
    the repo that needs telling.
    """
    found = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS or child.name.startswith("."):
            continue
        for manifest in MANIFESTS:
            if (child / manifest).is_file():
                found.append(f"{child.name}/{manifest}")
        for grandchild in sorted(child.iterdir()):
            if (not grandchild.is_dir() or grandchild.name in SKIP_DIRS
                    or grandchild.name.startswith(".")):
                continue
            for manifest in MANIFESTS:
                if (grandchild / manifest).is_file():
                    found.append(f"{child.name}/{grandchild.name}/{manifest}")
    return found


def _nested_note(members: list[str], detected: bool) -> str:
    """What to tell the operator about manifests the generated config ignores."""
    lines = []
    for path in members[:8]:
        name = path.rsplit("/", 1)[1]
        form = NESTED_INVOCATION.get(name)
        if form:
            lines.append(f"      {path}  ->  argv: "
                         + form.format(path=path, dir=path.rsplit("/", 1)[0]))
        else:
            lines.append(f"      {path}")
    more = f"\n      … and {len(members) - 8} more" if len(members) > 8 else ""
    lead = ("nothing at the repo root, but manifests exist further in"
            if not detected else
            "MORE THAN ONE STACK: the commands above cover the repo ROOT only, "
            "and these manifests below it got NO checks")
    return (f"{lead}:\n" + "\n".join(lines) + more
            + "\n      Detection generates for the root only. Add what you want "
              "yourself — the argv above runs each from the root, since checks "
              "take no shell.")


def detect(root: str | Path) -> Stack:
    """Read a repo and suggest its prepare commands and quality checks."""
    root = Path(root)
    stack = Stack()

    for detector in ECOSYSTEMS:
        detector(root, stack)

    for marker, label in CONTEXT_MARKERS:
        if label and (root / marker).is_file() and label not in stack.names:
            stack.names.append(label)

    # Rule 1, applied last so it OVERRIDES an inferred install: the project's own
    # recipe is the project's own answer.
    recipes = _just_recipes(root)
    for recipe in BOOTSTRAP_RECIPES:
        if recipe in recipes:
            stack.prepare.insert(0, Command(
                name="bootstrap", argv=["just", recipe], operation="install",
                area="repo", timeout_seconds=900,
                description=f"The project's own `just {recipe}`"))
            # Drop the inferred installer; two installs in a row is waste at best
            # and a fight over the lockfile at worst.
            stack.prepare = [c for c in stack.prepare
                             if c.name != "install" or c is stack.prepare[0]]
            stack.notes.append(
                f"used the project's own `just {recipe}` instead of an inferred "
                f"install — the repo knows what it calls things")
            break

    # Scanned WHETHER OR NOT the root matched. A polyglot repo is precisely the
    # one that needs telling, and gating this on `not stack.detected` is what
    # made a Tauri app's whole Rust half invisible.
    members = _member_manifests(root)
    if members:
        stack.notes.append(_nested_note(members, stack.detected))

    if not stack.detected:
        if not members and recipes:
            stack.notes.append(
                "no manifest recognised; this repo has a justfile, so its recipes "
                f"are the likeliest source of commands: {', '.join(recipes[:8])}")

    if "install-hooks" in recipes:
        stack.prepare.append(Command(
            name="hooks", argv=["just", "install-hooks"], operation="install",
            area="repo", timeout_seconds=60,
            description="The project's git hooks, which its own gates may require"))
        stack.notes.append(
            "`just install-hooks` added to prepare: the factory commits, so a "
            "commit-msg hook has to be live. NOTE git config is shared with the "
            "parent repo, so this reaches outside a worktree")

    return stack


# ── rendering into a config ──────────────────────────────────────────────────

def _yaml_argv(argv: list[str]) -> str:
    """A flow-style argv list, quoting only what YAML would misread."""
    def item(part: str) -> str:
        if part != part.strip() or any(c in part for c in ":#{}[],&*?|>'\"%@`") \
                or not part:
            return json.dumps(part)
        return part
    return "[" + ", ".join(item(p) for p in argv) + "]"


def render_block(title: str, commands: list[Command], indent: str = "  ") -> str:
    lines = []
    for command in commands:
        lines.append(f"{indent}{command.name}:")
        lines.append(f"{indent}  argv: {_yaml_argv(command.argv)}")
        lines.append(f"{indent}  area: {command.area}")
        lines.append(f"{indent}  operation: {command.operation}")
        lines.append(f"{indent}  timeout_seconds: {command.timeout_seconds}")
        if command.description:
            lines.append(f"{indent}  description: {command.description}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n" if lines else ""
