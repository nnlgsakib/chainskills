# Placement map — Arbitrum chains (Nitro)

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | extend | single sequencer; ordering policy (FCFS; Timeboost-style express lane or priority fees, depending on version) | Safety comes from the parent chain + BoLD, censorship resistance from the delayed inbox (force inclusion). Priority-fee collection exists in ArbOS 61 "Elara" (docs) |
| state-execution | native | EVM + Stylus (WASM: Rust, C, C++) in Nitro | ArbOS parameters via chain owner. Deep changes need a Nitro + replay-binary fork |
| staking-validators | custom | validator allowlist / BoLD bonds | No native PoS. Validator bonds are configured on the rollup contracts. App-level staking is contracts |
| rollup | native | RollupCreator contracts, SequencerInbox, Outbox, BoLD dispute protocol | Challenge period `confirmPeriodBlocks` (default ~1 week) |
| tokenomics | extend | fee parameters (L2 base fee, parent-chain data fee pricing), custom ERC-20 gas token, AEP fee router | AEP: 10% of protocol net revenue when settling outside Arbitrum One/Nova |
| governance | extend | chain owner (UpgradeExecutor), Security Council patterns, ArbOwner precompile | Stage targets dictate council and delay settings (protocol-rollup/stages.md) |
| randomness | custom | contracts + oracle/beacon | Don't rely on sequencer-controlled values |
| verifiable-participation | custom | contracts + off-chain operators | Pattern from protocol-verifiable-participation |
| data-availability | native | Rollup: parent chain (blobs on Ethereum); AnyTrust: DAC (N members, H honest assumed) | AnyTrust adds a DAC trust assumption |
| p2p | n/a | sequencer feed broadcast to nodes; no general p2p layer to design | Run feed relays and RPC replicas |
| interop | native | token bridge (gateways), retryable tickets, L3↔L2↔L1 messaging | Custom gateways for special tokens |
| smart-contracts | native | Solidity (EVM) and Stylus (WASM) | `build-smart-contracts`; Stylus activation and caching |
| node-software | native | Nitro node (sequencer, batch poster, validator, full/archive), DAS for AnyTrust | Pin Nitro versions; follow ArbOS upgrade docs |
| upgrades | native | ArbOS upgrades (scheduled), rollup and bridge contract upgrades via UpgradeExecutor | Coordinate node upgrades before ArbOS activation |
