# Production checklist

Report each item as DONE / N/A / TODO with a one-line reason. Do not mark DONE without evidence (test name, file, command output).

## Contents
1. State-machine determinism
2. Input validation and authorization
3. Gas, DoS and state bloat
4. Storage and protobuf compatibility
5. Testing
6. Upgrades and migrations
7. Genesis and launch
8. Node and validator operations
9. Build and release
10. Security and dependencies
11. Ecosystem integration

## 1. State-machine determinism

Every node must compute the same state from the same blocks, or the chain halts (consensus failure / app hash mismatch).

- [ ] No `time.Now()` — use `sdkCtx.HeaderInfo().Time` / `BlockTime()`.
- [ ] No `math/rand` / `crypto/rand` in tx or block logic. Randomness from block data is predictable; if needed, use a VRF/beacon design.
- [ ] No `float32/float64` — use `math.Int`, `math.LegacyDec`.
- [ ] No iteration over Go maps when the order affects writes, events, gas or output — sort keys first, or store in collections.
- [ ] No goroutines, `select`, channels in state transitions.
- [ ] No network, filesystem, env var or OS reads in state transitions.
- [ ] No reliance on `len()` of maps, pointer addresses, or `fmt` of maps.
- [ ] `scripts/audit_state_machine.py` clean or every finding justified.

## 2. Input validation and authorization

- [ ] Each msg server validates every field (see module-dev.md).
- [ ] Privileged msgs (`UpdateParams`, admin ops) check `authority` == gov module (or explicit admin set by gov).
- [ ] `Params.Validate()` has real bounds.
- [ ] Scaffolded owner checks on update/delete reviewed; not a substitute for business-level authorization.
- [ ] Module accounts that must not receive funds are blocked (`BlockedAddrs` in app wiring).
- [ ] Modules with mint/burn permissions are minimal (`app_config.go` `Permissions`).

## 3. Gas, DoS and state bloat

- [ ] No unbounded loops in `BeginBlock`/`EndBlock`/`PreBlock` (they run without a gas limit). Process a bounded batch per block, or use a queue.
- [ ] Tx-path loops bounded by msg-supplied, length-checked input.
- [ ] Heavy computation charges extra gas (`sdkCtx.GasMeter().ConsumeGas(n, "reason")`).
- [ ] Per-account limits / deposits on creating state (anti-spam).
- [ ] `minimum-gas-prices` set on every node; fee denom decided. Consider x/feemarket for dynamic fees.
- [ ] Queries paginated; no unbounded responses.

## 4. Storage and protobuf compatibility

- [ ] Proto packages versioned (`<chain>.<module>.v1`).
- [ ] Never renumber/reuse proto field numbers; deleted fields go in `reserved`.
- [ ] `buf lint` clean; `buf breaking --against '.git#tag=<last-release>'` in CI.
- [ ] Store prefixes and error codes frozen after release.
- [ ] Amino names (`amino.name` option) set for msgs if Ledger/legacy signing must work.

## 5. Testing

- [ ] Unit tests: every msg handler happy path + every rejection.
- [ ] Genesis round-trip (init → export → equal) per module.
- [ ] Invariant-style checks: e.g. module account balance == sum of tracked deposits.
- [ ] Simulation: module `simulation.go` ops implemented with realistic weights. Run `ignite chain simulate --numBlocks 500 --blockSize 200` and the SDK sim tests (`go test ./app -run TestFullAppSimulation -Enabled=true -NumBlocks=500 -Commit=true -v`). Also run app-state determinism test (`TestAppStateDeterminism`) if present.
- [ ] Integration/e2e: multi-node local network (`ignite testnet multi-node` or docker-compose), IBC with Hermes if IBC used (or interchaintest).
- [ ] `go test -race ./...`, `golangci-lint run`, fuzz tests for parsers/math.
- [ ] CI runs all of the above on every PR.

## 6. Upgrades and migrations

Software upgrades are coordinated through x/upgrade + governance; Cosmovisor swaps binaries at the upgrade height.

```go
// app/upgrades.go
const UpgradeName = "v2"

func (app *App) setupUpgradeHandlers() {
	app.UpgradeKeeper.SetUpgradeHandler(UpgradeName,
		func(ctx context.Context, plan upgradetypes.Plan, fromVM module.VersionMap) (module.VersionMap, error) {
			return app.ModuleManager.RunMigrations(ctx, app.Configurator(), fromVM)
		})

	info, err := app.UpgradeKeeper.ReadUpgradeInfoFromDisk()
	if err != nil {
		panic(err)
	}
	if info.Name == UpgradeName && !app.UpgradeKeeper.IsSkipHeight(info.Height) {
		app.SetStoreLoader(upgradetypes.UpgradeStoreLoader(info.Height, &storetypes.StoreUpgrades{
			Added: []string{ /* new module store keys */ },
		}))
	}
}
```

`storetypes` is `cosmossdk.io/store/types` on SDK v0.53 and `github.com/cosmos/cosmos-sdk/store/v2/types` on v0.55. When moving to v0.55, the same handler must also delete removed stores (`params`, and `protocolpool` if it was wired) and move any protocolpool balances (see the v0.55 upgrade guide).

```go
// x/<module>/module/module.go
func (AppModule) ConsensusVersion() uint64 { return 2 } // bump on state change

// in RegisterServices
if err := cfg.RegisterMigration(types.ModuleName, 1, m.Migrate1to2); err != nil { panic(err) }
```

