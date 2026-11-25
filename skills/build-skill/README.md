# build-skill — agent skill

Lets the chainskills suite extend itself. It creates new suite skills at any layer, project-local skills that capture a team's conventions (for Claude Code, Codex, Copilot, Cursor, Gemini CLI and other Agent Skills tools), and refreshes skills whose facts have gone stale. It researches primary sources first, starts from a template, and validates the result. Stack adapters are handed to `build-stack-adapter`.

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 scripts/check_skill.py ../*                       # validate every suite skill
python3 scripts/check_skill.py .agents/skills/my-skill --local
python3 scripts/check_skill.py --selftest
```

```
build-skill/
├── SKILL.md
├── scripts/     check_skill.py (Agent Skills format + suite conventions + stale-source warnings)
├── references/  conventions.md · project-local.md
└── assets/skill-template/  SKILL.md.tmpl · README.md.tmpl
```

Part of the chainskills suite ([install](../../README.md#install)). MIT license.
