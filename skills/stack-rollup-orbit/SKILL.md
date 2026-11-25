---
name: stack-rollup-orbit
description: Build, deploy and operate an Arbitrum chain (formerly "Orbit") on the Nitro stack — Rollup vs AnyTrust (DAC), the Arbitrum chain SDK (@arbitrum/chain-sdk) with RollupCreator and TokenBridgeCreator, node configuration, batch poster and blob posting, validators and BoLD dispute protocol, challenge period, custom gas token, fee parameters and AEP licensing/fee router, ArbOS upgrades, Stylus (Rust/C/C++ WASM contracts), fast withdrawals and Timeboost. Use whenever the user works with Arbitrum chains, Orbit, Nitro, L3s on Arbitrum One, AnyTrust, BoLD, Stylus chains, or chose Arbitrum in design-stack-selection.
license: MIT
---

# Arbitrum chain (Orbit) adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It turns the rollup design from `protocol-rollup` into an Arbitrum chain on Nitro. Contracts (Solidity, or Stylus in Rust/C/C++) follow `build-smart-contracts`.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives on an Arbitrum chain |
| `references/deploy-and-operate.md` | Deploying with the chain SDK, node roles, validation, upgrades |

## Adapter metadata
- Family: rollup
- Stack: Arbitrum chains (Nitro stack, by Offchain Labs)
- Versions verified: Nitro v3.12.4, `@arbitrum/chain-sdk` v0.28.0 (repo `OffchainLabs/arbitrum-chain-sdk`, which replaces the old orbit-sdk name)
- Verified on: 2026-11-25
- Sources: github.com/OffchainLabs/nitro/releases; github.com/OffchainLabs/arbitrum-chain-sdk (README, releases); docs.arbitrum.io (launch-arbitrum-chain: sdk-introduction, chain-config/validation/bold, chain-config/validation/challenge-period, chain-config/costs/aep-overview; llms.txt index); arbitrum.foundation/orbit
- Unverified parts: current Timeboost status (a Jun 2026 report says per-tx priority auctions replaced it), the exact ArbOS version your Nitro release defaults to, and whether L2-on-Ethereum launches still need a DAO proposal (stated on arbitrum.foundation/orbit). Confirm them.

## When to use this adapter
An EVM rollup, or an L3 on Arbitrum One/Nova, with optimistic fraud proofs (BoLD), a cheaper AnyTrust option, a custom gas token, and Stylus (WASM) contracts next to the EVM. Check the licence: Nitro is under a Business Source License. Chains settling to a parent other than Arbitrum One or Nova fall under the **Arbitrum Expansion Program (AEP)** and pay 10% of protocol net revenue.

## Placement map
Summary of `references/placement-map.md`:
- Native: rollup (RollupCreator contracts, BoLD), state-execution (EVM + Stylus WASM), data-availability (parent chain / blobs, or AnyTrust DAC), interop (token bridge, retryables), node-software, upgrades (ArbOS + contract upgrades), smart-contracts
- Extend: consensus (sequencer, Timeboost/priority ordering), governance (chain owner / UpgradeExecutor, Security Council), tokenomics (fee parameters, custom gas token, AEP fee router)
- Custom: staking-validators, randomness, verifiable-participation
- n/a: p2p (sequencer feed, see map)

## Setup
1. **Choose the type**: **Rollup** (data on the parent chain, highest security) or **AnyTrust** (data with a Data Availability Committee, cheaper, adds a trust assumption on the DAC).
2. **Testnet L3 first** on Arbitrum Sepolia, using the docs quickstart ("Run an L3 rollup from scratch").
3. **Deploy with the chain SDK** (recommended for deployment and chain-owner actions):
```bash
pnpm add @arbitrum/chain-sdk viem@^1.20.0      # library
npm i -g @arbitrum/chain-sdk                   # CLI: arbitrum-chain-sdk <command> '<json>'
```
   Order matters: **RollupCreator** first (Rollup, SequencerInbox, Inbox, Outbox, Bridge), then **TokenBridgeCreator**. It needs the inbox, sends retryables, and needs gas on the child chain (with a custom gas token, approve TokenBridgeCreator first). For genesis allocations, generate a custom genesis before deploying. Genesis generation runs from the SDK's Docker image only (no `generateGenesis` function in the npm package).
4. **Configure and run nodes** (docs "Configure your Arbitrum chain's node"): sequencer, batch poster (enable EIP-4844 blobs for Ethereum-settled chains), validator(s), and full/archive nodes for RPC.

Most production chains use a Rollup-as-a-Service provider, as the docs recommend.

## Implement
- **Solidity contracts**: standard EVM via `build-smart-contracts`.
- **Stylus contracts** (Rust/C/C++ compiled to WASM): `cargo stylus check|deploy|verify`. Contracts need **activation**, and caching (CacheManager) affects cost. OpenZeppelin Contracts for Stylus exists.
- **Chain-level customization**: ArbOS precompiles and parameters through the chain owner (ArbOwner), plus fee parameters, gas target and dynamic pricing. Deep protocol changes require forking Nitro and the fraud-proof (WAVM) replay binary, which is a heavy maintenance burden.
- **Fast withdrawals**: an optional configuration on top of the challenge period (docs guide).

## Test
- Local or devnet chain, then Arbitrum Sepolia L3. Test deposits (retryables), withdrawals through the outbox after the challenge period (shorten it only on test networks), and token bridge flows.
- BoLD: run a validator against an invalid assertion on a devnet before trusting withdrawals.
- Stylus: unit tests with the Stylus SDK test tooling plus integration tests on a devnet.

## Production
Read `references/deploy-and-operate.md`. It covers validator setup and bonds, BoLD (recommended, but **keep validation permissioned**, per the docs), challenge-period choice, batch poster fee tuning, keys, ArbOS upgrade process, the AEP fee router if applicable, and Stages targets from `protocol-rollup`.

## Known pitfalls
- **Licensing**: Nitro is BSL. Settling outside Arbitrum One/Nova means AEP terms (10% of protocol net revenue to the Arbitrum Foundation via the AEP fee router). Decide this early.
- The token bridge can't be deployed before or in parallel with the rollup contracts.
- Default challenge period is about **one week** (`confirmPeriodBlocks` ≈ 45,818 L1 blocks) plus an extra 200-block buffer. BoLD adds up to one more challenge period in the worst case. Plan withdrawal UX (fast withdrawals, liquidity providers).
- AnyTrust security depends on DAC honesty (choose N and H deliberately). Say so in the trust model.
- Permissionless BoLD validation carries extra risk: the docs recommend BoLD with **permissioned** validation for most chains.
- ArbOS upgrades are chain-owner actions with node version requirements. Coordinate node upgrades before activation.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Diff Nitro and chain-SDK releases and the docs.arbitrum.io "launch-arbitrum-chain" pages (ArbOS versions, BoLD, AEP, Timeboost), then update "Versions verified" and record breaking changes in README.
