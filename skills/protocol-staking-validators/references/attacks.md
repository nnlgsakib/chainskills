# Staking attack review

| Attack | Mechanism | Mitigation |
|---|---|---|
| Unbond-before-slash | Misbehave, then unbond before evidence lands | Unbonding ≥ evidence window; slash unbonding entries created at/after the infraction height |
| Redelegation escape | Redelegate away from a validator about to be slashed | Redelegations stay slashable for the source validator's past infractions; limit redelegation chains |
| Long-range | Old unbonded keys rewrite history for new nodes | Unbonding > weak-subjectivity period; trusted checkpoints for sync |
| Stake grinding | Manipulate selection randomness or timing to win slots | Selection from committed stake snapshots + unpredictable randomness (protocol-randomness) |
| Cartel / concentration | Few operators control > 1/3 or > 2/3 | Caps, Nakamoto coefficient monitoring, delegation incentives, diversity rules |
| Sybil splitting | One operator runs many validators to bypass caps | Identity/diversity disclosures, minimum self-bond per validator, accept and monitor |
| Commission bait-and-switch | Low commission to attract stake, then raise it | Max change rate per day; max commission |
| Slashing griefing | Framing a validator with forged evidence | Evidence verified cryptographically on-chain; no slashing on unverifiable reports |
| Redistribution abuse | Slash to profit from redistributed funds | Objective proofs only, delay + veto window, burn by default (see slashing.md) |
| Key compromise | Stolen consensus key double-signs | Remote signer/HSM, rate-limited key rotation, monitoring for equivocation |
| Reward rounding drain | Many tiny delegations exploit rounding up | Round down on payouts, minimum delegation amount, dust to pool |
| Hook DoS | Users create many tiny entries that end-of-block processing must handle | Bounded queues per block, deposits, minimum amounts |
