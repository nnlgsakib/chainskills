# build-stack-adapter — agent skill

Creates, refreshes and validates **stack adapters**: the `stack-*` skills that map chainskills' stack-neutral designs onto one framework. This is what lets the suite support any stack.

- Adapter contract: name, required sections, a placement map covering 14 concepts, README and LICENSE
- Research workflow based on primary sources (repo, code, changelogs), with every fact marked verified or unverified
- `scripts/check_adapter.py` checks any adapter against the contract

```bash
python3 scripts/check_adapter.py ../stack-rollup-op
python3 scripts/check_adapter.py --selftest
```

```
build-stack-adapter/
├── SKILL.md
├── scripts/  check_adapter.py
└── assets/adapter-template/  SKILL.md.tmpl · README.md · LICENSE · references/placement-map.md
```

Part of the chainskills suite. Installation: see the [main README](../../README.md#install). MIT license.
