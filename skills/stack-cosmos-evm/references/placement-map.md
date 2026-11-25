# Placement map — Cosmos EVM (cosmos/evm via Ignite EVM app)

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`. Everything in `stack-cosmos-ignite`'s map also applies. This file lists what EVM changes.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | CometBFT | As Cosmos. Block gas limit must be finite (consensus `max_gas`) |
| state-execution | native | EVM (x/vm) + Cosmos modules, EIP-1559 fee market (x/feemarket) | Two tx paths (Ethereum tx and Cosmos tx) share state. 18-decimal base denom |
| staking-validators | native | x/staking + staking precompile | Contracts can delegate through the staking precompile. Validator set stays a native module |
| rollup | n/a | — | Use `stack-rollup-*` for Ethereum L2s |
| tokenomics | native | x/mint, x/distribution, x/feemarket, x/erc20 | Native coin ↔ ERC20 representation via x/erc20. Fee burn/redistribution via feemarket params + custom module |
| governance | native | x/gov + gov precompile | On-chain Governor contracts possible but secondary to x/gov |
| randomness | custom | custom module or contract + oracle | Expose beacon output to Solidity through a custom precompile |
| verifiable-participation | custom | custom module + precompile, or Solidity contracts | Contracts for fast iteration. A module when it must run in BeginBlock/EndBlock |
| data-availability | extend | CometBFT gossip | As Cosmos |
| p2p | native | CometBFT p2p | JSON-RPC nodes separate from validators |
| interop | native | IBC + ICS20 precompile; ERC20 representations of IBC tokens | Ethereum bridges are external (contracts + relayers) |
| smart-contracts | native | Solidity/Vyper on EVM; precompiles at fixed addresses | `build-smart-contracts`. Foundry/Hardhat against :8545 |
| node-software | extend | `<chain>d` with JSON-RPC server, Ethereum keyring | Dedicated RPC/archive nodes with indexer |
| upgrades | native | x/upgrade + Cosmovisor; contract proxies for Solidity | A cosmos/evm version bump is a state-breaking upgrade |
