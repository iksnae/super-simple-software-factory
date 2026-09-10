# Quality Standards — what "done" checks

**Purpose:** the pass/fail conditions a README must meet before it ships.

## Why there is no score

The imported version of this file scored a README out of ten — completeness 2,
accuracy 3, clarity 2, functional 2, compliance 1 — and called 8.0 publication
ready.

We do not score. A score of 7.5 tells nobody what to fix, invites arguing the
number instead of the defect, and lets a README with **one false claim** pass on
the strength of good prose. One false claim is the whole failure mode: a reader
reasons from it.

So the standard is binary, per claim, and the report names what failed.

## The conditions

Every one is pass or fail. A single fail blocks.

| # | Condition | How it is checked |
| --- | --- | --- |
| 1 | The role is named and the shape matches it | SKILL.md §1 Step 1 |
| 2 | Every path, file and directory named exists | Layer 1 |
| 3 | Every quoted signature, field and version matches source exactly | Layer 2 |
| 4 | Every command runs as written | Layer 3, after risk classification |
| 5 | Every link resolves | Layer 4 |
| 6 | Every count and version was re-measured, not recalled | Layer 5 |
| 7 | No duplicated inventory, or a gate keeps the copy honest | SKILL.md §3 |
| 8 | No placeholder text ships | grep for TODO, `[Add`, "Coming soon" |
| 9 | Nothing a reader does not need *here* | judgement; length is the smell |

## Reporting

Report failures as **claim → layer → evidence**:

> `README.md:41` claims `schemas/KSPD/index.schema.json`. Layer 1: no such file.
> Nearest match `schemas/KSPD/info.schema.json`. Remove or correct.

Not "accuracy 2.5/3".

## What is not a quality problem

Recorded because the imported standards treated these as defects and they are
not, for our repositories:

- **No table of contents.** Under 150 lines it is noise. Over 150, the problem
  is the length.
- **No badges.** A badge a reader does not act on is decoration.
- **No Contributing or Code of Conduct section.** These are private repositories.
- **Short.** Brevity is the target, not a gap. The KSPD README went from 267
  lines to 94 and got better.

## Best Practices Checklist

### Content Best Practices

**DO:**
- ✅ Start with single-sentence description
- ✅ Include working, tested examples
- ✅ Use exact quotes from package metadata
- ✅ Link to detailed docs for complex topics
- ✅ Include badges (CI, version, license, downloads)
- ✅ Add table of contents if >100 lines
- ✅ Use code blocks with language tags
- ✅ Show expected output for examples
- ✅ Include troubleshooting for common issues
- ✅ Specify prerequisites (Node >=16, Python >=3.8)

**DON'T:**
- ❌ Write vague descriptions ("does stuff")
- ❌ Include untested examples
- ❌ Paraphrase package metadata
- ❌ Duplicate entire documentation
- ❌ Add fake badges
- ❌ Skip table of contents for long READMEs
- ❌ Use plain text instead of code blocks
- ❌ Assume users know the output
- ❌ Ignore common user issues
- ❌ Omit version requirements

---

### Writing Style Best Practices

**Tone:**
- Professional but friendly
- Direct and concise
- Action-oriented (use imperatives: "Run", "Install", "Create")
- Avoid marketing fluff

**Voice:**
- Second person ("You can install...")
- Imperative for instructions ("Run `npm install`")
- Avoid passive voice

**Language:**
- Simple, clear English
- Define technical terms
- Use consistent terminology
- Spell out acronyms on first use

**Formatting:**
- Use headings hierarchically (H1 → H2 → H3)
- Use lists for 3+ items
- Use tables for comparisons
- Use code blocks for commands/code
- Use blockquotes for notes/warnings

---

### Visual Elements Best Practices

**Screenshots:**
- Include for GUI applications
- Show actual interface, not mockups
- Keep images up-to-date
- Use alt text for accessibility
- Optimize size (<500KB per image)

**Badges:**
- Place near top, after description
- Use relevant badges only (CI, version, license)
- Verify badge URLs are correct
- Don't overuse (max 5-7 badges)

