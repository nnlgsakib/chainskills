# Changelog

## 0.2.0 — 2026-11-25

- **Any project, any stack**: example content is now project-neutral. `blockchain-dev` supports existing codebases (`references/existing-projects.md`), adapts to the project's conventions, and only bootstraps `CHAIN.md` on request.
- **New `blockchain-dev/scripts/detect_stack.py`**: detects 20+ stacks from manifests (Cosmos SDK, Ignite, Cosmos EVM, CosmWasm, CometBFT apps, OP Stack, Arbitrum Nitro/Stylus, Avalanche, geth/reth, Substrate, Malachite, Rust ABCI, Solana/Anchor, Sovereign SDK, Move, Foundry, Hardhat, zkSync, Fabric) and maps them to skills.
- **New skill `build-skill`**: the suite extends itself. It creates suite skills at any layer or project-local skills for any Agent Skills tool, and refreshes stale skills. Includes a template and `check_skill.py` (Agent Skills format, suite conventions, stale-source warnings).
- The router offers `build-skill` when no skill covers a recurring need.

## 0.1.0 — 2026-11-25

First public release: 20 skills.

- **L0 entry point**: `blockchain-dev`, a router with the shared `CHAIN.md` project-state format and an ADR template.
- **L1 design**: `design-protocol`, `design-spec`, `design-stack-selection`.
- **L2 protocol mechanisms**: `protocol-consensus`, `protocol-state-execution`, `protocol-staking-validators`, `protocol-rollup`, `protocol-randomness`, `protocol-verifiable-participation`, `protocol-tokenomics`, `protocol-governance`.
- **L3 build**: `build-smart-contracts`, `build-stack-adapter`.
- **L4 stack adapters**: `stack-cosmos-ignite`, `stack-cosmos-evm`, `stack-cosmos-apps`.
- **L5 quality**: `quality-security`, `quality-testing`, `quality-formal-verification`.
- Scripts, all with self-tests: `audit_state_machine.py`, `check_evm_genesis.py`, `check_adapter.py`, `check_contracts.py`, `committee_risk.py`, `emission_sim.py`, `trace_invariants.py`. Plus a Quint starter model, checked with Quint v0.34.0.
- Version-sensitive facts were checked against official sources on 2026-11-25. Each skill lists its sources.

Planned: `protocol-data-availability`, `protocol-p2p`, `protocol-interop`, `build-node-software`, `ops-*` (upgrades, infrastructure, rpc-data, launch, production-readiness), and more stack adapters (`stack-evm-l1`, `stack-rollup-op`, `stack-rollup-orbit`, `stack-rollup-zk`).
