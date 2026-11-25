---
name: build-stack-adapter
description: Create (full or on-the-fly project-local quick mode), refresh or validate a chainskills stack adapter — a `stack-<family>-<name>` skill that teaches an AI coding agent how to implement the suite's stack-neutral designs on one specific framework (OP Stack, Arbitrum Orbit, ZK Stack, Polygon CDK, Substrate, Avalanche L1, geth/reth/Besu fork, Hyperledger, CometBFT custom app, Malachite, Sovereign SDK, Solana SVM, Move chains, or anything else). Use whenever a chosen stack has no `stack-*` skill yet, the user asks to "add support for <framework>", an adapter is outdated after a framework release, or an adapter needs checking against the adapter contract.
license: MIT
---

# Build Stack Adapter

Stack adapters are the only framework-specific layer of chainskills. Everything above them (design, spec, protocol mechanisms) is stack-neutral. An adapter answers one question for its stack: *where and how does each protocol component get built, tested, released and operated here?*

Every adapter follows the same contract so the router and the other skills can rely on it. The template lives in `assets/adapter-template/`, and `scripts/check_adapter.py` verifies a skill against it.

## Adapter contract

- Folder and `name:` = `stack-<family>-<name>`. Family is one of `cosmos`, `evm`, `rollup`, `substrate`, `avalanche`, `custom`, `permissioned`, `svm`, `move`, or a new family when nothing fits. Examples: `stack-rollup-op`, `stack-evm-reth`, `stack-substrate-solo`.
- SKILL.md has these sections: **Adapter metadata** (stack, versions verified, date, sources), **When to use this adapter**, **Placement map** (summary + link), **Setup**, **Implement**, **Test**, **Production**, **Known pitfalls**, **Updating this adapter**.
- `references/placement-map.md` maps every suite concept to this stack. The concepts are the `protocol-*` mechanisms plus contracts, node software and upgrades. Each gets one support level: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), or `n/a` (doesn't apply to this stack, with the reason).
- README.md and LICENSE (distributable skill layout).
- Facts come from sources you actually read, such as official docs, the repo README, examples, changelogs, and the code. Anything not verified is marked `(unverified)`.

## Quick mode: an adapter on the fly, inside the user's project

Use this when a developer is working **now** on a stack with no adapter: `detect_stack.py` reports `MISSING`, or `design-stack-selection` picks an uncovered stack. The goal is framework-specific help in this session, not a polished suite release.

1. Research only what the current task needs, from primary sources: install, project layout, how the task's component is built on this stack, test tooling, and the top pitfalls. Record the sources and the date.
2. Create the adapter **project-locally** with the same contract (template, all 14 placement-map rows, with `(unverified)` where you didn't check). Put it in the project's skills folder (`.agents/skills/stack-<family>-<name>/`, plus `.claude/skills/` for Claude Code users; see `../build-skill/references/project-local.md`).
3. Validate with `check_adapter.py`. Errors must be fixed. Warnings are fine in quick mode.
4. Use it right away for the task.
5. Offer to upstream it: run the full workflow below to turn it into a suite adapter (complete research, README, registration) and contribute it to chainskills.

Quick mode keeps "any stack" honest. Every developer gets researched, framework-specific guidance on first contact, and the suite grows from real use.

## Workflow (full suite adapter)

### 1. Identify the target
Pin down the stack name, family, exact version or tag to target, and which project needs it (`CHAIN.md` → Stack, if present). If an adapter already exists, this is a **refresh**. Read it first and keep its structure.

### 2. Research from primary sources
In this order: the official repo (README, docs folder, examples, CHANGELOG, dependency files such as go.mod, Cargo.toml or package.json), the official docs site, then release notes for breaking changes. Prefer reading real code over blog posts, because generated code and defaults often differ from the docs. Record every source with its date or commit in Adapter metadata.

Capture:
- Install and toolchain requirements, supported OSes, and minimum versions.
- How to create a new chain or project, the project layout, and the config files.
- For each suite concept: where it lives in this stack, and what's built in versus what you write yourself.
- Test tooling, how local networks are run, and how releases and upgrades work.
- Production operations: node types, keys, monitoring, upgrade process.
- Pitfalls: defaults that are unsafe for production, surprising behaviour, known bugs in generated code.

### 3. Fill the template
Copy `assets/adapter-template/` to a sibling folder `../stack-<family>-<name>/` and rename `SKILL.md.tmpl` to `SKILL.md`. The template is stored as `.tmpl` so agents don't load it as a skill. Replace every `<...>` placeholder. Keep SKILL.md under ~250 lines and put detail in `references/`. Write the description so it triggers on the framework's names, CLI names and common phrasings ("OP Stack", "op-node", "Superchain", "deploy an L2 with OP").

### 4. Verify
> **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.

```bash
python3 <this-skill-dir>/scripts/check_adapter.py ../stack-<family>-<name>
```
Fix every error. If the environment allows it, run the adapter's own setup steps (install, create a project, start a local node), and mark the steps you ran as verified. Steps you couldn't run stay `(unverified)`.

### 5. Register
- Add the adapter to the suite README table under its family.
- `blockchain-dev` discovers `stack-*` skills automatically, so no routing edit is needed.
- If a project is waiting for this adapter, update its `CHAIN.md` → Stack → Adapter skill.
- Offer to rebuild the suite ZIP.

## Refreshing an adapter
Bump the "versions verified" field, diff the framework's changelog since the last verified version, update affected sections and pitfalls, then run the checker. In the README changelog, list the breaking changes users of the adapter must act on.

## Output to the user
Tell the user: the adapter path, the stack and version covered, a placement-map summary (how many concepts are native, extend, custom or n/a), the verified and unverified parts, and any pitfalls found.
