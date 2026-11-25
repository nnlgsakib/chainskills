# Rollup Stages (ETHBEAT, formerly L2BEAT)

Checked 2026-11-25 against the forum specification, which is the stated source of truth. The public stages page still showed "Last updated 23 Jul 2025" and the old 7-day value, so the forum spec is newer. Re-check both before claiming a stage. The framework measures decentralization and trust minimisation, not freedom from bugs.

## Stage 0
- Calls itself a rollup.
- State roots posted on L1.
- Data available on L1.
- Software exists to reconstruct state from L1 data.
- A proper proof system adjudicates state roots (fraud proofs reject invalid roots; ZK proofs accept valid ones).
- At least **5 external actors** can submit fraud proofs (moved from Stage 1 to Stage 0 on 20 Jun 2025).

## Stage 1
- The only way, other than bugs, to indefinitely block or push invalid L2→L1 messages is to compromise **≥ 75% of the Security Council**.
- Security Council: **≥ 8 participants**, **75% threshold**. Multiple addresses of one entity count as one, and identities or pseudonyms are public.
- Upgrades initiated outside the Security Council give users an exit window of **≥ 5 days**. Optimistic rollups need a challenge period of **≥ 5 days**, and grace periods or execution delays count toward it. This was reduced from 7 days on **30 Apr 2026**.
- Assumes a 1-of-N live proposer with unbounded N.

## Stage 2
- Fraud-proof submission is **permissionless**.
- Users have **≥ 30 days** to exit before unwanted upgrades, including DAO-initiated ones.
- The Security Council may act only on bugs adjudicable on-chain, such as two valid contradicting proofs. It has no general upgrade power.

## Changelog (forum)
- 30 Apr 2026: Stage 1 minimum challenge period 7d → 5d
- 5 Aug 2025: "calls itself a rollup" requirement updated
- 31 Jul 2025: Stage 1 redefined around the guiding principle
- 20 Jun 2025: 5-external-challenger requirement moved to Stage 0
- 4 Mar 2025: Security Council size/threshold assessment clarified

## Design checklist for a target stage

| Item | Stage 0 | Stage 1 | Stage 2 |
|---|---|---|---|
| Proof system live on L1 | ✅ | ✅ | ✅ |
| ≥ 5 external challengers/provers able to act | ✅ | ✅ | ✅ (permissionless) |
| Security Council ≥ 8 members, 75% threshold, public identities | — | ✅ | ✅ (emergency-only powers) |
| Non-council upgrades delayed ≥ exit window | — | ≥ 5 d | ≥ 30 d |
| Forced inclusion / exit without operator | recommended | needed in practice | ✅ |

Sources: https://forum.ethbeat.org/t/the-stages-framework/291 · https://ethbeat.org/stages
