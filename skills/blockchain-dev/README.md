# blockchain-dev — agent skill (suite entry point)

The router for the **chainskills** suite. Give it any blockchain idea on any stack, and it runs the work in the right order: design, spec, stack choice, build, quality, then ops. Each step goes to the skill that owns it. All skills share project state through `CHAIN.md`.

## What it does

- Finds or creates `CHAIN.md` and the `docs/` layout in your chain repo.
- Works out the current phase and routes to the next skill (`references/routing.md`).
- In production mode, applies phase gates: no stack choice without a spec, no mainnet without a readiness report.
- Finds stack adapters automatically: any installed `stack-*` skill.
- When a planned skill isn't installed yet, falls back to general knowledge and keeps the same output format.

## Files

```
blockchain-dev/
├── SKILL.md
├── references/
│   ├── routing.md            phase and topic → skill tables, the hierarchy, common skill chains
│   └── chain-md.md           CHAIN.md + docs/ layout, ID scheme, update rules
└── assets/
    ├── CHAIN.template.md     starting CHAIN.md
    └── ADR.template.md       decision record template used by every skill
```

## Install

Part of the **chainskills** suite. Install the whole suite, because skills hand work to each other. See the [main README](../../README.md#install) for Claude Code (plugin), Codex, GitHub Copilot, Cursor, Gemini CLI and 40+ other agents.

## License

MIT — see [LICENSE](LICENSE).
