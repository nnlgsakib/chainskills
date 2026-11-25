# Property catalogue

Pick the properties that apply, rename them to your spec IDs, and model the adversary explicitly.

## Consensus / validator rotation (custom rules)
- **Agreement (safety)**: no two honest nodes finalise different blocks at the same height, while Byzantine power < 1/3.
- **Validity**: finalised blocks satisfy the validity predicate.
- **Liveness (temporal)**: under partial synchrony after GST with > 2/3 honest and online, every height is eventually finalised.
- **Set update safety**: every node uses the same validator set for height h; no gap or overlap at epoch boundaries.
- **Accountability**: a safety violation implies provable equivocation by ≥ 1/3 of voting power.

## Staking / rewards / slashing
- Conservation: Σ liquid + Σ bonded + Σ unbonding = genesis + minted − burned.
- Pool consistency: bonded pool balance = Σ validator tokens.
- Non-negativity: no balance, share or bond goes below zero.
- Slash bound: slashed ≤ the stake at risk; unbonding entries after the infraction are slashed.
- Reward bound: rewards paid per period ≤ the budget.
- Exchange-rate monotonicity: a slash never increases any delegator's value.

## Participation / verification layer
- Pay only verified work (every payout has a verified record).
- Assignment unpredictability: no assignment uses a randomness round produced before the registration lock.
- No double commit; reveal must match its commit.
- Bond release only after every slashable window has closed.
- Liveness separation: absence never causes slashing (only provable fraud does).

## Bridge / light client / rollup
- Supply backing: L2 supply of a bridged asset ≤ L1 escrow.
- No double withdrawal: each withdrawal is finalised at most once.
- Message authenticity: accepted messages were committed on the source chain (under the light-client trust assumption).
- Dispute game: an honest challenger with sufficient bond and time always wins against an invalid claim (within the game's bounds).
- Forced inclusion: a tx submitted via L1 is included within the bound.

## Governance / timelock
- No execution before `voting_end + timelock`.
- Voting power read at the snapshot; transfers after the snapshot don't change the tally.
- Emergency executor restricted to the allowlist.
- Treasury spends per period ≤ the cap.

## Token
- Total supply rule (cap, issuance formula bound per period).
- Locked vesting amounts are non-transferable.
