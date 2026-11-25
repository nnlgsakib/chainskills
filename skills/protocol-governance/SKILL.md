---
name: protocol-governance
description: Design on-chain governance for any chain or protocol, independent of stack — what is governable (bounded parameters, software upgrades, treasury, emergency actions), voting-power models (stake-weighted with delegation, token-weighted with checkpoints, multi-house/role-based, councils, custom tally functions), proposal lifecycle (deposits, voting delay and snapshot, voting period, quorum, thresholds, veto, expedited proposals, late-quorum protection, timelocks), treasury controls, emergency powers and Security Councils with scope, threshold and sunset, defences against vote-buying, flash-loan and low-turnout capture, and tooling (Cosmos x/gov, OpenZeppelin Governor + Timelock, Snapshot with on-chain execution). Use whenever the user designs DAO or chain governance, upgrade processes, treasury spending, quorum/threshold parameters, a security council, emergency pause powers, or a path to decentralization.
license: MIT
---

# Protocol Governance

A building-block skill in chainskills (layer L2, stack-neutral). Governance decides who can change the system and how fast. Every privileged capability in other components (`P-*` parameters, upgrades, treasury, pause) must map to a governance path defined here.

Inputs from `CHAIN.md`: components with privileged operations, the parameter registry (`docs/spec/parameters.md`), roles (stakers, token holders, service nodes, team), and the decentralization goals. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/mechanisms.md` | Choosing the voting-power model, lifecycle parameters and tooling |
| `references/attacks.md` | Reviewing capture and abuse scenarios |
| `references/emergency-powers.md` | Designing a Security Council or pause powers, and their sunset |

## Workflow

### 1. Inventory the powers
List every privileged action across the specs: parameter changes (within which bounds), software upgrades, contract upgrades, treasury spends, minting, adding or removing validators (PoA), pause, freezing funds. For each, record its blast radius (what's the worst it can do?) and the urgency it might need.

### 2. Assign each power a path
- **Normal governance** for most things.
- **Expedited path** for time-sensitive but non-emergency changes, with a higher threshold.
- **Emergency path** (council or multisig) only for narrowly scoped, published actions such as pause or blocking an exploit, with a mandatory after-action report.
- **No path** (immutable) where the safest choice is "nobody can change this".
- **Delay** before execution must exceed the time users need to exit (unbonding for stakers, withdrawal windows for bridges and rollups).

### 3. Voting power
Use `references/mechanisms.md`. Options: stake-weighted (validators vote by default for delegators, who can override), token-weighted with checkpoints (power snapshotted at proposal start), multi-house (e.g. a stakers' house plus a service-operator or user house that can veto), councils, or custom tally functions. Cosmos SDK v0.54+ lets `x/gov` use a custom `CalculateVoteResultsAndVotingPowerFn`, so power can come from sources other than staking. Avoid quadratic or one-person-one-vote unless sybil resistance is real (`protocol-verifiable-participation` → sybil.md).

### 4. Lifecycle parameters
Deposit, voting delay (with the snapshot taken at proposal creation or earlier), voting period, quorum, threshold, veto threshold, expedited settings, late-quorum extension, timelock delay, and execution window. Make them all `P-GOV-*` with bounds, and decide whether governance can change its own parameters (and under what extra conditions).

### 5. Treasury controls
Spending caps per period, streaming payments instead of lump sums, recipient milestones, rate limits, and a separate small-grants path. Large or unusual spends need a higher threshold and a longer delay.

### 6. Attack review
Walk `references/attacks.md`. The 2026 governance exploits used **bought** voting power held across days, not flash loans. Defences have to cover patient capital as well: delays, vetoes, spending caps and turnout-aware quorums.

### 7. Decentralization path
Publish a staged plan. Launch powers (team multisig, council) shrink on dates or milestones, with each step recorded as an ADR. Rollups align this with the Stages framework (`protocol-rollup` → stages.md: a Security Council of at least 8 members at 75%, and upgrade delays of at least 5 days for Stage 1 or at least 30 days for Stage 2).

### 8. Hand off
To `design-spec`: component `GOV`, with proposal and vote state, operations, hooks (tally at the end of the period, execution queue), parameters and invariants:
- `INV-GOV-1` no proposal executes before `voting_end + timelock`
- `INV-GOV-2` voting power is read at the snapshot point, never at vote time
- `INV-GOV-3` each privileged operation in other components accepts only the governance or authorised emergency executor
- `INV-GOV-4` treasury spends in a period ≤ the cap

Implementation: Cosmos `x/gov` (stack adapter), or OpenZeppelin Governor + TimelockController + ERC20Votes (`build-smart-contracts`).

## Rules
- Every power has an owner, a path, a delay and a public record. Undocumented admin keys are a security finding.
- Execution delay ≥ the users' exit time.
- Emergency powers are narrow, threshold-protected, reported afterwards, and sunset.
- Don't depend on one hosted governance UI. Keep a self-hostable frontend or CLI path, because Tally announced its shutdown in Mar 2026.

## Sources (verified 2026-11-25)
Cosmos x/gov (custom tally function since v0.53 and required in v0.54; expedited proposals): docs.cosmos.network/sdk/latest/modules/gov · OpenZeppelin 5.7 Governor changes: openzeppelin.com/news/introducing-openzeppelin-contract-5-7 · Arbitrum Security Council (12 members, 9/12 for emergencies, two-year terms from Mar 2026, Apr 2026 KelpDAO-exploiter freeze): docs.arbitrum.foundation/concepts/security-council, forum.arbitrum.foundation · Governance attacks 2026 (BonkDAO, Term Finance): crypto.news, sentora.com · Tally shutdown: theblock.co/post/394026.
