# stack-cosmos-ignite — agent skill

Teaches AI coding agents to build **production-grade Cosmos SDK blockchains with [Ignite CLI](https://ignite.com/)**: from `ignite scaffold chain` through keeper logic, testing, upgrades, genesis launch and validator operations.

## What it does

- Scaffolds chains, modules, lists/maps/messages/queries/IBC packets with correct Ignite syntax
- Writes keeper and msg-server code in modern SDK style (collections, address codec, typed events, authority checks)
- Audits module code for non-determinism (wall-clock time, RNG, floats, goroutines, map iteration, I/O)
- Walks a production checklist: DoS/gas bounds, protobuf compatibility, simulation, upgrade handlers + migrations, real genesis, sentry/remote-signer setup, release builds

## Install

Part of the **chainskills** suite. Install the whole suite, because skills hand work to each other. See the [main README](../../README.md#install) for Claude Code (plugin), Codex, GitHub Copilot, Cursor, Gemini CLI and 40+ other agents.

## Requirements

- Go (version required by the scaffolded `go.mod`)
- Ignite CLI: `curl https://get.ignite.com/cli! | bash` or `brew install ignite`
- Linux or macOS. On Windows, use WSL2.
- Python 3 (for `scripts/audit_state_machine.py`)
- Optional: `buf`, `golangci-lint`, `govulncheck`, Docker

## Contents

```
stack-cosmos-ignite/
├── SKILL.md                         workflow Claude follows
├── references/
│   ├── placement-map.md             where each protocol concept lives in this stack
│   ├── cli.md                       Ignite command reference
│   ├── config-yml.md                dev config.yml reference
│   ├── module-dev.md                keeper / msg server / query patterns
│   └── production.md                production checklist
└── scripts/
    └── audit_state_machine.py       non-determinism scanner
```

Run the scanner yourself:

```bash
python3 scripts/audit_state_machine.py /path/to/mychain
python3 scripts/audit_state_machine.py --selftest
```

## Version note

Written against Ignite v29 (Cosmos release family 2025.1: SDK 0.53, CometBFT 0.38). Release family 2026.1 (SDK 0.55, CometBFT 0.40, Cosmos EVM 0.7) is current. See the adapter metadata in SKILL.md. The skill tells Claude to trust `ignite --help` and the project's `go.mod` when they differ from the references.

## License

MIT — see [LICENSE](LICENSE).
