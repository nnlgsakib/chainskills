---
name: stack-svm-solana
description: Build, test and ship on Solana and the SVM — on-chain programs with Anchor or native Rust, Agave CLI and local validator, program deployment, upgrade authority (multisig, immutability), compute units and priority fees, Token-2022, testing with LiteSVM, Mollusk and Surfpool (bankrun is deprecated), validator clients (Agave, Firedancer), Alpenglow consensus, and options for your own SVM chain or rollup. Use whenever the user works with Solana, SVM, Anchor, Agave, Firedancer, Solana programs, SPL tokens, or wants an SVM-based chain, or chose Solana/SVM in design-stack-selection.
license: MIT
---

# Solana / SVM adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). Most Solana work means **programs on Solana mainnet**. Building your own SVM chain is an advanced path covered as pointers only. The account model and parallel execution concepts are in `protocol-state-execution`.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |

## Adapter metadata
- Family: svm
- Stack: Solana (Agave and Firedancer validator clients), Anchor framework, SVM
- Versions verified: Agave v4.4.1 (latest stable; v4.5.0-beta testnet, v5.0.0-alpha not for production), Anchor v1.2.2 (28 Oct 2026), LiteSVM, Mollusk (`mollusk-svm`), Surfpool (from their READMEs)
- Verified on: 2026-11-25
- Sources: github.com/anza-xyz/agave/releases; github.com/solana-foundation/anchor/releases (page served as otter-sec/anchor, so check the canonical repo); github.com/LiteSVM/litesvm; github.com/anza-xyz/mollusk; github.com/solana-foundation/surfpool; github.com/kevinheavey/solana-bankrun (deprecated); github.com/firedancer-io/firedancer; solana.com/upgrades/alpenglow (Votor live since epoch 1064, 21 Oct 2026, from an earlier session check)
- Unverified parts (solana.com docs were rate-limited during research): exact install script URL, `solana program` subcommand flags, Token-2022 program ID, Firedancer mainnet status (Frankendancer vs full), the SVM crate name (`solana-svm` vs `agave-svm`), and SVM chain/rollup frameworks. Confirm before relying on them.

## When to use this adapter
High-throughput apps on Solana (DeFi, payments, consumer), or protocols needing Solana's parallel execution and liquidity. For your own SVM chain, read the pointers below and consider creating a dedicated adapter with `build-stack-adapter`.

## Placement map
Summary of `references/placement-map.md`:
- Native: state-execution (SVM, accounts declared per tx), smart-contracts (programs), consensus (Solana validators, Alpenglow), interop (via bridges), node-software
- Extend: tokenomics (SPL / Token-2022 mints, fee policy in programs), governance (program-based DAOs, multisig upgrade authority), upgrades (program upgrade authority)
- Custom: staking-validators (app-level staking programs), randomness (oracle/VRF programs), verifiable-participation
- n/a: rollup, data-availability, p2p (for program developers; relevant only when running your own SVM chain)

## Setup
```bash
sh -c "$(curl -sSfL https://release.anza.xyz/stable/install)"      # Agave CLI (unverified URL; check docs)
solana-test-validator                                               # local validator
solana config set --url localhost && solana airdrop 10
cargo install --git https://github.com/solana-foundation/anchor avm --locked && avm install latest
anchor init my_program && cd my_program && anchor build && anchor test
```
On Windows use WSL2. Firedancer, for example, is Linux-only.

## Implement
- Programs are stateless code. State lives in **accounts** that are passed explicitly into each instruction. Validate every account: owner, signer, writable, PDA seeds and bump, and discriminators (Anchor constraints do most of this, so don't bypass them).
- Spec mapping: State maps to account structs (sized, rent-exempt), Operations to instructions (checks C-n become constraints and `require!`), Hooks to cranks or keeper instructions (no block hooks), and Parameters to config accounts with authority checks.
- **Compute budget**: set a compute-unit limit and price (priority fee) per transaction. Benchmark with Mollusk's CU bencher.
- Tokens: SPL Token or Token-2022 (extensions such as transfer fees, transfer hooks, confidential transfers). Check extension compatibility with wallets and DEXes.

## Test
- **LiteSVM** (`cargo add --dev litesvm`, Node package `litesvm`, `anchor-litesvm`): fast in-process tests (`LiteSVM::new()`, `add_program`, `send_transaction`, `warp_to_slot`).
- **Mollusk** (`mollusk-svm`): instruction-level harness with explicit accounts, CU benchmarking, fixtures and a debugger.
- **Surfpool** (`surfpool start`): drop-in test-validator replacement that mirrors mainnet state lazily, for integration tests against real programs.
- **solana-bankrun is deprecated**. Don't start new suites on it.
- Fuzz instruction inputs and account combinations. Test every constraint failing.

## Production
- **Upgrade authority** in a multisig (e.g. Squads) with operational procedures. Decide when to make the program immutable (`--final`) deliberately.
- Verifiable builds, published IDL, and source verification. Audit before mainnet value (`quality-security`).
- Priority-fee strategy and retry logic in clients. Monitor failed transactions and compute exhaustion.
- RPC: dedicated providers or your own RPC nodes, separate from validators. Never depend on one public endpoint.

## Known pitfalls
- Missing account checks (owner, signer, PDA) are the top Solana exploit class. Anchor constraints help, but `UncheckedAccount` and remaining accounts need manual checks.
- Arithmetic: use checked math. Rounding direction matters for shares (`protocol-staking-validators/references/reward-accounting.md`).
- Account size is fixed at creation unless reallocated. Plan for growth.
- A single hot upgrade-authority key is a full-compromise risk.
- Agave pre-releases (beta/alpha) aren't for mainnet hosts.

## Your own SVM chain (pointers, unverified)
Options include forking Agave, building on the SVM execution API (Agave `svm/`), or SVM rollup and appchain frameworks (e.g. Eclipse, SOON). None are verified here. Run `build-stack-adapter` to create a dedicated adapter from primary sources before committing.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Check Agave and Anchor releases, solana.com docs (install, program deployment, Alpenglow/Rotor status), Firedancer status and testing-tool READMEs, then resolve the Unverified list.
