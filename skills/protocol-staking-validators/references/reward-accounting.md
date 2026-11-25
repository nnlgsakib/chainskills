# Reward and slash accounting (O(1) per operation)

Goal: any number of delegators, with no loops over them, ever. Two standard patterns: validator **exchange rate** (shares ↔ tokens) for slashing, and a **reward-per-share accumulator** for rewards. Cosmos's F1 distribution is a production variant of the second.

## Notation
`SCALE` = 10^18 or higher (fixed point). All divisions round DOWN unless stated, and remainders (dust) stay in the pool.

## Validator exchange rate (handles slashing)

```
validator v:
  tokens        : Amount   # bonded tokens incl. self-bond
  total_shares  : Dec

delegate(d, v, amount):
  shares := (v.total_shares == 0) ? amount * SCALE
                                  : amount * v.total_shares / v.tokens      # round DOWN
  v.tokens += amount ; v.total_shares += shares ; d.shares[v] += shares

value(d, v) = d.shares[v] * v.tokens / v.total_shares                       # round DOWN

slash(v, fraction):                     # applies to all delegators at once
  burned := v.tokens * fraction          # round UP (protocol favour)
  v.tokens -= burned
```

Pitfall: a validator with `tokens == 0` and `total_shares > 0` (fully slashed) must block new delegations, or the exchange rate divides by zero. Treat it as inactive.

## Reward-per-share accumulator (handles rewards)

```
validator v:
  acc        : Dec     # cumulative reward per share, scaled by SCALE
  commission : Ratio

on_reward(v, R):                         # called once per block or epoch per validator
  c       := R * v.commission            # round DOWN
  v.owed_commission += c
  v.acc   += (R - c) * SCALE / v.total_shares   # round DOWN; remainder carried as v.dust

delegation (d, v):
  shares, reward_debt                     # reward_debt = shares * acc / SCALE at last settle

pending(d, v)  = d.shares * v.acc / SCALE - d.reward_debt
settle(d, v)   : pay pending ; d.reward_debt = d.shares * v.acc / SCALE
# Call settle() before ANY change to d.shares (delegate, undelegate, redelegate).
```

How it combines with slashing: rewards are paid in tokens and slashing changes the exchange rate. Cosmos F1 tracks "periods" per validator so the two interact correctly. If you implement it yourself, include slashes in period boundaries or rewards will be over-paid after a slash.

## Distributing a block's reward across validators
Total reward R per block → each active validator by voting power (or by its signed share of the block). One loop over the **active set** (bounded by `max_validators`) per block is fine. Loops over delegators are not.

## Unbonding entries
Store `{delegator, validator, creation_height, initial_balance, balance, completion_time}`. On slash for an infraction at height h, reduce every entry with `creation_height ≥ h` (that stake was bonded when the fault happened), up to the slash fraction. Process completions from a time-ordered queue, bounded per block.

## Invariants to test
- Σ value(d, v) over all d ≤ v.tokens (equality up to dust)
- Σ paid rewards + Σ pending + dust == Σ rewards distributed − commission
- A slash never increases anyone's value
- settle() is idempotent within a block
