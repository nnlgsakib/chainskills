# Execution environments

Status facts checked 2026-11-25 are marked ✔.

## Options

| Environment | Languages | Ecosystem / tooling | Determinism & metering | Where it runs | Pick when |
|---|---|---|---|---|---|
| Native state machine | Go (Cosmos SDK), Rust (Substrate, custom) | framework-specific | you control it (gas meter per op) | any sovereign chain | protocol logic written by the core team; maximum control |
| EVM | Solidity, Vyper | largest: wallets, Foundry/Hardhat, OpenZeppelin, explorers, indexers | built-in gas schedule; follows Ethereum forks | EVM L1s, L2s, Cosmos EVM, Avalanche, Substrate (Frontier) | users and devs expect Ethereum tooling |
| WASM (CosmWasm) | Rust | Cosmos ecosystem | metered WASM, no floats | Cosmos chains (`ignite wasm`) | Rust contracts on Cosmos with IBC |
| WASM (Stylus) | Rust, C, C++ | Arbitrum; OpenZeppelin Contracts for Stylus exists ✔ | metered WASM, interoperates with the EVM | Arbitrum chains | compute-heavy contracts next to the EVM |
| Move | Move | Sui/Aptos ecosystems | resource-oriented safety | Move chains | asset-safety-first designs; teams that know Move |
| SVM | Rust (Anchor) | Solana ecosystem | declared accounts enable parallelism | Solana and SVM forks/rollups | Solana tooling and parallel execution |
| zkVM (RISC-V) | Rust (and others via RISC-V) | SP1, Risc0, ZKsync Airbender ✔ | proving cost dominates | proving off-chain, verification on-chain | ZK rollups, verifiable off-chain compute |

## EVM fork compatibility (checked 2026-11-25)

An "EVM-compatible" chain has to say which Ethereum fork's EVM it matches:

| Fork | Mainnet | Relevant to EVM chains |
|---|---|---|
| Prague/Electra (Pectra) | May 2025 | EIP-7702 (EOAs delegate to code; breaks `tx.origin`/EOA assumptions ✔), BLS12-381 precompile |
| Fulu/Osaka (Fusaka) | 3 Dec 2025 ✔ | PeerDAS; per-tx gas cap 2^24 = 16,777,216 (EIP-7825) ✔; CLZ opcode (Solidity `clz` Yul builtin for osaka) ✔; Fusaka dev guides list 12 EIPs incl. a secp256r1 precompile and an RLP block size limit (verify the per-EIP list before relying on it) |
| Gloas/Amsterdam (Glamsterdam) | expected Q4 2026, date not confirmed ✔ | ePBS (EIP-7732), block-level access lists (EIP-7928), contract code size limit raised to 64 KiB and initcode to 128 KiB (EIP-7954, used by Solidity 0.8.39 warnings) ✔, gas repricings |

Consequences:
- Solidity defaults to `osaka` since 0.8.31 ✔. Supported targets were narrowed in 0.8.37, which deprecated constantinople through berlin ✔. If your chain lags, tell developers the `evm_version` to use, and reject unknown opcodes clearly.
- Following Ethereum forks is ongoing work for every EVM chain: put "fork-compat upgrade" on the upgrade roadmap (ops-upgrades).
- Changes to gas cost and code size limits change which contracts deploy, so publish your chain's values.

## Precompiles
Native functions exposed to the VM (staking, governance, bridging, crypto). They run with native performance and privileges, so they get the same review as consensus code: deterministic, metered, bounded input sizes, and audited.

Sources: https://ethereum.org/roadmap/fusaka/ · https://blog.ethereum.org/2025/10/21/fusaka-gascap-update · https://ethereum.org/roadmap/glamsterdam/ · https://soliditylang.org/blog/category/releases/ · https://ethereum.org/roadmap/pectra/7702/ · https://www.zksync.io/airbender · https://docs.openzeppelin.com/contracts-stylus/changelog
