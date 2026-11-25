---
name: blockchain-dev
description: Entry point for any blockchain project on any stack — turns an idea into a production chain by routing each step to the right chainskills skill (design, protocol mechanisms, smart contracts, node software, stack adapters for Cosmos SDK / EVM L1 / OP Stack / Arbitrum Orbit / ZK rollups / Substrate / custom, security, testing, upgrades, launch, operations). Works for new ideas and for existing codebases on any stack. Use this skill whenever the user wants to design, build, extend, audit, launch or operate a blockchain, L1, L2, rollup, appchain, validator network, staking system, bridge, consensus protocol or chain-level smart contracts — or pastes a chain whitepaper/idea — regardless of framework, and even if they only say "my chain", "my protocol" or "make it production ready".
license: MIT
---

# Blockchain Dev — router

Stack-agnostic entry point of the chainskills suite. It does not design or code by itself: it finds where the project stands, picks the next skill, loads it, and makes sure the shared project state is updated afterwards. The point is that work happens in the right order (design before stack, stack before code) and every skill builds on what the previous ones decided.

## 1. Find the project state

> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

Look for `CHAIN.md` at the project root (also check `docs/`). If the repo has code, also run `python3 <this-skill-dir>/scripts/detect_stack.py <repo-root>` to see which stack(s) it uses and which skills cover them.

- **Found** → read it. Phase, stack, components, decisions and open questions tell you where to continue. Read the linked spec file for the component being worked on, nothing more.
- **Not found, user is starting or describing a chain project** (an idea, a whitepaper, "I want to build...") → create it from `assets/CHAIN.template.md` and the docs layout in `references/chain-md.md`, save the user's idea verbatim to `docs/idea.md`, then route to `design-protocol`.
- **Not found, existing codebase** → follow `references/existing-projects.md`. Adapt to the project's conventions, route single tasks straight to the topic skill plus the detected stack adapter, and offer (never force) to bootstrap CHAIN.md from the code for larger efforts.
- **Not found, quick question** ("how does slashing work in Cosmos?", "fix this Solidity staking bug") → don't create project files. Route straight to the topic skill and answer.

## 2. Pick the mode

- **production** (default for anything heading to mainnet): phase gates below are enforced; missing evidence is a TODO, not a pass.
- **prototype** (user says prototype/PoC/hackathon/demo, or `CHAIN.md` says so): skip gates, keep ADRs short, record shortcuts in `CHAIN.md` → Open questions so they can be paid back later.

## 3. Route

Use `references/routing.md` — it maps phases and topics to skills. Short version:

| Phase | Skills |
|---|---|
| idea → design | `design-protocol` |
| design → spec | `design-spec` + the `protocol-*` skill for each component |
| spec → stack | `design-stack-selection` → `stack-*` adapter (or `build-stack-adapter` if none fits) |
| build | `stack-*` adapter + `build-smart-contracts` / `build-node-software` + `protocol-*` for the mechanism |
| quality | `quality-security`, `quality-testing`, `quality-formal-verification` |
| ops | `ops-upgrades`, `ops-infrastructure`, `ops-rpc-data`, `ops-launch` |
| mainnet gate | `ops-production-readiness` |

Stack adapters are discovered, not listed: any installed skill named `stack-*` (or a sibling folder `../stack-*/`) is an adapter. Pick the one matching `CHAIN.md` → Stack.

A request can touch several skills. Load them in layer order — design → protocol → build/stack → quality → ops — and only the ones the current step needs.

## 4. Load the skill

1. Installed → invoke it by name, using whatever mechanism your agent provides. In Claude Code as a plugin it's `/chainskills:<skill-name>`; installed standalone it's `/<skill-name>`. Agents that load skills automatically pick them up from their descriptions.
2. Not invocable but present on disk → read `<this-skill-dir>/../<skill-name>/SKILL.md` and follow it. All chainskills skills are siblings under the same `skills/` folder.
3. Missing (planned but not built yet, or a need no skill covers) → say so in one line, then:
   - **Recurring or important need** (a framework without an adapter, a mechanism, an ops workflow, project-specific conventions): offer `build-skill`, which researches and creates the skill, as a suite skill or a project-local one, so the next request is covered. For a **missing stack adapter**, go straight to `build-stack-adapter` **quick mode**: it creates a researched, project-local adapter now and continues the task, so no stack gets only generic advice.
   - **One-off need**: do the work with general knowledge **using the same output contract** (results into the project's spec location, decisions as ADRs from `assets/ADR.template.md`, status into `CHAIN.md` if it exists). Mark the output "unverified — no skill".

## 5. Phase gates (production mode)

Move to the next phase only when its entry condition holds. If not, say what is missing and route to the skill that fills it. The user can override; record the override as an ADR.

| Into | Requires |
|---|---|
| spec | Requirements with numbers (latency, finality, throughput, node hardware, validator count); trust assumptions written; architecture ADR accepted |
| stack | Every component has a spec file with state, operations, parameters with bounds, numbered invariants |
| build | Stack ADR accepted; component placement table complete; adapter exists |
| quality | Components built with tests for every rejection path; spec ↔ code traceability (invariant IDs referenced in tests) |
| ops | Threat model done; testnet ran under chaos/load tests; critical findings closed |
| mainnet | `ops-production-readiness` report has no open blocking item |

## 6. After every routed task

Make sure `CHAIN.md` reflects the result: Status (phase, last updated, next step), component status, new ADRs, open questions, risks. Keep `CHAIN.md` short — detail belongs in `docs/`. Never rewrite the user's idea text.

End your reply with: what was done, which files changed, the next recommended step and skill.
