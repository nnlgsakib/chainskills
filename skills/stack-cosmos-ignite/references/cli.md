# Ignite CLI reference

Verified 2026-11-25 against the official CLI reference at tag **v29.10.1** (`docs/docs/03-CLI-Commands/01-cli-commands.md`) and the **v30.0.0** migration guide. Run `ignite <cmd> --help` for anything not listed here.

## Contents
- Versions and the v30 namespace change
- Install
- Chain commands
- Scaffold commands
- Field types
- Generate commands
- Apps
- Testnets

## Versions and the v30 namespace change

| Line | Status (2026-11-25) | Scaffolds | Cosmos commands |
|---|---|---|---|
| v29.10.x | latest stable (v29.10.1, 16 Jun 2026) | SDK v0.53.6, CometBFT v0.38.21, IBC v10, Go 1.25 (release family 2025.1) | `ignite scaffold …`, `ignite chain …`, `ignite generate …`, `ignite testnet …` |
| v30.0.0 | release candidate (rc.2, 24 Sep 2026) | SDK v0.55.0, CometBFT v0.40.0, IBC v11.2.0 (release family 2026.1) | **`ignite cosmos scaffold …`, `ignite cosmos chain …`, `ignite cosmos generate …`, `ignite cosmos testnet …`, `ignite cosmos account …`, `ignite cosmos doctor`** |

- In v30 the top-level `scaffold`, `chain`, `account` and `generate` commands target **gno.land** realms and packages. The top-level `chain`, `generate` and `testnet` commands print a deprecation error pointing to `ignite cosmos`.
- v30 works with both v0.55.x and v0.53.x chains. Its scaffolding generates v0.55 code, which won't compile in a v0.53 chain, so migrate the chain first (docs.ignite.com/migration/v30.0.0).
- The examples below use v29 syntax. On v30, insert `cosmos` after `ignite` (e.g. `ignite cosmos chain serve`). Check `ignite version` first.

## Install

```bash
curl https://get.ignite.com/cli! | bash          # latest stable
brew install ignite
ignite version
ignite doctor                                    # hidden command: fixes chain config after Ignite upgrades (v30: ignite cosmos doctor)
```

## Chain commands

| Command | Key flags (verified) |
|---|---|
| `ignite chain serve` | `-r/--reset-once`, `-f/--force-reset`, `-v/--verbose`, `--home`, `-p/--path`, `--skip-proto`, `--skip-build`, `--generate-clients`, `--quit-on-fail`, `-o/--output-file`, `--build.tags`, `-c/--config` (inherited) |
| `ignite chain build` | `--release`, `--release.targets` (e.g. `linux:amd64,darwin:arm64`), `--release.prefix`, `--output`, `--debug`, `--build.tags`, `--skip-proto`, `--clear-cache`, `--check-dependencies` |
| `ignite chain init` | initializes home and genesis from `config.yml` without starting |
| `ignite chain simulate` | `--numBlocks`, `--blockSize`, `--seed`, `--genesis`, `--params`, `--exportStatePath`, `--exportParamsPath`, `--exportStatsPath`, `--initialBlockHeight`, `--genesisTime`, `--lean`, `--simName` |
| `ignite chain debug` | `--server`, `--server-address` (Delve) |
| `ignite chain lint` | runs the linter on the chain code |
| `ignite chain modules list` | lists the chain's modules |
| `ignite chain faucet <addr> <coins>` | dev faucet |

## Scaffold commands

| Command | Key flags (verified) |
|---|---|
| `ignite scaffold chain [name]` | `--address-prefix`, `--default-denom`, `--coin-type`, `--no-module`, `--minimal`, `--params`, `--module-configs`, `--proto-dir`, `--skip-git`, `--skip-proto`, `--path` |
| `ignite scaffold module [name]` | `--dep` (e.g. `bank,staking`), `--ibc`, `--params`, `--module-configs`, `--ordering`, `--require-registration` |
| `ignite scaffold list NAME [field]...` | `--module`, `--no-message`, `--no-simulation`, `--signer` |
| `ignite scaffold map NAME [field]...` | `--index`, `--module`, `--no-message`, `--no-simulation`, `--signer` |
| `ignite scaffold single NAME [field]...` | `--module` and others (flags not extracted, see `--help`) |
| `ignite scaffold type NAME [field]...` | proto type only |
| `ignite scaffold message [name] [field:type]...` | `--module`, `--response`, `--signer`, `--desc`, `--no-simulation` |
| `ignite scaffold query [name] [field:type]...` | `--module`, `--response`, `--paginated`, `--desc` |
| `ignite scaffold params [param]...` | `--module` |
| `ignite scaffold configs [configs]...` | `--module` |
| `ignite scaffold packet [name] [field]... --module x` | `--ack`, `--no-message`, `--signer` (module must use `--ibc`) |
| `ignite scaffold migration [module]` | scaffolds a module state migration (consensus-version bump) |
| `ignite scaffold chain-registry` | generates chain-registry `chain.json` / `assetlist.json` |
| `ignite scaffold vue` | Vue frontend |
| `ignite scaffold type-list` | prints supported field types |

All scaffold commands also take `--path`, `--yes` and `--clear-cache`.

CRUD scaffolds (`list`, `map`, `single`) generate owner-only update/delete checks. They're a starting point, not your authorization model.

## Field types (from `ignite scaffold type-list`, v29.10.1)

`string` (default), `bool`, `int`/`int64`, `uint`/`uint64`, `address`, `bytes`, `coin`, `coins` = `array.coin`, `dec.coin`, `dec.coins` = `array.dec.coin`, `strings` = `array.string`, `ints` = `array.int`, `uints` = `array.uint`, and `custom` (a type created earlier with `scaffold type`).

AutoCLI limit: only one `coins`/`dec.coins` field per command can take multiple CLI values. For token amounts use `coin`/`coins` (or `string` parsed to `math.Int`), never `int`/`uint`.

## Generate commands

```bash
ignite generate proto-go      # *.pb.go (serve/build run this automatically)
ignite generate openapi       # docs/static/openapi.json by default (client.openapi.path)
ignite generate ts-client     # TypeScript client (client.typescript.path)
ignite generate composables   # Vue composables (client.composables.path)
```

## Apps
`ignite app install|list|describe|update|uninstall|scaffold` and `ignite appregistry`. Usage and the app catalog are in `stack-cosmos-apps`. EVM is in `stack-cosmos-evm`. The `ignite relayer` command comes from the Hermes app.

## Testnets

| Command | Purpose / flags |
|---|---|
| `ignite testnet in-place` | Starts a testnet from the current local state, including exported mainnet state. Mints coins to `config.yml` accounts. Flags: `--address-prefix`, `--coin-type`, `--home`, `--path`, `--skip-proto` |
| `ignite testnet multi-node` | Several local validator nodes. Flags: `--node-dir-prefix`, `--home`, `--reset-once`, `--path` |
| `ignite testnet simulate` | Simulation against a testnet; same flags as `chain simulate` |

Sources: https://github.com/ignite/cli/blob/v29.10.1/docs/docs/03-CLI-Commands/01-cli-commands.md · https://github.com/ignite/cli/blob/main/docs/docs/06-migration/v30.0.0.md · https://github.com/ignite/cli/releases (v29.10.1, v30.0.0-rc.1, v30.0.0-rc.2)
