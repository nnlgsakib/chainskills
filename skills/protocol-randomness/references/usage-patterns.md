# Using randomness safely

## Timeline rule

```
inputs locked (epoch e)  →  randomness for round r(e) produced  →  selection computed  →  actions
      ^ must happen strictly before ^
```

Bind each use to a **future** round number that is fixed when inputs are locked: `round = locked_at_round + P-RAND-delay`. Never use "the latest available round" at selection time, because someone can wait for a favourable one.

## Derivation

```
seed(purpose, epoch, i) = H( beacon[round] || "chain-id" || purpose || epoch || i )   # H = sha256 / keccak256
```

- `purpose` is a fixed domain tag (`"LEADER"`, `"VERIFIER_COMMITTEE"`, `"AUDIT"`, `"LOTTERY"`), so one value can't be reused across purposes.
- Draw as many values as needed by incrementing `i`.
- To map to `[0, n)` without modulo bias, use rejection sampling: draw `x`; accept if `x < floor(2^256 / n) * n`; return `x mod n`.

## Stake-weighted selection (deterministic)

```
candidates sorted by (id bytes) ascending
cum[k] = Σ_{j ≤ k} weight[j]                       # integer weights (stake), total W
pick(i): r = uniform(seed(purpose, epoch, i), W);  return first k with cum[k] > r   # binary search
```

Without replacement: after picking k, remove it and recompute (O(n) per pick for small n), or use a Fenwick tree. Specify which one, because both must be identical on every node.

Cap the influence of a single identity (max weight per candidate) if a sybil split would otherwise change the outcomes.

## Committee selection
- Committee size `k` from the tolerated failure probability: `protocol-verifiable-participation/scripts/committee_risk.py` computes P(≥ threshold malicious members) for N candidates with fraction f malicious.
- Reveal membership as late as possible (just before the work), so members can't be targeted or bribed early.
- Rotate every epoch. Never reuse a seed for a new committee.

## Reroll and abort protection
- Users must not be able to cancel after seeing a result (lotteries, games): settle automatically, or charge the cost of a cancel.
- Committee members who don't act after selection forfeit rewards (offline) or bonds (if non-action is strategic and provable).
- Proposers who withhold beacon contributions are penalised (in-protocol beacons).

## Fallbacks (choose one per use and write it in the spec)
1. **Wait**: delay the dependent action until the round exists, up to `P-RAND-max_wait`.
2. **Skip**: no selection this epoch, and the previous committee continues (bounded number of epochs).
3. **Degrade**: use a weaker source with an explicit event `RandomnessDegraded(epoch, source)` and reduced stakes (e.g. no slashing decisions that epoch).

## Tests
- Determinism: the same chain state gives the same selection across implementations and platforms.
- Distribution: chi-square over many seeds against expected stake weights.
- Timing: selection fails if the requested round precedes the input lock.
- Fallback paths exercised.
