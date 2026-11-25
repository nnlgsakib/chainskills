# chainskills

**Agent skills that take any blockchain idea, on any stack, to production.**

They work with Cosmos SDK, EVM L1s, OP Stack, Arbitrum Orbit and ZK rollups, Substrate, and fully custom chains. Chain logic can live in native modules, precompiles, validator-set and system contracts, custom contracts, or off-chain services. You bring the idea; `blockchain-dev` runs design, then spec, stack choice, build, and quality, sending each step to the skill that owns it.

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

Describe your chain or ask a blockchain question. Agents pick up `blockchain-dev` from its description, or you can call it directly (`/chainskills:blockchain-dev` in Claude Code). For a new project it creates `CHAIN.md` and `docs/` in your repo and walks the phases.

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
| L3 | `build-node-software` | planned |
| L4 | [`stack-cosmos-ignite`](skills/stack-cosmos-ignite/): Cosmos SDK with Ignite CLI (v29 stable / v30) | ✅ |
| L4 | [`stack-cosmos-evm`](skills/stack-cosmos-evm/): Cosmos EVM via the Ignite EVM app | ✅ |
| L4 | [`stack-cosmos-apps`](skills/stack-cosmos-apps/): Ignite Apps (Hermes, CosmWasm, Spaceship, Network, Evolve, ...) | ✅ |
| L4 | `stack-evm-l1`, `stack-rollup-op`, `stack-rollup-orbit`, `stack-rollup-zk`, any other stack via `build-stack-adapter` | planned |
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

| Script | Purpose |
|---|---|
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
