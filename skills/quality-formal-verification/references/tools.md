# Formal tools by layer

Facts checked 2026-11-25 are marked ✔.

## Protocol level

| Tool | What | Checkers | Notes |
|---|---|---|---|
| **Quint** | Modern specification language built on TLA+ semantics, with typed, programmer-friendly syntax | `quint run` (random simulator), `quint verify` (Apalache symbolic model checker; needs Java and downloads Apalache), TLC via transpilation | v0.34.0 released 22 Nov 2026 ✔; `invariant`, `observation` and `temporal` definitions ✔; ITF trace output (`--out-itf`) for model-based testing ✔; designed by the Apalache team at Informal Systems ✔; Thoughtworks Radar "Assess", calling the choice versus TLA+ a close call (better tooling and readability versus TLA+ maturity) ✔ |
| **TLA+** | The classic specification language | TLC (explicit-state), Apalache (symbolic) | mature, large literature (consensus protocols, distributed databases) |

Install Quint: `npm i -g @informalsystems/quint` (or per project). Verified working with Node 24 and Java 21 on 2026-11-25.

## Code level

| Language | Tool | Type | Notes |
|---|---|---|---|
| Solidity/EVM | **Certora Prover** | rule-based verification of bytecode (CVL specs) | open-sourced 24 Feb 2025 under GPL-3.0; supports EVM, Solana, Stellar ✔ |
| Solidity/EVM | **Halmos** (a16z) | symbolic testing that reuses Foundry tests | finds assertion violations symbolically ✔ |
| Solidity/EVM | **Kontrol** (Runtime Verification) | KEVM + Foundry | formal proofs over Foundry tests ✔ |
| Solidity/EVM | hevm | symbolic execution / equivalence | — |
| Solidity/EVM | `forge equivalence` | bytecode equivalence between two versions (refactors, optimisations) | new in Foundry v1.10.0 ✔ |
| Rust | **Kani** | bounded model checking (CBMC) with function and loop contracts → unbounded proofs | used at scale for Rust standard-library verification (16,000+ harnesses) ✔; `cargo install --locked kani-verifier && cargo kani setup` ✔ |
| Go | no mainstream verifier | — | use property-based tests, fuzzing, and replay of Quint traces (model-based testing) |

## Conformance / model-based testing
- Generate traces from the model (Quint `--out-itf`), drive the implementation with the same actions, and compare state after each step.
- Research: formal-model-guided conformance testing for blockchains with deterministic simulation (arXiv 2501.08550) ✔.

Sources: https://github.com/informalsystems/quint · https://github.com/informalsystems/quint/blob/main/docs/content/docs/quint.md · https://www.thoughtworks.com/radar/languages-and-frameworks/quint · https://certora.com/blog/certora-goes-open-source · https://github.com/Certora/CertoraProver · https://arxiv.org/abs/2607.01504 · https://ethereum.org/developers/tools/ · https://arxiv.org/abs/2501.08550
