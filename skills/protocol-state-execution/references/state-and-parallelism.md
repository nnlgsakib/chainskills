# State commitment, storage, parallel execution

Status facts checked 2026-11-25 are marked ✔.

## Authenticated state structures

| Structure | Used by | Proof size | Write cost | Notes |
|---|---|---|---|---|
| IAVL+ tree | Cosmos SDK (Store v2 landed in v0.54 ✔) | O(log n) | rebalancing, high write amplification | ICS-23 proofs for IBC |
| Merkle-Patricia trie (hexary) | Ethereum, EVM chains | large (hexary branching) | moderate | Ethereum is researching replacements |
| Unified binary tree | Ethereum EIP-7864 (Draft ✔) | ~4× shorter branches than hexary (per proposals) | — | revived interest over post-quantum concerns with Verkle ✔. Not scheduled for a fork |
| Jellyfish Merkle Tree | Aptos, Penumbra, others | O(log n) | low | versioned and efficient |
| Sparse Merkle Tree | many custom chains, ZK systems | O(log n), fixed depth | — | ZK-friendly with Poseidon-like hashes |

Choose by: light-client and bridge proof needs, ZK friendliness (if proving state), write throughput, and pruning and snapshot support.

## Parallel execution

| Approach | Example | Requirement on txs | Notes |
|---|---|---|---|
| Optimistic (Block-STM) | Aptos; Cosmos SDK v0.54+ (`SetBlockSTMTxRunner`), config-driven in v0.55 (`block-executor = "block-stm"`) ✔ | none | Re-executes on conflict. In the SDK, Block-STM is incompatible with the block gas meter, which is disabled automatically ✔. Gains depend on how much txs conflict |
| Declared access sets | Solana SVM | txs list the accounts they touch | scheduler parallelises non-overlapping txs |
| Block-level access lists | Ethereum EIP-7928 (Glamsterdam, expected Q4 2026) ✔ | the block producer records the touched state | enables parallel validation and prefetching |
| Object ownership | Sui | owned objects skip consensus ordering | different programming model |

Rule: the parallel result must equal sequential execution in block order. Test it with differential execution (run the same blocks sequentially and in parallel, compare app hashes) in `quality-testing`.

## State growth

| Control | Mechanism | Trade-off |
|---|---|---|
| Deposits | lock tokens per stored byte/object; refund on delete | simple; capital cost for users |
| Rent | periodic charge; evict when unpaid | complex UX |
| Expiry | archive inactive state; resurrect with proofs | protocol complexity |
| Pruning + snapshots | nodes keep recent state; archive nodes keep history | doesn't reduce live state |

Sources: https://docs.cosmos.network/sdk/latest/upgrade/v0.55 · https://docs.cosmos.network/sdk/latest/upgrade/v0.54 · https://eips.ethereum.org/EIPS/eip-7864 · https://ethereum.org/roadmap/glamsterdam/
