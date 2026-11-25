# design-protocol — agent skill

Turns any blockchain idea or whitepaper into a protocol architecture that doesn't depend on a stack. You get measurable requirements, node roles, trust assumptions, components, decision records, risks and open questions.

- "Do you need a chain at all?" ladder: contracts → rollup → shared security → sovereign L1
- Question bank that only asks what changes the architecture, with a default for each
- Review against known design failures (unverifiable rewards, predictable randomness, BFT liveness, admin keys, ...)

Outputs go to `CHAIN.md` and `docs/spec/architecture.md` in your chain repo. This is phase 1 of the chainskills suite (entry point: `blockchain-dev`).

```
design-protocol/
├── SKILL.md
├── references/  question-bank.md · architecture-classes.md · design-pitfalls.md
└── assets/      architecture.template.md
```

Installation: see the [main README](../../README.md#install). MIT license.
