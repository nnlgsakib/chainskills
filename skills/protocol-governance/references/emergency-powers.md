# Emergency powers and Security Councils

## Design checklist
- [ ] **Scope**: an exhaustive, published list of what the council may do (e.g. pause module X, block an exploit address, emergency upgrade on a proven bug). Everything else goes through normal governance.
- [ ] **Size and threshold**: Arbitrum's Security Council has 12 members, and emergency actions need 9 of 12 ✔. Rollup Stage 1 requires at least 8 participants with a 75% threshold, counts multiple addresses of one entity as one, and requires public identities ✔.
- [ ] **Independence**: members from different organisations and jurisdictions, with no single organisation able to reach the threshold.
- [ ] **Elections and terms**: staggered cohorts and published elections. Arbitrum moved to two-year terms from the March 2026 cohort ✔, and a constitutional change aims to stop key rotations after registration that led to non-emergency actions ✔.
- [ ] **Key hygiene**: hardware wallets, rotation procedures, regular liveness checks (signing drills).
- [ ] **Transparency**: mandatory after-action report within N days (what, why, evidence, outcome). Community calls for a written Emergency Action Policy after Arbitrum's Apr 2026 freeze ✔.
- [ ] **Sunset**: powers shrink over time, e.g. from emergency upgrades to pause-only to adjudicable on-chain bugs only (the Stage 2 standard ✔).
- [ ] **Override**: normal governance can remove council members and revoke powers.
- [ ] **Pause design**: pause stops the risky entry points. Withdrawals and exits stay open or have a strict maximum pause duration.

## Spec items
`P-GOV-council_size`, `P-GOV-council_threshold`, `P-GOV-emergency_actions` (enumerated), `P-GOV-max_pause_duration`, `P-GOV-council_sunset_height`, and the invariant `INV-GOV-5`: emergency executor can only call functions in the allowlist.

Sources (2026-11-25): https://docs.arbitrum.foundation/concepts/security-council · https://forum.arbitrum.foundation/t/march-2026-security-council-elections-complete/30909 · https://forum.arbitrum.foundation/t/constitutional-aip-ratification-of-security-council-election-process-improvements/31048 · https://forum.ethbeat.org/t/the-stages-framework/291
