---
name: stack-cosmos-ignite
description: Build, harden and ship production-grade Cosmos SDK blockchains with Ignite CLI (ignite.com). Use this skill whenever the user wants to scaffold a new blockchain or appchain, add Cosmos SDK modules/messages/queries/types, run a local chain with `ignite chain serve`, write keeper logic, add IBC, plan chain upgrades, prepare a mainnet/testnet launch (genesis, gentx, validators), implement a chainskills design on Cosmos SDK, or make an existing Ignite/Cosmos chain "production ready" — even if they only say "blockchain", "appchain", "Cosmos", "Starport", "L1", or "my own chain" without naming Ignite.
license: MIT
---

# Cosmos SDK + Ignite adapter

Stack adapter in the chainskills suite (router: `blockchain-dev`). Designs and specs come from `design-*` and `protocol-*` skills. This skill maps them onto Cosmos SDK modules built with Ignite. Sibling adapters: `stack-cosmos-evm` (EVM/Solidity), `stack-cosmos-apps` (Hermes, CosmWasm, Spaceship deploy, Network launch, explorers, rollups).

Ignite scaffolds the app wiring, protobuf, keepers, CLI, OpenAPI and TS client. That's the easy 10%. A chain is production-level only when the state machine is deterministic, every message is validated, state can be migrated, and nodes can be run safely.

If the project has a `CHAIN.md`, read its Stack placement table and the spec of the component you're building (`docs/spec/<component>.md`) first. Implement exactly what the spec says. Name tests after the invariant IDs they check (`TestINV_STAKE_2`). When a component is built and tested, set its status in `CHAIN.md`.

| File | Read when |
|---|---|
| `references/placement-map.md` | Deciding where a protocol component goes in Cosmos SDK |
| `references/cli.md` | Running any `ignite` command (scaffold, serve, build, generate, apps, testnet) |
| `references/config-yml.md` | Editing `config.yml` (dev accounts, genesis overrides, validators, build flags) |
| `references/module-dev.md` | Writing keeper / msg server / query code inside `x/<module>` |
| `references/production.md` | Hardening, testing, upgrades, genesis launch, node ops, release |

## Adapter metadata
- Family: cosmos
- Stack: Cosmos SDK app chain on CometBFT, scaffolded with Ignite CLI
- Versions verified: **Ignite v29.10.1** (latest stable, 16 Jun 2026) scaffolds Cosmos SDK v0.53.6 + CometBFT v0.38.21 + IBC v10, which is the **2025.1 release family** (still supported). **Ignite v30.0.0** (release candidate rc.2, 24 Sep 2026) scaffolds SDK v0.55.0 + CometBFT v0.40.0 + IBC v11.2.0, which is the current **2026.1 family**. SDK ≤ 0.50, CometBFT ≤ 0.37 and the retracted CometBFT v1.x are end-of-life or unsupported.
- **v30 command change:** Cosmos commands move under `ignite cosmos` (`ignite cosmos scaffold chain`, `ignite cosmos chain serve`, `ignite cosmos generate`, `ignite cosmos testnet`, `ignite cosmos doctor`). Top-level `scaffold`/`chain`/`account`/`generate` then target gno.land. Run `ignite version` and use the matching syntax. Examples here use v29 syntax.
- Moving a v29 chain to SDK v0.55 is a manual migration (docs.ignite.com/migration/v30.0.0): bump go.mod, update import paths (`x/evidence|feegrant|upgrade` move into the SDK, `log/v2`, `store/v2`), remove `x/params`/`x/group`/`x/circuit`/`x/nft`, add the staking `KeyRotationFeePoolName` module account, put bank first in EndBlockers, and drop `traceStore` from the app constructor. v30 scaffolding against an unmigrated v0.53 chain produces code that doesn't compile.
- Verified on: 2026-11-25 (CLI and config references re-checked against the v29.10.1 docs in the ignite/cli repo)
- Sources: github.com/ignite/cli (tags v29.10.1, v30.0.0-rc.1/rc.2; docs/docs/03-CLI-Commands, 06-migration/v30.0.0.md, 08-configuration), github.com/ignite/apps (main), docs.cosmos.network/sdk/latest/release-family, docs.cosmos.network/sdk/latest/upgrade/v0.54 and v0.55
- Unverified parts: `ignite scaffold single` flags; v30 behaviour until v30.0.0 final ships (re-check the release notes).

If a command or API here disagrees with reality, trust `ignite <cmd> --help`, the scaffolded code and `go.mod`.

## When to use this adapter
Sovereign PoS L1s or appchains (or ICS consumer chains via `validation: consumer`) that need native modules, their own validator set with BFT single-block finality, IBC, and Go. EVM compatibility on top → also `stack-cosmos-evm`. CosmWasm, rollup mode (Evolve) or GnoVM → also `stack-cosmos-apps`. For L2 rollups on Ethereum, use a `stack-rollup-*` adapter instead.

## Placement map
Summary of `references/placement-map.md`:
- Native: consensus (CometBFT), staking-validators (x/staking, x/slashing), tokenomics (x/mint, x/distribution), governance (x/gov), p2p, interop (IBC), upgrades (x/upgrade + Cosmovisor)
- Extend: state-execution, node-software, smart-contracts (CosmWasm/EVM via apps), data-availability (Evolve)
- Custom: randomness, verifiable-participation
- n/a: rollup (except sovereign rollup via Evolve)

## Setup

