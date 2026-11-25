---
name: stack-rollup-zk
description: Build and operate a ZK rollup or validium, primarily with ZK Stack (ZKsync) — ZKsync OS server (sequencer), zkstack CLI (ecosystem/chain create and init, contracts, server, prover, explorer, portal), shared Bridgehub/CTM contracts and chain ownership, Airbender RISC-V prover and proof wrapping, rollup vs validium DA, custom base tokens, Gateway settlement, Prividium private chains — with pointers for other validity-proof stacks (OP Succinct ZK proofs on OP Stack, Agglayer CDK, based/ZK rollups). Use whenever the user works with ZK Stack, ZKsync chains, zkstack, ZKsync OS, Airbender, Elastic Network, Prividium, validity-proof rollups or validiums, or chose a ZK rollup in design-stack-selection.
license: MIT
---

# ZK rollup adapter (ZK Stack first)

Stack adapter in the chainskills suite (router: `blockchain-dev`). It turns the rollup design from `protocol-rollup` into a validity-proof chain. The main path is **ZK Stack**. For ZK proofs on an OP Stack chain (OP Succinct / Agglayer CDK OP config), use `stack-rollup-op` plus the notes here.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives on ZK Stack |
| `references/zkstack.md` | Commands, components, ownership, Gateway, Prividium |

## Adapter metadata
- Family: rollup
- Stack: ZK Stack (Matter Labs / ZKsync). Other ZK stacks are covered only as pointers.
- Versions verified: zksync-os-server v0.23.0 (ZKsync OS sequencer), era-contracts v0.31.x (L1/L2 contracts; `v31-mainnet` tag), zksync-era core-v31.5.0 (legacy server, and home of `zkstack_cli`), airbender_prover_server v0.1.1. Local quickstarts use protocol versions v30.2 and v31.0.
- Verified on: 2026-11-25
- Sources: github.com/matter-labs/zksync-os-server (README, releases); matter-labs.github.io/zksync-os-server/latest/setup (local run, docker, multi-node consensus); github.com/matter-labs/zksync-era/tree/main/zkstack_cli (README); docs.zksync.io/zk-stack (quickstart, components/zksync-os, components/server, components/zksync-airbender, zk-chains, license, running/ownership-model, prividium/overview); github.com/matter-labs/era-contracts/releases
- Unverified parts: zkstack flags for prover mode, base token and validium DA (not shown in the pages read, so check `zkstack <cmd> --help`); Gateway availability on public networks (the README note may be stale); Airbender production status; whether registering a chain in the shared Bridgehub needs ecosystem governance approval (the ownership model suggests it does).

## When to use this adapter
EVM-compatible chains that want **validity proofs** (no week-long challenge window), a rollup or validium DA choice, a custom base token, native account abstraction, an optional private (Prividium) deployment, and the MIT/Apache-2.0 licence. The trade-off is prover infrastructure and cost.

## Placement map
Summary of `references/placement-map.md`:
- Native: rollup (validity proofs, Bridgehub/CTM), state-execution (ZKsync OS; EVM; EraVM supported as an execution environment), data-availability (rollup or validium), interop (shared bridge, Gateway), node-software, upgrades (protocol upgrades via governance), smart-contracts
- Extend: consensus (sequencer; multi-node consensus setups), governance (ChainAdmin multisig), tokenomics (base token, fee params, base-token multiplier)
- Custom: staking-validators, randomness, verifiable-participation
- n/a: p2p (see map)

## Setup
1. **Local first (ZKsync OS)**: the quickstart launches a chain with the ZKsync OS server, an in-memory L1 (anvil) and fake proofs:
```bash
./run_local.sh ./local-chains/v31.0/default     # in a zksync-os-server checkout; RPC on :3050
cast send --private-key <rich-key> --rpc-url http://localhost:3050 <to> --value 100
```
   The run script is "a temporary solution. Do not depend on it in production". Use the Docker and multi-node setups from the server docs for anything beyond local work.
