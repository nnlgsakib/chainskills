# Toolchain (checked 2026-11-25)

Re-check these versions when starting a project: the release pages are listed at the bottom.

## Compiler: Solidity

| Item | Value |
|---|---|
| Latest | **0.8.39** (19 Nov 2026) |
| Minimum to use | **0.8.34**. It fixed a high-severity via-IR bug where clearing could hit a storage variable instead of a transient one. Later releases fixed further optimizer and storage-corruption bugs (0.8.36–0.8.39), so prefer the latest |
| Default EVM version | `osaka` since 0.8.31. Amsterdam support since 0.8.36 |
| Deprecated EVM targets | constantinople, petersburg, istanbul, berlin (0.8.37) |
| Useful recent features | transient storage state variables (0.8.28), custom errors in `require` (0.8.26 IR / 0.8.27 legacy), `clz` Yul builtin (0.8.31), `erc7201` builtin for namespaced storage slots (0.8.35), `block.slotnum` (0.8.37, Amsterdam) |
| 0.9.0 deprecations (warnings since 0.8.31) | `send`/`transfer` on addresses, ABI coder v1, virtual modifiers, `memory-safe-assembly` comment, contract-type comparisons |

Settings:
- Pin an exact version (`pragma solidity 0.8.39;` or `=0.8.39` in config). Avoid floating `^` pragmas in deployable contracts.
- Set `evm_version` to what the **target chain** supports. Many EVM chains lag Ethereum forks, and contracts compiled for `osaka` may use opcodes (e.g. CLZ) they reject.
- `via_ir = true` gives better optimisation but slower builds. Test with the same settings you deploy with.

## Framework: Foundry

| Item | Value |
|---|---|
| Latest stable | **v1.10.0** (19 Nov 2026) |
| Big change | revm replaced by **evm2** across forge/anvil/cast/chisel; `forge test` up to 4.5× faster. Gas snapshots must be regenerated |
| Invariant testing | snapshot fuzzing on by default; minimized counterexamples; handler assertion messages |
| Other | Solar compiler support (`solc = "solar:<version>"`); `forge coverage --keep-optimizer`; new lints for ERC-7201 namespace collisions; `forge equivalence` (bytecode equivalence checks) |
| Breaking in 1.10 | only suites under `src`, `test`, `script` are discovered; dependency remapping conflicts are scoped to the dependency; fork warmth/transient storage no longer leak from `setUp` |

```toml
# foundry.toml (baseline)
[profile.default]
solc = "0.8.39"
evm_version = "osaka"        # set to the TARGET CHAIN's fork
optimizer = true
optimizer_runs = 200
via_ir = false
fuzz = { runs = 1000 }
invariant = { runs = 256, depth = 64, fail_on_revert = false }

[profile.ci]
fuzz = { runs = 10000 }
invariant = { runs = 1000, depth = 128 }
```

## Framework: Hardhat 3
Stable and production-ready (the Hardhat 2 end-of-life page says so). It has Foundry-compatible Solidity tests (`*.t.sol`, run with `npx hardhat test solidity`), TypeScript tests next to them, and built-in coverage (`--coverage`). Choose it when the team is TypeScript-first or uses Ignition deployments.

## Libraries
- **OpenZeppelin Contracts 5.7.0** (29/30 Jul 2026). Notable recent additions: ERC-4337 paymasters, cross-chain bridges via ERC-7786 gateways (`BridgeFungible`, `BridgeERC721`, ...), `GovernorCrosschain`, `Create3`, `RateLimiter`, `ERC20TransferAuthorization` (ERC-3009).
- Breaking changes to check when upgrading: 5.7 limits `EIP712` name/version to 31 bytes, changes Governor queue errors, and drops the `draft-` prefix from the ERC-4337 files. 5.6 makes proxies revert without an initializer, and single-item ERC1155 batches call `onERC1155BatchReceived`.

## Analysis tools
| Tool | Type | Use |
|---|---|---|
| `forge lint` | static, built into Foundry | every build |
| Slither (Trail of Bits) | static, 90+ detectors | CI on every PR |
| Aderyn (Cyfrin) | static, Rust | fast second opinion |
| Echidna / Medusa (Trail of Bits) | property/invariant fuzzers | long fuzz campaigns on critical contracts |
| Halmos / hevm | symbolic execution | prove critical properties |

## Sources
- https://soliditylang.org/blog/category/releases/ · https://github.com/ethereum/solidity/releases
- https://github.com/foundry-rs/foundry/releases
- https://hardhat.org/docs/reference/hardhat-2-end-of-life · https://hardhat.org/docs/learn-more/solidity-tests
- https://www.openzeppelin.com/news/introducing-openzeppelin-contract-5-7 · https://github.com/OpenZeppelin/openzeppelin-contracts/releases
- https://trailofbits.com/tools/ · https://ethereum.org/developers/tutorials/guide-to-smart-contract-security-tools/
