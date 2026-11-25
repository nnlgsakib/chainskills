# Placement map — Cosmos SDK + Ignite

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | CometBFT | Tune `timeout_propose`/`timeout_commit` in config.toml for block time. ABCI++ `PrepareProposal`/`ProcessProposal` and vote extensions for custom block content |
| state-execution | extend | Cosmos SDK modules, `collections` KV store (IAVL / Store v2 in v0.54+). Block-STM parallel execution (v0.54+, config-driven in v0.55: `block-executor = "block-stm"`) | One module per spec component (`ignite scaffold module`). Gas via `GasMeter`. Determinism rules in production.md §1 |
| staking-validators | native | x/staking, x/slashing, x/evidence. Consensus key rotation and ML-DSA-65 post-quantum validator keys in SDK v0.55. Enterprise PoA module (licensed) | Active-set size = `max_validators`. Epoch- or performance-based rotation needs a custom module that adjusts power, or a fork of x/staking. Minimum self-delegation per validator |
| rollup | n/a | — | Sovereign rollup via Evolve (`stack-cosmos-apps`). L2 on Ethereum → `stack-rollup-*` |
| tokenomics | native | x/mint, x/distribution (community pool), x/bank. `x/protocolpool` was removed in SDK v0.55 | Custom reward splits (e.g. a share for non-validator roles): a custom module taking a cut in `BeginBlock` before x/distribution, or a custom mint function |
| governance | native | x/gov. Authority can be centralized via consensus `AuthorityParams` (SDK v0.54+) | Authority = gov module account. Emergency pause: `contrib/x/circuit` (unmaintained since v0.54) or a custom pause module. `x/group` needs a Cosmos Enterprise licence |
| randomness | custom | custom module | Vote extensions with threshold signatures / VRF, or an external beacon (drand) verified on-chain. Never block hash alone |
| verifiable-participation | custom | custom module + off-chain service | Module: registration with bond, task assignment, commit-reveal, challenges, rewards. Service: Go client using the chain's gRPC |
| data-availability | extend | CometBFT block gossip; Evolve for external DA | Erasure-coded sampling needs a custom service and client. Celestia-style DA uses Evolve or a Celestia-app fork |
| p2p | native | CometBFT p2p (PEX, persistent peers, sentries) | Sentry topology, `max_num_inbound_peers`, seed nodes. libp2p not native |
| interop | native | IBC (ibc-go): transfer, ICA, light clients | `--ibc` modules and `scaffold packet`. Hermes relayer via `stack-cosmos-apps`. Ethereum bridges are external |
| smart-contracts | extend | CosmWasm (`ignite wasm`), EVM (`ignite evm`) | See `stack-cosmos-apps` / `stack-cosmos-evm` |
| node-software | extend | `<chain>d` binary, Cosmovisor, Ignite apps | Custom clients/services use gRPC + CometBFT RPC. Light client via CometBFT light package |
| upgrades | native | x/upgrade + Cosmovisor, module ConsensusVersion migrations | production.md §6. `ignite testnet in-place` for rehearsal |
