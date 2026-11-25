# design-stack-selection — agent skill

Picks the implementation stack and decides where each component lives.

- Hard filters, then a weighted 15-criterion score with a check on how sensitive the result is to the weights
- Catalog covering Cosmos SDK, Cosmos EVM, Substrate, Avalanche L1, geth/reth/Besu, OP Stack, Arbitrum Orbit, ZK Stack, Polygon CDK, sovereign rollups, shared security, permissioned chains, custom builds, and "no new chain"
- Places each component in one of: native module, precompile, system contract, smart contract, L1 contract, off-chain service, client
- Hands off to the matching `stack-*` adapter, or to `build-stack-adapter` if there isn't one

```
design-stack-selection/
├── SKILL.md
└── references/  stack-catalog.md · scoring.md · placement.md
```

Part of the chainskills suite. Installation: see the [main README](../../README.md#install). MIT license.
