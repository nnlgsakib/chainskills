# quality-testing — agent skill

Production test programme for any chain: a test plan traced to spec IDs, component, application and network-level tests, the CometBFT e2e runner, interchaintest, Kurtosis, chaos scenarios (partitions, more than 1/3 offline, churn, beacon stall, upgrades under load), deterministic simulation (Antithesis), determinism and differential tests, performance benchmarks against requirements, upgrade rehearsals and testnet exit criteria.

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 scripts/trace_invariants.py <project-root> --strict   # critical invariants without any test/model fail the run
python3 scripts/trace_invariants.py --selftest
```

```
quality-testing/
├── SKILL.md
├── scripts/     trace_invariants.py
└── references/  test-matrix.md · multi-node-chaos.md · performance.md
```

Part of the chainskills suite ([install](../../README.md#install)). MIT license.
