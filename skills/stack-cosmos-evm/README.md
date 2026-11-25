# stack-cosmos-evm — agent skill

Teaches AI coding agents to build **EVM-compatible Cosmos SDK chains** with the [Ignite EVM app](https://github.com/ignite/apps/tree/main/evm) and [cosmos/evm](https://github.com/cosmos/evm): Solidity contracts, MetaMask, Ethereum JSON-RPC, Foundry/Hardhat, ERC20 ↔ Cosmos coins, precompiles, and production hardening.

## What it adds beyond the app README

The skill flags rough edges found in the generated code (evm app v0.2.0) and tells Claude to fix them:

- EVM denom hard-coded to `stake`
- EVM chain ID taken from a hash of the Cosmos chain-id
- `ignite evm init` producing invalid denom metadata for `a…` denoms
- coin type may stay at 118 instead of 60
- unlimited consensus block gas against a fixed EVM mempool gas limit

It also includes a genesis checker:

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 scripts/check_evm_genesis.py ~/.mychain/config/genesis.json
python3 scripts/check_evm_genesis.py --selftest
```

## Install

Part of the **chainskills** suite. Install the whole suite, because skills hand work to each other. See the [main README](../../README.md#install) for Claude Code (plugin), Codex, GitHub Copilot, Cursor, Gemini CLI and 40+ other agents.

## Contents

```
stack-cosmos-evm/
├── SKILL.md                       workflow: scaffold → evm add → fix edges → test → harden
├── references/
│   ├── placement-map.md             where each protocol concept lives in this stack
│   ├── wiring.md                  exactly what `ignite evm add` changes; upgrading cosmos/evm
│   ├── tooling.md                 JSON-RPC config, keys, MetaMask, Foundry, Hardhat, smoke tests
│   └── production.md              EVM-specific production checklist
└── scripts/
    └── check_evm_genesis.py       genesis sanity checker
```

## Extending

This skill is the base for wider EVM work. Add new references (for example `solidity.md` or `precompiles.md`) and link them from the table in `SKILL.md`.

## License

MIT — see [LICENSE](LICENSE).
