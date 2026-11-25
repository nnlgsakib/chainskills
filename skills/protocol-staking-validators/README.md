# protocol-staking-validators — agent skill

Designs validator sets and staking on any stack: participation model, active set and epochs, deterministic performance-based rotation, self-bond, non-custodial delegation with O(1) share and reward accounting, commissions, unbonding, slashing and jailing, key rotation and post-quantum keys, and concentration controls. The same design can be built as a native module, validator-manager/system contracts, an L2 sequencer registry, or restaking operator sets.

```
protocol-staking-validators/
├── SKILL.md
└── references/  reward-accounting.md · slashing.md · implementations.md · attacks.md
```

Facts checked 2026-11-25 (Cosmos SDK v0.55 key rotation and ML-DSA-65, Avalanche ACP-99 v2, EigenLayer redistribution) are marked ✔. Part of the chainskills suite ([install](../../README.md#install)). MIT license.
