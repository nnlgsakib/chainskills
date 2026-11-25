# Placement map — Avalanche L1

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | Snowman (AvalancheGo); P-Chain tracks L1 validator sets | L1 validators sync only the P-Chain (Etna / ACP-77) |
| state-execution | native | Subnet-EVM (plugin built in avalanchego) or a custom VM | Precompiles configured in genesis and upgrades |
| staking-validators | native | ACP-99 `ValidatorManager` + `PoAManager` or staking manager (ERC-20, native per docs) | Contracts are consensus-critical. v1 PoS can't migrate to v2 |
| rollup | n/a | — | — |
| tokenomics | extend | native minter, fee manager, reward manager precompiles; staking rewards via the reward calculator | Fees burned or sent to an address (config) |
| governance | extend | owners of validator manager and precompile admin roles; Governor contracts | Multisig + timelock |
| randomness | custom | contracts + oracle/beacon | — |
| verifiable-participation | custom | contracts + off-chain operators | — |
| data-availability | n/a | — | — |
| p2p | native | AvalancheGo networking; `validatorOnly` for private L1s | — |
| interop | native | ICM (Teleporter), ICTT token transfers, Warp precompile, relayers | Run your own relayers for mainnet |
| smart-contracts | native | Solidity on Subnet-EVM | `build-smart-contracts`; `evm_version` per network upgrade |
| node-software | native | avalanchego v1.15.x + subnet-evm plugin; Builder Console; platform-cli | avalanche-cli in maintenance mode |
| upgrades | extend | avalanchego network upgrades; precompile config upgrades; contract proxies | Upgrade nodes before activation |
