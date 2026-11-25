---
name: stack-cosmos-evm
description: Add and run Ethereum Virtual Machine (EVM) support on a Cosmos SDK chain with the Ignite EVM app (`ignite evm add`, `ignite evm init`, cosmos/evm) — Solidity contracts, MetaMask, Ethereum JSON-RPC on :8545, Foundry/Hardhat deployment, eth_secp256k1 keys, 18-decimal tokens, ERC20 ↔ Cosmos coin conversion, precompiles (staking, bank, gov, IBC from Solidity), EIP-1559 fee market, and production hardening of an EVM appchain. Use whenever the user wants an EVM-compatible Cosmos chain, an "Ethereum-compatible L1", Solidity on Cosmos, MetaMask support for their chain, or is debugging cosmos/evm wiring, JSON-RPC or EVM chain ID issues.
license: MIT
---

# Cosmos EVM adapter (Ignite EVM app)

Turns an Ignite-scaffolded Cosmos SDK chain into an EVM chain using the official Ignite app `github.com/ignite/apps/evm`, which wires `github.com/cosmos/evm` (x/vm, x/feemarket, x/erc20, precompiles, EVM ante handler, EVM mempool, JSON-RPC server, Ethereum keyring).

Part of the `blockchain-dev` suite. Non-EVM chain work (modules, tests, genesis, validators) → `stack-cosmos-ignite`. Relayers/deploy/explorers → `stack-cosmos-apps`.

| Reference | Read when |
|---|---|
| `references/wiring.md` | Understanding or debugging what `ignite evm add` changed; upgrading cosmos/evm |
| `references/tooling.md` | Keys, MetaMask, Foundry/Hardhat, JSON-RPC config, local testing |
| `references/production.md` | Before any public testnet/mainnet |
| `references/placement-map.md` | Deciding where a protocol component goes on a Cosmos EVM chain |

## Adapter metadata
- Family: cosmos
- Stack: Cosmos SDK chain with EVM execution (cosmos/evm), added through the Ignite EVM app
- Versions verified: ignite/apps evm v0.2.0, cosmos/evm v0.6.0, cosmos/go-ethereum v1.16.2-cosmos-1, Cosmos SDK v0.53.6, Ignite CLI v29.9.2
- Verified on: 2026-11-25 (by reading the app source: cmd/, template/, go.mod)
- Sources: github.com/ignite/apps/tree/main/evm, github.com/cosmos/evm
- Newer upstream: Cosmos EVM **v0.7.x** belongs to release family 2026.1 (SDK 0.55, CometBFT 0.40). It adds the Krakatoa app-side mempool, optional Block-STM, and drops `x/precisebank`. The Ignite EVM app still pins v0.6.0 (family 2025.1, supported). To move up, follow docs.cosmos.network/evm/next/documentation/migrations/migration-v0.6-to-v0.7 (read 2026-11-25).
- Verified 2026-11-25 against the Cosmos EVM docs (docs.cosmos.network/evm/latest): `[json-rpc]` and `[evm]` app.toml keys and their defaults, `keys unsafe-export-eth-key` / `unsafe-import-eth-key`, `debug addr`, `--algo eth_secp256k1 --coin-type 60`, and the static precompile addresses.
- Unverified parts: whether the docs' "latest" pages match v0.6.0 exactly (they track v0.7). Diff against your `go.mod` version.

If `go.mod` shows other versions, trust the code and `--help` over these files.

## When to use this adapter
Use it when the chain needs Solidity contracts, MetaMask/Ethereum tooling and an Ethereum JSON-RPC, together with native Cosmos modules, IBC and a CometBFT validator set. Pure Ethereum-client L1s use `stack-evm-*` instead. L2 rollups on Ethereum use `stack-rollup-*`.

## Placement map
Summary of `references/placement-map.md`:
- Native: consensus, staking-validators, tokenomics, governance, p2p, interop, upgrades, smart-contracts (Solidity), state-execution (EVM + modules)
- Extend: node-software (JSON-RPC nodes), data-availability
- Custom: randomness, verifiable-participation
- n/a: rollup

## Setup

### 1. Scaffold a compatible chain

Requires Ignite ≥ v29.5.0 and a **non-minimal** chain (EVM keepers need staking, distribution, gov, IBC transfer, feegrant...).

Pick denoms first — EVM uses **18 decimals**, so the base denom is atto-units:

```bash
ignite s chain mychain --address-prefix mychain --no-module
cd mychain
git add -A && git commit -m "scaffold"      # undo point
```

Set the default denom in `config.yml` before adding EVM (e.g. `default_denom: amychain`; `a` = atto = 10^-18), and use it for accounts/validators.

