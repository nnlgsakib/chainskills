---
name: stack-move-sui-aptos
description: Build, test, publish and upgrade Move packages on Sui and Aptos — Sui CLI via suiup, Move 2024 edition, object model, sui client publish/upgrade with UpgradeCap and upgrade policies (compatible, additive, dependency-only, immutable), Aptos CLI (aptos move compile/test/publish/prove), Aptos objects, Move Prover on Aptos, local networks, gas and publishing costs, and security pitfalls; plus pointers for building your own Move-based chain. Use whenever the user works with Move, Sui, Aptos, Move packages or modules, UpgradeCap, Move Prover, or chose a Move chain in design-stack-selection.
license: MIT
---

# Move (Sui / Aptos) adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It covers building protocols as **Move packages on Sui or Aptos**. Building your own Move chain is a pointer only. Resource-oriented asset safety is the main reason to pick Move (`protocol-state-execution`).

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where each protocol component lives |

## Adapter metadata
- Family: move
- Stack: Sui (Mysten Labs) and Aptos (Aptos Labs) Move platforms
- Versions verified: Sui `mainnet-v1.84.2` (protocol 142; testnet v1.85.1 at protocol 144); Aptos node `aptos-node-v1.50.1` (mainnet), Aptos CLI 9.5.1
- Verified on: 2026-11-25
- Sources: github.com/MystenLabs/sui/releases; docs.sui.io (getting-started, sui-install, develop/publish-upgrade-packages, upgrade, custom-policies); github.com/aptos-labs/aptos-core/releases; aptos.dev (build/cli, install-cli-windows, working-with-move-contracts, running-a-local-network, install-move-prover, smart-contracts/objects, smart-contracts/prover)
- Unverified parts: Sui localnet command (`sui start`) and flags, Move Prover availability on Sui, Aptos upgrade-policy names and semantics, Aptos Move 2 specifics, and own-Move-chain frameworks (Movement, Initia MoveVM, forks).

## When to use this adapter
Asset-heavy protocols that benefit from Move's resource safety and object models: Sui for object-centric parallel execution, Aptos for account and object resources plus the Move Prover. Building on a Move L1 rather than running your own chain.

## Placement map
Summary of `references/placement-map.md`:
- Native: state-execution (MoveVM, objects), smart-contracts (Move packages), upgrades (UpgradeCap / package upgrades), node-software (localnets, CLIs), consensus (the platform's validators)
- Extend: tokenomics (coin/fungible asset standards), governance (multisig or DAO-held UpgradeCap; custom policies)
- Custom: staking-validators (app-level), randomness (platform randomness APIs or oracles; verify), verifiable-participation, interop (bridges)
- n/a: rollup, data-availability, p2p

## Setup
**Sui**
```bash
curl -sSfL https://raw.githubusercontent.com/Mystenlabs/suiup/main/install.sh | sh && suiup install sui@testnet   # or brew install sui / choco install sui
sui move new my_pkg && cd my_pkg && sui move build && sui move test     # Move.toml: edition = "2024"
sui client publish --dry-run && sui client publish
```
**Aptos**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; iwr https://aptos.dev/scripts/install_cli.ps1 | iex   # or winget/choco/scoop; Linux/macOS: see aptos.dev
```
```bash
aptos init --profile local --network local
aptos node run-local-testnet --with-indexer-api        # Docker needed; REST :8080, faucet :8081, GraphQL :8090
aptos move compile --package-dir . --named-addresses my_addr=default
aptos move test --package-dir . --coverage
aptos move publish --package-dir . --profile local
aptos update prover-dependencies && aptos move prove --package-dir .
```

## Implement
- Spec mapping: State maps to resources/objects (Sui: objects with `key`/`store`; Aptos: resources and objects), Operations to entry/public functions with `assert!` checks (abort codes as error IDs), Hooks to keeper-called functions (no block hooks), and Parameters to config objects/resources gated by capabilities.
- Use **capability objects** for admin powers. Capabilities replace `onlyOwner`. Store them in multisig accounts.
- Sui shared objects need **versioning**: old package versions stay callable, so shared objects should carry a version field plus a `migrate` function, and entry points should check it.
- Aptos: all modules of a package publish from the same account. Use `--included-artifacts none` to omit source if needed (bytecode can still be decompiled).

## Test
- `sui move test` / `aptos move test --coverage`. Test every abort path.
- **Aptos Move Prover** (`aptos move prove`) with `spec` blocks for critical invariants (supply, balances, access). This is a formal method that pairs with `quality-formal-verification`.
- Localnet integration tests. Upgrade tests: publish v1, create state, upgrade to v2, check that v1 entry points can't corrupt state.

## Production
- **Sui upgrade policy**: Compatible (default) → Additive → Dependency-only → Immutable. Restriction is **one-way** (`only_additive_upgrades`, `only_dep_upgrades`, `make_immutable`). Hold the `UpgradeCap` in a multisig or a custom policy package (time-locked, voted). Verify the upgrade digest before upgrading. Under protocol 143+ (testnet/devnet), each publish or upgrade costs 1 SUI plus 0.01 per module and per dependency.
- **Aptos**: choose the package upgrade policy deliberately (verify the semantics in aptos.dev), and keep publishing accounts in multisig.
- `sui client verify-source` / published sources for transparency. Audits before mainnet value.

## Known pitfalls
- Sui: `init` doesn't re-run on upgrade, and dependencies aren't auto-upgraded.
- Sui: old package versions remain callable. Unversioned shared objects can be manipulated through old code.
- The `UpgradeCap` (Sui) or publishing account (Aptos) is a single point of compromise.
- Publishing is irreversible. Dry-run first.
- Sui's GitHub "Latest" badge may point at a testnet tag. Pick `mainnet-*` tags for production tooling.

## Your own Move chain (pointers, unverified)
Forking Sui or Aptos, or Move-based frameworks (e.g. Movement, Initia MoveVM), are options not verified here. Create a dedicated adapter with `build-stack-adapter` first.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Check Sui and Aptos releases (protocol versions, CLI versions), the publish and upgrade docs, and Move Prover availability, and resolve the Unverified list.
