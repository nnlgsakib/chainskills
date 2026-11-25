# Routing reference

## Contents
- Suite hierarchy
- Route by phase
- Route by topic
- Combining skills

## Suite hierarchy

Lower layers never depend on higher ones. `protocol-*` and `design-*` never assume a framework; only `stack-*` does.

```
L0  blockchain-dev                     router (this skill)
L1  design-*                           idea → architecture → spec → stack decision
L2  protocol-*                         stack-neutral mechanisms
L3  build-*                            implementation surfaces (contracts, node software) and suite extension (new skills, new adapters)
L4  stack-*                            stack adapters (framework-specific)
L5  quality-*                          security, testing, formal verification
L6  ops-*                              upgrades, infrastructure, data access, launch, readiness
    extra-*                            optional (wallet/frontend, docs/devrel)
```

## Route by phase

| CHAIN.md phase | Typical next skill | Output it must leave |
|---|---|---|
| (none) / idea | `design-protocol` | `docs/idea.md`, requirements, `docs/spec/architecture.md`, architecture ADR |
| design | `design-spec` (+ `protocol-*` per component) | `docs/spec/<component>.md`, `parameters.md`, `invariants.md` |
| spec | `design-stack-selection` | stack ADR, placement table in CHAIN.md, adapter name |
| stack | `stack-*` setup; `build-stack-adapter` if none | scaffolded repo, adapter verified |
| build | `stack-*` + `build-smart-contracts` / `build-node-software` + `protocol-*` | code + tests per component; component status → built |
| quality | `quality-security` → `quality-testing` → `quality-formal-verification` | threat model, test reports, models; findings tracked |
| ops | `ops-upgrades`, `ops-infrastructure`, `ops-rpc-data`, `ops-launch` | runbooks, infra code, launch plan |
| pre-mainnet | `ops-production-readiness` | `docs/readiness.md` with DONE/TODO/N-A + evidence |

## Route by topic

| User talks about | Skill |
|---|---|
| idea, whitepaper, "what should my chain be", node roles, trust model | `design-protocol` |
| spec, invariants, parameters, state machine, transaction design | `design-spec` |
| which framework, Cosmos vs Substrate vs OP Stack vs custom, module vs contract | `design-stack-selection` |
| consensus, finality, block time, leader election, MEV, ordering | `protocol-consensus` |
| VM choice, account model, gas, storage layout, determinism | `protocol-state-execution` |
| validators, active set, epochs, delegation, slashing, unbonding | `protocol-staking-validators` |
| L2, rollup, sequencer, fraud/validity proofs, settlement, forced inclusion | `protocol-rollup` |
| token supply, inflation, fees, reward split, treasury, simulations | `protocol-tokenomics` |
| governance, proposals, voting, emergency powers, treasury spending | `protocol-governance` |
| randomness, VRF, beacons, committee selection, lotteries | `protocol-randomness` |
| rewards for useful work, service/operator/verifier nodes, DePIN, oracles, proof of service, sybil resistance | `protocol-verifiable-participation` |
| data availability, erasure coding, sampling, DA layers, history | `protocol-data-availability` |
| peers, gossip, libp2p, DDoS, sentry topology | `protocol-p2p` |
| bridges, IBC, light clients, cross-chain messaging | `protocol-interop` |
| Solidity/Rust/Move contracts, validator-set or system contracts, proxies | `build-smart-contracts` |
| node client, light client, sequencer, prover, relayer, oracle, keeper | `build-node-software` |
| "add support for <framework>", missing adapter, refresh adapter | `build-stack-adapter` |
| "make a skill for X", recurring need with no skill, capture this team's conventions, refresh stale skill facts | `build-skill` |
| existing repo, "what stack is this?", onboarding onto a codebase | `blockchain-dev` → `references/existing-projects.md` (+ `scripts/detect_stack.py`) |
| framework commands/code (Ignite, op-node, Nitro, Substrate, geth fork...) | matching `stack-*` |
| threat model, keys, remote signer, audits, fuzzing | `quality-security` |
| TLA+, Quint, model checking, proofs of protocol safety | `quality-formal-verification` |
| testnets, chaos, load, benchmarks, determinism tests | `quality-testing` |
| hard forks, upgrade handlers, proxy upgrades, migrations | `ops-upgrades` |
| servers, monitoring, alerts, backups, incidents, cloud diversity | `ops-infrastructure` |
| RPC nodes, indexers, explorers, SDKs | `ops-rpc-data` |
| testnet → mainnet, genesis ceremony, L1 contract deployment, onboarding | `ops-launch` |
| "are we production ready?", mainnet gate | `ops-production-readiness` |
| wallet, dApp UI | `extra-wallet-frontend` |
| docs, developer portal, tutorials | `extra-docs-devrel` |

## Combining skills

Typical chains of skills:

- **New chain from an idea:** `design-protocol` → `design-spec` (+ `protocol-*`) → `design-stack-selection` → `stack-*` → `build-*` → `quality-*` → `ops-*` → `ops-production-readiness`.
- **Add a mechanism to an existing chain:** `protocol-<mechanism>` (design) → `design-spec` (spec file) → `stack-*` / `build-*` (implement) → `quality-testing`.
- **Validator set as contracts (EVM L1, L2 sequencer set, Avalanche L1):** `protocol-staking-validators` → `build-smart-contracts` → `stack-*` for wiring to the client.
- **Rollup:** `protocol-rollup` → `protocol-data-availability` → `design-stack-selection` → `stack-rollup-*` → `build-smart-contracts` (L1 contracts if custom) → `ops-launch`.
- **Unknown framework chosen:** `design-stack-selection` → `build-stack-adapter` → new `stack-*` → continue.
