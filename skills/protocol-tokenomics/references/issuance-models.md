# Issuance models

Reference points checked 2026-11-25 are marked ✔. Use them as anchors and cite chain and date. Don't copy them blindly.

| Model | Rule | Pros | Cons | Reference |
|---|---|---|---|---|
| Disinflation to terminal | `rate_t = max(terminal, initial × (1 − decay)^t)` | predictable, easy to communicate | ignores staking conditions | Solana: fixed schedule toward a 1.5% terminal rate; inflation ≈ 4.18%, terminal expected ~2032 ✔. SIMD-0228 (market-based emissions) rejected Mar 2025 ✔; SIMD-0411 keeps the 1.5% terminal ✔ |
| Staking-target band | rate rises when bonded < target, falls when above, within [min, max], change capped per period | self-correcting security | yields fluctuate (institutions dislike that ✔); governance tweaks the band | Cosmos SDK x/mint: Hub band 7–20% around a 2/3 target; Hub cut the max to 10% in 2023 (prop 848) ✔; a zero-floor proposal was rejected in 2024 (prop 868) ✔ |
| Fixed amount per period | constant tokens per block/year | simple; inflation % falls as supply grows | no link to security needs | Bitcoin-style halvings are a variant |
| Hard cap | total supply never exceeds `max_supply` | scarcity narrative | security must eventually come from fees alone | — |
| Tail emission | small perpetual issuance after the schedule | permanent security budget floor | permanent dilution | — |
| Fee-only | no issuance; fees fund security | no dilution | needs real fee demand from day one | rare for new L1s |

## Choosing
- New sovereign PoS chain with uncertain fees: **staking-target band** or **disinflation**, with a published floor and ceiling, plus fee burn or distribution.
- Chain whose security is borrowed (L2, shared security): issuance funds ecosystem and operations, not security. Keep it low or zero.
- Any model: put the formula, bounds and change process in the spec. Governance changes need a timelock.

## Reward split pitfalls
- A fixed percentage to a role whose size grows (e.g. community nodes) dilutes rewards per node. Show reward per node at 10× and 100× participation.
- Validator and delegator splits double-count if commission also applies. Specify one formula.
- Unclaimed or unearned budgets: decide burn vs reserve vs roll-over explicitly.

Sources: https://www.galaxy.com/insights/research/solana-inflation-0411-crypto-simd · https://www.theblock.co/post/264683/cosmos-community-approves-capping-atom-inflation-rate-at-10 · https://www.theblock.co/amp/post/273899/cosmos-hub-inflation-reduction-proposal-rejection · https://blockworks.co/news/solana-proposal-could-spook-institutions