- [ ] Every state-layout change: ConsensusVersion bump + migration + test.
- [ ] Upgrade rehearsed on an exported mainnet state (`ignite testnet in-place` or `<chaind> export` → new genesis) before proposal.
- [ ] Gov proposal `MsgSoftwareUpgrade` with height + `info` JSON containing binary URLs + checksums (for Cosmovisor auto-download).
- [ ] Validators run Cosmovisor; `DAEMON_ALLOW_DOWNLOAD_BINARIES` policy decided.
- [ ] Emergency path known: a pause mechanism for msg types (`contrib/x/circuit` is unmaintained since SDK v0.54, so maintain it yourself or write a scoped pause module), and a documented halt-height procedure.

## 7. Genesis and launch

Build real genesis with the binary, not `config.yml`:

```bash
mychaind init <moniker> --chain-id mychain-1 --default-denom umychain
mychaind genesis add-genesis-account <addr> 1000000000umychain
mychaind genesis gentx <key> 500000000umychain --chain-id mychain-1 --keyring-backend file
mychaind genesis collect-gentxs        # coordinator collects all validators' gentxs
mychaind genesis validate-genesis
```

(Older SDK: these are top-level subcommands without `genesis`.)

- [ ] chain-id final (`name-N`, increment N only on hard reset).
- [ ] Bond/fee/mint denoms set everywhere (staking, mint, gov min_deposit, and crisis if still wired). No leftover `stake`/`token` demo denoms.
- [ ] Bank `denom_metadata` for the native token.
- [ ] Gov: voting period (days, not seconds), min deposit, quorum/threshold; expedited params.
- [ ] Staking: unbonding time, max validators, min commission.
- [ ] Slashing: downtime window, slash fractions, jail duration.
- [ ] Mint: inflation range, goal bonded, blocks per year matched to block time.
- [ ] Token distribution reviewed; vesting accounts for team/investors.
- [ ] No demo accounts, no mnemonics in the repo.
- [ ] Final genesis sha256 published; validators verify before start.
- [ ] Incentivized/public testnet run with the exact release candidate before mainnet.

## 8. Node and validator operations

- [ ] Keyring backend `file` or `os` — never `test` — on any machine holding funds.
- [ ] Validator behind sentry nodes: validator `pex = false`, `persistent_peers` = sentries only; sentries list validator in `private_peer_ids`.
- [ ] Remote signer via CometBFT privval (`priv_validator_laddr`). Cosmos docs recommend **Cosmos-KMS** (github.com/cosmos/kms, v0.1.0, Jul 2026): PKCS#11 HSM or AWS KMS backend, outbound-only connections (`noise://` for mutual peer pinning), per-key double-sign state, and support for ed25519, secp256k1eth and ML-DSA-65. Migrate from TMKMS per docs.cosmos.network/sdk/latest/kms/migrate-from-tmkms. For a threshold/MPC signer, Horcrux (e.g. 3-of-5). Set `double_sign_check_height`, and never run two signers for the same key (connect one signer to several nodes instead).
- [ ] `minimum-gas-prices` in app.toml.
- [ ] Pruning: validators `default`/`everything`; archive/RPC nodes `nothing`.
- [ ] State sync snapshots on some nodes (`snapshot-interval`, `snapshot-keep-recent`).
- [ ] Public RPC/API/gRPC only on dedicated nodes, behind a reverse proxy with rate limits; validator never exposes them.
- [ ] Metrics: `prometheus = true` (config.toml), `telemetry.enabled = true` (app.toml); alerts on missed blocks, peers, disk, height stall.
- [ ] systemd units with restart, file limits (`LimitNOFILE`), log rotation.
- [ ] Backups of `priv_validator_key.json` and `node_key.json` offline; `priv_validator_state.json` never restored from an old backup (double-sign risk).

## 9. Build and release

```bash
ignite chain build --release --release.targets linux:amd64,linux:arm64,darwin:arm64   # tarballs + checksums in release/ (v30: ignite cosmos chain build ...)
```

- [ ] Version injected via ldflags (`version.Name`, `version.AppName`, `version.Version`, `version.Commit`); `mychaind version --long` shows them.
- [ ] Builds reproducible (`-trimpath`, pinned Go version, `CGO_ENABLED=0` unless a C dep is required).
- [ ] Docker image: multi-stage, non-root user, pinned base digest.
- [ ] GitHub release with binaries + checksums; tag = upgrade name.
- [ ] CHANGELOG marks state-breaking vs API-breaking vs non-breaking changes.

## 10. Security and dependencies

- [ ] `govulncheck ./...` clean.
- [ ] Cosmos SDK, CometBFT, IBC-go pinned to latest patch of their line (check security advisories).
- [ ] No `replace` directives pointing to forks without review.
- [ ] Custom modules externally audited before handling real value.
- [ ] IBC: consider rate-limit middleware and packet-forward middleware policy; channel/connection whitelist if needed.
- [ ] Bug bounty / security contact in README.

## 11. Ecosystem integration

- [ ] Chain registry entry (cosmos/chain-registry): chain.json + assetlist.json.
- [ ] Wallet support (Keplr/Leap) via chain registry or `experimentalSuggestChain`.
- [ ] Explorer (Ping.pub / Mintscan) configured.
- [ ] Public endpoints, seeds and persistent peers documented.
- [ ] TS client published (`ignite generate ts-client`) for frontends.