```bash
go version          # v29 chains: Go 1.25+; v30 chains: Go 1.26+ (match the go directive in go.mod)
ignite version      # v29.x → `ignite scaffold/chain ...`; v30.x → `ignite cosmos scaffold/chain ...`
```

- Not installed: `curl https://get.ignite.com/cli! | bash` (Linux/macOS) or `brew install ignite`.
- Windows: Ignite does not run natively. Use WSL2 and keep the project inside the WSL filesystem (`~/...`, not `/mnt/c/...`), because cross-filesystem builds are very slow.
- Also useful: `buf` (proto lint and breaking-change checks), `golangci-lint`, `govulncheck`, Docker.

Decide these before scaffolding. They come from `CHAIN.md` if it exists:
- **Chain identity**: Go module path (`github.com/org/mychain`), bech32 address prefix, chain-id (`mychain-1`), staking/fee denom (`umychain`, 6 decimals by convention; 18 decimals if EVM).
- **Modules**: one per spec component. Declare dependencies on built-ins (`bank`, `staking`, `account`, ...) with `--dep`.
- **State**: for each entity, choose `list` (auto-increment ID), `map` (custom key), `single` (one value), or plain `type`.
- **Messages** (state changes) vs **queries** (reads), and which messages are governance-only.
- **IBC**: if needed, add `--ibc` to the module and use `scaffold packet`. Relay with Hermes (`stack-cosmos-apps`).
- **VM**: for EVM, scaffold with `--no-module` and without `--minimal`, then `stack-cosmos-evm`. CosmWasm/GnoVM → `stack-cosmos-apps`. Rollup → `stack-cosmos-apps` (evolve, `--minimal --no-module`). These flags must be right at scaffold time.

Scaffold names become proto packages, store keys and CLI commands, so renaming after launch means a migration.

```bash
ignite scaffold chain github.com/org/mychain --address-prefix mychain
cd mychain
ignite scaffold module blog --dep bank
ignite scaffold list post title body --module blog
ignite scaffold message tip-post id:uint amount:coin --module blog --response tipped:bool
ignite scaffold query posts-by-author author --module blog --response posts:Post
```

See `references/cli.md` for every scaffold type, field type and flag. Run `go build ./...` after each scaffold, and commit between scaffolds so `git checkout .` is the undo button.

## Implement

Scaffolded handlers are stubs or naive CRUD. Fill them following `references/module-dev.md`. Map spec sections as follows: State → `collections`, Operations → msg server handlers (checks C-n in order, then effects E-n), Hooks → `BeginBlock`/`EndBlock`/`PreBlock`, Parameters → module params with `Validate()` bounds, Events → typed proto events.
- Validate every msg field (addresses via the address codec, length and amount bounds, authority).
- Use `math.Int`/`math.LegacyDec` for numbers and take block time from the context.
- Register errors with stable codes.

Then run the state-machine audit:

```bash
python3 <skill-dir>/scripts/audit_state_machine.py .
```

It flags non-determinism hazards in non-test module code: wall-clock time, `math/rand`, floats, goroutines, env/network I/O, map iteration. Fix each finding, or justify it with `// audit:ok <reason>`.

Run locally:

```bash
ignite chain serve                # build, init, start, hot-reload
ignite chain serve --reset-once   # wipe state once (after genesis/proto changes)
mychaind tx blog create-post "hi" "body" --from alice --chain-id mychain --yes
mychaind q blog list-post
```

## Test

The minimum bar is below; details are in `references/production.md` §5.
- Keeper/msg-server unit tests for the happy path **and** every rejection check (C-n).
- An invariant test per INV-ID, run after randomized operation sequences.
- Genesis export → import round-trip test per module.
- `go test -race ./...`, `golangci-lint run`, `govulncheck ./...`.
- Simulation: `ignite chain simulate` (or the app's `TestFullAppSimulation`) with module simulation ops filled in.
- `buf lint`, and once released, `buf breaking --against` the last release tag.

## Production

Walk `references/production.md` top to bottom and report each item as done / N/A / TODO. It covers determinism, DoS and gas bounds, authority on privileged messages, upgrade handlers and store migrations, real genesis (not `config.yml`), keyring and validator security, and release binaries.

## Known pitfalls
- `config.yml` is a **dev** tool. Build mainnet/testnet genesis with `<chaind> init` and the `genesis` subcommands, never from `config.yml` and never with its demo mnemonics.
- Never renumber protobuf fields, error codes or store prefixes after a release. Add new ones and mark old field numbers `reserved`.
- Every change to state layout after launch needs a consensus-version bump, a migration and an upgrade handler.
- `BeginBlock`/`EndBlock` run without a gas limit. Unbounded loops there halt the chain.
- Prefer maintained SDK modules (authz, feegrant, gov, staking, distribution) over custom code for the same job. Since SDK v0.54, `x/circuit`, `x/nft` and `x/crisis` live in `contrib/` and are no longer maintained by Cosmos Labs. `x/group` and the PoA module are Cosmos Enterprise modules, which need a licence for production use.
- SDK v0.55+: validators can rotate consensus keys (`MsgRotateConsPubKey`). Indexers and monitoring must not treat a validator's consensus address as permanent.
- When unsure whether something is consensus-critical, assume it is.

## Updating this adapter
Run `build-stack-adapter` in refresh mode after new Ignite or SDK major releases. Re-check `references/cli.md` against `ignite --help`, and update the "Versions verified" field.

## Output to the user
After each milestone, report: what was scaffolded or changed (files), how to run it (exact commands), and what remains on the production checklist.
