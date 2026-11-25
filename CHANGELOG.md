# Changelog

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
