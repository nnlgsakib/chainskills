# Placement map — ZK Stack

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | extend | sequencer (ZKsync OS server); multi-node consensus setup documented for the server | Safety from validity proofs on L1. Liveness from the sequencer. Check forced-inclusion support for your version |
| state-execution | native | ZKsync OS (RISC-V-proven OS hosting EVM; EraVM and WASM described as possible VMs) | Check EVM-equivalence differences for your contracts. Native account abstraction |
| staking-validators | custom | — | No native PoS. Operator/committer is set by ChainAdmin. App staking is contracts |
| rollup | native | Bridgehub + chain type manager (CTM) + diamond proxy per chain; validity proofs verified on L1 (FFLONK-wrapped) | Shared contracts under ecosystem governance |
| tokenomics | extend | custom base token, fee parameters, base-token multiplier (ChainAdmin) | Base token fixed at chain creation. Treat it as permanent |
| governance | extend | ChainAdmin (operator multisig) for chain params; ecosystem ProtocolUpgradeHandler → DecentralizedGovernance for shared contracts | Your upgrade path follows ecosystem protocol versions |
| randomness | custom | contracts + oracle/beacon | — |
| verifiable-participation | custom | contracts + off-chain operators | — |
| data-availability | native | rollup (Ethereum) or validium (DA validator pair; Prividium) | Validium weakens exit guarantees |
| p2p | n/a | centralized sequencer + RPC/external nodes; no p2p layer to design | Run RPC replicas and external nodes |
| interop | native | shared bridge via Bridgehub, Gateway settlement layer, ecosystem interop | Third-party bridges are app-level |
| smart-contracts | native | Solidity/Vyper (EVM); EraVM toolchain where used | `build-smart-contracts` |
| node-software | native | ZKsync OS server (or legacy zksync-era server), Airbender prover, explorer, portal, zkstack CLI | Pin versions per release |
| upgrades | native | protocol version upgrades (era-contracts), server upgrades | Rehearse on staging, and track ecosystem upgrade schedules |
