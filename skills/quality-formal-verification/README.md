# quality-formal-verification — agent skill

Formal methods for the parts of a chain where a bug is fatal: choosing targets, modelling with Quint or TLA+ and checking with the simulator or Apalache, mutation checks, model-based testing against the code, and code-level provers (Certora, Halmos, Kontrol, hevm, `forge equivalence`, Kani).

Includes a tested Quint starter model, `assets/participation.qnt`: bonded participants, commit/reveal, slashing, bounded rewards and supply conservation. On 2026-11-25 with Quint v0.34.0 it typechecked, passed 2,000 random traces, passed Apalache bounded checking up to 5 steps, and caught a planted bug.

```bash
quint typecheck assets/participation.qnt
quint run assets/participation.qnt --max-steps=40 --max-samples=2000
quint verify assets/participation.qnt --invariant=INV_TOKEN_1 --max-steps=5
```

```
quality-formal-verification/
├── SKILL.md
├── assets/      participation.qnt
└── references/  tools.md · property-catalog.md
```

Part of the chainskills suite ([install](../../README.md#install)). MIT license.
