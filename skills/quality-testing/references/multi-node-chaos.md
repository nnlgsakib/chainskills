# Multi-node, chaos and deterministic simulation

Facts checked 2026-11-25 are marked ✔.

## Multi-node frameworks

| Tool | For | Notes |
|---|---|---|
| CometBFT e2e runner (`test/e2e`) | CometBFT-based chains | TOML manifest defines nodes; can generate random manifests; per-node `perturb` list (e.g. pause, kill, restart, disconnect, upgrade to `upgrade_version`); stages: setup → start → load → perturb → wait → test → stop → cleanup; tests run with `E2E_MANIFEST=... go test ./tests/...` ✔ |
| interchaintest (Go module v10) | IBC / multi-chain tests in Docker (chains + relayers) | used by ibc-go's e2e suite and downstream chains in 2026 ✔; upstream maintenance signals mixed, so check the repo before adopting ✔ |
| Kurtosis ethereum-package | Ethereum-style multi-client devnets, shadowforks of public networks | moved to the **ethpandaops** org ✔ |
| Stack-native | `ignite testnet multi-node`, op-devnet / Orbit local stacks, Substrate zombienet | see the stack adapter |
| docker-compose / Kubernetes | anything | write your own; put validators in separate network namespaces for chaos |

## Chaos and fault injection
Tools: Linux `tc netem` (latency, loss, partition), toxiproxy (TCP faults), Chaos Mesh / LitmusChaos (Kubernetes), process signals (SIGSTOP/SIGKILL), disk-fill and clock-skew utilities (libfaketime, chrony offsets).

### Mandatory scenarios (each with an expected outcome written in advance)

| # | Scenario | Expected |
|---|---|---|
| C1 | Random validator restarts under load | no halt; no equivocation; catches up |
| C2 | Partition 60/40 (neither side > 2/3) | halt (BFT); no conflicting commits; resumes after healing |
| C3 | > 1/3 voting power offline | halt; resumes when power returns; documented recovery time |
| C4 | Latency matrix of the real target regions + 1–5% loss | block time within R-N p95 |
| C5 | Clock skew ±N s on a subset | consensus time unaffected beyond bounds |
| C6 | Validator churn at an epoch boundary (rotation) | set updates apply; no stall |
| C7 | 50% of non-consensus participants (operators, verifiers, relayers, oracles) disappear | chain unaffected; rewards drop; no slashing for absence |
| C8 | Randomness beacon stalls | the specified fallback (wait/skip/degrade) happens |
| C9 | Upgrade at height H under load | all nodes switch; no app-hash mismatch |
| C10 | New node joins via state sync/snapshot | syncs within R-N; serves queries |
| C11 | RPC flood | validators unaffected (sentries absorb it) |
| C12 | Disk full / IO stall on one validator | that validator stops safely; no corruption |

## Deterministic simulation testing
- **Antithesis**: runs the system in a deterministic hypervisor, injects faults (partitions, restarts, disk fills, pauses), and replays failures exactly ✔. Used by the Ethereum Foundation for major upgrades ✔. It's proprietary and paid; findings are replayed on its platform.
- Alternatives: write the node to run under a deterministic simulator (simulated time and network) in-house, or combine model-guided conformance testing with a formal model (arXiv 2501.08550) ✔.

## Determinism tests
- Same blocks on N nodes (different OS/CPU, different builds from the same tag) give the same app hash every block.
- Parallel execution on vs off gives the same app hash.
- Replay an exported mainnet/testnet history through the new binary.

Sources: https://pkg.go.dev/github.com/cometbft/cometbft/test/e2e · https://pkg.go.dev/github.com/cosmos/interchaintest/v10 · https://github.com/ethpandaops/ethereum-package · https://antithesis.com/industries/blockchain/ · https://fortune.com/2026/03/23/antithesis-janestreet-ethereum-will-wilson-foundationdb-software · https://arxiv.org/abs/2501.08550
