# Implementation surfaces for staking

The design is the same everywhere. These are the places it can live. Facts checked 2026-11-25 are marked ✔. For exact APIs, load the matching `stack-*` adapter.

| Surface | Example | What you get | What you write | Notes |
|---|---|---|---|---|
| Native module (Cosmos) | x/staking + x/slashing + x/distribution + x/evidence | bounded active set, delegation, F1 rewards, slashing, jailing, consensus key rotation (v0.55) ✔ | custom rotation/performance rules (wrapper module or fork), custom reward splits | Enterprise PoA module for permissioned sets needs a Cosmos Enterprise licence ✔ |
| Native pallet (Substrate) | pallet-staking (NPoS), session, election providers | nominations, elections, era rewards | custom elections or reward curves | election computation is off-chain-assisted; mind the weight limits |
| Ethereum-style beacon chain | own beacon chain (Prysm/Lighthouse forks) | Gasper; since Pectra: EIP-7251 (max effective balance 2048 ETH), EIP-7002 (exits triggered from the execution layer) | genesis, deposit contract, client ops | very heavy for a new L1 |
| Avalanche L1 validator manager | ACP-77 (P-Chain, Warp messages) + ACP-99 contracts: `ValidatorManager` plus `PoAManager` or `NativeTokenStakingManager` / `ERC20TokenStakingManager` ✔ | validator set as Solidity, PoA or PoS | reward calculator, custom eligibility | v2 splits manager and staking contracts; no v1→v2 migration for PoS ✔; the PoS manager must live on the chain holding the reward token ✔ |
| System contracts (EVM L1, BSC-style) | genesis-deployed staking/validator-set contracts + client hook reading the set each epoch | flexibility, Solidity tooling | the client integration (consensus reads contract state), all accounting | contract bugs are consensus bugs, so audit to consensus standards |
| L2 sequencer/validator registry on L1 | bonded sequencer set, proposer/challenger bonds | L1-secured bonds and slashing | registry + slashing on L1 proofs | see protocol-rollup |
| Restaking operator sets | EigenLayer (slashing live, redistribution live) ✔, Symbiotic, Babylon (BTC) | borrowed economic security | AVS/service manager contracts, objective slashing conditions, operator software | redistribution creates slashing incentives ✔; correlated risk across services |

## Contract-based checklist (EVM surfaces)
- Epoch transitions are triggered by a keeper or tx and process bounded batches. There are no unbounded loops.
- Use the reward-per-share accumulator, never per-delegator loops (reward-accounting.md).
- Evidence verification is on-chain (signature checks, proofs) before any slash.
- Upgrades sit behind a timelock longer than the unbonding period, so stakers can exit before a bad upgrade.
- See `build-smart-contracts` → `references/validator-set-contracts.md`.

Sources: https://build.avax.network/docs/quick-start/validator-manager · https://docs.cosmos.network/sdk/latest/upgrade/v0.55 · https://docs.cosmos.network/sdk/latest/upgrade/v0.54 · https://blog.eigencloud.xyz/redistribution-is-live-on-mainnet/
