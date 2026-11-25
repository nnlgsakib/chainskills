# Governance mechanisms

Facts checked 2026-11-25 are marked ✔.

## Voting-power models

| Model | How | Pros | Cons | Implementations |
|---|---|---|---|---|
| Stake-weighted with inheritance | Bonded stake votes; validators' votes count for their delegators unless delegators override | aligns with security; high default turnout | validators dominate passive delegators | Cosmos `x/gov` default tally ✔ |
| Custom tally | Chain-defined voting power and result function | multi-source power (stake + role + reputation) | complexity, novel attack surface | Cosmos SDK `CalculateVoteResultsAndVotingPowerFn` (optional in v0.53, required constructor argument in v0.54+, with `NewDefaultCalculateVoteResultsAndVotingPower(stakingKeeper)` for the default) ✔ |
| Token-weighted with checkpoints | ERC20Votes snapshots at proposal start; delegation to self or a delegate | standard EVM tooling | plutocracy; vote buying | OpenZeppelin Governor + TimelockController ✔ |
| Multi-house / bicameral | Separate houses (stakers, service nodes, users) must both approve, or one can veto | balances interest groups | slower; house definition needs sybil resistance | custom (tally function or multiple Governors) |
| Council / multisig | Elected or appointed members, M-of-N | fast | centralised; needs elections, terms, scope | Safe multisig; Arbitrum Security Council 12 members ✔ |
| Optimistic governance | Proposals pass unless vetoed | low voter fatigue | needs an active veto group | Cosmos ADR-069 describes optimistic proposals, but they're not in the current `x/gov` module docs, so don't assume they're available ✔ |
| Off-chain signalling + on-chain execution | Snapshot votes, executed by a Safe module or trusted executor | gasless voting | the execution bridge is a trust point | Snapshot (most-used off-chain tool) ✔ |

## Lifecycle parameters (decide all, publish all)

| Parameter | Guidance |
|---|---|
| Proposal deposit / threshold | High enough to deter spam; refunded unless vetoed (Cosmos burns on veto or if the minimum deposit isn't reached ✔) |
| Voting delay + snapshot | Power snapshotted at or before proposal creation. Gives time to review payloads |
| Voting period | Long enough for global participation (days). Short periods favour attackers |
| Quorum | % of eligible power. Too low means capture; too high means paralysis. Consider quorum based on circulating or delegated supply |
| Threshold | e.g. > 50% of non-abstain Yes. Higher for constitutional changes |
| Veto | Cosmos `NoWithVeto` > 1/3 fails the proposal and burns deposits ✔ |
| Expedited | Shorter period, higher threshold; if it fails, it converts to a regular proposal ✔ (Cosmos) |
| Late-quorum protection | Extend voting if quorum is reached late. OpenZeppelin 5.7 caps the extension at `_maxLateQuorumVoteExtension` (default `votingPeriod()`) ✔ |
| Timelock | ≥ users' exit time. Proposals in the queue are public |
| Execution window | Expired proposals can't be executed later |

## Tooling notes (2026-11-25)
- **Tally** (a widely used on-chain governance UI) announced its shutdown on 17 Mar 2026 ✔. Don't make a hosted UI a single point of failure: keep a self-hostable frontend, a CLI, and documented contract calls.
- **Snapshot** remains the default off-chain voting tool. Votes don't bind on-chain without an execution module ✔.
- **OpenZeppelin Governor** 5.7: `GovernorCrosschain` for cross-chain execution; Governor queue errors changed ✔.

Sources: https://docs.cosmos.network/sdk/latest/modules/gov/README.md · https://docs.cosmos.network/main/build/architecture/adr-069-gov-improvements · https://www.openzeppelin.com/news/introducing-openzeppelin-contract-5-7 · https://www.theblock.co/amp/post/394026/ethereum-governance-solution-tally-uniswap-arbitrum-others-winding-down · https://docs.arbitrum.foundation/concepts/security-council
