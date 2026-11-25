---
name: design-stack-selection
description: Choose the implementation stack for a blockchain and decide where every component lives — compare Cosmos SDK, Cosmos EVM, Polkadot SDK/Substrate, OP Stack, Arbitrum Orbit, ZK Stack, Polygon CDK, Avalanche L1, geth/reth/Besu forks, Hyperledger, sovereign rollups, custom Rust/Go on CometBFT or other BFT engines, or contracts on an existing chain — against the project's requirements with a weighted scoring matrix, then place each component as a native module/pallet, precompile, system or validator-set contract, smart contract, rollup L1 contract, off-chain service or client logic. Use whenever the user asks which framework/stack/chain to build on, "Cosmos vs Substrate vs OP Stack", whether something should be a module or a contract, how to implement a validator set on an EVM chain, or wants to migrate stacks.
license: MIT
---

# Design Stack Selection

Third design step of the chainskills suite. It converts a stack-neutral architecture and spec into two decisions: **which stack** and **which implementation surface for each component**. It then hands off to the matching `stack-*` adapter, or to `build-stack-adapter` when none exists.

Shared state: `CHAIN.md` and `docs/` (`../blockchain-dev/references/chain-md.md`). Inputs: Requirements and Architecture in `CHAIN.md`, `docs/spec/architecture.md`, component specs if available. Selection can start before every spec is finished, but the placement table needs each component's operations and hooks.

| Reference | Read when |
|---|---|
| `references/stack-catalog.md` | Building the candidate list; facts per stack |
| `references/scoring.md` | Weighting criteria and scoring candidates |
| `references/placement.md` | Choosing a surface per component; what each stack supports |

Stack facts change quickly. The catalog has a review date. Before you recommend a stack, check current versions, license and maintenance status: the official repo's latest release, its changelog, and the license file. Note what you checked in the ADR.

## Workflow

### 1. Hard filters
Turn requirements and constraints into pass/fail filters, e.g. "must be EVM-compatible", "own validator set", "deterministic finality ≤ 6 s", "team writes Go or Rust", "permissive license", "inherit Ethereum security". Drop every candidate that fails one. Write down which filter removed which stack. If nothing survives, a requirement is too strict. Show the user the conflict and don't quietly relax it.

### 2. Score the survivors
Use `references/scoring.md`. Take the weights from the requirements, so a time-critical project weights time-to-market high. Score each criterion 1–5, with a one-line justification that cites a fact from the catalog or a source you checked. Show the top 2–3 with totals. Do a sensitivity check: would a plausible change in weights flip the winner? If yes, say so, and name the assumption that decides it.

### 3. Place every component
For each row in the Components table, choose a surface using `references/placement.md`:

`native module/pallet` · `precompile` · `system contract` (genesis-deployed, privileged) · `smart contract` · `L1 contract` (rollup settlement/bridge) · `off-chain service` (sequencer, prover, relayer, oracle, verifier) · `client` (node/wallet logic)

Rules of thumb:
- Consensus-critical and on the hot path (every block): put it native, or in a privileged system contract on EVM-only stacks.
- Needs composability with user contracts: use a contract or a precompile.
- Heavy compute or work that can't be verified on-chain: run it as an off-chain service, plus an on-chain verification/challenge component.
- Must change often in year one: a contract or a governable module beats a hard fork.
- On an L2 you usually can't add native modules without forking the node. Prefer predeploys and contracts.

Fill the placement table in `CHAIN.md` → Stack: component, surface, location (module name / contract name / service), ADR.

### 4. Decide and record
One ADR for the stack, with options, scores, filters, sources checked, what becomes hard to change, and the revisit trigger. Add one ADR per non-obvious placement, e.g. "validator set as system contract instead of native".

### 5. Hand off to an adapter
- If a `stack-*` skill for the chosen stack is installed or exists as a sibling folder, name it in `CHAIN.md` → Stack → Adapter skill.
- If none exists, route to `build-stack-adapter` with the stack name, version and sources.
- Set Status to phase `stack` and the next step to the adapter's setup.

## Changing stacks later
The specs are stack-neutral, so a migration only touches placement and code. Write a new stack ADR that supersedes the old one, redo step 3, and list each component whose surface changes as a Q-item.

## Output to the user
Report: filters and what they removed, a top-3 table with scores, the recommendation and what it depends on, the placement table, the ADR links, and the next step.