### 2. Add EVM

```bash
ignite app install -g github.com/ignite/apps/evm
ignite evm add            # -p <path> if not in chain dir
go build ./...
git diff --stat           # review: app/app.go, app/app_config.go, app/evm.go, app/ante.go, cmd/*, go.mod, config.yml
```

What it does: adds cosmos/evm + `replace github.com/ethereum/go-ethereum => github.com/cosmos/go-ethereum`, generates `app/evm.go` and `app/ante.go`, registers EVM/feemarket/erc20 stores and modules (manually — they don't support depinject), mint/burn permissions, EVM mempool, EVM-flavoured `start` (JSON-RPC) and `keys` commands, sets power reduction to 10^18 and rewrites `config.yml` validator stake to 10^18 units.

## Implement

Custom protocol components: native Cosmos modules follow `stack-cosmos-ignite` → Implement. Logic that Solidity contracts must call goes in a precompile, or in a contract that talks to modules through the default precompiles. Contracts follow `build-smart-contracts`.

### 3. Fix the known rough edges (do this every time)

The generated code is a starting point. Check and fix:

1. **Hard-coded `stake` denom.** `app/evm.go` sets `evmtypes.DefaultEVMDenom`, `WithDefaultEvmCoinInfo{Denom...}` to `sdk.DefaultBondDenom` (= `"stake"`). Replace with your base/display denoms (constants), and make genesis `app_state.evm.params.evm_denom` match.
2. **Denom metadata.** `ignite evm init` writes bank metadata with display = base minus a leading `u`. With an `a…` base denom both units get the same name (invalid). Write metadata explicitly: base `amychain` exp 0, display `mychain` exp 18.
3. **EVM chain ID.** The app's `GetEVMChainID` derives it from an FNV-32a hash of the Cosmos chain-id, falling back to `"ignite"` if genesis isn't found. Upstream cosmos/evm instead reads `[evm] evm-chain-id` from app.toml (flag `--evm.evm-chain-id`, default 262144). Wallets and EIP-155 signatures bind to this ID, so pick a deliberate, unique one (check chainlist.org), set it identically on every node (hard-code it, or use the app.toml key), and never change it after launch.
4. **Coin type.** Confirm `ChainCoinType` in `app/app.go` is `60` (Ethereum HD path `m/44'/60'`) so MetaMask and CLI derive the same address from one mnemonic. The app's replace step targets the literal `ChainCoinType = 60`, so depending on the scaffold it may be left at `118`.
5. **Block gas limit.** EVM mempool uses `BlockGasLimit: 100_000_000`. Set consensus `block.max_gas` in genesis to the same value (never `-1` on an EVM chain — fee market and gas estimation need a finite limit).

Then run the genesis checker:

```bash
ignite evm init                                    # inits home + genesis (dev)
python3 <skill-dir>/scripts/check_evm_genesis.py ~/.mychain/config/genesis.json
```

## Test

### 4. Run and test

```bash
ignite chain serve      # JSON-RPC must be enabled in app.toml — see references/tooling.md
cast chain-id --rpc-url http://localhost:8545
cast block-number --rpc-url http://localhost:8545
```

Deploy and exercise a contract with Foundry/Hardhat, connect MetaMask, and also send a Cosmos-native tx — both paths share state and must both work (`references/tooling.md`).

## Production

### 5. Harden

Walk `references/production.md` (EVM-specific) **and** `stack-cosmos-ignite` → `references/production.md` (chain-wide). Report each item DONE / N/A / TODO.

## Known pitfalls

- Decide denom, decimals, EVM chain ID and coin type before genesis. All four are effectively permanent.
- Every amount is 18 decimals: `1000000000000000000amychain` = 1 MYCHAIN. Scale config.yml coins, gov deposits, min gas prices, mint params accordingly.
- Precompiles and the EVM ante handler are consensus code. Enable only the precompiles you need; any custom precompile must be deterministic and gas-metered.
- JSON-RPC is an API surface, not consensus — run it on dedicated RPC nodes, never on validators.
- The `scripts/audit_state_machine.py` from `stack-cosmos-ignite` will flag `os.Open` in `app/evm.go` (`GetEVMChainID` reads genesis at startup). That runs at boot, not in state transitions; annotate with `// audit:ok startup only`, or remove it by hard-coding the EVM chain ID (step 3.3).

## Updating this adapter
Run `build-stack-adapter` in refresh mode whenever the ignite/apps `evm/CHANGELOG.md` or cosmos/evm publishes a release. Re-read `cmd/` and `template/` in the app, update `references/wiring.md`, the rough-edges list and the "Versions verified" field.
