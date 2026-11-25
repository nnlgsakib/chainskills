# protocol-verifiable-participation — agent skill

Designs permissionless participation layers (community/verifier nodes, DePIN, relay, storage, DA sampling, oracles) that pay only for verifiable work. It covers the verifiability ladder, the assign → commit → reveal → challenge → settle template, claims-and-proofs (as in Pocket Network's relay mining), defences against lazy verifiers and collusion, sybil resistance, and deterrence economics. It also keeps the layer off the finality path.

```bash
python3 scripts/committee_risk.py committee --nodes 1000 --malicious 0.2 --threshold-frac 0.334 --target 1e-9
python3 scripts/committee_risk.py deterrence --gain 10 --audit-rate 0.05 --tasks 20
python3 scripts/committee_risk.py selftest
```

```
protocol-verifiable-participation/
├── SKILL.md
├── scripts/     committee_risk.py (exact hypergeometric committee risk + minimum penalty)
└── references/  work-types.md · protocol-template.md · sybil.md
```

Part of the chainskills suite ([install](../../README.md#install)). MIT license.
