# Sybil resistance

One operator running many identities is only a problem if it earns more, or gains more influence, than the same operator with one identity doing the same work. Design so splitting gains nothing.

| Technique | How it works | Good for | Limits |
|---|---|---|---|
| Work-proportional rewards | Pay per verified unit of work, not per node | any service layer | doesn't stop sybils in *committees* (influence), only in rewards |
| Bond per identity | Each identity locks stake; the bond is slashable | committees, voting, task assignment | capital-heavy operators still dominate; size the bond so k identities cost k× |
| Weight caps per operator | Max share of assignments or rewards per operator | concentration control | needs operator identity linking (otherwise split to bypass) |
| Stake-weighted committee sampling | Probability ∝ bond, capped | verifier committees | see committee_risk.py for sizing |
| Hardware attestation (TEE, secure elements) | Device proves genuine hardware | DePIN, physical services | vendor trust, side channels, revocation handling |
| Diversity requirements | Witnesses/committees must span ASNs, regions, operators | physical and network services | data must be verifiable, not self-declared |
| Reputation with decay | Long-lived good behaviour raises weight | reducing the impact of new sybils | slow onboarding; can be farmed |
| Proof of personhood | One human, one credential | per-person programs (airdrops, grants, one-person-one-vote) | wrong tool for infrastructure (one person can legitimately run many machines). Options as of 2026-11-25: Human Passport (formerly Gitcoin Passport, Holonym since Feb 2025; aggregated stamps/ML/ZK, no biometrics required) ✔; World ID (iris via Orb) ✔. Weigh privacy, coverage and gaming risk |

## Default recipe for a permissionless service layer
1. Rewards ∝ verified work units (rung 1–3 only).
2. A minimum bond per node, enough that a node's maximum epoch reward is far below its slashable bond.
3. Stake-weighted, capped committee selection with randomness revealed after lock.
4. Operator-level caps where operator identity is declared and enforced through the bond's owner address.
5. Monitor: the distribution of rewards per operator, and correlated behaviour (identical results/latency patterns).

Sources (2026-11-25): https://www.human.tech/blog/human-passport-proof-of-personhood-and-sybil-resistance-for-web3 · https://hackernoon.com/holonym-acquires-gitcoin-passport-to-build-the-worlds-largest-proof-of-humanity-network
