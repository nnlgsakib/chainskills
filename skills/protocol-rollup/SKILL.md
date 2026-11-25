---
name: protocol-rollup
description: Design an L2/L3 rollup or validium independent of framework — rollup type (optimistic, ZK, validium/optimium, sovereign, based), settlement layer, data availability (Ethereum blobs/PeerDAS, alt-DA), proof system (fault proofs, BoLD-style disputes, ZK provers, multi-proofs), sequencing (centralized, shared, based with preconfirmations), MEV policy, canonical bridge, withdrawals and forced inclusion, upgrade keys and Security Council, decentralization stage targets (ETHBEAT/L2BEAT Stages 0/1/2), and operator roles (sequencer, batcher, proposer, challenger, prover). Use whenever the user wants to build or review an L2, L3, rollup, appchain on Ethereum, sequencer design, fraud/validity proofs, exit windows, or wants to reach Stage 1/Stage 2.
license: MIT
---

# Protocol Rollup

A building-block skill in chainskills (layer L2, stack-neutral). It designs a rollup's trust model and components. The framework (OP Stack, Arbitrum Orbit, ZK Stack, Agglayer CDK, custom) is picked afterwards in `design-stack-selection` and built with the matching `stack-rollup-*` adapter.

Inputs from `CHAIN.md`: architecture class (must be L2/L3 or sovereign rollup), throughput, fee and latency targets, interoperability needs, trust assumptions. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/stages.md` | Setting the decentralization target and checking requirements |
| `references/proof-systems.md` | Choosing fraud vs validity proofs and the prover setup |
| `references/risks.md` | Risk review before spec and before launch |

## Workflow

### 1. Rollup type
| Type | Security of funds | Withdrawal latency | Cost driver |
|---|---|---|---|
| Optimistic rollup | settlement L1 + at least 1 honest challenger + DA on L1 | challenge period (≥ 5 days for Stage 1 under the 30 Apr 2026 rules) | DA |
| ZK rollup | settlement L1 + proof soundness + DA on L1 | proof generation + verification (minutes–hours) | proving + DA |
| Validium / optimium | as above, plus a DA committee | as above | lower DA cost; weaker exits |
| Sovereign rollup | own nodes' fork choice + DA layer | no L1 bridge by default | DA |
| Based rollup | L1 proposers sequence; proofs as above | as type | L1 inclusion; preconfirmations for UX |

Choose by required exit guarantees, withdrawal latency and cost. Record it as an ADR.

### 2. Settlement and DA
- Settlement layer (Ethereum, an L2 for L3s, another chain) and its finality.
- DA: Ethereum blobs (PeerDAS live since Fusaka, 3 Dec 2025; BPO forks raised the blob target/max to 14/21) or an alternative DA layer (`protocol-data-availability`). Model the cost at your target throughput, including blob fee spikes.

### 3. Proof system
Use `references/proof-systems.md`. Decide on single vs multi-proof, permissionless vs allowlisted proposers and challengers, the challenge period or proving cadence, and bond sizes. Proof systems are where the most dangerous bugs live, so plan audits, bug bounties and an emergency path that doesn't give anyone the power to steal.

### 4. Sequencing and ordering
Choose a centralized sequencer (most chains start here), a shared sequencer, or based sequencing. Define:
- The forced-inclusion path through L1 and its delay. This guarantees censorship resistance even with a centralized sequencer.
- What happens if the sequencer is down (users fall back to L1 inclusion).
- MEV and ordering policy (`protocol-consensus` → `references/ordering-mev.md`) and where MEV revenue goes.
- Preconfirmations, if fast UX matters, and what guarantees they really give.

### 5. Bridge and withdrawals
The canonical bridge's L1 and L2 contracts are the rollup's security core. Cover deposit and withdrawal flows, message passing, replay protection, escrow handling for natively issued versus bridged tokens, rate limits, and pause scope.

### 6. Upgrades and governance
- Who can upgrade L1 contracts and with what delay. The **exit window** (upgrade delay minus time to exit) is what the Stages framework measures.
- Security Council: size, threshold, member independence, and powers limited to emergencies.
- Write the target stage explicitly and check it against `references/stages.md`.

### 7. Operator roles
Sequencer, batcher/poster, proposer, challenger, prover, and RPC/archive nodes. For each, define who runs it, its bonds, failure impact and monitoring. These feed `build-node-software` and `ops-infrastructure`.

### 8. Hand off
To `design-spec`: components `BRIDGE`, `SEQ`, `PROOF`, `UPGRADE`, with invariants such as `INV-BRIDGE-1` (total L2 supply of a bridged token ≤ L1 escrow) and `INV-BRIDGE-2` (each withdrawal is finalised at most once). Then to `design-stack-selection` for the framework, and update `CHAIN.md`.

## Rules
- Without a working proof system and L1 DA, it isn't a rollup. Call it what it is (sidechain, validium, optimium).
- Forced inclusion and exit paths must work even if the operator team disappears.
- An upgrade delay shorter than the exit window means users can't escape a malicious upgrade. Size the delays together.
- Proof-system bugs exist in production. Kona's fallback proof system needed a 2026 security fix, and OP Succinct needed upstream fixes too. Multi-proofs and conservative upgrade paths reduce the blast radius.

## Sources (verified 2026-11-25)
Stages framework (ETHBEAT, formerly L2BEAT): forum.ethbeat.org/t/the-stages-framework/291, ethbeat.org/stages · Fusaka/PeerDAS/BPO: blog.ethereum.org/2025/11/06/fusaka-mainnet-announcement · OP Stack Upgrade 20 / Kona / OP Succinct: docs.optimism.io/notices/upgrade-20 · Arbitrum BoLD: theblock.co/post/340278 · ZKsync Airbender: zksync.io/airbender · Taiko preconfirmations: docs.taiko.xyz/protocol/preconfirmations.
