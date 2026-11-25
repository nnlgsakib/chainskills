---
name: protocol-randomness
description: Design secure randomness for any blockchain, independent of stack — choose and combine sources (in-protocol threshold BLS beacons via vote extensions, per-validator VRFs, commit-reveal, RANDAO/prevrandao, external beacons such as drand quicknet/evmnet, oracle VRFs such as Chainlink VRF v2.5), define unpredictability, bias resistance, liveness and verifiability requirements, and use randomness safely for leader election, committee and verifier selection, task assignment, sampling and lotteries (domain separation, stake-weighted sampling, commit-before-reveal ordering, reroll/abort protection, fallback when the beacon stalls). Use whenever the user needs random selection, lotteries, unpredictable committees, random audits or task assignment, VRF integration, or asks whether block hash/timestamp/prevrandao is safe.
license: MIT
---

# Protocol Randomness

A building-block skill in chainskills (layer L2, stack-neutral). Randomness is a dependency of consensus (leader election), staking (selection), verifiable participation (random task and audit assignment) and apps (lotteries). This skill designs the source and the rules for using it.

Inputs from `CHAIN.md`: the components that consume randomness, the trust assumptions, and the stack (if already chosen). Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/sources.md` | Choosing a randomness source; current facts per source |
| `references/usage-patterns.md` | Deriving values, weighted sampling, committee selection, reroll protection, fallbacks |

## Workflow

### 1. List the consumers and what an attacker gains
For each use, note what an attacker gains by predicting or biasing the value, and how much value is at stake. Leader election, verifier committees and high-value lotteries need strong guarantees. A UI shuffle doesn't.

### 2. State the required properties

| Property | Question |
|---|---|
| Unpredictability | Who could know the value before the inputs it affects are locked? |
| Bias resistance | Can any party influence it, including by withholding (e.g. the last revealer or proposer)? |
| Liveness | What happens if the beacon or oracle doesn't deliver on time? |
| Public verifiability | Can every node and contract verify the value cheaply? |
| Latency | How soon after the request must the value exist? |

### 3. Choose the source
Use `references/sources.md`. Rules of thumb:
- **Never** use block hash, timestamp or tx data alone for anything with value at stake.
- RANDAO/prevrandao: acceptable only when a single proposer's one-bit-per-slot bias doesn't matter, and with lookahead.
- In-protocol threshold BLS beacon (validators sign the round; any t of n produce a unique signature): the strongest option for a sovereign chain. It needs a DKG and key resharing on validator-set changes.
- External beacon (drand): strong and cheap to verify on-chain (BLS12-381 via the EIP-2537 precompile, or BN254 via evmnet), but it adds a trust assumption on the League of Entropy threshold and a liveness dependency.
- Oracle VRF (e.g. Chainlink VRF v2.5): per-request and simple for contracts. It has request–fulfil latency, trust in the oracle network, and fees.
- Combine sources, e.g. XOR a beacon with a commit-reveal, when no single party should be trusted. The combination is only as live as the least live input.

### 4. Define safe usage
Use `references/usage-patterns.md`:
- **Commit before reveal**: inputs (participants, bets, task lists) are locked *before* the randomness for that round exists.
- **Domain separation**: `seed = H(beacon_round_value || purpose || epoch || index)`.
- **No optional actions after the reveal**: whoever sees the value must not be able to choose whether to act on it (no free rerolls or aborts). Penalise non-reveal or non-action.
- **Deterministic sampling**: stake-weighted sampling and sampling without replacement are specified exactly, so every node gets the same committee.
- **Fallback**: if the source stalls, the protocol waits, skips with a defined rule, or falls back to a weaker source *with the degradation recorded*. It never silently uses block hash.

### 5. Hand off
To `design-spec`: component `RAND`, with parameters (`P-RAND-*`: round period, max wait, committee sizes), invariants (`INV-RAND-1`: no selection uses a round produced before its inputs were committed), and failure handling. Committee-size risk goes to `protocol-verifiable-participation` (its `committee_risk.py` computes the probability of a malicious committee). Then update `CHAIN.md`.

## Rules
- Randomness is consensus-critical whenever it decides who does what. Treat its source and derivation as consensus code.
- Every random choice is reproducible by every node from chain data.
- Assume anyone who can see the value early will use it.

## Sources (verified 2026-11-25)
drand: docs.drand.love/blog/2025/08/26/verifying-bls12-on-ethereum (quicknet BLS12-381 on EIP-2537 chains, evmnet BN254, gas comparison) · Chainlink VRF v2.5 (replaced V1/V2 on 29 Nov 2024; subscription and direct funding): docs.chain.link/vrf · EIP-7917 deterministic proposer lookahead: eips.ethereum.org/EIPS/eip-7917.
