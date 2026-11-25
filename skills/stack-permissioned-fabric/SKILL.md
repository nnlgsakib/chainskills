---
name: stack-permissioned-fabric
description: Build and operate a permissioned enterprise blockchain with Hyperledger Fabric v3 — organizations, MSPs and Fabric CA identities, channels, the SmartBFT (BFT) or Raft ordering service, chaincode in Go/Java/Node with the lifecycle (package, install, approveformyorg, commit, sequence-based upgrades), endorsement policies, private data collections, the Fabric Gateway client API (legacy SDKs unmaintained), the test network, capability upgrades, and production hardening. Use whenever the user works with Hyperledger Fabric, chaincode, channels, orderers, MSPs, endorsement policies, consortium/enterprise ledgers, or chose a permissioned non-token chain in design-stack-selection.
license: MIT
---

# Hyperledger Fabric adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). Fabric is a permissioned ledger without a native token. Its trust model is known organizations with PKI identities, so many `protocol-*` topics (staking, tokenomics, public governance) don't apply or move off-chain into consortium agreements.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |

## Adapter metadata
- Family: permissioned
- Stack: Hyperledger Fabric (LF Decentralized Trust, Graduated project)
- Versions verified: Fabric v3.1.5 (18 Jun 2026, Latest; Go 1.26.4, CouchDB 3.4.2), LTS v2.5.16; v3.0 added the SmartBFT ordering service and Ed25519 MSP signing (channel capability `V3_0`); v3.1 added chaincode read/write batching
- Verified on: 2026-11-25
- Sources: github.com/hyperledger/fabric/releases; hyperledger-fabric.readthedocs.io/en/latest (whatsnew, status, getting_started, install, test_network, deploy_chaincode, bft_configuration, upgrade)
- Unverified parts: whether `install-fabric.sh -f 3.1.5` resolves v3 images (the script defaults to 2.5.16 / CA 1.5.17), the explicit n = 3f+1 statement for BFT consenters (the docs give "less than a third" and a 4-orderer example), endorsement-policy and private-data guide details, Fabric Gateway language support, and Fabric-X / next-gen status.

## When to use this adapter
Consortium or enterprise ledgers among known organizations: supply chain, trade, records. You get fine-grained endorsement, private data and no gas token. Pick a public chain or rollup instead when you need permissionless users, a native token, or public verifiability.

## Placement map
Summary of `references/placement-map.md`:
- Native: consensus (SmartBFT or Raft ordering), state-execution (chaincode + endorse/order/validate), governance (channel config and lifecycle policies), node-software, upgrades (lifecycle sequence, capabilities), p2p (gossip, with block gossip deprecated)
- Extend: smart-contracts (chaincode), interop (Fabric Gateway, external bridges), data-availability (private data collections)
- Custom: randomness, verifiable-participation
- n/a: staking-validators, tokenomics, rollup

## Setup
```bash
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh && chmod +x install-fabric.sh
./install-fabric.sh --fabric-version 3.1.5 docker binary samples      # default is 2.5.16, so pin v3 explicitly (verify)
cd fabric-samples/test-network
./network.sh up createChannel -ca                     # Raft single orderer + Fabric CAs
./network.sh up -bft && ./network.sh createChannel -bft   # 4 BFT orderers + 2 peers
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-go -ccl go
```
The test network is for learning only, **not a production template**.

## Implement
- **Chaincode** (Go/Java/Node/TypeScript): spec operations map to transaction functions, state to world-state keys (composite keys for indexes), and invariants to checks inside chaincode plus endorsement policies. Use v3.1 batching (`GetMultipleStates`, `StartWriteBatch`/`FinishWriteBatch`) for bulk operations.
- **Lifecycle**: `peer lifecycle chaincode package|install|queryinstalled|approveformyorg|checkcommitreadiness|commit|querycommitted`. Approval is per organization and needs an **admin** identity. The default endorsement policy is a majority of channel members. To upgrade: install the new package, approve with a new version and `--sequence` + 1, then commit.
- **Endorsement policies** per chaincode or collection. **Private data collections** for data shared by a subset of organizations.
- **Clients**: the Fabric Gateway client API. The legacy SDKs are unmaintained and incompatible with v3 features such as SmartBFT.

## Test
- Chaincode unit tests (mock stubs) plus integration on the test network, including BFT mode.
- Endorsement policy tests: transactions fail without the required endorsements. Private data visible only to members.
- Upgrade rehearsal: a new sequence on a copy of the network, plus a capability update.

## Production
- Real CAs (per-organization CA and TLS CA), no `cryptogen`. Planned identity lifecycle (enrollment, revocation, rotation).
- **BFT ordering**: tolerates fewer than one third of orderers being malicious, so plan consenter counts to match (the test network uses 4). Reconfigure consenters only when all are healthy, in a maintenance window. Tune batch and timeout parameters (`RequestBatchMaxCount`, `RequestPoolSize` ≥ 2× batch count, `LeaderHeartbeatTimeout`, `ViewChangeTimeout`). BFT orderers can rotate enrollment certificates without a config update if the keys stay the same (v3.1.2).
- Monitoring: `cluster_size`, `committed_block_number`, `is_leader`, `leader_id`.
- Disable deprecated block gossip (`peer.gossip.orgLeader: true`, `useLeaderElection: false`, `state.enabled: false`, `deliveryclient.blockGossipEnabled: false`).
- Upgrades: back up ledgers and MSPs, then roll orderers, then peers, then update channel capabilities.

## Known pitfalls
- System channel, Solo, Kafka, legacy lifecycle and the old SDKs are deprecated or removed. Don't follow old tutorials.
- Forgetting to increment `--sequence` on upgrade, or approving without an admin identity.
- Non-deterministic chaincode (timestamps, randomness, map iteration) gives endorsement mismatches.
- The install script defaults to the v2.5 LTS. Pin v3 explicitly if you need SmartBFT.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Check Fabric releases and the readthedocs "whatsnew" and upgrade pages, Fabric Gateway docs, and Fabric-X status, and resolve the Unverified list.
