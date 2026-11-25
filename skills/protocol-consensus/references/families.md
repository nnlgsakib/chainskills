# Consensus families

Status facts checked 2026-11-25 are marked ✔ (sources at the bottom). Everything else is protocol background that changes slowly.

## Comparison

| Family | Examples | Finality | Fault tolerance | Message complexity | Typical set size | Notes |
|---|---|---|---|---|---|---|
| Tendermint-style BFT | CometBFT (Cosmos), Malachite (Rust) | deterministic, one block | < 1/3 Byzantine, needs > 2/3 online | O(n²) per round (all-to-all votes) | up to ~150–200 | Halts instead of forking. ABCI++ hooks (PrepareProposal, ProcessProposal, vote extensions) for app logic in consensus |
| HotStuff family | Jolteon/AptosBFT, HotStuff-2 | deterministic, a few network hops | < 1/3 Byzantine | linear per phase (leader aggregates) | 100s | Pipelined and leader-based. Needs signature aggregation |
| DAG-based BFT | Narwhal/Bullshark, Mysticeti (Sui) | deterministic, low latency | < 1/3 Byzantine | separates data dissemination from ordering | ~100+ | High throughput. More complex implementation and testing |
| Gasper (Ethereum) | Ethereum beacon chain | economic finality after 2 epochs (~12.8 min); faster finality is research | < 1/3 for finality; LMD-GHOST fork choice keeps producing | committees + BLS aggregation | very large (sharded into committees) | Keeps running without finality. Needs a beacon chain, which is heavy for a new L1 |
| Avalanche Snowman | Avalanche C-chain, L1s | probabilistic, fast (~1–2 s) | parameterised by sampling | sub-quadratic (repeated sampling) | large | Metastable sampling. Validator set for L1s via ACP-77/99 contracts ✔ |
| Solana Alpenglow | Solana | Votor live since epoch 1064 (21 Oct 2026), ~150 ms finality target ✔ | per protocol paper | — | large | Rotor (data dissemination) planned, not yet scheduled ✔ |
| BABE/Aura + GRANDPA | Polkadot SDK solo chains | GRANDPA finalises chains of blocks | < 1/3 Byzantine | — | ~100s (NPoS) | Block production and finality are separate gadgets |
| PoA BFT | QBFT/IBFT 2.0 (Besu) | deterministic | < 1/3 Byzantine | O(n²) | small (≤ ~30) | Permissioned/consortium. Clique is deprecated upstream in geth |
| Nakamoto PoW | Bitcoin-style | probabilistic (k confirmations) | < 50% hashrate | gossip | open | Energy cost, slow finality. Rarely right for new chains |
| Centralized sequencer (rollup) | most L2s | soft: sequencer; hard: L1 settlement + proofs | trusts sequencer for liveness and ordering, not safety (with forced inclusion) | — | 1 | Plan forced inclusion and decentralization (protocol-rollup) |
| Shared / based sequencing | Taiko (based, preconfirmations since Aug 2025) ✔, shared sequencer networks | inherits L1 ordering (based) | L1 proposers | — | L1 set | Preconfirmations give fast UX. Based rollups cede MEV to L1 |

## Choosing

1. Need deterministic finality, a sovereign chain, and up to ~150 validators: **Tendermint-style BFT** via an existing engine (CometBFT in Go; Malachite or CometBFT over ABCI for Rust apps).
2. Need hundreds of validators and very high throughput, with a team that can run a complex engine: **HotStuff or DAG-based** (usually by adopting the chain framework that ships them).
3. An L2: consensus is mostly **sequencing** plus L1 settlement. Go to `protocol-rollup`.
4. Known operators (consortium): **PoA BFT**.
5. Very large open validator sets with liveness over finality: **Gasper-like** or Snowman-like. Expect major engineering effort.

## Engine maturity notes (2026-11-25)

- **CometBFT**: supported lines are v0.38.x (Cosmos release family 2025.1) and v0.40.x (2026.1) ✔. v0.39 added an experimental libp2p stack and an app-side mempool mode (`mempool.type = "app"`), and v0.40 fixed a socket-transport bug in that mode ✔. The v1.x line was retracted and is unsupported ✔. Apply security patches promptly: 2026 advisories include CSA-2026-001 (patched in v0.38.22) ✔.
- **Malachite**: Rust Tendermint BFT. Published crates are still pre-1.0 (0.7.0-pre) and the old README said "not audited", but it runs in production for Circle's Arc and inside Starknet's Pathfinder ✔. Check its audit status before choosing it.

## Sources
- https://docs.cosmos.network/sdk/latest/release-family · https://docs.cosmos.network/sdk/latest/upgrade/v0.55
- https://github.com/circlefin/malachite · https://www.arc.io/blog/arcs-deterministic-finality-the-bespoke-consensus-layer-built-using-malachite
- https://solana.com/upgrades/alpenglow
- https://docs.taiko.xyz/protocol/preconfirmations
- https://build.avax.network/docs/quick-start/validator-manager
