# Contributing

## Ground rules
- **Stack-neutral above L4.** `design-*`, `protocol-*`, `quality-*` and `ops-*` skills never assume a framework. Framework-specific material goes into a `stack-*` adapter.
- **Verify, then write.** Check every version, API, standard or "current best practice" against a primary source (official docs, repo, release notes). Mark checked facts with ✔, mark the rest `(unverified)`, and list sources with dates.
- **One skill, one folder under `skills/`** (open Agent Skills format): `SKILL.md` (frontmatter `name` = folder name, lowercase-hyphen, ≤ 64 chars; `description` ≤ 1024 chars saying what the skill does and when to use it; `license: MIT`), `README.md`, `LICENSE`, and optional `references/`, `scripts/`, `assets/`.
- **Scripts** are stdlib-only Python with a `--selftest` (or `selftest`) mode that must pass.
- **Shared state**: skills read and write the `CHAIN.md` / `docs/` layout defined in `blockchain-dev/references/chain-md.md`.

## Adding a skill
Use the `build-skill` skill (template in `skills/build-skill/assets/skill-template/`), then validate:

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 skills/build-skill/scripts/check_skill.py skills/<new-skill>
```

## Adding a stack adapter
Use the `build-stack-adapter` skill. It copies `build-stack-adapter/assets/adapter-template/`, and you validate with:

```bash
python3 skills/build-stack-adapter/scripts/check_adapter.py skills/stack-<family>-<name>
```

## Before opening a PR
```bash
for s in skills/*/scripts/*.py; do python3 "$s" --selftest 2>/dev/null || python3 "$s" selftest; done
python3 skills/build-skill/scripts/check_skill.py skills/*
python3 skills/build-stack-adapter/scripts/check_adapter.py skills/stack-*
claude plugin validate . --strict      # if you have Claude Code
```
Update `CHANGELOG.md` and the skill table in `README.md`.
