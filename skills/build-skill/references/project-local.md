# Project-local skills

A project-local skill captures how *one* project works: its module scaffold, its review checklist, its deployment runbook, its naming and test conventions. It lives in the project's repo, so every teammate's agent loads it.

## Naming
- Use a short project prefix: `<project>-<topic>` (e.g. `acme-module-template`, `acme-release-runbook`). The suite's layer prefixes are reserved for suite skills.
- One skill per workflow. Don't make a "everything about our repo" skill. Agents match on descriptions, so narrow skills trigger better.

## Where to put it (project scope)
Paths from the `skills` CLI agent table and vendor docs, checked 2026-11-25. Each agent's docs are authoritative.

| Agent | Project skills folder |
|---|---|
| Claude Code | `.claude/skills/<name>/` |
| Codex, Cline, Warp, Zed, OpenCode, ... | `.agents/skills/<name>/` |
| GitHub Copilot | `.github/skills/<name>/` (also reads `.agents/skills/`) |
| Cursor | `.cursor/skills/<name>/` (also reads `.agents/skills/`) |
| Gemini CLI | `.gemini/skills/<name>/` (also reads `.agents/skills/`) |
| Windsurf | `.windsurf/skills/<name>/` |
| Kiro | `.kiro/skills/<name>/` |

For a mixed-agent team, `.agents/skills/` covers the most agents. Add `.claude/skills/` (a copy, or a symlink where the team's OS allows it) if anyone uses Claude Code. Commit the skill folder with the project.

## Content
- Base it on the project's real code: point to the actual files (`x/<module>/keeper/…`, `contracts/…`, `Makefile` targets, CI jobs) and describe the exact steps the team follows.
- Include the "don'ts" the team learned (past incidents, review comments that keep repeating).
- If it depends on suite skills, say so ("use `protocol-staking-validators` for design; this skill covers our module layout").
- No secrets, keys, internal hostnames or credentials, because skills are plain files that get shared.

## Validate
> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 <build-skill-dir>/scripts/check_skill.py .agents/skills/<name> --local
```
`--local` relaxes suite-only rules (layer prefix, README/LICENSE, sources section) to warnings. The Agent Skills format rules still apply.
