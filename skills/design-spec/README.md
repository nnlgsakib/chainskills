# design-spec — agent skill

Writes specs that engineers can implement and auditors can check, for any blockchain component, without tying them to a stack. Each spec covers state, operations with numbered checks and effects, hooks, parameters with bounds, numbered invariants, lifecycles, adversarial cases and test vectors. It also keeps the parameter and invariant registries for the whole project.

The same spec can be implemented as a Cosmos module, a Substrate pallet, a Solidity contract or an off-chain service.

```
design-spec/
├── SKILL.md
├── references/  notation.md (types, pseudocode, determinism rules) · review-checklist.md
└── assets/      component.template.md · registries.template.md
```

Part of the chainskills suite (entry point: `blockchain-dev`). Installation: see the [main README](../../README.md#install). MIT license.
