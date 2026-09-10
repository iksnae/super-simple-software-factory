@AGENTS.md

## Claude Code specifics

- **The skill in this repo is for operating the factory, not for changing it.**
  `.claude/skills/sssf/SKILL.md` loads when the request is "run a workflow",
  "set up a repo", "add an agent". When the request is to change this codebase,
  `AGENTS.md` above governs and the skill is reference material at most.
- **Do not edit the skill to work around a code problem.** The cookbooks describe
  what the code does; if they are wrong, one of the two is a bug and it is
  usually not the cookbook.
