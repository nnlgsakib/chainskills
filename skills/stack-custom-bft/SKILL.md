---
name: stack-custom-bft
description: Build a custom blockchain on an existing BFT consensus engine without a full framework — a CometBFT ABCI 2.0 application in any language (InitChain, CheckTx, PrepareProposal, ProcessProposal, ExtendVote, VerifyVoteExtension, FinalizeBlock, Commit, snapshots for state sync), Rust ABCI via tendermint-rs, the Malachite Rust Tendermint library (channel, actor or core-library integration), and Commonware Rust primitives — covering determinism rules, state commitment, validator-set updates, mempool and proposal logic, crash recovery, and what you must build yourself (staking, governance, sync, tooling). Use whenever the user wants a custom chain or appchain in Rust/Go/other languages on CometBFT/Tendermint ABCI, Malachite, Commonware or a similar engine, or chose "custom" in design-stack-selection.
license: MIT
---

# Custom BFT chain adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). Use it when the state machine is your own code and consensus comes from a proven engine. You get BFT consensus. Everything else (state storage and proofs, staking, slashing, governance, fees, RPC, sync, tooling) you build or assemble. Design those pieces with the `protocol-*` skills first.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding what the engine gives you and what you build |
| `references/abci.md` | Implementing a CometBFT ABCI 2.0 application |

## Adapter metadata
- Family: custom
- Stack: CometBFT ABCI 2.0 apps (any language), Malachite (Rust), Commonware (Rust primitives)
- Versions verified: CometBFT v0.40.0 (Latest; adds `mldsa65` keys) and v0.38.x (supported lines per Cosmos release families 2026.1 / 2025.1; v1.x retracted); Go ≥ 1.22 for v0.38.x; tendermint-rs (now github.com/cometbft/tendermint-rs, pre-1.0, README says tested with Tendermint Core v0.34.21); Malachite (`arc-malachitebft-*` crates, Rust ≥ 1.82, "alpha… not externally audited", consensus foundation for Circle's Arc); Commonware monorepo (Apache-2.0 OR MIT, stability tiers ALPHA…EPSILON)
- Verified on: 2026-11-25
- Sources: docs.cosmos.network/cometbft (ABCI Overview and Methods); docs.cosmos.network/sdk/latest/release-family; github.com/cometbft/cometbft (+ releases); github.com/cometbft/tendermint-rs; github.com/circlefin/malachite (README, ARCHITECTURE.md); github.com/commonwarexyz/monorepo; commonware.xyz
- Unverified parts: ABCI client transport options (socket / gRPC / in-process) and app-side mempool details; whether `tendermint-abci` supports ABCI 2.0 methods at your target CometBFT version; Malachite and Commonware latest versions and audit status; `tower-abci` status.

## When to use this adapter
The design needs a state machine that no framework fits (novel execution, a non-Go language, an unusual data model), but you don't want to write consensus. Choose CometBFT for the most mature, widely deployed engine with an app interface in any language, Malachite for an embeddable Rust Tendermint, and Commonware for building blocks with consensus specialists on the team. If Cosmos SDK fits, use `stack-cosmos-ignite` instead, since it gives you staking, governance, IBC and tooling.

## Placement map
Summary of `references/placement-map.md`:
- Native: consensus (engine), p2p (engine networking: CometBFT p2p / Malachite libp2p)
- Extend: node-software (engine + your app binary), upgrades (engine upgrades; app versioning via `app_version`)
- Custom: state-execution, staking-validators (you emit validator updates), tokenomics, governance, randomness (vote extensions can carry beacon shares), verifiable-participation, interop (light clients; IBC requires implementing its spec), smart-contracts (only if you embed a VM), data-availability (snapshots and state sync you implement)
- n/a: rollup

## Setup
- **CometBFT**: install a supported release (v0.40.x or v0.38.x), run `cometbft init`, and connect your app (see `references/abci.md`). Pin a tag and never build from `main`.
- **Malachite**: start with the **channel-based** integration (`arc-malachitebft-app-channel`). It provides sync, crash recovery and networking. Move to actor-based or the sans-IO core library only when you must replace components. Rust ≥ 1.82. Quint specs are in the repo.
- **Commonware**: take primitives (consensus, p2p, storage, broadcast, cryptography) according to their stability tier. Examples are ALPHA and not for production. **Windows isn't supported** (use Linux or WSL2), and x86-64 needs AVX2/BMI2/ADX.

## Implement
1. Design the state machine with `design-spec` (state, operations, invariants) and `protocol-state-execution` (commitment structure, gas).
2. Implement deterministic execution: FinalizeBlock (CometBFT) or the Decide handler (Malachite) applies blocks. Follow the determinism rules in `design-spec/references/notation.md` without exception.
3. Commit state to an authenticated structure and return the app hash. Persist before returning from Commit.
4. Validator-set changes from your staking logic (`protocol-staking-validators`): CometBFT applies `validator_updates` from block H at **H+2**.
5. Build what the engine lacks: account and signature scheme, fees and anti-spam in CheckTx, RPC and indexing, state sync snapshots, upgrades and migration, and the operator CLI.

## Test
- Determinism: replay the same blocks on multiple nodes and platforms and compare app hashes (`quality-testing`).
- The CometBFT e2e runner (manifests, perturbations) for multi-node and crash tests. Malachite and Commonware have their own test harnesses and Quint specs to reuse.
- Property tests on every ABCI method, especially ProcessProposal and VerifyVoteExtension (deterministic, and must not reject honest proposals).

## Production
- Everything in `quality-security`, `quality-testing`, `quality-formal-verification` and `ops-*` applies, and you own all of it, because there's no framework hardening to lean on.
- Remote signer for validator keys (CometBFT privval; Cosmos-KMS supports CometBFT privval), sentry topology, and monitoring.
- Upgrade path: coordinated halt-height upgrades or app versioning. Rehearse.
- Audit the app **and** the integration with the engine. Malachite isn't externally audited (per its README).

## Known pitfalls
- A non-deterministic FinalizeBlock or ProcessProposal halts the chain (app-hash mismatch) or splits votes.
- Rejecting valid proposals in ProcessProposal or vote extensions in VerifyVoteExtension hurts liveness. CometBFT's docs advise accepting unless you understand the implications.
- An invalid PrepareProposal response crashes CometBFT. Always respect `max_tx_bytes`.
- Setting `retain_height` too low can make new nodes unable to bootstrap without state sync.
- Underestimating the "everything else" work. Budget for staking, governance, upgrades, sync, explorers and audits.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Check CometBFT releases and release families, tendermint-rs, and the Malachite and Commonware repos (versions, audits, integration APIs), and resolve the Unverified list.
