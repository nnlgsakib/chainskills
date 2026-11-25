# Test plan and traceability

## `docs/testing/plan.md` template

### 1. Scope
Components, versions, environments.

### 2. Traceability matrix

| Spec ID | Kind (INV / C / AC / R-N) | Component | Test level (unit / fuzz / invariant / sim / e2e / chaos / perf / model) | Test name(s) | Status |
|---|---|---|---|---|---|
| INV-STAKE-1 | INV | STAKE | invariant + sim | `TestINV_STAKE_1`, `invariant_INV_STAKE_1` | ✅ |
| STAKE.Delegate.C2 | C | STAKE | unit | `TestDelegate_C2_UnknownValidator` | ✅ |
| R-N1 block time ≤ 4 s p95 | R-N | CONS | perf | `perf/blocktime-50val-3region` | ⏳ |

### 3. Levels and tools
| Level | Tool (per stack) | Runs in |
|---|---|---|
| unit | go test / cargo test / forge test / hardhat test | every PR |
| fuzz | go test -fuzz / cargo-fuzz / forge fuzz / Echidna / Medusa | PR (short), nightly (long) |
| invariant (stateful) | handlers + invariants | PR (short), nightly (long) |
| simulation | app simulation | nightly |
| e2e multi-node | CometBFT e2e runner / interchaintest / Kurtosis | nightly + pre-release |
| chaos | see multi-node-chaos.md | weekly + pre-release |
| performance | see performance.md | weekly + pre-release |
| formal models | Quint / TLA+ / Certora / Kani (quality-formal-verification) | PR for model changes |

### 4. Exit criteria per release
- All critical invariants tested (`trace_invariants.py --strict` passes).
- No open critical or high bugs.
- Chaos suite green on the release candidate.
- Performance within R-N with a published report.
- Upgrade rehearsal passed (when the release includes a migration).

## Naming conventions
- Go: `TestINV_<COMP>_<n>_<desc>`, `TestOpName_Cn_<desc>`
- Solidity (Foundry): `invariant_INV_<COMP>_<n>()`, `test_OpName_Cn_<desc>()`
- Rust: `#[test] fn inv_<comp>_<n>_...`
- Quint/TLA+: `invariant INV_<COMP>_<n> = ...`

`trace_invariants.py` accepts `INV-X-1` and `INV_X_1` spellings.
