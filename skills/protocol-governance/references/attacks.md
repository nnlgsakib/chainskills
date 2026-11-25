# Governance attack review

Facts checked 2026-11-25 are marked ✔ (several 2026 incident details come from secondary sources).

| Attack | Mechanism | Examples | Defences |
|---|---|---|---|
| Bought voting power (patient capital) | Buy enough tokens on the market, hold them across the snapshot, pass a malicious proposal | BonkDAO: a treasury drained by an auto-executed proposal in Jul 2026, with no flash loan used ✔; Term Finance: ~$8.5M via bought governance power, with no flash loan or oracle manipulation ✔ | timelock with veto (guardian or other house), spending caps per period, quorum relative to circulating supply, payload review, alerts on large voting-power changes |
| Flash-loan voting | Borrow tokens within one tx to vote | Beanstalk 2022 (reference case) | snapshot at proposal creation or earlier; holding-period requirements; less common since timelocks spread ✔ |
| Low-turnout capture | Quorum reachable by a small holder group | many small DAOs | adequate quorum, longer voting periods, delegation programmes |
| Malicious payload | Proposal text says X, calldata does Y | — | simulate and publish decoded calldata; review period; verified-payload tooling |
| Proposal spam / griefing | Floods of proposals or vetoes | — | deposits, proposal thresholds, rate limits |
| Delegate cartels | Few delegates control most delegated power | common | caps, delegate transparency, easy re-delegation |
| Cross-chain governance | Votes or execution bridged across chains | — | bridge trust and rate limits; delays on the receiving chain |
| Governance self-modification | Lower quorum or threshold, then pass the real attack | — | constitutional parameters need a higher threshold and longer delay; bounds on parameters |
| Emergency-power abuse | Council exceeds its scope | debate after Arbitrum's Apr 2026 freeze of KelpDAO-exploiter ETH ✔ | published scope, threshold, after-action reports, sunset |
| Validator default-vote dominance (stake-weighted) | Delegators don't override validator votes | Cosmos-style chains | encourage delegator voting; validator vote transparency |

## Treasury-specific
- Spending caps per period, enforced on-chain, so a captured vote can't drain everything at once.
- Streaming payments with clawback.
- Two-step large transfers: approval, then a delay, then execution.

Sources: https://crypto.news/the-bonk-governance-attack-how-a-dao-lost-20-million-in-one-proposal/ · https://sentora.com/market-events/governance-as-an-attack-surface-lessons-from-the-term-finance-exploit · https://blockaid.io/blog/governance-takeovers-how-22m-was-drained-and-how-to-stop-them · https://coincentral.com/arbitrum-freezes-71-million-in-eth-after-kelpdao-exploit-sparking-decentralization-debate/
