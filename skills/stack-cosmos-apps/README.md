# stack-cosmos-apps — agent skill

Teaches AI coding agents to use **[Ignite Apps](https://github.com/ignite/apps)**, the plugins that extend Ignite CLI, and to write new ones.

| App | Use |
|---|---|
| hermes | IBC relaying between chains |
| wasm | CosmWasm smart contracts |
| spaceship | Deploy a chain to a server over SSH |
| network | Coordinate a genesis with validators on Ignite Chain |
| explorer | Gex terminal explorer / Ping.pub web explorer |
| connect | Talk to any Cosmos SDK chain from the CLI |
| cca | Chain web frontend (create-cosmos-app) |
| fee-abstraction | Pay fees with IBC tokens |
| evolve | Rollups on a data-availability layer |
| gnovm | Gno smart contracts |
| appregistry | Discover community apps |

EVM is covered by the separate `stack-cosmos-evm` skill.

## Install

Part of the **chainskills** suite. Install the whole suite, because skills hand work to each other. See the [main README](../../README.md#install) for Claude Code (plugin), Codex, GitHub Copilot, Cursor, Gemini CLI and 40+ other agents.

## Contents

```
stack-cosmos-apps/
├── SKILL.md                 catalog + install + production notes
└── references/
    ├── apps.md              commands and gotchas for every app
    ├── authoring.md         writing your own Ignite App (manifest, commands, hooks, testing, publishing)
    └── placement-map.md     where each protocol concept lives (which app covers it)
```

Based on the ignite/apps main branch, November 2026. Each app pins its own minimum Ignite version (listed in SKILL.md).

## License

MIT — see [LICENSE](LICENSE).
