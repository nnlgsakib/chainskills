# EVM L1 routes (read 2026-11-25)

## A. Hyperledger Besu QBFT (permissioned / consortium)
- Project and docs moved to **besu-eth** (docs.besu-eth.org, github.com/besu-eth/besu). Latest line **26.x** (26.11.2). Besu still supports Ethereum public networks too.
- Genesis `qbft` block (defaults): `blockperiodseconds` 1, `emptyblockperiodseconds` 0, `epochlength` 30000, `requesttimeoutseconds` 1, `blockreward` 0, `pertxgaslimit` (EIP-7825 default 2^24 if omitted), `startblock`, `miningbeneficiary`. Docs example: `blockperiodseconds: 5, epochlength: 30000, requesttimeoutseconds: 10`.
- Validator management:
  - **Block header**: initial validators in `extraData` (`besu rlp encode --type=QBFT_EXTRA_DATA`). Changes via `qbft_proposeValidatorVote` / `qbft_discardValidatorVote` / `qbft_getPendingVotes`. A validator is added when more than 50% of validators propose it.
  - **Contract**: `validatorcontractaddress` matching an `alloc` entry with initial storage. Add/remove by contract transactions (JSON-RPC votes don't apply).
  - Switch methods or block period later via `transitions`.
- Fault tolerance: ≥ 2/3 of validators sign each block. **Minimum 4 validators** for BFT. Never lose more than 1/3.
- Use the latest protocol milestone in the genesis.

## B. Ethereum-style PoS with your own beacon chain
- Components: execution client (geth, reth, Besu, Nethermind, Erigon, ...), consensus client (Lighthouse, Prysm, Teku, Lodestar, Nimbus, Grandine), validator clients, and a deposit contract.
- Genesis: EL and CL genesis generated together (ethpandaops ethereum-genesis-generator, used by the Kurtosis ethereum-package).
- geth private networks "only work in PoS mode and in concert with a consensus client". The geth docs point to the Kurtosis guide. Clique isn't an option since geth v1.14.
- Devnets: `kurtosis run --enclave my-testnet github.com/ethpandaops/ethereum-package` (Kurtosis ≥ 1.23.0). EL options include geth, nethermind, erigon, besu, ethereumjs, reth, nimbus-eth1, ethrex. CL options include nimbus, lighthouse, lodestar, teku, prysm, grandine. **The package is not intended for production.**
- Production example: Gnosis Chain runs its own PoS beacon chain with Ethereum clients (reth lists "Reth Gnosis" as Gnosis Chain's execution client). Architecture details unverified.
- Client diversity: run at least two EL and two CL implementations, so a client bug can't finalize an invalid chain.

## C. reth SDK (custom EVM node in Rust)
- reth v2.11.0. The SDK uses a node builder: `NodeBuilder::new(config).with_types::<EthereumNode>().with_components(...)`, with components for Primitives, Network, Consensus, EVM, RPC, Transaction Pool and DB (MDBX + static files).
- Advertised uses: custom execution nodes (e.g. payload building), new RPC endpoints, **custom consensus**. Production users listed: Base node, Bera Reth, Reth Gnosis, Reth BSC.
- Exact custom-precompile and EVM trait APIs: read `reth.rs/sdk/node-components/evm` and `/consensus` for your version (unverified here).

## D. PoSA geth fork (BSC-style)
- BNB Smart Chain: a go-ethereum fork with **Parlia** consensus (Proof of Staked Authority, 21 validators, turn-taking). Validator sets are elected by staking-based governance, through **system contracts** that handle liveness slashing, revenue distribution and validator-set renewal.
- Copying this pattern means maintaining a client fork plus genesis system contracts. Every upstream geth hardfork and security fix must be merged.
- System-contract addresses and APIs: docs.bnbchain.org (unverified here).

## E. Avalanche L1 (pointer)
- Validator set managed by **ACP-77** (P-Chain registration via Warp messages) plus **ACP-99** contracts: `ValidatorManager` with `PoAManager` or `NativeTokenStakingManager` / `ERC20TokenStakingManager` (icm-contracts v2; no v1→v2 PoS migration; the PoS manager must live on the chain holding the reward token).
- Execution via Subnet-EVM (or a custom VM). Interop via ICM.
- For full coverage, create `stack-avalanche-l1` with `build-stack-adapter`.
