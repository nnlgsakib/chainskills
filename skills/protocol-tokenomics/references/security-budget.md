# Security budget

## Cost to attack (PoS)

```
cost_to_halt     ≈ price × bonded_supply × 1/3      (acquire > 1/3 stake: stop finality)
cost_to_rewrite  ≈ price × bonded_supply × 2/3      (acquire > 2/3: finalize conflicting history; slashable)
```

Compare against **value at risk**: bridged assets, DeFi TVL, the value of censoring or halting. If `cost_to_halt` is less than the attacker's plausible gain, the chain isn't secure at that price. Check at pessimistic prices (−80%).

Notes:
- Stake can't be bought instantly (liquidity, unbonding), but liquid-staking tokens and lending markets make it easier. Include them.
- Delegated stake concentrates. Effective cost is set by the stake needed to control the top validators, so use the Nakamoto coefficient.

## Required yield

Stakers need `nominal_yield − net_inflation ≥ opportunity_cost + risk_premium` (slashing, illiquidity during unbonding).

```
nominal_yield = (issuance × staker_share + fees_to_stakers) / bonded_supply
real_yield    = nominal_yield − net_inflation
```

If the target bonded ratio requires a real yield above what issuance plus fees can pay sustainably, change the design: lower the target, add fee capture, or borrow security.

## Fee transition
Plot `fees_to_stakers / (issuance × staker_share)` over time. A sustainable chain trends toward fees carrying a growing part of the security budget. If issuance must stay high forever, say so publicly and justify it.

## Service-layer budget
For the community/service share, compute reward per unit of verified work and per node at expected and 10× participation. Make sure honest operators can cover their costs (hardware, bandwidth, power) at the pessimistic price. Otherwise only subsidised or fake nodes remain.

Use `scripts/emission_sim.py` for the numbers.
