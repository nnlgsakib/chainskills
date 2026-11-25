---
name: protocol-tokenomics
description: Design a chain's token economics independent of stack — token roles, genesis allocation and vesting, issuance policy (disinflation schedules, staking-target dynamic inflation bands, tail emission, hard caps), fee markets and burns, the security budget (cost to attack vs staking yield), reward splits across validators, delegators, community/service nodes and treasury, treasury rules, simulation (deterministic projection, then agent-based with cadCAD/radCAD/Mesa/TokenSPICE) and public disclosure (monetary policy, EU MiCA white paper). Use whenever the user designs or reviews token supply, inflation, staking rewards, fee burn, reward percentages, vesting, treasury, emission schedules, or asks whether their rewards are sustainable.
license: MIT
---

# Protocol Tokenomics

A building-block skill in chainskills (layer L2, stack-neutral). It decides how much value flows to whom, and why that's sustainable. The mechanics of paying it out are in `protocol-staking-validators` (stakers) and `protocol-verifiable-participation` (service nodes). Spending rules are in `protocol-governance`.

Inputs from `CHAIN.md`: roles and their incentives, trust assumptions (how much stake must be at risk), fee model (`protocol-state-execution`), any reward percentages in the idea. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/issuance-models.md` | Choosing an issuance policy; real-world reference points |
| `references/security-budget.md` | Checking that staking secures the chain at plausible prices |
| `references/simulation.md` | Running scenarios; tools |
| `references/disclosure.md` | Publishing the policy; MiCA and legal pointers |
| `scripts/emission_sim.py` | Yearly projection of supply, inflation, yields and role payouts |

## Workflow

### 1. Token roles
What the token is used for: staking (security), gas, governance, collateral, payment for services. Each role creates demand or lock-up, so write down which ones are real at launch and which are aspirational.

### 2. Genesis allocation and vesting
Allocate to the community/ecosystem, team, investors, treasury, validator bootstrapping and airdrop. Add vesting (cliff and linear) and an unlock schedule. Check that no single holder can control more than 1/3 of stake at launch (a BFT safety threshold), and plot circulating supply over time.

### 3. Issuance policy
Pick a model (`references/issuance-models.md`): disinflation toward a terminal rate, a staking-target band (rate moves to hit a bonded ratio), a fixed amount, or none (fee-only). Every parameter is `P-TOKEN-*` with bounds, and governance can change it only within those bounds.

### 4. Fees
Decide where fees go: burn (as in EIP-1559), validators, treasury, or service roles. Burning offsets issuance, while distribution pays security. With low fees early on, issuance carries the security budget, so plan the transition.

### 5. Reward split across roles
Example from an idea: 50% validators, 25% delegators, 15% community services, 10% reserve. Make the split concrete:
- **Validator vs delegator shares** interact with commission. Decide whether "validators 50%" includes rewards on their own stake, and whether commission applies to the delegator pool. If unclear, implement as: the staker pool (validators + delegators) is distributed pro rata to stake, validators take commission from their delegators' part, and a separate validator bonus is paid for performance. Write the formula in the spec.
- The **service-node share** is paid only for verified work. Unspent budget goes to reserve or is burned, never to unverified claims.
- **Reserve/treasury**: spending rules and caps belong in `protocol-governance`.
- Percentages are parameters, not constants.

### 6. Security budget
Use `references/security-budget.md`: cost to attack (price × bonded × attack fraction) versus value secured, and the staking yield needed to keep the bonded ratio at target against the opportunity cost of capital. Run it at pessimistic prices.

### 7. Simulate
- **Baseline**: `python3 scripts/emission_sim.py config.json` gives supply, issuance, burn, net inflation, nominal and real staking yield, and payouts per role per year.
- **Scenarios** (`references/simulation.md`): price −80%, fee revenue 10× lower than planned, bonded ratio swings, a large unlock cliff, service nodes growing 10× (reward per node dilution).
- **Agent-based** (cadCAD/radCAD/Mesa, or TokenSPICE with the EVM in the loop) when behaviour matters (unstaking under low yield, sell pressure).
Record results and decisions as ADRs.

### 8. Disclose
Publish: supply, issuance formula, caps, fee policy, split, vesting, treasury rules, and who can change what. For EU offers or admission to trading, a MiCA crypto-asset white paper is required, in machine-readable format since 23 Dec 2025 (`references/disclosure.md`). Get legal counsel; this skill doesn't give legal advice.

### 9. Hand off
To `design-spec`: component `TOKEN` (mint and distribution hooks, parameters, invariants):
- `INV-TOKEN-1` total supply = genesis + Σ minted − Σ burned
- `INV-TOKEN-2` minted per period ≤ cap from the issuance formula
- `INV-TOKEN-3` the split sums to 100%, and each payout ≤ its budget
- `INV-TOKEN-4` vesting accounts can't transfer locked amounts

## Rules
- Never promise a fixed APY. Rewards are a share of a bounded budget.
- Pay only for work that's verified or stake that's at risk.
- Every economic parameter is bounded and governable, and changes are timelocked.
- Model the bad case first: low price, low fees, high unlocks.

## Sources (verified 2026-11-25)
Cosmos Hub inflation history (max cut 20% → 10% in 2023, prop 848; zero-floor prop 868 rejected 2024; 2026 tokenomics research with Gauntlet): theblock.co, forum.cosmos.network · Solana (SIMD-0228 rejected Mar 2025; SIMD-0411; inflation ≈ 4.18%, 1.5% terminal): galaxy.com/insights/research/solana-inflation-0411-crypto-simd · MiCA white paper format (iXBRL from 23 Dec 2025): esma.europa.eu · Tools (cadCAD, radCAD, TokenSPICE, Mesa): tokenengineeringcommunity.github.io.
