---
name: quality-testing
description: Test a blockchain to production standard, independent of stack — a test plan traced to spec invariants and checks, unit/property/fuzz/invariant tests, app-level simulation, multi-node end-to-end networks (CometBFT e2e runner manifests and perturbations, interchaintest for IBC, Kurtosis ethereum-package devnets and shadowforks), chaos testing (partitions, >1/3 offline, latency, clock skew, churn, restarts, beacon stalls), deterministic simulation testing (Antithesis), determinism and differential tests (parallel vs sequential, multi-client, replay), load testing and benchmarks against block-time/finality/throughput targets, upgrade rehearsals, and testnet programmes with exit criteria. Use whenever the user asks how to test a chain, set up a testnet, run chaos or load tests, benchmark TPS/finality, check determinism, or prove the chain meets its performance targets.
license: MIT
---

# Quality: Testing

A quality skill in chainskills (layer L5). It turns the spec's invariants, checks and non-functional requirements into tests and evidence. Unit tests come with each build/stack skill. This skill adds the system-level layers and makes sure nothing in the spec is left untested.

Inputs: `docs/spec/*` (INV/P/R IDs), R-N targets in `CHAIN.md`, the stack adapter (test tooling), the threat model (`quality-security`). Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/test-matrix.md` | Writing the test plan and traceability |
| `references/multi-node-chaos.md` | Multi-node networks, chaos and fault injection, deterministic simulation |
| `references/performance.md` | Load tests, benchmarks, performance reports |
| `scripts/trace_invariants.py` | Finding spec invariants that no test or model references |

## Workflow

### 1. Plan from the spec
Build `docs/testing/plan.md` from `references/test-matrix.md`: every `INV-*` gets at least one test, every check `C-n` gets a rejection test, every acceptance criterion gets a test, and every R-N gets a benchmark scenario. Then run:

```bash
python3 <skill-dir>/scripts/trace_invariants.py . --strict   # fails if a critical invariant has no test or model
```

### 2. Component level (per stack skill)
Unit tests, fuzz tests (`go test -fuzz`, cargo-fuzz, Foundry fuzz), and stateful invariant tests with handlers modelling real actors. Name the tests after their IDs (`TestINV_STAKE_2`, `invariant_INV_STAKE_2`).

### 3. Application level
- Random operation sequences against the full app, checking all invariants after every block. Cosmos: simulation (`ignite chain simulate` / `TestFullAppSimulation`). EVM: Foundry invariant tests on the deployed system.
- Genesis export/import round-trips.
- **Determinism**: run the same blocks on several nodes and platforms and compare app hashes. Compare parallel and sequential execution (e.g. Block-STM on vs off). For multi-client chains, compare implementations.

### 4. Network level
Use `references/multi-node-chaos.md`:
- **Multi-node e2e**: the CometBFT e2e runner (TOML manifest; perturbations: pause, kill, restart, disconnect, upgrade), interchaintest for IBC, and Kurtosis ethereum-package for Ethereum-style devnets and shadowforks.
- **Chaos scenarios**: partitions, more than 1/3 of voting power offline (expect a halt, then recovery), latency matrices, clock skew, validator churn, half of the non-consensus participants leaving, randomness beacon stalls, upgrades under load, state-sync joins.
- **Deterministic simulation testing** (e.g. Antithesis) for consensus and timing bugs that ordinary chaos runs miss.

### 5. Performance
Use `references/performance.md`: a realistic tx mix, geo-distributed validators matching R-N, and measurements of throughput, inclusion and finality latency (p50/p95/p99), block time, and resource use. Compare to R-N, keep a regression baseline in CI, and publish the report.

### 6. Upgrades
Rehearse every upgrade: export the latest state, run the migration on a fork (in-place testnet or shadowfork), then run invariants and a smoke load test. Test a rollback or halt plan as well (`ops-upgrades`).

### 7. Testnet programme
devnet → internal multi-region testnet → public (incentivised) testnet → mainnet candidate. Each stage has exit criteria: no open critical bugs, R-N met for N consecutive days, chaos suite green, upgrade rehearsed.

### 8. Report and update
Write `docs/testing/reports/<date>-<scope>.md` (environment, versions, results versus targets, failures and issue links). In `CHAIN.md`, move components to `tested` only with a report link. Tested invariants get their test names in `docs/spec/invariants.md`.

## Rules
- Untested invariants are open risks. Critical ones block the readiness gate.
- Performance claims cite a report with its environment and percentiles. Never quote a peak TPS without the latency and the setup.
- Every bug fix comes with a regression test named after the bug or issue.
- Test the failure modes you promised in the spec (halt, recovery, degraded randomness), not only the happy path.

## Sources (verified 2026-11-25)
CometBFT e2e runner (manifests, perturbations, stages): pkg.go.dev/github.com/cometbft/cometbft/test/e2e · interchaintest v10: pkg.go.dev/github.com/cosmos/interchaintest/v10 · Kurtosis ethereum-package (moved to ethpandaops): github.com/ethpandaops/ethereum-package · Antithesis (used by the Ethereum Foundation; deterministic hypervisor, fault injection): antithesis.com/industries/blockchain, fortune.com (Mar 2026) · Formal-model-guided conformance testing for blockchains: arxiv.org/abs/2501.08550.
