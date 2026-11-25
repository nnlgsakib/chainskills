# What `ignite evm add` wires (evm app v0.2.0 / cosmos/evm v0.6.0)

Use this to review the diff, debug startup panics, or redo wiring by hand on a chain the app can't modify.

## Contents
- go.mod
- app/evm.go
- app/ante.go
- app/app.go changes
- app/app_config.go changes
- cmd changes
- config.yml changes
- Upgrading cosmos/evm

## go.mod

```
require github.com/cosmos/evm v0.6.0
replace github.com/ethereum/go-ethereum => github.com/cosmos/go-ethereum v1.16.2-cosmos-1
```

The replace is mandatory — cosmos/evm depends on the Cosmos fork of geth. Don't drop it in `go mod tidy` fights.

## app/evm.go (generated)

- `init()`: `sdk.DefaultPowerReduction = utils.AttoPowerReduction` (1 voting power = 10^18 base units); sets `evmtypes.DefaultEVMDenom/DisplayDenom/ExtendedDenom = sdk.DefaultBondDenom` ← **replace with your denoms**.
- `registerEVMModules(appOpts)`:
  - KV stores: `evm`, `feemarket`, `erc20`; transient stores for evm + feemarket.
  - `FeeMarketKeeper` (authority = gov).
  - `EVMKeeper` with: auth, bank, staking, feemarket, consensus params, erc20 keepers, EVM chain ID, tracer (from `--evm.tracer`), `.WithStaticPrecompiles(DefaultStaticPrecompiles(staking, distr, bank, erc20, transfer, channel, gov, slashing))`, `.WithDefaultEvmCoinInfo({Denom, ExtendedDenom, DisplayDenom, Decimals: 18})`.
  - `Erc20Keeper` (authority = gov) with transfer keeper.
  - `RegisterModules(vm, feemarket, erc20)` — not via depinject.
- `setEVMMempool()`: `ExperimentalEVMMempool` with `BlockGasLimit: 100_000_000`, custom CheckTx handler, PrepareProposal with Eth signer extraction. Required for JSON-RPC tx submission.
- `GetEVMChainID(appOpts)`: `--chain-id` flag → else parse genesis → FNV-32a hash of the Cosmos chain-id (fallback hash of `"ignite"`).
- `RegisterEVM(...)`: registers EVM module basics on the client side (autocli, interfaces) because depinject can't.
- `ProvideMsgEthereumTxCustomGetSigner()`: custom signer for `MsgEthereumTx`, injected into depinject.

## app/ante.go (generated)

`setAnteHandler(txConfig, maxGasWanted)` builds `evmante.NewAnteHandler` with account/bank/feegrant/IBC/EVM/feemarket keepers, `HasDynamicFeeExtensionOption`, `SigVerificationGasConsumer`, `MaxTxGasWanted`, and a `PendingTxListener` that fans out to JSON-RPC subscribers. This ante routes Ethereum txs (`MsgEthereumTx`) and Cosmos txs through different decorator chains.

## app/app.go changes

- Imports geth JS/native tracers (side-effect imports) and cosmos/evm packages.
- `ChainCoinType` string replace (check final value is 60).
- `const BaseDenomUnit int64 = 18`.
- `App` struct gains: `clientCtx`, `pendingTxListeners`, `FeeGrantKeeper`, `FeeMarketKeeper`, `EVMKeeper`, `Erc20Keeper`, `EVMMempool`.
- In `New(...)`: EVM registration after IBC modules (comment in code: "evm must be instantiated after IBC modules"), ante handler + mempool set up, `GetStoreKeysMap()` helper added. The IBC transfer wiring is adjusted so the erc20 keeper can hook transfers (IBC tokens get ERC20 representations) — inspect the transfer keeper lines in the diff.

## app/app_config.go changes

- Module account permissions: `evm` (Minter, Burner), `erc20` (Minter, Burner), `feemarket` (none).
- `getBlockAccAddrs()` replaces the blocked-address list (`BlockedModuleAccountsOverride`) — check your own module accounts are still blocked where needed.

## cmd changes

- `cmd/<bin>d/cmd/commands.go`: `server.AddCommandsWithStartCmdOptions` → `cosmosevmserver.AddCommands(...)` (start command gains JSON-RPC/EVM flags); `keys.Commands()` → `cosmosevmcmd.KeyCommands(app.DefaultNodeHome, false)` (eth key import/export).
- `cmd/<bin>d/cmd/root.go`: client keyring uses `cosmosevmkeyring.Option()` (eth_secp256k1 default) and `WithLedgerHasProtobuf(true)`; depinject gets the custom MsgEthereumTx signer; EVM modules added to `moduleBasicManager` and `autoCliOpts`.

## config.yml changes

`validators[0].bonded` and that validator's account coins become `1000000000000000000<default_denom>` (1 voting power at 18 decimals). Other accounts are untouched — scale them yourself.

## `ignite evm init`

Runs `ignite chain init` then rewrites bank `denom_metadata` to one entry: base = default denom (exp 0), display = default denom without leading `u` (exp 18), symbol = upper(display). Overwrites any existing metadata list.

## Upgrading cosmos/evm

- Read the ignite/apps `evm/CHANGELOG.md` and cosmos/evm release notes/migration guides for every version hop (v0.1.x → v0.2.0 of the app moved cosmos/evm to v0.6.0 with manual steps).
- On a live chain, a cosmos/evm bump is a state-breaking upgrade: upgrade handler, `RunMigrations`, rehearsal on exported state (see `stack-cosmos-ignite` production §6).
- Re-check: geth replace version, ante options struct, keeper constructor args, precompile list, mempool API — these change between cosmos/evm minors.
