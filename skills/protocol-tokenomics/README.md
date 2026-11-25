# protocol-tokenomics — agent skill

Designs token economics on any stack: token roles, allocation and vesting, issuance models (disinflation, staking-target band, caps, tail emission), fees and burn, reward splits across roles, the security budget, simulation, and disclosure (including notes on the EU MiCA white paper).

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 scripts/emission_sim.py --example > config.json
python3 scripts/emission_sim.py config.json [--csv out.csv]
python3 scripts/emission_sim.py --selftest
```

```
protocol-tokenomics/
├── SKILL.md
├── scripts/     emission_sim.py (yearly supply, inflation, nominal and real staking yield, payouts per role)
└── references/  issuance-models.md · security-budget.md · simulation.md · disclosure.md
```

Reference points checked 2026-11-25 (Cosmos Hub, Solana, MiCA, token-engineering tools). Not legal advice. Part of the chainskills suite ([install](../../README.md#install)). MIT license.
