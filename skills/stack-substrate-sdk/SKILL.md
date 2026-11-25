---
name: stack-substrate-sdk
description: Build and operate a chain with the Polkadot SDK (Substrate, FRAME, Cumulus) — parachains on Polkadot via coretime (bulk or on-demand), solo chains, runtime development with FRAME pallets, polkadot-omni-node and chain-spec-builder, Pop CLI, staking/collator pallets, weights and benchmarking (frame-omni-bencher), forkless runtime upgrades, testing with zombienet-sdk and chopsticks, and smart contracts on Polkadot Hub (pallet-revive: REVM + PolkaVM, Solidity via resolc). Use whenever the user works with Substrate, Polkadot SDK, FRAME, parachains, coretime, runtime upgrades, pallets, Polkadot Hub contracts, or chose Polkadot SDK in design-stack-selection.
license: MIT
---

# Polkadot SDK / Substrate adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It maps stack-neutral designs onto a FRAME runtime. A parachain is secured by the Polkadot relay chain through coretime, and a solo chain brings its own consensus and validators.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |

## Adapter metadata
- Family: substrate
- Stack: Polkadot SDK (Substrate + FRAME + Cumulus), by Parity and the Polkadot community
- Versions verified: `polkadot-stable2609-2` (node v1.25.2; `polkadot-omni-node` 0.25.0, `frame-omni-bencher` 0.29.0, `frame-benchmarking-cli` 64.0.1, `pallet-revive` 0.22.0, `polkadot-sdk` 2609.3.0). `polkadot-stable2611-rc1` is a pre-release (becomes v1.26.0). Pop CLI needs Rust ≥ 1.91.1.
- Verified on: 2026-11-25
- Sources: github.com/paritytech/polkadot-sdk/releases; developers.polkadot.com (formerly docs.polkadot.com): parachains/get-started, launch-a-parachain/set-up-the-parachain-template, obtain-coretime, runtime-maintenance/runtime-upgrades, smart-contracts/overview (updated 29 Jun 2026); github.com/r0gue-io/pop-cli
- Unverified parts: Pop CLI subcommand syntax (`pop new …`, `pop up …`), solo-chain template details (Aura/BABE + GRANDPA, staking pallets), try-runtime/zombienet/chopsticks versions, `authorize_upgrade` flow, mainnet coretime steps, and the SDK licence file. Check with `--help` and the repo.

## When to use this adapter
App-specific chains that want **custom runtime logic in Rust** with forkless upgrades, either secured by Polkadot validators (parachain plus coretime, no validator bootstrapping) or standalone (solo chain with your own validator set). Also for contracts on Polkadot Hub (Solidity via REVM or PolkaVM).

## Placement map
Summary of `references/placement-map.md`:
- Native: state-execution (FRAME runtime, Wasm), staking-validators (staking/session/collator pallets), governance (OpenGov pallets), upgrades (forkless `setCode`), interop (XCM), p2p, node-software, consensus (relay chain for parachains; Aura/BABE + GRANDPA for solo, unverified)
- Extend: tokenomics (balances/assets pallets, inflation config), smart-contracts (pallet-revive on your chain, or Polkadot Hub), data-availability (relay chain for parachains)
- Custom: randomness (beyond the BABE/relay VRF), verifiable-participation
- n/a: rollup (parachains are validated by the relay chain, not rollups in the Ethereum sense)

## Setup
Rust toolchain plus `wasm32-unknown-unknown`. The tutorial pins Rust 1.88, but match what your template's `rust-toolchain` file says.
```bash
git clone https://github.com/paritytech/polkadot-sdk-parachain-template.git parachain-template
cd parachain-template && cargo build --release --locked
chain-spec-builder create -t development --relay-chain paseo --para-id 1000 \
  --runtime ./target/release/wbuild/parachain-template-runtime/parachain_template_runtime.compact.compressed.wasm \
  named-preset development
polkadot-omni-node --chain ./chain_spec.json --dev          # ws://localhost:9944, state purged on exit
```
- Install `polkadot-omni-node` and `chain-spec-builder` at the versions of the **current stable release**. The official tutorial still pins older ones (stable2512 / omni-node 0.13.2), so don't copy those.
- **Pop CLI** (`cargo binstall pop-cli --locked`, `brew install r0gue-io/pop-cli/pop`) wraps templates, zombienet-sdk local networks and srtool deterministic builds. ink! support is opt-in (`--features contract`).

## Implement
- **Pallets**: one per spec component (`#[pallet::call]` for operations, `on_initialize`/`on_finalize`/`on_idle` hooks for per-block logic, storage items for state, `Config` constants and on-chain params for `P-*`). Map invariants to `try-runtime` checks and unit tests.
- **Weights**: every extrinsic needs benchmarked weights (`frame-omni-bencher`). Unbenchmarked or under-weighted calls are DoS vectors.
- **Parachain path**: reserve a para ID, register it, run collators, and obtain **coretime**:
  - *on-demand*: `onDemand.placeOrderAllowDeath` / `placeOrderKeepAlive`, one block per order;
  - *bulk*: `broker.purchase` then `broker.assign` on the Coretime chain. A region lasts up to 28 days and needs renewal (assign with `Final` if you'll renew).
- **Contracts**: on Polkadot Hub, `pallet-revive` gives REVM (unmodified EVM; Hardhat, Foundry, Remix, viem) and PolkaVM (Solidity via `resolc`, or Rust). You can also add pallet-revive to your own runtime.

## Test
- Unit and integration tests per pallet. Benchmarks in CI. `try-runtime` against live state before every upgrade (unverified CLI version).
- Local multi-node and relay networks with zombienet-sdk (via Pop CLI). Fork live chains with chopsticks for upgrade rehearsal.
- Determinism: deterministic runtime builds (srtool) so every collator and validator runs identical Wasm.

## Production
- Runtime upgrades: bump `spec_version` (forgetting it makes the upgrade a no-op), build the compressed Wasm, then **governance referendum** (not sudo) → `system.setCode`. Verify `system.lastRuntimeUpgrade()` and the `ValidationFunctionApplied` event.
- Remove `sudo` before mainnet, or restrict it with a sunset plan (`protocol-governance`).
- Parachain: secure coretime renewal (calendar plus funded account), collator set redundancy, monitoring of block production per core.
- Solo chain: validator set, session keys, and the GRANDPA/BABE operations in `protocol-staking-validators` / `quality-security`.
- Plus the `quality-*` skills and `ops-*`.

## Known pitfalls
- Release naming is `polkadot-stable<YYMM>[-patch]`. Pin a stable tag, never `master`. Tutorials lag releases.
- Weights must reflect worst-case execution. The runtime can't charge more than it declared.
- Storage migrations run in `on_runtime_upgrade` within block weight limits. Large migrations need multi-block migration patterns.
- Coretime is a recurring cost. A missed renewal stops block production.
- XCM configuration errors can drain sovereign accounts. Restrict barriers and trusted origins.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Read the latest `polkadot-stable*` release notes (breaking changes per crate), developers.polkadot.com changes, and the Pop CLI README, then update "Versions verified" and resolve the Unverified list.
