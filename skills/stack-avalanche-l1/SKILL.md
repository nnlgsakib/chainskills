---
name: stack-avalanche-l1
description: Launch and operate an Avalanche L1 (formerly Subnet) — Etna/ACP-77 sovereign L1 validators that only sync the P-Chain, Subnet-EVM (now built inside avalanchego) or a custom VM, genesis and precompile configuration (allowlists, native minter, fee and reward managers, Warp), ACP-99 ValidatorManager contracts for PoA or PoS (native token or ERC-20 staking), L1 validator balances, ICM/Teleporter and ICTT interop with relayers, private L1s, and tooling (Builder Console, platform-cli, avalanche-cli in maintenance mode). Use whenever the user works with Avalanche L1s, Subnets, Subnet-EVM, AvalancheGo, ValidatorManager, ICM/Teleporter, or chose Avalanche in design-stack-selection.
license: MIT
---

# Avalanche L1 adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It maps stack-neutral designs onto an Avalanche L1: an EVM (or custom-VM) chain with its own validator set managed by on-chain contracts, interoperating with other Avalanche chains through ICM.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |

## Adapter metadata
- Family: avalanche
- Stack: Avalanche L1s on AvalancheGo (Snowman consensus), Subnet-EVM, ACP-77/ACP-99 validator management, ICM
- Versions verified: avalanchego v1.15.3 (5 Nov 2026; ships `subnet-evm` plugin binaries; Helicon activated on mainnet 22 Sep 2026); avalanche-cli v1.9.7 (**maintenance mode since Dec 2025**); subnet-evm repo archived (last tag v0.8.0), with the code now in avalanchego; icm-contracts repo archived (validator-manager v2.1.0: standalone PoAManager; v2.0.0: ValidatorManager + standalone StakingManager, `IACP99Manager`)
- Verified on: 2026-11-25
- Sources: github.com/ava-labs/avalanchego/releases; github.com/ava-labs/avalanche-cli/releases; github.com/ava-labs/subnet-evm (archived); github.com/ava-labs/icm-contracts/releases (archived); build.avax.network/docs/avalanche-l1s; build.avax.network/console (Builder Console, platform-cli); build.avax.network/docs/primary-network
- Unverified parts: L1 validator continuous-fee rate and minimum balance, exact precompile names and addresses, native-token staking manager naming in v2, platform-cli commands, ICM relayer production setup, and hardware requirements. Check the Builder Console, L1 Toolbox and node system-requirements pages.

## When to use this adapter
An EVM L1 that wants **its own validator set and token**, fast finality (Snowman), validator management as **Solidity contracts** (PoA or PoS), optional private (allowlisted) operation, and native interop with the Avalanche ecosystem through ICM. Since Etna, L1 validators don't have to validate the Primary Network. They only sync the P-Chain and pay a continuous balance-based fee.

## Placement map
Summary of `references/placement-map.md`:
- Native: consensus (Snowman), state-execution (Subnet-EVM, or a custom VM), staking-validators (ValidatorManager + PoA/PoS managers), interop (ICM/ICTT), node-software, smart-contracts
- Extend: tokenomics (native minter, fee manager, reward manager precompiles), governance (contract owners of managers and precompiles), upgrades (network upgrades plus contract upgrades)
- Custom: randomness, verifiable-participation
- n/a: rollup, data-availability

## Setup
1. **Tooling**: the Builder Console at build.avax.network/console (create an L1, add and remove validators, L1 validator balance, tokenomics, ICM setup) and **platform-cli** (`curl -sSfL build.avax.network/install/platform-cli | sh`). **avalanche-cli** still works but gets only security fixes. Use it for existing scripts, verifying syntax with `avalanche blockchain --help`.
2. **Nodes**: avalanchego v1.15.x with the Subnet-EVM plugin, which ships with avalanchego releases. Use `validatorOnly` node config for private L1s.
3. **Genesis**: chain ID (unique, register on chainlist), gas config, initial allocations, and precompile configuration (deployer and tx allowlists, native minter, fee manager, reward manager, Warp). Decide these deliberately, because several are hard to change later.
4. **Validator manager**: deploy the ACP-99 contracts. **PoA** = `ValidatorManager` + `PoAManager`; **PoS** = `ValidatorManager` + a staking manager (ERC-20 staking is confirmed; native-token staking is per current docs). Convert the subnet to an L1 with the manager as the authority that can change the validator set (via Warp messages to the P-Chain).
5. **Fund each L1 validator's P-Chain balance**. The continuous fee is deducted from it, and validators become inactive when it runs out.

## Implement
- Contracts via `build-smart-contracts`. Validator-set and staking extensions follow `build-smart-contracts/references/validator-set-contracts.md` and must respect ACP-99 interfaces.
- v2 method names changed (`initiateValidatorRegistration`, `initiateValidatorRemoval`-style flows, reward recipient set at registration). Read the v2 interface before extending.
- Native-token economics through precompiles (minting, fee parameters, reward address). Governance of those precompile admin roles goes into `protocol-governance`.
- Cross-chain messaging: ICM (Teleporter messenger and registry), token transfers via ICTT, and relayers (managed relayer for Fuji only; run your own for mainnet).

## Test
- Local network and Fuji L1 before mainnet. Validator add/remove under load. Balance-depletion scenario (validator goes inactive), then recovery.
- ICM round-trips with relayer restarts. Precompile permission tests (allowlisted vs not).
- PoS manager: delegation, rewards and removal flows. Uptime-based reward calculation tested.

## Production
- Validator manager owner and precompile admins on multisig + timelock. Contracts audited.
- Validators across independent operators and regions. Balance top-up automation and alerts.
- Own ICM relayer(s) with redundancy. Monitoring of message delivery.
- Track avalanchego network upgrades (e.g. Granite, Helicon). Upgrade nodes before activation.
- Plus the `quality-*` and `ops-*` skills.

## Known pitfalls
- **v1 PoS validator-manager contracts can't migrate to v2** (v1 PoA can). Start on v2.
- The PoS manager must live on the chain holding the reward token, with a reward calculator contract.
- Archived repos (subnet-evm, icm-contracts) mean new fixes land elsewhere. Pin versions and watch avalanchego releases.
- An empty P-Chain balance silently drops validators from the active set. Monitor it.
- avalanche-cli is in maintenance mode, so don't build new automation solely on it.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Check avalanchego releases (network upgrades, plugin version), Builder Console/platform-cli docs, the validator-manager contract location after the icm-contracts archive, and resolve the Unverified list.
