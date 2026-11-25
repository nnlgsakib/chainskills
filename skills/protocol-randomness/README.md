# protocol-randomness — agent skill

Designs secure randomness for any chain: it chooses the source (threshold BLS beacon, VRF, commit-reveal, prevrandao, drand quicknet or evmnet, Chainlink VRF v2.5), the required properties, and safe usage (commit-before-reveal, domain separation, deterministic stake-weighted sampling, reroll protection, fallbacks).

```
protocol-randomness/
├── SKILL.md
└── references/  sources.md · usage-patterns.md
```

Facts checked 2026-11-25 are marked ✔ and cite their sources. Part of the chainskills suite ([install](../../README.md#install)) (entry point: `blockchain-dev`). MIT license.
