# <Chain name>

> <One-sentence description of what the chain is for.>

## Status
<!-- owner: every skill -->
- Mode: production | prototype
- Phase: idea | design | spec | stack | build | quality | ops | mainnet
- Last updated: YYYY-MM-DD by <skill>
- Next step: <action> → <skill>

## Idea
<!-- owner: design-protocol. Full original text in docs/idea.md -->
<3–5 line summary of the user's idea>

## Requirements
<!-- owner: design-protocol -->
### Functional
- R-F1 ...
### Non-functional (always with a number)
- R-N1 ...
### Constraints
- R-C1 ...
### Non-goals
- ...

## Architecture
<!-- owner: design-protocol. Detail: docs/spec/architecture.md -->
- Architecture class: <L1 sovereign | L2 rollup | appchain | shared-security chain | permissioned | contracts on existing chain>
- Node roles: ...
- Trust assumptions: ...

## Stack
<!-- owner: design-stack-selection -->
- Framework + versions: ...
- Adapter skill: stack-...
- Decision: ADR-....

| Component | Surface (module / precompile / system contract / contract / L1 contract / off-chain / client) | Location | ADR |
|---|---|---|---|

## Components
<!-- owner: design-spec (rows), building skills (status) -->
| Component | protocol-* skill | Spec | Status | Evidence |
|---|---|---|---|---|

## Decisions
<!-- owner: any skill that writes an ADR -->
| ADR | Title | Status |
|---|---|---|

## Open questions
<!-- owner: any skill -->
- [ ] Q1 ... (blocking: yes/no, owner skill)

## Risks
<!-- owner: design-protocol, quality-security -->
| ID | Risk | Likelihood | Impact | Mitigation | Owner skill |
|---|---|---|---|---|---|

## Production readiness
<!-- owner: ops-production-readiness -->
See docs/readiness.md
