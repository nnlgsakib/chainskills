# Ignite Apps — per-app reference

Source: README of each app in https://github.com/ignite/apps (main branch). If a command fails, run `ignite <app-command> --help` — app CLIs evolve independently of Ignite.

## Contents
- hermes — IBC relayer
- wasm — CosmWasm
- spaceship — SSH deploy
- network — coordinated launch on Ignite Chain
- explorer — Gex / Ping.pub
- connect — any Cosmos chain
- cca — frontend
- fee-abstraction
- evolve — rollups
- gnovm
- appregistry

---

## hermes — IBC relayer

```bash
ignite app install -g github.com/ignite/apps/hermes
# both chains must be running and have IBC
ignite relayer hermes configure <chain-a-id> <chain-a-rpc> <chain-a-grpc> <chain-b-id> <chain-b-rpc> <chain-b-grpc> [flags]
ignite relayer hermes start <chain-a-id> <chain-b-id> [flags]
```

Example — two local chains on different ports:

```bash
ignite relayer hermes configure "mars-1" "http://localhost:26649" "http://localhost:9082" \
                                "venus-1" "http://localhost:26659" "http://localhost:9092"
ignite relayer hermes start "mars-1" "venus-1"
```

Running two chains locally: give each its own `config.yml` with different `validators[].app` (`api.address`, `grpc.address`) and `validators[].config` (`rpc.laddr`, `p2p.laddr`) ports, and different `--home`. Check `configure --help` for flags to set gas price, accounts/mnemonics, channel ports and versions.

Custom IBC packets: scaffold the module with `--ibc` and packets with `ignite scaffold packet` (see `stack-cosmos-ignite`), then relay with this app.

## wasm — CosmWasm

```bash
ignite app install -g github.com/ignite/apps/wasm
cd mychain
ignite wasm add          # wires x/wasm into app + cmd
# if the chain has no config yet:
ignite chain init
ignite wasm config       # writes wasm config into the chain's app.toml
```

- wasmd uses CGO (wasmvm). On Ubuntu/WSL: `sudo apt-get install build-essential`. Release builds need the matching `libwasmvm` (static muslc for Alpine/Docker) — `CGO_ENABLED=0` will not work.
- Permissioned uploads (recommended for mainnet, open later via governance):

```yaml
# config.yml (dev) — mirror these values in the real genesis
genesis:
  app_state:
    wasm:
      params:
        code_upload_access:
          addresses: []
          permission: "Nobody"        # or "AnyOfAddresses" with an allowlist; "Everybody" = permissionless
        instantiate_default_permission: "Nobody"
```

- Smart query gas limits and `memory_cache_size` live in app.toml `[wasm]` — set them on public RPC nodes.
- Contract dev workflow: build with `cosmwasm/optimizer` docker image, `mychaind tx wasm store`, `instantiate`, `execute`, `query wasm contract-state smart`.

## spaceship — SSH deploy (dev/test servers)

Requires Ignite ≥ v29.0.0.

```bash
ignite app install -g github.com/ignite/apps/spaceship
ignite spaceship deploy <user>@<ip> --key $HOME/.ssh/id_rsa
ignite spaceship deploy <user>@<ip> --password
ignite spaceship deploy <ip> --user root --key $HOME/.ssh/id_rsa
ignite spaceship deploy <user>@<ip> --key $HOME/.ssh/id_rsa --key-password <pw>
ignite spaceship deploy <user>@<ip> --key ~/.ssh/id_rsa --faucet [--faucet-port 8077]
ignite spaceship deploy <user>@<ip> --key ~/.ssh/id_rsa --init-chain   # re-init home on redeploy

ignite spaceship status  <user>@<ip> --key ~/.ssh/id_rsa
ignite spaceship log     <user>@<ip> --key ~/.ssh/id_rsa [--real-time] [--app faucet]
ignite spaceship restart <user>@<ip> --key ~/.ssh/id_rsa
ignite spaceship stop    <user>@<ip> --key ~/.ssh/id_rsa
```

Builds locally, inits the chain locally from `config.yml` (validators section → app/config/client toml), copies to `$HOME/workspace/<chain-id>/{bin,home,log,run.sh,spaceship.pid}` and starts with `nohup`.

Limits: single validator, dev keyring, no systemd, no sentry, no TLS. Prefer key auth over `--password` / `--user-password` (those end up in shell history). For anything public, follow `stack-cosmos-ignite` → `references/production.md` §8.

