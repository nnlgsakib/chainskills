# Simulation

## Levels
1. **Deterministic projection**: `scripts/emission_sim.py`. Yearly supply, issuance, burn, net inflation, yields and payouts per role. Fast. Use it for every parameter change.
2. **Scenario sweeps**: run (1) over grids of price, fees, bonded ratio and participation. Look for regions where real yield turns negative or service rewards fall below operator costs.
3. **Agent-based models**: heterogeneous actors (stakers who unstake below a yield threshold, traders, service operators who join or leave by profitability, attackers).

## Tools (checked 2026-11-25)
| Tool | Type | Notes |
|---|---|---|
| cadCAD | Python, system dynamics + agent-based, Monte Carlo, A/B tests, parameter sweeps | most-cited token-engineering framework |
| radCAD | cadCAD derivative with a simpler API | faster to start |
| cadEVM | radCAD + Ape, EVM-in-the-loop, can fork live networks | work in progress |
| TokenSPICE | agent-based with the EVM in the loop | ties the simulation to the actual Solidity contracts |
| Mesa | Python agent-based framework | often paired with cadCAD for heterogeneous agents |
| Machinations, NetLogo, AnyLogic | visual/general modelling | good for communicating designs |

Maintenance status for cadCAD and radCAD in 2026 wasn't confirmed, so check repo activity before relying on them.

## Mandatory scenarios
- Price −80% sustained for 12 months.
- Fees at 10% of plan.
- Bonded ratio drops from target to 40% within one unbonding period.
- The largest unlock cliff hits while price is −50%.
- Service-node count ×10 (reward per node) and ×0.1 (coverage).
- Governance raises inflation to its maximum bound (check the worst case).

## Output
For each scenario: real staking yield, cost to halt, reward per service node versus its operating cost, and treasury runway. Write conclusions as ADRs and turn the violated thresholds into parameter bounds.

Sources: https://tokenengineeringcommunity.github.io/website · https://github.com/0x3327/cadEVM · https://medium.com/tokenspice/tokenspice-design-verification-flows-5b795c594f9c · https://arxiv.org/pdf/2603.25100
