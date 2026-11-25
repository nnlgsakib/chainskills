# Stack catalog

Last reviewed: 2026-11-25. Cells marked ✔ were checked against the sources at the bottom on that date. Unmarked cells are general background. Before recommending a stack, verify versions, licences and maintenance status again.

## Contents
- Sovereign L1 / appchain frameworks
- EVM L1 options
- Rollup / L2 frameworks
- Shared-security options
- Permissioned
- Custom build
- No new chain

## Sovereign L1 / appchain frameworks

| Stack | Language | Consensus | Execution | Validator model | Finality | Strengths | Watch out |
|---|---|---|---|---|---|---|---|
| **Cosmos SDK + CometBFT** | Go | CometBFT (Tendermint BFT) | native modules; optional CosmWasm or EVM; Block-STM parallel execution (SDK v0.54+) ✔ | PoS (x/staking) with consensus key rotation and ML-DSA-65 post-quantum validator keys (v0.55) ✔; licensed Enterprise PoA module ✔ | single-block deterministic | release families pin compatible versions (2026.1: SDK 0.55, CometBFT 0.40, Cosmos EVM 0.7; 2025.1 still supported) ✔; IBC now under LF Decentralized Trust ✔ | BFT set size limits (~100–200); Go only for modules; Enterprise modules (PoA, Groups) need a licence ✔; you bootstrap security |
| **Cosmos EVM (cosmos/evm)** | Go + Solidity | CometBFT | EVM + Cosmos modules + precompiles; v0.7 adds the Krakatoa app-side mempool and optional Block-STM ✔ | as Cosmos SDK | single-block | EVM tooling + native modules, IBC | 18-decimal tokens, EVM chain ID, see stack-cosmos-evm pitfalls |
| **Polkadot SDK (Substrate)** | Rust | BABE/Aura block production + GRANDPA finality (solo), or relay chain (parachain) | FRAME pallets; EVM via Frontier; ink! contracts | NPoS (solo) or relay-chain security | GRANDPA: seconds, finalises chains of blocks | highly customisable runtime, forkless runtime upgrades, Rust | steep learning curve; parachain needs coretime; licence mix (Apache-2.0 / GPL-3.0 client parts) |
| **Avalanche L1** | Go (AvalancheGo), Solidity | Snowman | Subnet-EVM or custom VM | validator set managed by ACP-77 + ACP-99 ValidatorManager contracts (PoA, or PoS with Native/ERC20 StakingManager; v2 splits manager and staking contracts, no v1→v2 PoS migration) ✔ | ~1–2 s | EVM-native, validator set as contracts, ICM messaging | Snowman semantics differ from BFT; ecosystem coupling |
| **Sovereign custom (CometBFT + own app)** | any (ABCI: Go, Rust, ...) | CometBFT | your own state machine | you implement it | single-block | full freedom with proven consensus | you implement staking, slashing, governance, sync tooling |

## EVM L1 options

| Stack | Language | Consensus options | Notes |
|---|---|---|---|
| **geth fork** | Go | Ethereum PoS with own beacon chain (own validator network), or legacy PoA | LGPL/GPL; PoA Clique deprecated upstream; system contracts possible via fork (BSC-style) |
| **reth fork / reth SDK** | Rust | as above (beacon chain) or custom via SDK | Apache-2.0/MIT; modular node SDK for custom chains |
| **Hyperledger Besu** | Java | QBFT/IBFT 2.0 (permissioned/PoA), Ethereum PoS | Apache-2.0; enterprise focus |
| **BSC-style (Parlia)** | Go | PoSA with system contracts for validator set/staking | validator set and staking as genesis system contracts |

## Rollup / L2 frameworks

