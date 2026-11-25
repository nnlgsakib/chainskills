# Design pitfalls

Check each pattern. If it applies: change the design, or record a K-risk with mitigation and owner skill.

## Contents
- Consensus and validators
- Incentives and economics
- Randomness and selection
- Participation layers and sybils
- Rollups and bridges
- Governance and keys
- Data, state, performance
- Process

## Consensus and validators
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Expecting BFT to stay live with > 1/3 offline | Impossible: BFT needs > 2/3 online to finalise | State "halts, safety preserved"; plan recovery runbook |
| Unbounded or very large BFT validator set | Message cost ~n², block time grows | Cap the active set; let others participate in other roles |
| No long-range attack defence in PoS | Old keys with unbonded stake can rewrite history for new nodes | Unbonding period > weak-subjectivity window; checkpoints / trusted sync |
| Selection by performance without a deterministic, on-chain metric | Nodes disagree on who is in the set → fork | Metrics derived only from on-chain data (signed blocks, missed votes) |
| Validator concentration on one cloud/provider/jurisdiction | Correlated failure > 1/3 | Diversity requirements, monitoring, possibly caps |
| Delegation flows to top validators | Power concentration | Voting-power caps, commission floors, UI nudges |

## Incentives and economics
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Rewarding unverifiable work (self-reported uptime, bandwidth, storage) | Sybils fake it | Reward only challenge-verified or proven work |
| Fixed APY promises | Becomes unpayable or hyperinflationary | Rewards as share of a bounded issuance budget |
| Security paid only by inflation, no fee capture | Security budget falls as token price falls | Fee burn/redistribution; model in tokenomics |
| Hard-coded reward percentages | Can't adjust after launch | Governable parameters with bounds |
| Rewards credited per block per account with loops | State bloat and unbounded gas | Lazy accounting (reward-per-share accumulators) |

## Randomness and selection
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Block hash / timestamp as randomness | Proposer can grind or withhold | VRF, threshold-BLS beacon, commit-reveal with penalties |
| Committee known in advance | Targeted bribery/DoS | Unpredictable selection revealed at use time |
| Selection without stake weighting or sybil cost | Attacker spins identities to dominate committees | Weight by stake/bond; minimum bond per identity |

## Participation layers and sybils
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Community/verifier reports trusted directly | Collusion and fake reports | Redundant assignment, challenges, slashing on provable fraud |
| Verifier "lazy copying" (copying others' answers) | Verification adds nothing | Commit-reveal, unique per-node tasks, spot checks with known answers |
| Extra layer on the consensus critical path | Its outages halt the chain | Keep it off the finality path; failures degrade rewards only |
| Penalising honest-but-offline home nodes like attackers | Drives away the target users | Separate "missed work" (lower reward) from "provable fraud" (slash) |

## Rollups and bridges
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Single sequencer, no forced inclusion | Censorship; "L2" without L2 guarantees | Forced inclusion via L1; plan sequencer decentralisation |
| Upgradeable L1 contracts with no delay | Upgrader can steal funds | Timelock longer than exit window; security council |
| Multisig bridge with few keys | Largest historic exploit category | Light-client / proof-based bridges; rate limits; caps |
| DA assumption unstated | Funds stuck if data withheld | State DA choice and exit path explicitly |

## Governance and keys
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| "Decentralised" but admin keys can change anything | Misleading users; key compromise = total loss | Document powers; multisig + timelock; sunset plan |
| Low quorum governance | Cheap capture | Quorum + threshold + deposit; veto; timelock |
| Emergency powers with no expiry | Permanent backdoor | Sunset date or block height; scoped to pause |

## Data, state, performance
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| State grows forever, free to write | Node costs rise until only big operators remain | Deposits, rent, or pruning-friendly design |
| Every node must store all history | Excludes home hardware | Snapshots/state sync; history served by archive/DA roles |
| Performance targets without a benchmark plan | Numbers become marketing | Define benchmark scenarios early (quality-testing) |
| Non-determinism (floats, wall clock, map order, local config) | Consensus failure | Determinism rules in the spec |

## Process
| Pitfall | Why it bites | Fix direction |
|---|---|---|
| Choosing the framework first | Requirements bent to fit the tool | Design → spec → stack selection |
| Novel mechanism mixed into every component | Unauditable | Isolate novel parts behind interfaces |
| No written trust assumptions | Nobody knows what the system guarantees | Architecture doc section, reviewed by security |
