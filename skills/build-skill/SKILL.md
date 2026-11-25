---
name: build-skill
description: Create, extend or refresh agent skills for blockchain development so the suite grows with new needs — new chainskills skills at any layer (protocol mechanisms like data availability, p2p, interop, MEV, bridges; ops workflows; quality practices; extras), project-local skills that capture one team's conventions (custom module patterns, deployment runbooks, review rules) installed into the project for Claude Code, Codex, Copilot, Cursor, Gemini CLI and other Agent Skills tools, and refreshes of skills whose facts are stale. Research-first from primary sources, template-based, validated with check_skill.py. Use whenever no existing skill covers a recurring need, the user asks to "make/add/create a skill", wants the agent to remember how their project does something, a framework or standard changed, or a skill's sources are older than six months. Stack adapters are handed to build-stack-adapter.
license: MIT
---

# Build Skill

This skill lets the suite extend itself. When a request has no skill, or a project has conventions an agent should follow every time, it creates a skill that follows the open Agent Skills format (`SKILL.md` folders), so it works in any compatible agent. It also keeps skills current.

| Reference / asset | Use when |
|---|---|
| `references/conventions.md` | Writing a suite skill: layers, naming, structure, writing style, sources, scripts |
| `references/project-local.md` | Creating a skill for one project or team, and where each agent loads it from |
| `assets/skill-template/SKILL.md.tmpl` | Starting a new skill (rename it to `SKILL.md` in the new folder) |
| `assets/skill-template/README.md.tmpl` | Starting the skill's README |
| `scripts/check_skill.py` | Validating any skill, new or existing (`--local` for project skills) |

## Modes

| Mode | Trigger | Output |
|---|---|---|
| **New suite skill** | a mechanism, workflow or practice that's useful for many chains and has no skill | `skills/<layer>-<topic>/` in the chainskills repo (or next to the installed suite) |
| **New stack adapter** | a framework or stack with no `stack-*` skill | hand over to `build-stack-adapter` |
| **Project-local skill** | how *this* project does something (its module template, deploy steps, review checklist, naming) | a skill in the project's skills folder (`references/project-local.md`) |
| **Extend** | an existing skill lacks a topic | new reference file + workflow step in that skill, not a new skill |
| **Refresh** | `check_skill.py` warns that sources are older than 180 days, or a framework or standard released something major | re-verified facts, updated dates, changelog entry |

## Workflow

### 1. Define the need precisely
- What tasks should the skill handle? Write 3 realistic user requests it must handle, and 2 near-misses it must *not* take.
- Check the existing skills first (the topic table in `../blockchain-dev/references/routing.md`). If one is close, **extend** it instead of creating an overlapping skill. Overlapping descriptions make agents pick the wrong one.
- Decide the mode and, for suite skills, the layer: design (L1), protocol mechanism (L2), build/implementation (L3), stack adapter (L4), quality (L5), ops (L6), or extra.

### 2. Research from primary sources
Before writing anything version-sensitive: official docs, specs (EIPs, RFCs, standards bodies), repos at a tag (README, CHANGELOG, code), release notes. Prefer code over blog posts. Note the source URL and date for each fact. Facts you can't verify go in as `(unverified)`. This rule exists because a skill that's confidently out of date does more harm than no skill. Project-local skills research the project itself: read its code, docs, CI and recent PRs, and ask the team where conventions aren't written down.

### 3. Write the skill
Copy `assets/skill-template/` to the new folder, rename the `.tmpl` files, and fill every placeholder, following `references/conventions.md`:
- `name` = folder name (lowercase, hyphens, ≤ 64 chars), with the layer prefix for suite skills.
- `description` (≤ 1024 chars) says **what** it covers and **when** to use it, including trigger phrases and indirect cases. This is what agents match on, so be specific and a little pushy.
- Body under about 250 lines: the workflow in imperative steps that explain *why*, a hand-off section (files, IDs, next skill), rules, and Sources. Put detail in `references/` with a "read when" table.
- Scripts only for deterministic, repeated work: stdlib Python with a `--selftest`.
- Stay agent-neutral: no single-harness tool names. Refer to other skills by name and to shared files by relative path (`../blockchain-dev/...`).

### 4. Validate
> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 <this-skill-dir>/scripts/check_skill.py <new-skill-dir>            # suite skill
python3 <this-skill-dir>/scripts/check_skill.py <new-skill-dir> --local    # project-local skill
python3 <new-skill-dir>/scripts/<script>.py --selftest                     # each bundled script
```
Fix all errors. Then dry-run the 3 requests from step 1 against the skill (if your agent supports subagents or evals, run them for real) and check that the near-misses don't trigger it.

### 5. Register and install
- **Suite skill**: add a row to the main README's skill table and to `blockchain-dev/references/routing.md` (topic → skill), add a CHANGELOG entry, and bump the plugin version (`.claude-plugin/plugin.json`) when releasing, since users only get updates when the version changes.
- **Project-local skill**: place it per `references/project-local.md` and commit it with the project.
- Tell the user how to load it now. Most agents pick up new skill folders on restart or reload (e.g. `/reload-plugins` or a new session).

### 6. Refresh mode
Run `check_skill.py` across all skills, then for each stale or affected one:
1. Diff upstream changelogs since the last verified date.
2. Update the facts, the ✔ marks and the "Sources (verified DATE)" line.
3. Run the skill's scripts' self-tests.
4. Record the breaking changes in CHANGELOG.

## Rules
- Prefer extending a skill over creating a near-duplicate.
- No fact without a source. Unverifiable means `(unverified)`, never invented.
- Keep skills general unless they're explicitly project-local. Examples should vary (different chains and stacks) so the skill doesn't overfit one project.
- Every new skill passes `check_skill.py` before it's used or shipped.
