# Question bank

Ask only what changes the architecture. Offer a default with every question.

## Contents
- Purpose and users
- Security and trust
- Validators and participation
- Performance
- Execution and contracts
- Economics
- Interoperability
- Governance and upgrades
- Data and storage
- Team, time, money, law

## Purpose and users
| Question | Why it matters | Typical default |
|---|---|---|
| What can users do on the chain that they can't do on an existing chain? | Decides whether a new chain is justified at all | — (must answer) |
| Who are the first 1,000 users and what do they transact? | Drives tx types, throughput, fee model | — |
| General-purpose platform or single application? | General → VM + contracts; single app → native logic | single application |

## Security and trust
| Question | Why it matters | Typical default |
|---|---|---|
| Own validator set, or borrow security (Ethereum L2, shared security, restaking)? | Biggest cost and sovereignty trade-off | borrow unless sovereignty is a hard requirement |
| Must finality be deterministic (BFT) or is probabilistic OK? | Rules consensus families in or out | deterministic |
| Halt or keep going when > 1/3 of validators are offline? | Safety vs liveness choice | halt (safety first) |
| Permissioned validators at launch? Path to permissionless? | Launch speed vs decentralization claims | permissioned set with published path |
| Who holds admin/upgrade keys at launch, and when are they removed? | Most real-world exploits go through privileged keys | multisig + timelock, sunset date |

## Validators and participation
| Question | Why it matters | Typical default |
|---|---|---|
| Target active validator count now and in 2 years? | BFT message cost grows ~n²; drives block time | 50 → 100 |
| Can ordinary users run nodes on home hardware? With what role? | Separate roles or one role for all | full nodes yes; consensus no |
| What work, besides consensus, should be rewarded? Can it be proven? | Unprovable work gets gamed | only provable work |
| How is a single person running 1,000 nodes prevented from earning 1,000×? | Sybil resistance design | stake or bond per identity |

## Performance
| Question | Why it matters | Typical default |
|---|---|---|
| Block time / time to finality target (p95)? | Consensus choice, network topology | 2–6 s / same as block (BFT) |
| Peak sustained TPS and tx size? | Execution, DA, bandwidth | measure from user flows |
| Max acceptable node hardware for each role? | Who can participate | validator: 8–16 cores, 32–64 GB, NVMe |
| Time for a new node to sync? | State sync, snapshots, light clients | < 1 hour via snapshots |

## Execution and contracts
| Question | Why it matters | Typical default |
|---|---|---|
| Must existing Ethereum tools/wallets work (MetaMask, Solidity)? | Forces EVM compatibility | yes if consumer-facing |
| Do third parties deploy contracts, or only the core team writes logic? | VM vs native modules | core team only at launch |
| Account model or UTXO? | Parallelism, privacy, tooling | account |
| Any privacy requirement? | ZK / TEE / encryption changes everything | none |

## Economics
| Question | Why it matters | Typical default |
|---|---|---|
| Native token? Existing token elsewhere? | Staking, fees, bridge design | native token |
| Fee model: gas market, fixed, subsidised, paid in other tokens? | UX and spam resistance | EIP-1559-style |
| Issuance: fixed cap, inflation range, tail emission? | Security budget sustainability | bounded inflation, published |
| Reward split between roles? Are percentages final? | Many components depend on it | treat as parameters, not constants |

## Interoperability
| Question | Why it matters | Typical default |
|---|---|---|
| Which chains must assets/messages move to/from? | Bridge type and trust | Ethereum + one ecosystem |
| Trust-minimised (light client) or trusted (multisig/committee) bridge acceptable? | Bridges are the top exploit target | light client where possible |

## Governance and upgrades
| Question | Why it matters | Typical default |
|---|---|---|
| Who can change parameters and upgrade code? | Governance component scope | token-weighted gov + timelock |
| Emergency powers? Who, for how long? | Must be limited and sunset | pause-only, multisig, 12–24 months |
| How often do you expect breaking upgrades? | Upgrade tooling | quarterly in year one |

## Data and storage
| Question | Why it matters | Typical default |
|---|---|---|
| How long must full history be available, and from whom? | Archive nodes, DA, pruning | archive by RPC providers; validators prune |
| Expected state growth per year? Who pays for storage? | State rent / deposits | deposits per stored object |

## Team, time, money, law
| Question | Why it matters | Typical default |
|---|---|---|
| Team languages and experience? | Stack fit | — |
| Time to testnet / mainnet? | Build vs buy | testnet in 3–6 months |
| Budget for audits and infra? | Scope and number of custom components | audits ≈ 10–20% of build budget |
| Jurisdictions, token classification, KYC needs? | May force permissioned roles | consult counsel; out of scope here |
