# OP Stack components (verified 2026-11-25)

Versions are the latest component tags on github.com/ethereum-optimism/optimism/releases at that date. Always pin per component.

| Component | Version | Role | Notes |
|---|---|---|---|
| op-deployer | v0.9.0 | Deploy and upgrade L1 contracts from an intent file; emit genesis.json and rollup.json | `init` → edit `intent.toml` → `apply` → `inspect genesis/rollup`. Also `bootstrap`, `verify`, upgrade flows |
| op-contracts | v9.0.0 | L1 contracts (OptimismPortal, SystemConfig, DisputeGameFactory, bridges, OPCM) | Contract releases are tagged `op-contracts/vX` |
| op-node | v1.20.2 | Rollup consensus node: derives L2 from L1, drives the execution client via the Engine API | `--l2.enginekind=reth` for op-reth |
| op-reth | v2.9.0 | Execution client (reth-based) | Now released from the optimism monorepo. Archive by default |
| op-geth | — | **End-of-support 2026-05-31**; doesn't support Karst | Migrate to op-reth |
| kona-node | v1.11.0 | Rust rollup node | Alternative to op-node, so check maturity for your use |
| kona-client / kona-host | v1.9.0 | Fault-proof program and host | Needs the absolute prestate matching your chain config |
| op-batcher | v1.18.1 | Posts L2 batches to L1 (blobs) | Funded hot key, monitored balance |
| op-proposer | v1.17.1 | Posts output or super roots / creates dispute games | Funded key |
| op-challenger | v1.12.0 | Honest challenger for fault (or ZK) dispute games | Must stay online; funded bonds |
| op-dispute-mon | v1.6.6 | Monitors dispute games, alerts on incorrect outcomes | Production requirement |
| op-conductor | v0.9.6 | HA sequencer control (Raft leadership across sequencers) | RPC unauthenticated, so keep it on a private network |
| op-supernode | v1.1.2 | Runs every chain of an interop dependency set in one process | For Superchain interop deployments |

## Network roles at production
- **3 sequencers** (op-node + op-reth each) in separate failure domains, managed by op-conductor, private network only.
- **Replicas / RPC nodes** facing users. The sequencer isn't directly internet-facing.
- **L1-facing services**: batcher, proposer, challenger, dispute-mon, each with its own key and alerting.
- **Explorer / indexer** on archive replicas.

## Versioning rules (from the chain-operator best practices)
- Production releases are tagged `<component>/v<semver>`.
- Monorepo `v<semver>` tags cover Go components together and don't include contract changes.
- Keep every deployment artifact (op-deployer state, versions, commit hashes). You need them for upgrades and the Superchain Registry.
