---
name: stack-rollup-op
description: Build, deploy and operate an OP Stack L2/L3 rollup — op-deployer intents and L1 contract deployment (op-contracts), genesis/rollup.json, op-node + op-reth sequencers (op-geth is end-of-support), op-batcher, op-proposer, op-challenger and op-dispute-mon, fault proofs (Kona/Cannon, permissioned → permissionless, ZK dispute games via OP Succinct), op-conductor high-availability sequencing, custom gas token, Alt-DA, predeploys, Superchain Registry and interop (op-supernode), upgrades and hardforks. Use whenever the user works with OP Stack, Optimism, Superchain, Base-style L2s, op-node/op-reth/op-deployer/op-batcher, Agglayer CDK OP Stack config, or chose OP Stack in design-stack-selection.
license: MIT
---

# OP Stack adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It turns the stack-neutral rollup design from `protocol-rollup` and the component specs into an OP Stack chain. Contracts follow `build-smart-contracts`. The production gate is `quality-*` plus this adapter's Production section.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives on OP Stack |
| `references/components.md` | Running or configuring any OP Stack service; versions and roles |
| `references/production.md` | Taking a chain from testnet to mainnet |

## Adapter metadata
- Family: rollup
- Stack: OP Stack (optimistic rollup framework by OP Labs / Optimism Collective)
- Versions verified: op-deployer v0.9.0, op-contracts v9.0.0, op-node v1.20.2, op-reth v2.9.0, op-batcher v1.18.1, op-proposer v1.17.1, op-challenger v1.12.0, op-dispute-mon v1.6.6, op-conductor v0.9.6, op-supernode v1.1.2, kona-node v1.11.0, kona-client v1.9.0 (all from the ethereum-optimism/optimism monorepo releases)
- Verified on: 2026-11-25
- Sources: github.com/ethereum-optimism/optimism/releases; docs.optimism.io (create-l2-rollup tutorial: op-deployer-setup, op-reth-setup; launch-a-chain-with-fault-proofs-and-ha-sequencing; chain-operator best practices; llms.txt index); docs.optimism.io/notices/upgrade-20
- Unverified parts: exact Karst activation timing for your chain, op-supernode production readiness for non-interop chains, and current Stages status of individual chains. Check the notices and the Superchain Registry.

## When to use this adapter
An EVM rollup settling to Ethereum (or another EVM L1), optimistic with fault proofs or ZK dispute games, with an EVM-equivalent developer experience, Superchain interop, an MIT licence, and a large operator ecosystem. Not a fit when you need your own validator set as a product feature (use an L1 adapter) or non-EVM execution.

## Placement map
Summary of `references/placement-map.md`:
- Native: rollup, state-execution (EVM via op-reth), data-availability (Ethereum blobs, Alt-DA), interop (standard bridge, Superchain interop), upgrades (op-deployer + OPCM), node-software, smart-contracts
- Extend: consensus (sequencer + op-conductor HA), governance (L1 ProxyAdmin / Security Council multisigs), tokenomics (fee vaults, custom gas token)
- Custom: staking-validators (sequencer set or app-level staking as contracts), randomness, verifiable-participation
- n/a: p2p beyond the built-in op-node gossip (see map)

## Setup
1. **Testnet first.** Follow the official create-l2-rollup tutorial on Sepolia: op-deployer → sequencer (op-node + op-reth) → batcher → proposer → challenger. A complete example lives in the optimism monorepo (`create-l2-rollup-example/`).
2. **Deploy L1 contracts with op-deployer**:
```bash
op-deployer init --l1-chain-id 11155111 --l2-chain-ids <L2_CHAIN_ID> --workdir .deployer --intent-type standard-overrides
# edit .deployer/intent.toml (roles, fee recipients, overrides)
op-deployer apply --workdir .deployer --l1-rpc-url <L1_RPC> --private-key <DEPLOYER_KEY>
op-deployer inspect genesis --workdir .deployer <L2_CHAIN_ID> > .deployer/genesis.json
op-deployer inspect rollup  --workdir .deployer <L2_CHAIN_ID> > .deployer/rollup.json
```
   Intent types: `standard` (defaults), `standard-overrides` (recommended: defaults plus selected overrides), `custom` (everything manual).
3. **Sequencer**: op-reth (`--chain=genesis.json`, no separate init step; archive by default) and op-node (`--l2=http://op-reth:8551 --l2.jwt-secret … --l2.enginekind=reth --rollup.config=rollup.json`). Tune the op-reth builder for 2 s blocks (`--builder.deadline=2 --builder.interval=100ms`).
4. **L1-facing services**: op-batcher (blobs), op-proposer, op-challenger (with the kona-client absolute prestate), and op-dispute-mon.

Run `op-deployer --help` and each service's `--help` against your pinned versions. Flags change between releases.

## Implement
- **App and protocol logic** goes in L2 contracts via `build-smart-contracts`, at a target EVM fork matching the chain's hardfork.
- **Protocol-level changes** (new precompiles, a custom state transition) need a fork of op-reth and of the proof program (kona). A change in execution must be provable, or the fault proofs break. Avoid this unless the design demands it, and budget for maintaining the fork through every OP Stack hardfork.
- **Custom gas token**: deploy via op-deployer's custom gas token flow (docs guide). Decide it before genesis.
- **Alt-DA**: Alt-DA mode with a DA server. This reduces exit guarantees, so state that in the trust model (`protocol-rollup`).
- **Interop / Superchain**: follow the Superchain interop guides. op-supernode runs every chain of an interop dependency set in one process.

## Test
- Local devnet via the tutorial's Docker Compose example or Kurtosis (`optimism-package`, unverified name, so check it). Run end-to-end deposit, withdrawal (prove + finalize) and fault-proof game tests.
- Fault proofs: run op-challenger against deliberately invalid proposals on a devnet, and confirm the game resolves correctly before trusting withdrawals.
- Contract tests with Foundry against an L2 fork. Fork-test bridging flows against Sepolia deployments.
- Sequencer HA: failover drills with op-conductor (kill the leader, then check block production continues without reorgs).

## Production
Follow `references/production.md`. It covers op-conductor HA sequencing (3 sequencers in separate failure domains, private network), fault proofs from day one, the key-management posture for batcher, proposer and challenger, op-dispute-mon alerting, a staggered upgrade rollout, keeping deployment artifacts (needed for the Superchain Registry), Stages targets, and `protocol-rollup/references/stages.md`.

## Known pitfalls
- **op-geth is end-of-support (2026-05-31)** and doesn't support the active Karst hardfork. op-geth nodes can't follow the canonical chain. Use op-reth.
- `op-node` must be told the engine kind (`--l2.enginekind=reth`) when driving op-reth.
- op-conductor's RPC has **no authentication**. Never expose it publicly.
- Fault-proof components need the matching **absolute prestate** for your chain config and upgrade. A wrong prestate means invalid games go uncontested.
- Production tags are per component (`op-node/vX`, `op-contracts/vX`). Monorepo `vX` tags don't include contract changes. Pin each component explicitly.
- A custom gas token, Alt-DA and the L2 chain ID are effectively permanent. Decide them before genesis.
- Upgrades follow hardfork notices with deadlines. Missing one stalls your nodes, so subscribe to the notices.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Diff the monorepo release notes per component, re-read docs.optimism.io notices (hardforks and end-of-support dates), update "Versions verified", and record breaking changes in README.