| Stack | Proof system | Settlement | Execution | DA | Notes |
|---|---|---|---|---|---|
| **OP Stack** | optimistic, permissionless fault proofs; Kona-based proofs and Super Root dispute games (Upgrade 20) ✔; ZK option via OP Succinct ✔ | Ethereum (or other EVM L1) | op-reth (op-geth unsupported from Upgrade 19 / Karst) ✔ | Ethereum blobs, alt-DA mode | MIT; Superchain interop in progress ✔; customise via predeploys or forking the client |
| **Arbitrum Orbit (Nitro)** | optimistic, BoLD permissionless validation (live on One/Nova since Feb 2025) ✔ | Arbitrum One/Nova or Ethereum | EVM + Stylus (Rust/C/C++ via WASM) | Rollup or AnyTrust (DAC) | Timeboost ordering auction, reportedly replaced by per-tx priority auctions in Jun 2026 (unverified); licensing terms (BSL + Arbitrum Expansion Program), check before choosing |
| **ZK Stack (ZKsync)** | validity proofs; Airbender RISC-V prover replaces Boojum for new chains ✔ | Ethereum / ZKsync gateway | EraVM, EVM bytecode support | rollup or validium | MIT/Apache-2.0; native account abstraction; "Elastic Network" of ZK chains ✔ |
| **Agglayer CDK (Polygon)** | two configs: OP Stack (cdk-opgeth, op-geth/op-reth) or CDK Erigon ✔; SP1 proofs on Katana ✔ | Ethereum via Agglayer | EVM | three modes, differing in DA and prover ✔ | no fee to connect to Agglayer (Polygon claim) ✔ |
| **Based rollup (e.g. Taiko)** | per project | Ethereum (L1 proposers sequence) | EVM | Ethereum | L1 inherits sequencing; preconfirmations for UX (Taiko mainnet since Aug 2025) ✔ |
| **Sovereign rollup (Evolve/Rollkit, Sovereign SDK)** | none on L1 (sovereign) or optional | self | Cosmos SDK app (Evolve) or Rust (Sovereign SDK) | Celestia / other DA | own fork choice; no L1 bridge guarantees by default |
| **Rollup-as-a-service** (Conduit, Caldera, Gelato, Alchemy...) | per framework | per framework | per framework | per framework | buys operations, not design; check exit and key custody |

## Shared-security options

| Option | What you get | Notes |
|---|---|---|
| Polkadot parachain | relay-chain validators secure your blocks | needs coretime |
| Cosmos Interchain Security (consumer chain) | provider chain validator set | provider governance decides |
| Restaking-secured (EigenLayer AVS, Symbiotic, Babylon BTC staking) | economic security from restaked assets | slashing conditions and operator set are your design work |

## Permissioned

| Stack | Notes |
|---|---|
| Hyperledger Besu (QBFT) | EVM, permissioning contracts, enterprise privacy options |
| Hyperledger Fabric | channels, chaincode (Go/Java/JS), no native token, not EVM |
| Cosmos SDK with PoA module | Cosmos tooling with a known validator set |

## Custom build

| Building blocks | Notes |
|---|---|
| CometBFT + ABCI app in Rust (tendermint-rs) or Go | proven consensus, custom everything else |
| Malachite (Rust Tendermint-BFT library) | embeddable consensus engine. Crates still pre-1.0 (0.7.0-pre), but used in production by Circle's Arc and Starknet's Pathfinder ✔ |
| HotStuff-family engines, commonware-style Rust primitives | for teams with consensus expertise |
| libp2p, RocksDB/MDBX, Merkle trees (IAVL, JMT, Patricia, SMT) | standard components |

Custom is justified only when a hard requirement can't be met by any framework, or when the novel mechanism needs deep consensus integration. Budget for implementing staking, slashing, governance, sync, tooling and audits yourself.

## No new chain

Contracts on an existing chain (Ethereum, an L2, Solana, a Cosmos chain with CosmWasm/EVM). This always belongs in the candidate list. It's the baseline every other option has to beat.

## Sources (read 2026-11-25)
- Cosmos release families: https://docs.cosmos.network/sdk/latest/release-family · v0.54/v0.55 upgrade guides: https://docs.cosmos.network/sdk/latest/upgrade/v0.55 · Cosmos EVM v0.6→v0.7: https://docs.cosmos.network/evm/next/documentation/migrations/migration-v0.6-to-v0.7
- OP Stack: https://docs.optimism.io/notices/upgrade-20 · Kona: https://gov.optimism.io/t/vulnerability-in-kona-fallback-proof-system/10650 · OP Succinct: https://optimism.io/blog/optimism-partners-with-succinct-as-preferred-provider-to-accelerate-zk-proving-on-the-superchain
- Arbitrum BoLD: https://www.theblock.co/post/340278/ · Timeboost change (unverified): https://cryptobriefing.com/arbitrum-priority-gas-auctions-replace-timeboost/
- ZKsync Airbender: https://www.zksync.io/airbender · Agglayer CDK: https://docs.polygon.technology/chain-development/cdk/get-started/overview · Taiko preconfs: https://docs.taiko.xyz/protocol/preconfirmations
- Malachite: https://github.com/circlefin/malachite · Arc: https://www.arc.io/blog/arcs-deterministic-finality-the-bespoke-consensus-layer-built-using-malachite
- Avalanche validator manager (ACP-77/99): https://build.avax.network/docs/quick-start/validator-manager