## network — coordinated launch on Ignite Chain

```bash
ignite app install -g github.com/ignite/apps/network@latest
# `ignite n` is shorthand for `ignite network`
```

Coordinator:

```bash
ignite n chain publish github.com/org/mychain [--genesis-url <url-to-genesis.json-or-tarball>]   # → Launch ID
ignite n request list <launch-id>
ignite n request approve <launch-id> 1,2      # also "1-3,4"
ignite n request reject  <launch-id> 3
ignite n chain launch <launch-id> [--launch-time 2026-12-01T00:00:00Z]
```

Validator:

```bash
ignite n chain list
ignite n chain init <launch-id>                        # interactive: stake, commission → gentx
ignite n chain join <launch-id> --amount 100000000stake [--gentx path/to/gentx.json]
ignite n chain prepare <launch-id>                     # final genesis + config; prints start command
# advanced/manual node setup:
ignite n chain show genesis <launch-id>
ignite n chain show peers <launch-id>
```

Other requests: `ignite n request add-account <id> <addr> <coins>`, `remove-account`, `remove-validator`. Request types on-chain: AddGenesisAccount, AddVestingAccount, AddGenesisValidator, RemoveAccount, RemoveValidator, ChangeParam. Approvals are irreversible; revert via the opposite request.

Use when you need public, auditable coordination of a genesis with independent validators. Check the Ignite Chain network is live/supported for your target before planning a mainnet around it; otherwise use the manual gentx flow in `stack-cosmos-ignite`.

## explorer — Gex (TUI) / Ping.pub (web)

```bash
ignite app install -g github.com/ignite/apps/explorer
ignite chain serve                                   # in another terminal
ignite explorer gex --rpc-address http://localhost:26657
ignite explorer pingpub --port 8080                  # needs Node.js ≥ 18 + Yarn
```

## connect — interact with any Cosmos SDK chain

```bash
ignite app install -g github.com/ignite/apps/connect
ignite connect discover               # list chains (chain registry)
ignite connect add atomone            # by registry name
ignite connect add simapp localhost:9090   # local chain via gRPC
ignite connect                        # list connected chains
ignite connect rm atomone
```

Generates CLI commands from the chain's reflection/AutoCLI — useful for scripting against other chains (e.g. IBC counterparties).

## cca — chain frontend

Requires Ignite ≥ v28.7.0, Node.js, Corepack.

```bash
ignite app install -g github.com/ignite/apps/cca
ignite chain serve                    # terminal 1
ignite s cca                          # terminal 2 → web/
cd web && yarn install && yarn dev
```

Based on Cosmology create-cosmos-app (cosmos-kit wallets, telescope/interchainjs clients).

## fee-abstraction

Requires Ignite ≥ v28.5.2.

```bash
ignite app install -g github.com/ignite/apps/fee-abstraction
ignite s chain mars --fee-abstraction
```

Adds osmosis-labs fee-abstraction module so users can pay fees with IBC tokens (priced via Osmosis TWAP). Production: needs a live IBC channel to Osmosis + ICQ, configured host zone params, and relayer support.

## evolve — rollups (formerly Rollkit)

Requires Ignite ≥ v28.9.0.

```bash
ignite s chain gm --address-prefix gm --minimal --no-module
cd gm
ignite app install -g github.com/ignite/apps/evolve@latest
ignite evolve add
ignite chain build --skip-proto
ignite evolve init                        # only for new (genesis) chains
go tool github.com/evstack/ev-node/tools/local-da    # local DA (or use Celestia)
gmd start --rollkit.node.aggregator
```

Migrating a live CometBFT chain:

```bash
ignite evolve add-migrate     # adds migration module
# add the module in an upgrade handler, pass gov proposal for validator-set migration
# after the chain halts, on every node:
gmd evolve-migrate
# then follow the normal `evolve add` flow
```

Docs: https://ev.xyz/

## gnovm

Requires Ignite ≥ v29.5.0, non-minimal chain.

```bash
ignite s chain gm --address-prefix gm --no-module
cd gm
ignite app install -g github.com/ignite/apps/gnovm
ignite gnovm add
```

## appregistry

```bash
ignite app install -g github.com/ignite/apps/appregistry
ignite appregistry list
ignite appregistry details <app_name>
ignite appregistry install <app_name>
```

Community apps are listed via the Ignite app registry repository (PR an entry to publish yours).
