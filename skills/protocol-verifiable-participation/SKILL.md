---
name: protocol-verifiable-participation
description: Design permissionless participation layers where nodes earn rewards only for verifiable work — community/verifier nodes, DePIN-style networks, relay and bandwidth providers, storage and data-serving nodes, data availability samplers, re-execution verifiers, oracles and keepers — covering the verifiability ladder (cryptographic proofs, fraud proofs, challenge-response, known-answer spot checks, witnesses), assignment–commit–reveal–challenge–settle protocols, claims-and-proofs with probabilistic auditing, lazy-verifier and collusion defences, sybil resistance (bonds, work-proportional rewards, hardware attestation, proof of personhood), deterrence economics, and keeping the layer off the consensus critical path. Use whenever the user wants to reward nodes for services, add community or light nodes with real duties, prevent fake nodes, design audits or challenges, or asks how to prove that work was actually done.
license: MIT
---

# Protocol Verifiable Participation

A building-block skill in chainskills (layer L2, stack-neutral). It designs any layer where many, possibly unreliable, possibly malicious participants provide services and get paid. The main rule: **pay only for work that can be verified, and price cheating out with detection probability × penalty.**

Inputs from `CHAIN.md`: node roles, the services they provide, trust assumptions, the reward budget (from `protocol-tokenomics`), the randomness source (`protocol-randomness`). Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/work-types.md` | Per-service verification methods, with real-world examples |
| `references/protocol-template.md` | Writing the assignment → commit → reveal → challenge → settle state machine |
| `references/sybil.md` | Preventing one operator from posing as many |
| `scripts/committee_risk.py` | Sizing committees and penalties |

## Workflow

### 1. Define each service as measurable work
For each service (verify blocks, serve history, sample DA, relay txs, store data, compute), write down the **unit of work**, **who benefits**, **how much it's worth**, and **what cheating looks like** (not doing it, faking it, copying others, or colluding).

### 2. Place each service on the verifiability ladder
1. **Cryptographic proof**: signatures, Merkle proofs, SNARKs, storage proofs. Pay directly.
2. **Deterministic re-check**: anyone can re-execute, and fraud proofs can slash. Pay after the challenge window.
3. **Challenge-response / spot checks**: random audits, known-answer ("canary") tasks. Pay with probabilistic audits.
4. **Witness attestations**: other nodes vouch. Collusion-prone, so use it only with diversity requirements and bonds.
5. **Self-reported**: uptime, bandwidth or resource claims. **Never pay on these.**

If a service is only at rung 4–5, redesign the service or don't reward it.

### 3. Choose the protocol shape
Use `references/protocol-template.md`. The usual shape:
- **Register**: bond and keys.
- **Assign**: tasks assigned from unpredictable randomness, after registration is locked.
- **Commit**: hash of the result.
- **Reveal**: the result itself.
- **Compare or audit**: compare reveals, or audit them.
- **Challenge window**.
- **Settle**: pay rewards or slash.

A variant is **claims and proofs**: a node claims aggregate work (a Merkle root), and the protocol requires a proof for a random subset. Pocket Network's relay mining (Shannon) does this, with a claim window, a proof window, probabilistic proof requirements, and forfeiture or slashing on failure.

### 4. Defend against lazy and colluding participants
- Commit-reveal stops copying other nodes' answers.
- Unique or salted tasks per node, where possible.
- Known-answer canary tasks, injected at a published rate, catch nodes that "always say valid".
- Redundant assignment (k of n), with disagreement triggering escalation to a larger committee or on-chain re-execution.
- Committee size from `scripts/committee_risk.py`.

### 5. Price cheating out
For each cheat, use deterrence: `penalty × P(detect) > gain from cheating`. Run `python3 scripts/committee_risk.py deterrence --gain G --audit-rate p --tasks n` to get the minimum penalty. Bonds must cover the maximum penalty.

### 6. Separate absence from fraud
Home and consumer nodes disconnect. Missing work means **no reward** (and optionally slowly decaying reputation or assignment weight). **Provable fraud** means slashing. Never slash for being offline, or the target participants will leave.

### 7. Sybil resistance
Use `references/sybil.md`. The default: rewards proportional to verified work (not to the number of identities), plus a bond per identity sized so splitting gains nothing.

### 8. Keep it off the critical path
The participation layer must not be needed for block finality unless the architecture explicitly says so (see `protocol-consensus`). Its failure reduces rewards and extra assurance only.

### 9. Hand off
To `design-spec`: component `PART` (or one per service), with state (registry, assignments, commitments, claims, challenges), operations, epoch hooks with bounded work, parameters (`P-PART-*`: bond, audit rate, committee size k, windows, penalties) and invariants:
- `INV-PART-1` rewards paid in an epoch ≤ the epoch's budget
- `INV-PART-2` every paid unit of work has a verification record (proof, unchallenged reveal, or passed audit)
- `INV-PART-3` no node is assigned a task whose randomness round precedes its registration lock
- `INV-PART-4` slashed amount ≤ the bonded amount

Off-chain client work → `build-node-software`. On-chain registry and settlement → module or contracts via `design-stack-selection`.

## Sources (verified 2026-11-25)
Pocket Network Shannon relay mining (claims, probabilistic proofs, windows, v1.31 difficulty fix): docs.pocket.network/protocol/sessions-claims-proofs, forum.pokt.network PNF Q4 2025/Jan 2026 report · Filecoin PoRep/PoSt: docs.filecoin.io/basics/the-blockchain/proofs · Celestia DAS (light nodes take ≥ 16 samples per block): forum.celestia.org/t/celestia-das-reconstruction-simulations-and-light-node-requirements/1891 · DePIN coverage verification and spoofing issues: arxiv.org/pdf/2609.02125 · Human Passport (formerly Gitcoin Passport, acquired by Holonym, Feb 2025): human.tech/blog.
