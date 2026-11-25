# Work types and how to verify them

Facts checked 2026-11-25 are marked ✔.

| Work | Ladder rung | Verification method | Real-world reference | Pitfalls |
|---|---|---|---|---|
| Independent block verification / re-execution | 2–3 | Assigned verifiers re-execute and commit to the post-state root; disagreement escalates to more verifiers or an on-chain fraud proof | optimistic rollup challengers; re-execution committees | "always valid" laziness, so use canary blocks with known invalid results in a test channel or audit sampling against the canonical root; finality must not depend on it |
| Data availability sampling | 1–3 | Light nodes request random shares + Merkle proofs from an erasure-coded block; enough successful samples ⇒ available | Celestia light nodes take ≥ 16 samples per block before declaring availability ✔ (forum argues the number should scale with network size ✔) | rewarding the *sampler* is hard (sampling is cheap to fake). Reward *serving* shares instead, verified by Merkle proofs on request |
| Historical data serving | 1 + 3 | Random challenges "return block/share X with proof" against a known commitment; time-bounded response | archive/history networks | Proofs show possession at challenge time, not continuous service. Use frequent random challenges |
| Storage over time | 1 | Proof of replication at ingest + periodic proofs of spacetime | Filecoin PoRep (unique sealed copy) + WindowPoSt (each partition proven by a deadline; missing it forfeits collateral and reduces power) ✔ | Sealing cost is the anti-cheat. Without it, a node can regenerate data on demand |
| Relay / RPC service | 1 + 3 | Signed request/response pairs, aggregated into a Merkle sum tree; claim the root, prove a random sample | Pocket Network Shannon relay mining: one claim per app per session, claim window then proof window, probabilistic proof requirement, missing a window forfeits rewards, invalid proofs can be slashed, difficulty per service via EMA of relay volume ✔ | Requires the user/app to sign requests (otherwise self-dealing). v1.31 fixed difficulty tracking that had rejected valid proofs ✔, so test edge cases at window boundaries |
| Transaction / block propagation | 4 (weak) | Peer attestations, gossip scoring | — | Hard to prove. Usually better rewarded indirectly (via fees to RPC/relay roles) or not at all |
| Physical coverage (DePIN) | 4 | Witness reports, radio challenges, oracle validation | Helium-style proof of coverage; research notes spoofing and "hotspots in empty fields" incentive failures ✔ | Location spoofing and collusion. Needs hardware attestation, diversity, and demand-based rewards |
| Compute | 1–3 | SNARK/zkVM proof, TEE attestation, or redundant execution + spot checks | zk coprocessors, verifiable compute markets | Proving cost; TEE trust assumptions |
| Oracle / attestation | 3–4 | Multiple independent reporters + aggregation (median) + deviation bounds + slashing for provable lies | price oracles | Collusion; cost of corruption must exceed profit from manipulation |

## Choosing what to reward
Reward work that is (a) valuable to users, (b) at rung 1–3, and (c) not cheaper to fake than to do. Propagation and uptime usually fail (b). Treat them as part of other roles or don't reward them separately.

Sources: https://docs.pocket.network/protocol/sessions-claims-proofs/ · https://forum.pokt.network/t/pnf-q4-2025-january-2026-transparency-report/5626 · https://docs.filecoin.io/basics/the-blockchain/proofs · https://forum.celestia.org/t/celestia-das-reconstruction-simulations-and-light-node-requirements/1891 · https://arxiv.org/pdf/2609.02125
