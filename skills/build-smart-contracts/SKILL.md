---
name: build-smart-contracts
description: Build, test and harden production smart contracts for chain-level and application logic — Solidity/EVM with Foundry or Hardhat 3, OpenZeppelin Contracts 5.x, upgradeable proxies (UUPS/transparent, ERC-7201 namespaced storage, initializers), access control and timelocks, validator-set / staking / system contracts, rollup bridge contracts, precompile interfaces, EIP-7702-safe patterns, unit/fuzz/invariant/symbolic testing, static analysis (Slither, Aderyn, forge lint), deterministic deployment, and audit preparation against the OWASP Smart Contract Top 10 (2026). Use whenever the user writes, reviews, tests, deploys or upgrades smart contracts, implements a spec component as contracts, or builds validator-set, staking, governance or bridge contracts on any EVM chain.
license: MIT
---

# Build Smart Contracts

The contract implementation skill of chainskills (layer L3). It implements spec components (`docs/spec/<component>.md`) whose placement is `smart contract`, `system contract` or `L1 contract`. The mechanism design comes from `protocol-*` skills, and chain-specific deployment details from the `stack-*` adapter.

Scope today: **EVM / Solidity**. Rust (CosmWasm, Stylus), Move and ink! contracts belong to their stack adapters until dedicated references are added.

| Reference | Read when |
|---|---|
| `references/toolchain.md` | Setting up or upgrading a project; compiler and framework versions |
| `references/patterns.md` | Writing contracts: access control, upgrades, reentrancy, math, pausing, deployment |
| `references/security-checklist.md` | Before every review and audit; OWASP SC Top 10 2026 mapping |
| `references/validator-set-contracts.md` | Staking, validator-set, sequencer/operator registry or system contracts |

## Workflow

### 1. Read the spec
Load `docs/spec/<component>.md`. Map it as follows:

| Spec | Code |
|---|---|
| State | storage, as an ERC-7201 namespace if upgradeable |
| Operations | external functions, with checks C-n as `require`/custom errors in order and effects E-n after them |
| Hooks | keeper-triggered bounded functions, because contracts have no block hooks unless they're system contracts |
| Parameters | governable variables with bounds checks in their setters |
| Invariants | invariant tests named after their INV-IDs |

### 2. Set up the toolchain
Use `references/toolchain.md`: Foundry (v1.10) or Hardhat 3, a pinned `solc` (0.8.39 is the latest as of 2026-11-25; never older than 0.8.34, which fixed a high-severity IR bug), and `evm_version` set to the **target chain's** fork, not the compiler default (`osaka`).

### 3. Implement with standard building blocks
Use OpenZeppelin Contracts 5.x (5.7.0 is the latest as of 2026-11-25) instead of hand-rolling access control, proxies, tokens, governance, timelocks, reentrancy guards or rate limiters. Follow `references/patterns.md`. Key defaults:
- Explicit roles (`AccessControl` or `AccessManager`). Ownership transfers in two steps. Every privileged function sits behind a timelock unless it's emergency-only.
- If upgradeable: UUPS or transparent proxy, ERC-7201 namespaced storage, `_disableInitializers()` in the implementation constructor, and the initializer called in the same transaction as deployment. OpenZeppelin 5.6+ proxies revert at deployment without initializer data.
- Never use `tx.origin` or code-size checks to detect EOAs. EIP-7702 broke those assumptions.
- Checks-effects-interactions plus a reentrancy guard on every function that makes external calls.
- Explicit rounding direction in the protocol's favour (`Math.mulDiv` with a rounding mode).

### 4. Test
- Unit tests for every check C-n (each revert path) and every effect.
- Fuzz tests for every function with numeric inputs.
- **Invariant tests**, one per INV-ID, using handlers that model the real actors. Foundry 1.10 enables snapshot fuzzing by default, so handlers must not assume fresh state per run.
- Fork tests against the target chain for integrations (oracles, bridges, precompiles).
- For critical math or access paths: symbolic checks (Halmos/hevm, or `forge equivalence` for refactors).
- Coverage: `forge coverage` or `npx hardhat test --coverage`. Read the uncovered lines, don't just chase a percentage.

### 5. Static analysis
> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 <skill-dir>/scripts/check_contracts.py src/     # quick suite-specific checks (EIP-7702, initializers, pragma, ...)
forge lint                                              # Foundry built-in detectors
slither .                                               # broad detector suite
aderyn .                                                # second opinion, fast
```
Triage every finding as fixed, false positive (with the reason written down), or accepted risk (as an ADR).

### 6. Deploy
Scripted and reproducible (`forge script` / Hardhat Ignition), deterministic addresses where useful (CREATE2/CREATE3, and OpenZeppelin 5.7 ships `Create3`), verified source, admin roles transferred to multisig/timelock in the same script, and a deployment record (addresses, commit, compiler settings) in `docs/deployments/<network>.md`.

### 7. Audit preparation
Use `references/security-checklist.md`. Provide auditors with the spec, invariants, threat model, test and coverage reports, static-analysis triage, and a frozen commit.

### 8. Update CHAIN.md
Set the component to `built` (with the test report as evidence), and later to `audited` (with the audit report).

## Rules
- Contracts implementing consensus-relevant logic (validator sets, system contracts, bridges) are reviewed to consensus-code standards.
- No unbounded loops over user-controlled collections.
- Every external call is to a known contract or treated as hostile.
- Upgrades go through a timelock at least as long as users need to exit.

## Sources (verified 2026-11-25)
Solidity 0.8.39 and earlier release notes: soliditylang.org/blog/category/releases · Foundry v1.10.0: github.com/foundry-rs/foundry/releases · Hardhat 3 stable: hardhat.org/docs/reference/hardhat-2-end-of-life · OpenZeppelin Contracts 5.7.0: openzeppelin.com/news/introducing-openzeppelin-contract-5-7, github.com/OpenZeppelin/openzeppelin-contracts/releases · OWASP SC Top 10 2026: scs.owasp.org/sctop10 · EIP-7702 guidance: ethereum.org/roadmap/pectra/7702.
