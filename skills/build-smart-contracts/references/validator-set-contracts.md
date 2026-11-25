# Validator-set, staking and system contracts

Mechanism design comes from `protocol-staking-validators`. This file covers implementing it as EVM contracts.

## Where these contracts live
| Setting | How the chain uses the contract | Example |
|---|---|---|
| System contract on an EVM L1 | Client reads the validator set from contract state at epoch boundaries; the contract may be called by the protocol (system txs) | BSC-style staking/validator contracts |
| Avalanche L1 | ACP-99 `ValidatorManager` + staking manager send Warp messages to the P-Chain; P-Chain enforces the set (ACP-77) | `PoAManager`, `NativeTokenStakingManager`, `ERC20TokenStakingManager` (icm-contracts v2) |
| L2 sequencer / operator registry | L1 contract holds bonds; proofs or challenges slash | rollup sequencer sets, AVS operator registries |
| Restaking service | Service manager + operator sets on a restaking protocol | EigenLayer AVS (slashing and redistribution live) |

## Design rules for contracts
1. **Epochs without loops over stakers.** Store an `epoch` counter. Pending changes go into per-epoch queues, and `advanceEpoch()` (permissionless, keeper-incentivised) processes at most `MAX_BATCH` items per call until done.
2. **Active-set selection.** Keep a sorted structure bounded by `maxCandidates` (or an off-chain-computed ordering verified on-chain: submit the list, the contract checks it's sorted and complete against stored stakes). Tie-break by address.
3. **Rewards.** Use the reward-per-share accumulator (`protocol-staking-validators/references/reward-accounting.md`), with `settle()` before every share change.
4. **Slashing.** Slash only on-chain-verifiable evidence: signature verification of two conflicting signed messages (precompile for the consensus signature scheme, or a light-client proof). Slashing reduces the validator's exchange rate, not per-delegator balances.
5. **Unbonding.** Time-ordered queue. Withdrawal after `unbondingPeriod`, slashable until then.
6. **Client interface.** Validator-set reads used by the node must be cheap and bounded (`getActiveSet(epoch)` returns a fixed-size array). Version this interface, because the node depends on it.
7. **Upgrades.** Timelock delay > `unbondingPeriod`, so stakers can exit before a contested upgrade.
8. **Pausing.** Can pause new delegations and validator creation. Withdrawals stay open, or the pause has a strict maximum duration.

## Tests that must exist
- Invariant: Σ stake accounted == token balance held (plus pending withdrawals).
- Invariant: |active set| ≤ max; every active validator ≥ minimum self-bond; no tombstoned validator is active.
- Invariant: rewards paid ≤ rewards funded.
- Fuzzed epoch transitions with random delegate/undelegate/slash sequences across many epochs.
- Gas test: worst-case `advanceEpoch` batch and `getActiveSet` stay under the block and per-tx gas caps.
- Upgrade test: storage layout preserved across versions, and state migrates correctly.

## Avalanche specifics (checked 2026-11-25)
- v2 splits `ValidatorManager` and the staking manager into separate contracts. **v1 PoS contracts can't migrate to v2**.
- The PoS manager must be deployed on the chain that holds the reward token, with a reward-calculator contract.
- Use the `stack-*` adapter for Avalanche (when built) for deployment and P-Chain registration steps.

Sources: https://build.avax.network/docs/quick-start/validator-manager · https://github.com/ava-labs/icm-contracts/releases · https://docs.eigencloud.xyz/eigenlayer/concepts/slashing/redistribution
