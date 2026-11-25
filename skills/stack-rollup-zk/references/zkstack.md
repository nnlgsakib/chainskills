# ZK Stack details (read 2026-11-25)

## Components
| Component | Version / status | Role |
|---|---|---|
| zksync-os-server | v0.23.0 | Sequencer for ZKsync OS ("the new operating system of the ZK Stack"): JSON-RPC (default :3050), batcher, minimal async persistence |
| zksync-os | ongoing | The OS/VM proven by Airbender |
| zksync-era (core) | core-v31.5.0 | Legacy server; repo also hosts `zkstack_cli` |
| era-contracts | v0.31.x, `v31-mainnet` | L1/L2 contracts: Bridgehub, CTM, diamond proxies, bridges |
| Airbender | airbender_prover_server v0.1.1 | RISC-V proof system; final proof wrapped to FFLONK for L1 verification; runs on GPUs |
| zkstack CLI | installed via `zkstackup` | ecosystem/chain lifecycle, containers, server, prover, explorer, portal, gateway |

## zkstack command map (README)
- Install: `curl -L https://raw.githubusercontent.com/matter-labs/zksync-era/main/zkstack_cli/zkstackup/install | bash`, then `zkstackup` (`--local` builds from a checkout).
- Ecosystem: `ecosystem create`, `ecosystem init [--dev] [--no-genesis --zksync-os] [--resume]`, `ecosystem init-core-contracts --l1-rpc-url`, `ecosystem init-new-ctm --l1-rpc-url --bridgehub`, `ecosystem register-ctm --l1-rpc-url`.
- Chains: `chain create`, `chain init`, `chain set-da-validator-pair-calldata`.
- Gateway: `chain gateway convert-to-gateway --chain <gw>`, `chain gateway migrate-to-gateway --chain <c> --gateway-chain-name <gw>`, `migrate-to-gateway-calldata`, `migrate-from-gateway-calldata`, `finalize-chain-migration-from-gateway`.
- Run: `containers`, `server --chain <name>`, `explorer init`, `portal`, `update`.
- Prover (legacy pipeline): `prover init`, `prover run --component gateway|witness-generator|witness-vector-generator|prover|compressor` (needs the CUDA toolkit).
- Verification options: `--verifier etherscan|sourcify|blockscout`.
- Limitation (README): you can't use an existing ecosystem to register a new chain yet.

## Ownership model
- Bridgehub and CTM are owned by `ProtocolUpgradeHandler`, which is owned by `DecentralizedGovernance`.
- **ChainAdmin** is owned by the chain operator's multisig. It controls fee parameters, the validator (committer), the transaction filterer and the base-token multiplier.

## Prividium
A private, permissioned chain anchored to Ethereum. It runs as a validium, posting only state roots and ZK proofs. Access goes through a proxy RPC (Okta SSO / SIWE), with permissions in an admin dashboard. **Licensed product**: non-production use requires accepting the licence, and production requires a commercial agreement.

## Licence
ZK Stack components are dual-licensed **MIT or Apache-2.0** (server, Airbender, contracts, portal, explorer, SDKs, CLI). Prividium is excluded.

## Production checklist
- [ ] Server line chosen (ZKsync OS vs legacy), with versions pinned to an era-contracts protocol version.
- [ ] Real proving enabled (no fake provers). Prover capacity sized from a benchmark, plus redundancy.
- [ ] Sequencer HA (multi-node consensus setup) and RPC/external nodes separate from the sequencer.
- [ ] ChainAdmin = multisig, keys in HSM/KMS for operator/committer, balance alerts for L1 posting.
- [ ] DA choice recorded (rollup vs validium) with its exit guarantee in user-facing docs.
- [ ] Ecosystem governance and upgrade schedule tracked. Staging rehearsal for each protocol upgrade.
- [ ] Explorer, portal and bridge UI deployed. Withdrawal finalisation monitored (proof verified on L1).
- [ ] Stages assessment (`protocol-rollup/references/stages.md`).
