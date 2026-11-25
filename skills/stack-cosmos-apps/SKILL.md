---
name: stack-cosmos-apps
description: Use Ignite Apps (github.com/ignite/apps), the plugin ecosystem of Ignite CLI — Hermes IBC relayer, CosmWasm smart contracts (`ignite wasm`), Spaceship SSH deployment, Ignite Network coordinated validator launches, Gex/Ping.pub explorers, Connect to any Cosmos chain, CCA frontend scaffolding, Osmosis fee abstraction, Evolve (Rollkit) rollups, GnoVM, the app registry — and writing your own Ignite App with commands and hooks. Use whenever the user wants to relay IBC between chains, add CosmWasm, deploy a chain to a server, coordinate a genesis with validators, explore a running chain, build a chain frontend, turn a Cosmos chain into a sovereign rollup, or extend `ignite` with custom commands. For EVM/Solidity use the `stack-cosmos-evm` skill instead.
license: MIT
---

# Ignite Apps adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). It extends `stack-cosmos-ignite` with Ignite Apps: Go plugins (hashicorp go-plugin over gRPC) that add commands and hooks to `ignite`. Each app lives in its own Go module in https://github.com/ignite/apps. EVM is a separate adapter: `stack-cosmos-evm`.

| Reference | Read when |
|---|---|
| `references/apps.md` | Using any app: full commands, flags, gotchas |
| `references/authoring.md` | Writing your own Ignite App |
| `references/placement-map.md` | Deciding which app covers a protocol component |

## Adapter metadata
- Family: cosmos
- Stack: Ignite Apps on top of an Ignite-scaffolded Cosmos SDK chain
- Versions verified: ignite/apps main branch. Per-app minimum Ignite versions are in the catalog below. App code targets `github.com/ignite/cli/v29`.
- Verified on: 2026-11-25 (from each app's README, app.ignite.yml, and the evm, fee-abstraction and examples source)
- Sources: github.com/ignite/apps (main), docs.ignite.com/apps
- Compatibility (checked 2026-11-25): every official app on ignite/apps main still targets `github.com/ignite/cli/v29` (evm and gnovm v29.9.2, wasm/hermes/spaceship/explorer/evolve v29.8.0, network v29.4.0). Ignite **v30** (release candidate) changes the plugin module path to `.../cli/v30`, so apps need v30 builds before they work with Ignite v30. Use Ignite v29.10.x with these apps until their maintainers publish v30 versions.
- Unverified parts: app flags not shown in the READMEs (check `ignite <app> --help`), and whether the Ignite Chain network for `network` is live

## When to use this adapter
Use it on a Cosmos SDK chain built with `stack-cosmos-ignite` that needs one of: IBC relaying, CosmWasm, GnoVM, a sovereign rollup on a DA layer (Evolve), a quick SSH deployment, coordinated genesis via Ignite Chain, explorers, a frontend, or fee abstraction. It's also for writing custom Ignite tooling.

## Placement map
Summary of `references/placement-map.md`:
- Native: interop (hermes), smart-contracts (wasm, gnovm)
- Extend: data-availability and rollup (evolve), node-software (spaceship, explorer, connect, cca), tokenomics (fee-abstraction)
- Everything else: as `stack-cosmos-ignite`

## Setup

```bash
ignite app install -g github.com/ignite/apps/<app>          # -g = global (all chains); omit for current chain only
ignite app install -g github.com/ignite/apps/<app>@<ref>    # pin a version/tag/commit, e.g. evolve@latest
ignite app install -g /abs/path/to/local/app                # local checkout (dev)
ignite app list
ignite app uninstall -g github.com/ignite/apps/<app>
```

Run `ignite app --help` for the update/describe subcommands in your Ignite version. Every app pins a minimum Ignite version: check `ignite version` against the catalog first, since mismatched versions are the most common failure.

## Implement

Pick the app by need:

| Need | App | Min Ignite | Key commands |
|---|---|---|---|
| IBC relaying between two chains | `hermes` | v28 | `ignite relayer hermes configure`, `ignite relayer hermes start` |
| CosmWasm smart contracts | `wasm` | v28.3.0 | `ignite wasm add`, `ignite wasm config` |
| Deploy chain to a server over SSH | `spaceship` | v29.0.0 | `ignite spaceship deploy/status/log/restart/stop` |
| Coordinate genesis + validators on Ignite Chain | `network` | — | `ignite network chain publish/init/join/launch/prepare`, `ignite network request ...` |
| Explore a running chain (TUI / web) | `explorer` | v28.3.0 | `ignite explorer gex`, `ignite explorer pingpub` |
| Talk to any Cosmos chain from the CLI | `connect` | — | `ignite connect discover/add/rm` |
| Chain web frontend (create-cosmos-app) | `cca` | v28.7.0 | `ignite s cca` |
| Pay fees in IBC tokens (Osmosis fee abstraction) | `fee-abstraction` | v28.5.2 | `ignite s chain <name> --fee-abstraction` |
| Rollup on a DA layer (Evolve, ex-Rollkit) | `evolve` | v28.9.0 | `ignite evolve add/init/add-migrate` |
| Gno smart contracts | `gnovm` | v29.5.0 | `ignite gnovm add` |
| Discover/install community apps | `appregistry` | — | `ignite appregistry list/details/install` |
| EVM / Solidity | → `stack-cosmos-evm` | v29.5.0 | `ignite evm add/init` |

Full usage, flags and gotchas per app are in `references/apps.md`. Read the section for your app before running it. `consumer` exists in the repo but is internal (ICS consumer chains), so never install it manually.

To write your own app, read `references/authoring.md`. In short: `ignite app scaffold <name>`, implement `Manifest` (commands and hooks) and the `Execute*` methods, then install locally with `ignite app install -g $(pwd)`.

## Test
- After any app that rewrites code (`wasm add`, `evolve add`, `evm add`, `fee-abstraction`), run `go build ./... && go test ./...` and review `git diff`.
- IBC: test with two local chains and `hermes` before any public testnet. Cover packet timeouts and relayer restarts.
- Custom apps: `integration/app_test.go` pattern in `references/authoring.md`.

## Production
- Spaceship is for dev and test servers: single node, a `nohup` runner, config from `config.yml`. A mainnet validator needs the `stack-cosmos-ignite` production checklist (systemd, sentries, remote signer, real genesis).
- Hermes via this app is for local and dev relaying. Production relayers run Hermes directly, with their own config, funded keys, monitoring, and packet clearing tuned.
- CosmWasm on mainnet: make code upload permissioned (`references/apps.md` → wasm).
- Evolve: decide the DA layer, aggregator/sequencer operations and the migration path before launch.

## Known pitfalls
- Apps rewrite your chain's code. Commit before running them.
- wasm needs CGO (libwasmvm). `CGO_ENABLED=0` builds fail, and Alpine/Docker needs the muslc static library.
- `--password` / `--user-password` on spaceship end up in shell history. Use SSH keys.
- Network approvals are irreversible. Revert with the opposite request.
- `evolve` needs a minimal chain without the default module (`--minimal --no-module`). evm and gnovm need a non-minimal chain.

## Updating this adapter
Run `build-stack-adapter` in refresh mode. Re-read the READMEs, `app.ignite.yml` and each app's CHANGELOG in ignite/apps, then update the catalog, `references/apps.md` and the "Versions verified" field.