2. **Ecosystem and chains with zkstack**:
```bash
curl -L https://raw.githubusercontent.com/matter-labs/zksync-era/main/zkstack_cli/zkstackup/install | bash && zkstackup
zkstack ecosystem create && cd <ecosystem>
zkstack containers                                  # local L1 + Postgres
zkstack ecosystem init --dev                        # add --zksync-os (with --no-genesis) for ZKsync OS contracts
zkstack chain create && zkstack chain init          # additional chains, registered in the ecosystem's Bridgehub
zkstack server --chain <name>                       # legacy server path
zkstack explorer init ; zkstack portal
```
   Production L1 deployment: `zkstack ecosystem init-core-contracts --l1-rpc-url …`, and for a new chain type manager `init-new-ctm` and `register-ctm` (needs a Bridgehub address). The README notes you **can't yet register a new chain into an existing ecosystem** with the CLI.
3. **Prover**: Airbender (RISC-V, GPU) produces proofs, wrapped into an FFLONK SNARK verified on L1. Legacy prover commands are `zkstack prover init` and `zkstack prover run --component <gateway|witness-generator|witness-vector-generator|prover|compressor>`.

## Implement
- **Contracts**: Solidity via `build-smart-contracts`. Check EVM-equivalence details for your execution environment (ZKsync OS EVM vs EraVM) and use native account abstraction where it helps.
- **Chain parameters** via ChainAdmin (chain operator multisig): fee parameters, validator (committer) address, transaction filterer, base-token multiplier.
- **Validium**: off-chain DA with a DA validator pair (`zkstack chain set-da-validator-pair-calldata`). State the weaker exit guarantee in the trust model.
- **Private chain (Prividium)**: validium with a proxy RPC (Okta SSO / SIWE) and an admin dashboard. **Separately licensed**: production needs a commercial agreement.
- **Gateway**: a ZK chain acting as settlement layer for other chains (`zkstack chain gateway convert-to-gateway | migrate-to-gateway …`). Chains settle to Ethereum by default.

## Test
- Local ZKsync OS server with fake proofs for app and integration tests. Then enable real proving (`prover_api_fake_provers_enabled=false`) on a staging deployment, and measure proof latency and cost per batch.
- Deposit/withdraw tests through the shared bridge. Finalisation needs a verified proof on L1.
- Upgrade rehearsal: protocol version upgrades on a staging ecosystem.

## Production
Read `references/zkstack.md` → Production. It covers prover capacity and redundancy, sequencer HA (multi-node consensus), ChainAdmin multisig, keys for the committer/operator, DA choice and exit guarantees, the governance and upgrade path, explorer and portal, and Stages targets (`protocol-rollup`).

## Known pitfalls
- Two server lines exist: **ZKsync OS server** (new) and the legacy **zksync-era** server. Pick one deliberately. Docs and CLI flags differ (`--zksync-os`).
- Fake proofs are the default locally. Never ship a config that still uses fake provers.
- The ZK Stack contracts share a Bridgehub/CTM under ecosystem governance (ProtocolUpgradeHandler → DecentralizedGovernance). Your chain's upgrades follow that ecosystem's protocol upgrades.
- Validium and Prividium aren't rollups for exit-guarantee purposes. Label them correctly.
- Prover hardware and cost dominate operating expenses. Benchmark Airbender on your target batch sizes before committing.

## Other ZK stacks (pointers, verify before use)
- **OP Succinct / ZK dispute games on OP Stack**: `stack-rollup-op` (docs: "Migrating to ZK proofs", "Configure op-challenger for ZK dispute games").
- **Agglayer CDK**: OP Stack config (cdk-opgeth, op-geth/op-reth) with SP1 proofs and Agglayer, or CDK Erigon. For the OP config, use `stack-rollup-op` plus the Agglayer docs.
- **Others** (Scroll, Taiko-style based rollups, Linea, Starknet appchains): no adapter yet. Create one with `build-stack-adapter`.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Re-read the zksync-os-server releases and docs, the zkstack_cli README and CHANGELOG, era-contracts releases (protocol versions), and the docs.zksync.io ZK Stack pages. Update "Versions verified" and resolve the Unverified list.
