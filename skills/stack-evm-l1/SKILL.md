---
name: stack-evm-l1
description: Build and operate your own EVM Layer-1 chain — choosing between a permissioned/PoA BFT network (Hyperledger Besu QBFT with block-header or contract-based validator management), an Ethereum-style PoS network with its own beacon chain (execution client geth/reth/Besu/Nethermind + consensus client Lighthouse/Prysm/Teku/Lodestar/Nimbus, genesis generation), a custom node built with the reth SDK (custom EVM, precompiles, RPC, consensus), a BSC-style PoSA geth fork with system contracts, or an Avalanche L1 — plus genesis, validators, hardfork tracking, testing with Kurtosis, and production operations. Use whenever the user wants an EVM L1, a private/consortium EVM network, QBFT/IBFT, a geth or reth fork, their own beacon chain, system contracts for validator sets, or chose an EVM L1 in design-stack-selection.
license: MIT
---

# EVM L1 adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It maps stack-neutral designs (consensus, staking, execution) onto a sovereign EVM chain. Contracts follow `build-smart-contracts`. For EVM inside a Cosmos chain use `stack-cosmos-evm`, and for EVM rollups use `stack-rollup-*`.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |
| `references/paths.md` | Details per route: Besu QBFT, PoS beacon chain, reth SDK, PoSA fork, Avalanche L1 |
| `references/production.md` | Before any public network |

## Adapter metadata
- Family: evm
- Stack: sovereign EVM L1s built from Ethereum client software
- Versions verified: go-ethereum v1.17.10, reth v2.11.0, Hyperledger Besu 26.11.2 (repo and docs now under `besu-eth`), Lighthouse v8.3.3, ethpandaops/ethereum-package 6.1.0, BSC client `v1.5.x` line
- Verified on: 2026-11-25
- Sources: github.com/ethereum/go-ethereum/releases; geth.ethereum.org/docs (fundamentals/private-network, developers/dapp-developer/dev-mode); github.com/paradigmxyz/reth/releases; reth.rs/sdk; github.com/besu-eth/besu/releases; docs.besu-eth.org/private-networks/how-to/configure/consensus/qbft (updated 16 Nov 2026); github.com/sigp/lighthouse/releases; github.com/ethpandaops/ethereum-package (README); github.com/bnb-chain/bsc (README); build.avax.network/docs/quick-start/validator-manager
- Unverified parts: reth SDK custom-precompile and custom-consensus API details (sub-pages not read); BSC system-contract addresses and functions; Gnosis Chain's exact architecture; Avalanche L1 tooling versions (only ACP-77/99 checked). Create `stack-avalanche-l1` via `build-stack-adapter` for full Avalanche coverage.

## When to use this adapter
Your own EVM chain with your own validator set: a consortium or enterprise network, an app-specific L1, or a PoS L1 that keeps the Ethereum client ecosystem (wallets, tooling, Solidity). If you don't need your own validator set, a rollup is cheaper (`protocol-rollup`).

## Placement map
Summary of `references/placement-map.md`:
- Native: state-execution (EVM), smart-contracts, node-software, p2p (devp2p/libp2p), upgrades (hardfork scheduling in genesis)
- Extend: consensus (QBFT / Ethereum PoS / Parlia-style), staking-validators (QBFT validator contract, beacon deposit contract, PoSA system contracts, Avalanche ValidatorManager), governance (contracts), tokenomics (block rewards / issuance config, fee recipient)
- Custom: randomness (beyond RANDAO), verifiable-participation, interop (bridges)
- n/a: rollup, data-availability (all nodes keep full data, except an L1 with its own DA design)

## Setup

Choose a route (details in `references/paths.md`):

| Route | Consensus | Validator set | Finality | Effort | Fits |
|---|---|---|---|---|---|
| **A. Besu QBFT** | QBFT (BFT) | block-header votes or validator contract | immediate (BFT) | low | permissioned / consortium / enterprise |
| **B. Ethereum-style PoS** | Gasper (own beacon chain) | beacon deposit contract | ~2 epochs | high (two client layers) | open PoS L1 with Ethereum semantics |
| **C. reth SDK custom node** | your choice (custom consensus possible) | your design | your design | high (Rust engineering) | novel execution or consensus needs |
| **D. PoSA geth fork (BSC-style)** | Parlia-like PoSA | system contracts (staking, slashing) | fast, checkpoint-based | high (fork maintenance) | staking-based validator elections with EVM tooling |
| **E. Avalanche L1** | Snowman | ACP-99 ValidatorManager contracts (PoA/PoS) | ~1–2 s | medium | EVM L1 inside the Avalanche network (ICM interop) |

Local devnets: **Kurtosis ethereum-package** for route B (multi-client; *not intended for production*), `besu` with a QBFT genesis for route A, and `geth --dev` for single-node dApp work (simulated PoS, blocks on demand).

## Implement
- Contracts via `build-smart-contracts`. Set `evm_version` to your chain's active fork.
- Validator-set logic: route A validator contract, route D system contracts, route E ValidatorManager, all to consensus-code standards (`build-smart-contracts/references/validator-set-contracts.md`).
- Protocol changes (precompiles, gas schedule, consensus): route C (reth SDK) or a client fork. Budget for tracking upstream hardforks.

## Test
- Multi-node devnet with the real client mix (Kurtosis for B; docker-compose for A/D). Run the chaos suite from `quality-testing` (more than 1/3 offline, partitions, restarts).
- Hardfork activation tests: schedule forks at low heights in a devnet genesis.
- Validator-set changes under load (votes or contract calls) with rotation at epoch boundaries.

## Production
Follow `references/production.md` plus the `quality-*` skills.

## Known pitfalls
- **Clique is gone in geth.** Since v1.14 it isn't an option. geth private networks need PoS with a consensus client. Use Besu QBFT for PoA/BFT.
- QBFT needs **≥ 4 validators** to tolerate one fault, and halts if more than 1/3 are lost. With the contract method, the JSON-RPC vote methods don't work.
- `ethereum-package` is for testing, **not production**.
- An Ethereum-style PoS L1 means running and securing a beacon chain, deposit contract and validator clients. That's the heaviest route, and its security depends on your token's staked value.
- Forked clients (route D, custom geth) drift from upstream. Every Ethereum hardfork and security patch becomes merge work.
- The EIP-7825 per-tx gas cap (2^24) applies by default in recent Besu QBFT genesis unless overridden (`pertxgaslimit`). Decide it explicitly.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Diff geth, reth, Besu and consensus-client releases (hardfork names and dates), re-read the Besu QBFT docs and reth SDK pages, and update "Versions verified".
