# stack-evm-l1 — agent skill

A chainskills stack adapter for **sovereign EVM L1s**. It covers five routes: Besu QBFT (permissioned BFT), an Ethereum-style PoS network with its own beacon chain, a custom node built with the reth SDK, a BSC-style PoSA geth fork with system contracts, and Avalanche L1 (pointer). Each route comes with genesis, validator management, testing and a production checklist.

- Versions verified (2026-11-25): geth v1.17.10, reth v2.11.0, Besu 26.11.2 (now `besu-eth`), Lighthouse v8.3.3, ethereum-package 6.1.0
- Placement map: 5 native, 5 extend, 3 custom, 2 n/a

```
stack-evm-l1/
├── SKILL.md
└── references/  placement-map.md · paths.md · production.md
```

Part of the chainskills suite ([install](../../README.md#install)). MIT license.
