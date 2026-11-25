---
name: protocol-consensus
description: Design the consensus layer of any blockchain, independent of stack — choose the consensus family (Tendermint/CometBFT-style BFT, HotStuff, DAG-based, Ethereum Gasper, Avalanche Snowman, Solana Alpenglow, Polkadot BABE+GRANDPA, PoA/QBFT, Nakamoto PoW, rollup sequencing incl. based and shared sequencers), set validator count, block time and finality targets, define safety/liveness guarantees and halt behaviour, proposer selection, transaction ordering and MEV/censorship policy, and review against known attacks. Use whenever the user asks how blocks get produced or finalised, which consensus to use, block time/finality/throughput trade-offs, validator set size, MEV, censorship resistance, inclusion lists, sequencers, or what happens when validators go offline.
license: MIT
---

# Protocol Consensus

A building-block skill in chainskills (layer L2, stack-neutral). It produces the consensus design. `design-spec` turns that design into `docs/spec/consensus.md`, and a `stack-*` adapter implements it, usually by configuring an existing engine rather than writing one.

Inputs from `CHAIN.md`: R-N targets (block time, finality, throughput), validator count and hardware, trust assumptions, architecture class. Shared-state rules are in `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/families.md` | Choosing or comparing consensus families |
| `references/attacks.md` | Step 6, the attack review |
| `references/ordering-mev.md` | Step 5, ordering, MEV, censorship resistance |

## Workflow

### 1. Pin the requirements
Turn the requirements into these answers. Mark anything assumed as `(assumed)`.
- **Finality type**: deterministic (BFT, final after one block or round) or probabilistic/economic (Nakamoto, Gasper's two-epoch finality)?
- **Who participates**: permissioned set, stake-weighted permissionless set, or a single or shared sequencer (rollups)?
- **Set size now and later**: BFT message cost grows roughly with n², so this drives block time.
- **Network model**: partial synchrony is the standard assumption for BFT. Write down the expected geographic spread and latency between validators.
- **Throughput and latency**, as p50/p95 targets.

### 2. Choose the family
Use `references/families.md`. Start from proven engines. Writing a consensus protocol from scratch is almost never justified, and the custom parts of most chain ideas sit around consensus, not inside it. Record the choice as an ADR with the alternatives you rejected.

### 3. Set parameters
- Active validator count and its cap.
- Block interval and timeout schedule. Most BFT engines use per-round timeouts that increase after failed rounds.
- Proposer selection: round-robin weighted by stake, or randomized. If randomized, the source comes from `protocol-randomness`.
- Block limits: bytes, gas, number of txs. Also budget the size of votes and signatures. Post-quantum signatures are much larger: ML-DSA-65 is 3309 bytes versus 64 for ed25519, and CometBFT v0.40 raised its signature size limits for this.
- Vote extensions or other per-vote payloads, if the design needs them (oracles, randomness, attestations from other roles). They add bytes to every vote.

### 4. State the guarantees explicitly
Write these into the spec:
- **Safety**: e.g. "no two conflicting blocks are finalised while < 1/3 of voting power is Byzantine".
- **Liveness**: e.g. "new blocks are finalised while > 2/3 of voting power is online and honest and the network is synchronous".
- **Halt behaviour**: what happens when liveness is lost (BFT halts, it does not fork), and the recovery procedure (coordinated restart, governance or social layer). This is a requirement for `ops-infrastructure` runbooks.
- **Extra layers** (verifier committees, service operators, oracles, DA samplers) are off the finality path unless the design explicitly says otherwise. If they go offline, rewards drop but the chain doesn't halt.

### 5. Ordering, MEV, censorship
Decide using `references/ordering-mev.md`: mempool visibility, builder/proposer separation, priority ordering, inclusion guarantees (forced inclusion, inclusion lists), and whether MEV revenue is captured or redistributed. Ordering rules that affect state must be deterministic and checkable by every validator.

### 6. Attack review
Walk `references/attacks.md`. For each attack, record the mitigation or add a K-risk to `CHAIN.md`.

### 7. Hand off
- To `design-spec`: consensus parameters (`P-CONS-*`), invariants (e.g. `INV-CONS-1`: at most one finalised block per height), validator lifecycle hooks shared with `protocol-staking-validators`.
- To `quality-testing`: benchmark scenarios covering n validators, the latency matrix, block size, the target p95, validator churn, partitions, and recovery from more than 1/3 going offline.
- Update `CHAIN.md`: consensus component status → `designed`, plus ADRs.

## Rules
- Safety over liveness, always stated. A BFT chain with more than 1/3 offline must halt, not fork.
- Every consensus-affecting input (time, randomness, ordering, validator set) is derived deterministically from chain data.
- Don't put unreliable participants (home nodes, optional committees) on the critical path to finality.
- Benchmark before promising numbers. Block time and finality depend on set size, geography, block size and execution cost.

## Sources (verified 2026-11-25)
CometBFT v0.40 and post-quantum signature limits: docs.cosmos.network/sdk/latest/upgrade/v0.55. Ethereum Glamsterdam (ePBS, EIP-7732, expected Q4 2026) and Hegotá (FOCIL, EIP-7805, expected Q2 2027): ethereum.org/roadmap. Solana Alpenglow Votor live since 21 Oct 2026: solana.com/upgrades/alpenglow. Malachite: github.com/circlefin/malachite. Full links are in each reference file.
