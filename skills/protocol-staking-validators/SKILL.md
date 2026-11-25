---
name: protocol-staking-validators
description: Design validator sets and staking for any chain, independent of stack — PoS/DPoS/NPoS/PoA/hybrid and restaking-secured models, active-set size and epochs, deterministic validator selection and performance-based rotation, self-bond rules, non-custodial delegation and share accounting, commissions, unbonding and redelegation, slashing and jailing (double-sign, downtime, provable misbehaviour), evidence windows, consensus key rotation and post-quantum keys, voting-power concentration controls — implementable as a native module, validator-set/system contracts (EVM L1, Avalanche L1 ValidatorManager), L2 sequencer sets or restaking operator sets. Use whenever the user designs or reviews staking, delegation, validator rotation, slashing, rewards per validator, validator-set contracts, or sequencer/operator sets.
license: MIT
---

# Protocol Staking & Validators

A building-block skill in chainskills (layer L2, stack-neutral). It designs who secures consensus, how they're chosen, and how they're paid and punished. Reward amounts and splits come from `protocol-tokenomics`; this skill does the accounting mechanics. Consensus parameters come from `protocol-consensus`.

Inputs from `CHAIN.md`: node roles, validator count targets, trust assumptions, consensus ADR, the placement decision (module vs contracts). Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/reward-accounting.md` | Designing delegation shares, reward distribution, slashing math |
| `references/slashing.md` | Defining offences, penalties, evidence, jailing |
| `references/implementations.md` | Mapping the design onto a module, contracts, or a restaking layer |
| `references/attacks.md` | Reviewing the design |

## Workflow

### 1. Participation model
Pick one: open PoS (stake-weighted), delegated PoS with a bounded active set, nominated PoS (an election algorithm), PoA (known operators), restaking-secured (operators from another chain's stake), or a hybrid (for example a PoS core set plus other bonded roles). Name every role that bonds stake and what it's slashable for.

### 2. Active set and epochs
- Active-set cap (from consensus benchmarks), candidate pool, epoch length.
- **Selection** at each epoch boundary is deterministic and uses chain data only: stake, self-bond, eligibility, jailed/tombstoned status, and performance metrics computed from on-chain evidence (signed or missed blocks, provable faults). Never use self-reported metrics.
- Tie-breaking rule (for example stake, then operator address bytes).
- Churn limits per epoch, so the set can't swing completely in one step.

### 3. Bonding and delegation
- Minimum self-bond (absolute and/or as a share of total stake), so validators always have skin in the game.
- Delegation is non-custodial: funds move into a protocol-controlled pool, never into the validator's keys.
- Share accounting so rewards and slashes apply to all delegators in O(1). Use `references/reward-accounting.md`. Never loop over delegators in block hooks.
- Commission: rate, maximum rate, maximum change per day, and an optional protocol-wide minimum.

### 4. Unbonding and redelegation
- Unbonding period longer than the evidence window, so stake that misbehaved can still be slashed after the misbehaviour is reported. It also bounds long-range attacks.
- Redelegation rules (instant but still slashable for the source validator's past faults; limit chains of redelegations).
- Bounded queue processing per block or epoch.

### 5. Slashing and jailing
Use `references/slashing.md`: offences, evidence, penalty, jail duration, tombstoning, how slashes reach unbonding and redelegating stake, and what happens to slashed funds (burn, treasury, redistribution). Separate *missed work* (lower rewards) from *provable fraud* (slash).

### 6. Keys
Consensus key vs operator key, remote signer support, key rotation (rate-limited, with old keys still slashable until evidence expires), and post-quantum readiness. Cosmos SDK v0.55 already supports ML-DSA-65 validator keys and rotation.

### 7. Concentration controls
Target a Nakamoto coefficient. Use voting-power caps per validator or per operator group, delegation UI nudges, and monitoring. Caps must not create sybil incentives, such as splitting one operator into many validators. Combine caps with identity or diversity requirements, or accept that sybils exist and design for it.

### 8. Choose the implementation surface
With `design-stack-selection` and `references/implementations.md`: a native module (Cosmos x/staking, Substrate NPoS), validator-manager contracts (Avalanche ACP-99), system contracts (BSC-style), an L2 sequencer registry on L1, or restaking operator sets (EigenLayer, Symbiotic). The design above stays the same, only the surface changes.

### 9. Hand off to design-spec
Spec component `STAKE` with: state (validators, delegations, unbonding queue, rotation queue), operations (create validator, delegate, undelegate, redelegate, edit commission, unjail, rotate key, submit evidence), hooks (epoch end, block end), parameters `P-STAKE-*`, and invariants:
- `INV-STAKE-1` pool balance = Σ validator tokens + Σ unbonding entries
- `INV-STAKE-2` validator tokens ≥ 0, shares ≥ 0
- `INV-STAKE-3` |active set| ≤ P-STAKE-max_validators
- `INV-STAKE-4` every active validator's self-bond ≥ P-STAKE-min_self_bond
- `INV-STAKE-5` no tombstoned validator is ever active again

## Rules
- Validator selection, rotation and slashing are deterministic functions of chain state.
- No per-delegator loops in block or epoch hooks. Use lazy accounting.
- Every slash is backed by verifiable evidence. Reports from other participants trigger verification, not automatic slashing.
- Publish every parameter. Validators and delegators make financial decisions based on them.

## Sources (verified 2026-11-25)
Cosmos SDK v0.55 (key rotation, ML-DSA-65, key_rotation_fee): docs.cosmos.network/sdk/latest/upgrade/v0.55 · Enterprise PoA (licensed): docs.cosmos.network/sdk/latest/upgrade/v0.54 · Avalanche ACP-77/99 validator manager v2: build.avax.network/docs/quick-start/validator-manager · EigenLayer slashing and redistribution live: blog.eigencloud.xyz/redistribution-is-live-on-mainnet, docs.eigencloud.xyz/eigenlayer/concepts/slashing/redistribution.
