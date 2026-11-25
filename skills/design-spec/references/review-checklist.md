# Spec review checklist

A component is `specified` only when every item is satisfied or recorded as a Q-item.

## Completeness
- [ ] Every requirement listed in the header is covered by at least one operation, hook or invariant.
- [ ] Every stored entity has type, key, writer and size bound.
- [ ] Every operation has auth, numbered checks with errors, ordered effects, events, cost.
- [ ] Every entity with a status has a lifecycle diagram; every transition has a trigger and guard.
- [ ] Every parameter has default, bounds, unit, who changes it and what a runtime change does.
- [ ] Every interaction with another component lists failure handling.

## Correctness
- [ ] At least one invariant per stored aggregate (sums, counts, pool balances).
- [ ] Invariants hold after every op and hook (walk through each mentally; note doubtful ones).
- [ ] Value conservation: every transfer has a source and a destination; mint/burn explicit and authorised.
- [ ] Every division has rounding direction and dust destination.
- [ ] No operation can make an `Amount` negative.

## Determinism
- [ ] No floats, wall clock, local config, external calls, unordered iteration.
- [ ] Ties in sorting have a secondary key.
- [ ] Randomness source named and owned by protocol-randomness.

## Bounds and DoS
- [ ] Every loop (op or hook) has a bound tied to a parameter or input length.
- [ ] Per-block/per-epoch hooks cannot be made expensive by users (or users pay for it).
- [ ] Creating state costs something (fee, deposit, bond) or is rate-limited.
- [ ] Queries are paginated or bounded.

## Security
- [ ] Privileged operations name the authority and how it is controlled (gov, multisig, timelock).
- [ ] Every role's possible misbehaviour listed in section 12 with a response.
- [ ] No reliance on an actor reporting its own performance without verification.
- [ ] Reentrancy / callback order considered where components call each other.
- [ ] Front-running / ordering sensitivity considered for value-moving ops.

## Testability
- [ ] Acceptance criteria cover happy paths and every check (C-n) failing.
- [ ] Invariants are phrased so they can be asserted in code.
- [ ] IDs (R, INV, P) are stable and unique across the project.
