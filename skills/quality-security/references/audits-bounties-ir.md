# Audits, bounties, monitoring, incident response

Facts checked 2026-11-25 are marked ✔.

## Audits
- **When**: spec frozen, code complete for the scope, tests and invariants passing, static analysis triaged.
- **Scope**: list the files and commit, out-of-scope items, trust assumptions, and known issues.
- **Package**: spec (`docs/spec`), threat model, invariants with test names, coverage report, deployment plan.
- **Depth**: two independent firms for consensus, staking, bridge and rollup proof code, or one firm plus a competitive audit contest.
- **Fix review**: auditors re-review the fixes, and the final report names the commit.
- **Publish** reports, and link them in `CHAIN.md` as evidence for `audited`.

## Bug bounty
- Launch before significant value is at risk. Rewards scale with funds at risk (a percentage with a cap).
- Clear scope, severity table, response SLA, and payout terms.
- Platforms include Immunefi and Cantina. Both support SEAL Safe Harbor integration ✔.

## SEAL Safe Harbor ✔
- An opt-in framework that protects whitehats who **rescue funds during an active exploit**. It isn't a bug-bounty channel and doesn't cover the original attacker.
- Rescued funds go to protocol-designated addresses within **72 hours**. The protocol sets the bounty percentage and cap (e.g. Euler 10% capped at $2.5M; Lido 10% capped at $2M).
- Adopt it via governance, and publish the asset-recovery address and the scope.

## Monitoring (alert to on-call)
- Invariants: supply rules, bridge escrow ≥ L2 supply, pool balances, reward budgets.
- Privileged activity: role grants, upgrades queued, council or multisig proposals, parameter changes.
- Consensus: missed blocks, equivocation evidence, voting-power concentration, peer counts, halted height.
- Governance: new proposals (decoded payloads), sudden voting-power moves.
- Services: oracle deviations, relayer backlog, sequencer liveness.

## Incident response
- **Runbooks** for: pause contracts or modules, coordinated chain halt (halt-height) and patched upgrade, key revocation or rotation, frontend takedown or DNS recovery, and communications (status page, social, partners, exchanges).
- **Roles**: incident commander, technical lead, comms, legal. Keep the contact list current.
- **SEAL 911**: 24/7 emergency help for incidents and disclosures, which handled 1,800+ tickets in 2025 ✔. Keep the contact in runbooks.
- **SEAL Frameworks**: OpSec, wallet security, incident response and more. Modular and adoptable step by step; SEAL also runs certification programmes ✔.
- **Drills**: tabletop exercises at least twice a year, including a "signer UI compromised" scenario.
- **Post-mortem**: timeline, root cause, impact, fixes, and follow-up owners, published.

Sources: https://frameworks.securityalliance.org/safe-harbor · https://cantina.xyz/blog/euler-seal-safe-harbor-cantina-verification · https://docs.lido.fi/security/safeharbor · https://frameworks.securityalliance.org/intro/overview-of-each-framework.html · https://www.theblock.co/post/384079/crypto-exploit-triage-group-seal-sees-uptick-tickets-2025
