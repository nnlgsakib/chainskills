# Placement map — EVM L1

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | extend | QBFT (Besu), Gasper (own beacon chain), Parlia-style PoSA (fork), Snowman (Avalanche), custom (reth SDK) | Choose a route in SKILL.md. BFT routes halt when more than 1/3 is offline |
| state-execution | native | EVM in the chosen client(s) | Set the hardfork schedule in genesis. Custom precompiles need a client fork or the reth SDK |
| staking-validators | extend | QBFT validator contract or header votes; beacon deposit contract; PoSA system contracts; Avalanche ValidatorManager | Contracts are consensus-critical (`build-smart-contracts/references/validator-set-contracts.md`) |
| rollup | n/a | — | Sovereign L1. For rollups use `stack-rollup-*` |
| tokenomics | extend | native coin issuance (block rewards / `blockreward`, beacon issuance), fee recipient, EIP-1559 base fee burn | Model with protocol-tokenomics. Many PoA chains have zero issuance |
| governance | extend | contracts (Governor + timelock), validator votes (QBFT), off-chain coordination for hardforks | Hardforks require coordinated node upgrades |
| randomness | custom | RANDAO/`prevrandao` (PoS routes), oracle/beacon contracts | prevrandao is proposer-influenced (protocol-randomness) |
| verifiable-participation | custom | contracts + off-chain operators | — |
| data-availability | n/a | full nodes keep all data | — |
| p2p | native | devp2p (EL), libp2p (CL); static/boot nodes; permissioning (Besu) | Sentry-style topology for validators |
| interop | custom | bridges (light-client or committee based), ICM on Avalanche | protocol-interop (planned) / third-party bridges |
| smart-contracts | native | Solidity/Vyper | `build-smart-contracts`; `evm_version` = chain fork |
| node-software | native | geth / reth / Besu / Nethermind + consensus and validator clients | Pin versions; client diversity |
| upgrades | native | hardfork activation by block or timestamp in genesis/config; coordinated releases | Rehearse on a devnet with low activation heights |
