---
name: quality-formal-verification
description: Apply formal methods where a blockchain bug is fatal, independent of stack — choosing what to verify (custom consensus or finality rules, staking and reward accounting, bridges and light clients, rollup dispute/proof logic, verification-layer protocols, governance timelocks, token supply), protocol modelling and model checking with Quint (Apalache, simulator) or TLA+ (TLC/Apalache), model-based and conformance testing against the implementation, and code-level verification (Certora Prover, Halmos, Kontrol, hevm, forge equivalence for Solidity; Kani for Rust). Use whenever the user wants to formally verify, model check, prove invariants, write a Quint or TLA+ spec, use Certora/Halmos/Kani, or asks how to get stronger assurance than tests for critical chain logic.
license: MIT
---

# Quality: Formal Verification

A quality skill in chainskills (layer L5). Tests sample behaviours, while models and provers check all behaviours within stated bounds. Formal methods are expensive, so use them on the few components where a bug loses funds or breaks consensus, and connect them to the code so the assurance is real.

Inputs: `docs/spec/<component>.md` (state, operations, invariants), `docs/spec/invariants.md` (severity), the threat model. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference / asset | Use when |
|---|---|
| `references/tools.md` | Choosing a tool per layer and language |
| `references/property-catalog.md` | Picking properties to verify per component type |
| `assets/participation.qnt` | Starting a Quint model (bonded participants, commit/reveal, slashing, bounded rewards, supply conservation) |

The starter model was checked on 2026-11-25 with Quint v0.34.0: `quint typecheck` passed; `quint run` passed 2,000 random traces of 40 steps with all 4 invariants holding and both observations reachable; `quint verify` (Apalache) found no violation of `INV_TOKEN_1` up to 5 steps; and a mutated version (slash without reducing the bond) was caught by `INV_TOKEN_1`.

## Workflow

### 1. Choose the targets
From `invariants.md`, take every **critical** invariant plus any novel protocol logic: custom consensus or rotation rules, the verification layer's assignment/challenge protocol, bridge and light-client verification, dispute games, reward and slashing accounting, timelock and governance execution. Write the choice and its rationale as an ADR, so it's clear what isn't formally covered.

### 2. Pick the level and tool (`references/tools.md`)
- **Protocol level** (distributed behaviour, adversaries, message interleavings): Quint or TLA+.
- **Code level**: Solidity with Certora, Halmos, Kontrol or hevm; Rust with Kani; Go with property-based tests plus model-based testing from Quint traces.
- **Conformance**: generate traces from the model and replay them against the implementation.

### 3. Model
- State = the spec's State section. Actions = the spec's operations and hooks (guards = checks C-n, updates = effects E-n). Include adversary actions within the stated trust assumptions (e.g. f < n/3 Byzantine nodes that may equivocate or withhold).
- Name invariants after their spec IDs (`invariant INV_STAKE_1 = ...`). Express liveness as `temporal` properties under explicit fairness or synchrony assumptions.
- Keep the model small: 3–4 nodes, small value ranges. Most bugs show up in small configurations.
- Add `observation`s for states you expect to be reachable, so a vacuous model (nothing ever happens) is detected.

### 4. Check
1. `quint typecheck` → `quint run` (random simulation, fast, finds shallow bugs).
2. `quint verify` (Apalache bounded model checking) for each critical invariant. Increase `--max-steps` until runtime becomes a limit, and record the bound.
3. **Mutation sanity check**: plant a known bug and make sure an invariant fails. If nothing fails, the invariants are too weak.
4. For every counterexample: decide whether it's a spec bug, a model bug or a real bug, fix it at the source, and add a regression test in `quality-testing`.

### 5. Connect to code
- Quint `--out-itf` traces → a replay harness that drives the implementation through the same steps and compares state (model-based testing).
- Code-level provers on the contracts or crates that implement the critical invariants.
- Keep the model, spec and code IDs aligned. `quality-testing/scripts/trace_invariants.py` counts `.qnt`/`.tla` references as coverage.

### 6. Report
For each component, write `docs/verification/<component>.md` with: properties verified, tool and version, bounds (steps, node count, value ranges), assumptions, what's *not* covered, results, and counterexamples found and fixed. Then update `invariants.md` (Model column) and `CHAIN.md`.

## Rules
- Every claim states its bounds and assumptions ("verified for ≤ 4 nodes, ≤ 10 steps, f < n/3").
- A model that never reaches interesting states proves nothing, so check the observations.
- Verification doesn't replace audits or tests. It finds a different class of bugs.
- Models change with the spec. Run quick checks in CI on every spec or model change.

## Sources (verified 2026-11-25)
Quint v0.34.0 (released 22 Nov 2026; `invariant`/`observation`/`temporal` definitions, `quint run`/`verify` via Apalache): github.com/informalsystems/quint · Thoughtworks Radar (Quint: "Assess", 4 Nov 2026): thoughtworks.com/radar/languages-and-frameworks/quint · Certora Prover open-sourced, GPL-3.0 (24 Feb 2025): certora.com/blog/certora-goes-open-source · Kani (ASE 2026 industry paper): arxiv.org/abs/2607.01504 · Halmos and Kontrol: ethereum.org developer tools · Foundry `forge equivalence` (v1.10.0): github.com/foundry-rs/foundry/releases.
