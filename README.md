# chainskills

**Agent skills that take any blockchain idea, on any stack, to production.**

Framework-specific adapters ship for **Cosmos SDK (Ignite, Cosmos EVM, Ignite Apps), EVM L1s (Besu/geth/reth/BSC-style), OP Stack, Arbitrum chains, ZK Stack, Polkadot SDK, Avalanche L1, Solana/SVM, Move (Sui/Aptos), custom CometBFT/Malachite chains and Hyperledger Fabric**. Any other stack gets a researched adapter on the fly (`build-stack-adapter` quick mode). Chain logic can live in native modules, precompiles, validator-set and system contracts, custom contracts, or off-chain services. Use it on a **new idea** or an **existing codebase**. `blockchain-dev` detects your stack, adapts to your project's conventions, and routes each task to the skill that owns it. When no skill fits, **`build-skill` creates one**: a new suite skill, or a project-local skill that captures your team's way of working. That way the suite grows with your needs.

The skills use the open [Agent Skills](https://agentskills.io) format (`SKILL.md`). They ship as a **Claude Code plugin** and also work in **Codex, GitHub Copilot, Cursor, Gemini CLI, OpenCode, Windsurf, Kiro** and other agents that read `SKILL.md`.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add nnlgsakib/chainskills
/plugin install chainskills@chainskills
```

Or in one step (Claude Code 2.1.275+): `/plugin install chainskills --marketplace nnlgsakib/chainskills`. From a terminal:

```bash
claude plugin marketplace add nnlgsakib/chainskills
claude plugin install chainskills@chainskills --scope user
```

Skills are namespaced as `/chainskills:<skill>`, e.g. `/chainskills:blockchain-dev`. To update: `/plugin marketplace update chainskills`, then `/reload-plugins`.

### Any agent (Codex, Copilot, Cursor, Gemini CLI, OpenCode, Windsurf, Kiro, Claude Code, ...)

The [`skills` CLI](https://github.com/vercel-labs/skills) detects your installed agents and copies the skills into each one:

```bash
npx skills add nnlgsakib/chainskills                 # interactive: pick agents and skills
npx skills add nnlgsakib/chainskills --all -g        # every skill, every detected agent, user scope
npx skills add nnlgsakib/chainskills -a codex -a github-copilot -a cursor -a gemini-cli -g
```

### Gemini CLI (native)

```bash
git clone https://github.com/nnlgsakib/chainskills
# inside Gemini CLI:
/skills link ./chainskills/skills --scope user
```

### Manual copy

Copy the folders in `skills/` into your agent's skills directory. Keep all of them together, because skills hand work to each other.

| Agent | User scope | Project scope |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex, Cline, Warp, Zed, ... | `~/.agents/skills/` | `.agents/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` or `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` or `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` or `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.agents/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` |
| Kiro | `~/.kiro/skills/` | `.kiro/skills/` |

```bash
git clone https://github.com/nnlgsakib/chainskills
cp -r chainskills/skills/* ~/.agents/skills/      # pick the directory from the table
```

Paths are taken from the `skills` CLI agent table and vendor docs (checked 2026-11-25). Your agent's own docs are authoritative.

## Use

Describe your chain or ask a blockchain question. Agents pick up the right skill from its description, or you can call the router directly (`/chainskills:blockchain-dev` in Claude Code).

- **New project**: it creates `CHAIN.md` and `docs/` and walks design → spec → stack → build → quality.
- **Existing project**: it runs `detect_stack.py` (Cosmos SDK, Ignite, Cosmos EVM, CosmWasm, OP Stack, Arbitrum, Avalanche, geth/reth, Substrate, Solana, Move, Foundry/Hardhat, CometBFT/Malachite apps, ...), follows your repo's conventions, and only bootstraps `CHAIN.md` if you want it.
- **Single question**: it answers with the relevant skill and creates no project files.

## Extend it

- **Missing stack** (e.g. Substrate, OP Stack): `build-stack-adapter` researches the framework and creates a `stack-*` adapter.
- **Missing topic or workflow**: `build-skill` creates a new skill from primary sources and validates it with `check_skill.py`.
- **Your team's conventions**: `build-skill` creates a project-local skill (e.g. `acme-module-template`) in `.agents/skills/` or `.claude/skills/`, committed with your repo.
- **Stale facts**: `check_skill.py` warns when a skill's sources are older than 180 days, and `build-skill` has a refresh mode.

## Hierarchy

The name prefix is the layer. Lower layers never depend on higher ones, and only `stack-*` skills are framework-specific.

```
blockchain-dev                         L0  entry point: reads CHAIN.md and routes
├── design-*                           L1  idea → architecture → spec → stack decision
├── protocol-*                         L2  stack-neutral mechanisms
├── build-*                            L3  contracts, node software, new adapters
├── stack-*                            L4  stack adapters
├── quality-*                          L5  security, testing, formal verification
├── ops-*                              L6  upgrades, infrastructure, data access, launch, readiness
└── extra-*                                optional
```

## Skills

| Layer | Skill | Status |
|---|---|---|
| L0 | [`blockchain-dev`](skills/blockchain-dev/): router, `CHAIN.md` format, ADR template | ✅ |
| L1 | [`design-protocol`](skills/design-protocol/): idea → requirements, roles, trust, architecture | ✅ |
| L1 | [`design-spec`](skills/design-spec/): stack-neutral component specs, invariants, parameters | ✅ |
| L1 | [`design-stack-selection`](skills/design-stack-selection/): stack scoring + where each component lives | ✅ |
| L2 | [`protocol-consensus`](skills/protocol-consensus/): consensus family, finality, halt behaviour, ordering/MEV | ✅ |
| L2 | [`protocol-state-execution`](skills/protocol-state-execution/): VM, EVM fork compatibility, gas, state, parallelism | ✅ |
| L2 | [`protocol-staking-validators`](skills/protocol-staking-validators/): validator sets, delegation, rewards, slashing | ✅ |
| L2 | [`protocol-rollup`](skills/protocol-rollup/): L2 type, proofs, sequencing, bridge, Stages | ✅ |
| L2 | [`protocol-randomness`](skills/protocol-randomness/): beacons, VRF, safe selection and sampling | ✅ |
| L2 | [`protocol-verifiable-participation`](skills/protocol-verifiable-participation/): pay-for-verified-work layers, sybil resistance, committees | ✅ |
| L2 | [`protocol-tokenomics`](skills/protocol-tokenomics/): issuance, fees, reward splits, security budget, simulation | ✅ |
| L2 | [`protocol-governance`](skills/protocol-governance/): powers, voting, treasury, Security Council, attacks | ✅ |
| L2 | `protocol-data-availability`, `protocol-p2p`, `protocol-interop` | planned |
| L3 | [`build-smart-contracts`](skills/build-smart-contracts/): Solidity/Foundry/OZ 5.7, upgrades, testing, audit prep | ✅ |
| L3 | [`build-stack-adapter`](skills/build-stack-adapter/): adapter contract, template, checker | ✅ |
| L3 | [`build-skill`](skills/build-skill/): create or refresh any skill (suite or project-local), `check_skill.py` | ✅ |
| L3 | `build-node-software` | planned |
| L4 | [`stack-cosmos-ignite`](skills/stack-cosmos-ignite/): Cosmos SDK with Ignite CLI (v29 stable / v30) | ✅ |
| L4 | [`stack-cosmos-evm`](skills/stack-cosmos-evm/): Cosmos EVM via the Ignite EVM app | ✅ |
| L4 | [`stack-cosmos-apps`](skills/stack-cosmos-apps/): Ignite Apps (Hermes, CosmWasm, Spaceship, Network, Evolve, ...) | ✅ |
| L4 | [`stack-evm-l1`](skills/stack-evm-l1/): own EVM L1 (Besu QBFT, PoS beacon chain, reth SDK, PoSA fork, Avalanche L1) | ✅ |
| L4 | [`stack-rollup-op`](skills/stack-rollup-op/): OP Stack (op-deployer, op-node + op-reth, fault proofs, op-conductor) | ✅ |
| L4 | [`stack-rollup-orbit`](skills/stack-rollup-orbit/): Arbitrum chains / Orbit (chain SDK, BoLD, AnyTrust, Stylus, AEP) | ✅ |
| L4 | [`stack-rollup-zk`](skills/stack-rollup-zk/): ZK Stack (ZKsync OS, zkstack, Airbender, Gateway, Prividium) | ✅ |
| L4 | [`stack-substrate-sdk`](skills/stack-substrate-sdk/): Polkadot SDK parachains and solo chains, FRAME, coretime, runtime upgrades | ✅ |
| L4 | [`stack-avalanche-l1`](skills/stack-avalanche-l1/): Avalanche L1s (ACP-77/99 validator managers, Subnet-EVM, ICM) | ✅ |
| L4 | [`stack-svm-solana`](skills/stack-svm-solana/): Solana programs (Anchor, Agave, LiteSVM/Mollusk/Surfpool), SVM pointers | ✅ |
| L4 | [`stack-move-sui-aptos`](skills/stack-move-sui-aptos/): Move on Sui and Aptos (publish/upgrade policies, Move Prover) | ✅ |
| L4 | [`stack-custom-bft`](skills/stack-custom-bft/): custom chains on CometBFT ABCI 2.0, Malachite, Commonware | ✅ |
| L4 | [`stack-permissioned-fabric`](skills/stack-permissioned-fabric/): Hyperledger Fabric v3 (SmartBFT, chaincode lifecycle) | ✅ |
| L4 | **any other stack**: `build-stack-adapter` quick mode creates a researched, project-local adapter on first contact | on demand |
| L5 | [`quality-security`](skills/quality-security/): threat model, keys, SDLC, audits, bounties, incident response | ✅ |
| L5 | [`quality-testing`](skills/quality-testing/): traceability, multi-node, chaos, determinism, performance | ✅ |
| L5 | [`quality-formal-verification`](skills/quality-formal-verification/): Quint/TLA+, Certora/Halmos/Kani, tested Quint starter | ✅ |
| L6 | `ops-upgrades`, `ops-infrastructure`, `ops-rpc-data`, `ops-launch`, `ops-production-readiness` | planned |

When a planned skill is missing, `blockchain-dev` falls back to general knowledge, keeps the same output format, and marks the result unverified.

## How the skills connect

Every skill reads and updates the shared project state in your chain repo:

```
CHAIN.md                 phase, stack, components, decisions, questions, risks
docs/idea.md             your original idea, verbatim
docs/spec/               architecture, one spec per component, parameters, invariants
docs/decisions/          decision records (ADRs)
```

## Scripts (Python 3, stdlib only, each with a self-test)

Run them with `python3`. If that command isn't found (common on Windows), use `python`, then `py -3`. Every skill tells agents to retry the same way.

| Script | Purpose |
|---|---|
| `blockchain-dev/scripts/detect_stack.py` | detect a repo's blockchain stack(s) and the matching skills |
| `build-skill/scripts/check_skill.py` | validate any skill (Agent Skills format, suite conventions, stale sources) |
| `stack-cosmos-ignite/scripts/audit_state_machine.py` | flag non-determinism in Cosmos module code |
| `stack-cosmos-evm/scripts/check_evm_genesis.py` | sanity-check a Cosmos EVM genesis |
| `build-stack-adapter/scripts/check_adapter.py` | validate a stack adapter against the contract |
| `build-smart-contracts/scripts/check_contracts.py` | EIP-7702, initializer, upgrade-guard and compiler checks for Solidity |
| `protocol-verifiable-participation/scripts/committee_risk.py` | committee failure probability and minimum deterrent penalty |
| `protocol-tokenomics/scripts/emission_sim.py` | supply, inflation, yield and per-role payout projection |
| `quality-testing/scripts/trace_invariants.py` | find spec invariants that no test or model covers |

## Freshness

Version-sensitive facts (framework versions, standards, tool flags) were checked against official sources on **2026-11-25**. Each skill lists its sources, and checked facts are marked ✔. Unconfirmed items are marked `(unverified)`. See [CHANGELOG.md](CHANGELOG.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
