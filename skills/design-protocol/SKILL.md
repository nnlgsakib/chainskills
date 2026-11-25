---
name: design-protocol
description: Turn any blockchain idea — a one-line pitch, a long whitepaper, a list of features — into a concrete, stack-neutral protocol architecture with measurable requirements, actors and node roles, trust assumptions, components, alternatives with trade-offs, risks and open questions. Use this skill whenever the user shares a chain idea or whitepaper, asks "how should I design my blockchain/L1/L2/rollup/appchain", wants feedback on a protocol design, asks whether they even need their own chain, or wants to rethink an existing chain's architecture — on any stack (Cosmos, EVM, OP Stack, Arbitrum, Substrate, custom).
license: MIT
---

# Design Protocol

First design step of the chainskills suite. It produces the architecture every later skill builds on, so mistakes here are the most expensive ones. Stay stack-neutral: say "a BFT PoS consensus with ~50 validators", never "use x/staking" — the stack is chosen later by `design-stack-selection`.

Shared state: `CHAIN.md` and `docs/` as defined by `blockchain-dev` (`../blockchain-dev/references/chain-md.md`, templates in `../blockchain-dev/assets/`). Create them if missing.

| Reference | Read when |
|---|---|
| `references/question-bank.md` | Step 3 — finding what's missing in the idea |
| `references/architecture-classes.md` | Step 4 — L1 vs L2 vs appchain vs shared security vs contracts-only |
| `references/design-pitfalls.md` | Step 7 — reviewing the design for known failure patterns |
| `assets/architecture.template.md` | Step 6 — writing `docs/spec/architecture.md` |

## Workflow

### 1. Capture the idea
Save the user's text verbatim to `docs/idea.md` (append a dated section on later revisions — never edit old text). Summarise it in 3–5 lines in `CHAIN.md` → Idea.

### 2. Extract requirements
Read the idea and pull out:
- **Functional** (R-F): what users, validators, other node types can do.
- **Non-functional** (R-N): always a number and a percentile or bound — block time, time to finality, throughput, validator count, node hardware, sync time, availability. "Fast" or "scalable" is not a requirement; ask for or propose a number and mark it `(proposed)`.
- **Constraints** (R-C): team language, budget, timeline, regulation, must-be-EVM-compatible, existing token, licensing.
- **Non-goals**: what the chain explicitly won't do. Prevents scope creep later.

Where the idea says "may", "could", "in the future": record as a requirement only if it shapes the architecture now; otherwise list under Non-goals or open questions.

### 3. Fill the gaps
Use `references/question-bank.md`. Ask the user only questions whose answer **changes the architecture** — at most 5 at a time, each with your proposed default so they can just say yes. Everything else: pick a sensible default, mark it `(assumed)`, list it in open questions.

### 4. Choose the architecture class
Before anything else, run the "do you need a chain at all" ladder in `references/architecture-classes.md`: contracts on an existing chain → rollup/L2 → appchain with shared security → sovereign L1. Climb only as far as the requirements force. Write one sentence per rung on why it does or doesn't suffice. This is the single biggest cost decision in the project.

### 5. Actors, roles, trust
- **Actors and node roles**: for each — what it does, hardware/connectivity, how many, permissioned or permissionless, what it stakes, how it's rewarded, how it's punished.
- **Trust assumptions**, explicit and quantified: e.g. "> 2/3 of stake honest and online for liveness; < 1/3 Byzantine for safety", "1-of-N honest verifier for fraud proofs within 7 days", "DA layer available". Each assumption names what breaks if it fails.
- **Incentive check**: for every role, is honest behaviour the most profitable behaviour? If a role is rewarded for something that can't be verified, flag it now.

### 6. Components and architecture
Decompose into components (consensus, staking, execution, rewards, verification layer, DA, networking, bridge, governance...). For each: one-paragraph responsibility, the `protocol-*` skill that owns its design, dependencies on other components.

Write `docs/spec/architecture.md` from `assets/architecture.template.md`: overview, roles, trust assumptions, component diagram (mermaid), transaction lifecycle, block lifecycle, failure scenarios (what happens when each role disappears or misbehaves).

For the top 1–3 architectural forks (e.g. "verification layer on-chain vs off-chain with challenges"), present 2–3 options with trade-offs and a recommendation. Record each as an ADR (`docs/decisions/`, template `../blockchain-dev/assets/ADR.template.md`).

### 7. Review against pitfalls
Walk `references/design-pitfalls.md`. For each pattern that applies, either change the design or record an explicit risk (K-item) with mitigation. Common hits: rewarding unverifiable work, predictable randomness, unbounded validator sets in BFT, admin keys calling themselves decentralized, fixed-APY promises.

### 8. Update CHAIN.md and hand off
- Requirements, Architecture, Components (status `designed`), Decisions, Open questions, Risks.
- Status: phase `design`, next step → `design-spec` (and which `protocol-*` skills each component needs).

## Output to the user

Short summary: architecture class and why, roles, the 3 most important trust assumptions, components list, decisions taken (ADR links), questions that block the next phase. Then the next step. Don't paste whole files into chat — they're on disk.

## Principles

- Safety over liveness, explicitly: say what the chain does when assumptions fail (halt, degrade, fork) — never leave it implicit.
- Every number is either from the user, from a benchmark, or marked `(proposed)` / `(assumed)`.
- Separate what must be on-chain (consensus-critical, needs agreement) from what can be off-chain (verifiable later, or just a service). Most "decentralised" features are cheaper as off-chain work with on-chain verification.
- Prefer existing, battle-tested mechanisms; novelty is a cost. When the idea is genuinely novel (e.g. a new verification layer), isolate it as one component with a clear interface so the rest stays standard.
