# protocol-consensus — agent skill

Designs a chain's consensus layer on any stack. It chooses the consensus family, sets validator count, block time and timeouts, states safety, liveness and halt behaviour, decides ordering/MEV/censorship policy, and reviews the design against known attacks.

```
protocol-consensus/
├── SKILL.md
└── references/  families.md · attacks.md · ordering-mev.md
```

Facts checked 2026-11-25 (CometBFT v0.40 and release families, Malachite, Solana Alpenglow, Ethereum ePBS and FOCIL timelines) are marked ✔ and cite their sources. Part of the chainskills suite ([install](../../README.md#install)) (entry point: `blockchain-dev`). MIT license.
