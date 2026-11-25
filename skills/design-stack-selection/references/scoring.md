# Scoring

## Criteria

| # | Criterion | 5 means | Typical weight |
|---|---|---|---|
| 1 | Requirement fit | Meets every R-F/R-N natively | 3 |
| 2 | Customisability where needed | The components that need custom logic can be implemented natively | 3 |
| 3 | Security model fit | Matches the trust assumptions (own set / inherited / shared) | 3 |
| 4 | Finality and latency | Beats R-N targets with margin | 2 |
| 5 | Throughput headroom | ≥ 3× peak target in benchmarks | 2 |
| 6 | Developer ecosystem | Wallets, explorers, SDKs, libraries the users expect | 2 |
| 7 | Team fit | Language and experience match | 2 |
| 8 | Maturity | Production chains, audits, release cadence, security process | 3 |
| 9 | Time to market | Testnet in weeks, not months | 1–3 |
| 10 | Operational burden | Few moving parts to run (sequencer, prover, DA, relayers) | 2 |
| 11 | Cost | Infrastructure + security bootstrapping + DA/settlement fees | 2 |
| 12 | Interoperability | Native bridges and messaging to the required ecosystems | 1–3 |
| 13 | Licence | Permissive, no revenue share, no field-of-use limits | 1–3 |
| 14 | Decentralisation path | Clear route to permissionless validators/sequencers | 2 |
| 15 | Upgrade agility | Can ship breaking changes safely (forkless or coordinated upgrades) | 1 |

Adjust weights from the requirements and record them in the ADR. A criterion that was a hard filter is not scored again.

## Matrix template

| Criterion (weight) | Stack A | Stack B | Stack C |
|---|---|---|---|
| Requirement fit (3) | 4 — <reason/source> | | |
| ... | | | |
| **Weighted total** | | | |

## Sensitivity check

For the top two stacks, find the smallest weight change that would flip the order. If it's within reason (one weight ±1), the choice depends on that criterion. Name it in the ADR, under "Revisit when".

## Prototype spike

If the top two are close, or a critical component's feasibility is uncertain, recommend a time-boxed spike (1–2 weeks): implement the riskiest component on both stacks and benchmark it. Record the result in the ADR.
