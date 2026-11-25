# Placement map — Hyperledger Fabric

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | ordering service: SmartBFT (v3, BFT) or Raft (CFT) | BFT: fewer than 1/3 malicious orderers |
| state-execution | native | chaincode endorsement (simulate) → ordering → validation and commit; world state (LevelDB/CouchDB) | Deterministic chaincode required |
| staking-validators | n/a | — | Permissioned identities, no stake |
| rollup | n/a | — | — |
| tokenomics | n/a | — | No native token. Token logic would be chaincode |
| governance | native | channel configuration policies, lifecycle endorsement policy, capabilities | Consortium agreements off-chain |
| randomness | custom | external sources; never inside endorsement (non-deterministic) | — |
| verifiable-participation | custom | chaincode + off-chain services | — |
| data-availability | extend | private data collections (subset of organizations); ledgers on all channel peers | — |
| p2p | native | gossip among peers (block gossip deprecated; use deliver service) | — |
| interop | extend | Fabric Gateway clients; cross-network bridges are custom | — |
| smart-contracts | extend | chaincode (Go/Java/Node/TypeScript) | Lifecycle with sequence-based upgrades |
| node-software | native | peers, orderers, Fabric CA, `peer`/`osnadmin`/`configtxgen` binaries | Real CAs in production |
| upgrades | native | rolling binary upgrades → channel capability updates; chaincode `--sequence` + 1 | Back up ledgers and MSPs first |
