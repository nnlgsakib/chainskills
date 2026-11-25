---
name: protocol-state-execution
description: Design how a blockchain stores state and executes transactions, independent of stack — account vs UTXO vs object model, VM choice (native modules, EVM, WASM/CosmWasm/Stylus, Move, SVM, zkVM), EVM fork compatibility (Prague/Osaka/Amsterdam opcodes and limits), gas and fee metering, state commitment structures (IAVL, Merkle-Patricia, JMT, sparse/binary trees), parallel execution (Block-STM, access lists, block-level access lists), state growth controls (deposits, rent, expiry), and determinism rules. Use whenever the user asks which VM or execution model to use, how to price gas, how to make execution parallel or faster, how to structure state or storage, how to stay EVM-equivalent, or how to stop state bloat.
license: MIT
---

# Protocol State & Execution

A building-block skill in chainskills (layer L2, stack-neutral). It decides the execution environment and state model. `design-spec` uses the result for every component's State and Operations sections, so settle this before specifying components in depth.

Inputs from `CHAIN.md`: functional requirements (who deploys logic), throughput and latency targets, constraints (EVM-compatible? team language?), architecture class. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/vm-comparison.md` | Choosing an execution environment; EVM fork compatibility |
| `references/gas-and-fees.md` | Metering and pricing resources |
| `references/state-and-parallelism.md` | State commitment, storage layout, parallel execution, state growth |

## Workflow

### 1. Logic model
Who writes on-chain logic?
- Only the core team, at launch and for a long time: **native** state machine (modules, pallets, custom app). This is fastest and fully controllable, but every change is a chain upgrade.
- Third parties deploy logic: a **VM**. The ecosystem you need decides which one (`references/vm-comparison.md`). Being EVM-compatible brings Solidity, wallets and tools, and also the obligation to track Ethereum forks.
- Hybrid (native modules plus a VM): common, and the cleanest place for protocol-critical logic. Expose native features to contracts through precompiles.

### 2. Data model
Account, UTXO or object model. The account model is the default and has the best tooling. UTXO and object models make parallelism and some privacy designs easier. Record the decision as an ADR.

### 3. State commitment and storage
Pick the authenticated structure (IAVL, Merkle-Patricia, JMT, sparse Merkle, binary tree) by proof size, write amplification, and light-client and bridge needs (`references/state-and-parallelism.md`). The bridges and light clients in `protocol-interop` verify these proofs, so changing the structure later breaks them.

### 4. Metering and fees
Every operation that consumes a resource (compute, storage write, storage growth, bandwidth, proof verification) has a cost that a user pays. Method in `references/gas-and-fees.md`: benchmark, price each resource, add a safety margin, cap per-tx and per-block usage. The fee market design (EIP-1559-style base fee, priority fee, burn or redistribution) feeds `protocol-tokenomics`.

### 5. Parallelism (only if throughput needs it)
Measure first. Options, from cheapest to most invasive: optimistic parallel execution (Block-STM), declared access sets (Solana-style), block-level access lists (Ethereum EIP-7928, Glamsterdam), object ownership (Sui-style). Determinism is the constraint: the parallel result must equal a sequential execution in a fixed order.

### 6. State growth
Decide who pays for state forever: storage deposits refunded on deletion, rent, expiry, or pruning-friendly designs. Unbounded free state is the most common long-term cost failure.

### 7. Determinism rules
Adopt the nine rules in `../design-spec/references/notation.md` as chain-wide requirements, and add any VM-specific ones (for example banned opcodes, or float-free WASM).

### 8. Hand off
ADRs (logic model, VM, data model, commitment structure, fee model), parameters (`P-EXEC-*`: block gas, per-tx gas cap, storage deposit, ...), invariants (supply conservation, fee accounting). Then `CHAIN.md` → component `execution` → `designed`.

## Rules
- EVM-compatible means compatible with a specific fork. Name it (e.g. Osaka), test against it, and publish it so developers set `evm_version` correctly. Solidity has compiled for `osaka` by default since 0.8.31, so contracts built with defaults can contain opcodes such as CLZ that a chain stuck on an older fork rejects.
- Every resource has a price, and every price has a cap.
- Native code that contracts can call (precompiles) is consensus code: it must be deterministic, gas-metered and audited.
- Keep execution independent of node configuration, so the same block always gives the same state on every node.

## Sources (verified 2026-11-25)
Cosmos Block-STM (SDK v0.54+, config in v0.55): docs.cosmos.network/sdk/latest/upgrade/v0.55 · Glamsterdam scope (EIP-7928, EIP-7954, ...): ethereum.org/roadmap/glamsterdam · Fusaka (live 3 Dec 2025, EIP-7825 tx gas cap 2^24): ethereum.org/roadmap/fusaka, blog.ethereum.org/2025/10/21/fusaka-gascap-update · Solidity defaults: soliditylang.org/blog (0.8.31, 0.8.37, 0.8.39) · EIP-7864 (binary tree, still Draft): eips.ethereum.org/EIPS/eip-7864.