**Code Blocks:**
- Always specify language (```bash, ```python, etc.)
- Include syntax highlighting
- Show input AND expected output
- Keep examples concise (<20 lines)

**Links:**
- Use descriptive text (not "click here")
- Verify all links work
- Use relative paths for repo files
- Use absolute URLs for external sites

---

## Anti-Patterns to Avoid

### Content Anti-Patterns

❌ **"Empty README"**
```markdown
# Project Name

TODO: Add documentation
```
**Fix:** Use template-library.md to structure content

❌ **"Copy-Paste from Other Projects"**
```markdown
# MyLib

Similar to lodash but better...
```
**Fix:** Write original description based on YOUR code

❌ **"Outdated Examples"**
```markdown
npm install old-package-name  # Package renamed 2 years ago
```
**Fix:** Verify examples against current codebase

❌ **"Broken Links"**
```markdown
[Docs](./docs/guide.md)  # File doesn't exist
```
**Fix:** Validate all links (Layer 4 validation)

❌ **"Invented Features"**
```markdown
- Automatic caching (not implemented)
- Real-time updates (not implemented)
```
**Fix:** Only document features that exist in code

---

### Style Anti-Patterns

❌ **"Wall of Text"**
```markdown
This is a very long paragraph that goes on and on without any breaks or structure making it very difficult to read...
```
**Fix:** Break into 3-5 sentence paragraphs

❌ **"Unclear Commands"**
```markdown
Run the thing:
some-command
```
**Fix:** Use code blocks with language tags:
\`\`\`bash
npm run build
\`\`\`

❌ **"Assumed Knowledge"**
```markdown
Configure your environment and run it.
```
**Fix:** Provide specific steps:
```bash
1. Copy .env.example to .env
2. Set DATABASE_URL in .env
3. Run: npm start
```

❌ **"Marketing Fluff"**
```markdown
The world's best, fastest, most amazing library!
```
**Fix:** Be factual:
```markdown
A TypeScript library for data validation with 10,000+ downloads/week.
```

---

## Length Guidelines

**Overall README:**
- Minimum: 50 lines (below this is incomplete)
- Ideal: 100-300 lines (comprehensive but scannable)
- Maximum: 500 lines (beyond this, split into multiple docs)

**If >500 lines:**
- Use progressive disclosure
- Create separate docs (API.md, CONTRIBUTING.md, etc.)
- Link from README
- Keep README as high-level overview

**Section Lengths:**
```
Title + Description: 3-5 lines
Installation: 5-15 lines
Quick Start: 10-30 lines
API Reference: 20-100 lines (or link to docs)
Examples: 20-50 lines
Configuration: 10-30 lines
Contributing: 3-10 lines (or link)
License: 1-3 lines
```

---

## Fixing what failed

Work the failures in this order. It is not a preference — the first two make a
reader act on something untrue, and the rest do not.

1. **Existence and accuracy** (Layers 1–2). A named file that does not exist, or
   a signature that does not match. Fix first, always.
2. **Execution** (Layer 3). A command that does not run as written.
3. **Duplication.** An inventory copied from elsewhere: link it, or gate it.
4. **Shape.** Wrong role template, benefits copy, three intro sections.
5. **Length.** What belongs one link away.

Re-run the failing layer only. A full re-verify after every edit hides which fix
addressed which failure.

---

## Before it ships

- [ ] Role named, shape matches (SKILL.md §1 Step 1)
- [ ] Layers 1–5 pass (`validation-checklist.md`)
- [ ] Every command executed as written, after risk classification
- [ ] No duplicated inventory, or a gate keeps the copy honest (SKILL.md §3)
- [ ] No placeholder text — grep `TODO`, `[Add`, "Coming soon"
- [ ] Licence stated and `LICENSE` linked
- [ ] Every count and version re-measured at the moment of writing

If any box is unchecked, say which one in the report. Do not ship with a summary
that implies the whole list passed.
