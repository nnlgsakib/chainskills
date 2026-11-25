# CHAIN.md — shared project state

Every chainskills skill reads and updates the same files in the user's chain repository. This is how skills hand work to each other without knowing about each other.

## Layout

```
CHAIN.md                      one-page state: phase, stack, components, decisions, questions, risks
docs/
├── idea.md                   the user's original idea/whitepaper, verbatim — never edited
├── spec/
│   ├── architecture.md       actors, node roles, trust assumptions, component diagram, tx lifecycle
│   ├── <component>.md        one per component (design-spec template)
│   ├── parameters.md         every tunable in one table
│   ├── invariants.md         every invariant, numbered, linked to its component
│   └── glossary.md           terms used in the spec
├── decisions/
│   └── NNNN-<slug>.md        ADRs (template: blockchain-dev/assets/ADR.template.md)
└── readiness.md              written by ops-production-readiness
```

Create only what is needed; empty files are noise.

## IDs (stable, never reused)

| Prefix | Meaning | Example |
|---|---|---|
| `R-F<n>` | functional requirement | R-F3 delegators can undelegate at any time |
| `R-N<n>` | non-functional requirement (with a number) | R-N1 block time ≤ 4 s p95 |
| `R-C<n>` | constraint | R-C2 team writes Rust |
| `INV-<COMP>-<n>` | invariant | INV-STAKE-2 total bonded == Σ validator bonded |
| `P-<COMP>-<name>` | parameter | P-STAKE-unbonding_period |
| `ADR-<nnnn>` | decision | ADR-0004 use Cosmos SDK |
| `Q<n>` | open question | Q7 who funds the reserve? |
| `K<n>` | risk | K2 >1/3 stake on one cloud |

Code, tests and audit reports reference these IDs, so a reviewer can trace requirement → spec → code → test.

## Update rules

- Each skill updates only the sections it owns (listed in the template) plus Status.
- Status → phase, date, which skill, next step.
- Component status values: `todo → designed → specified → built → tested → audited`. Move forward only with evidence (file path, test name, report).
- Superseded decisions are not deleted: mark the old ADR `superseded by ADR-xxxx`.
- Keep CHAIN.md under ~200 lines. Move detail into docs/ and link it.
