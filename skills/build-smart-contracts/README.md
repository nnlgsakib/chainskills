# build-smart-contracts — agent skill

Builds production EVM contracts from chainskills specs: Foundry v1.10 or Hardhat 3, Solidity 0.8.39, OpenZeppelin 5.7, safe upgrade patterns (UUPS, ERC-7201, initializers), EIP-7702-safe code, unit/fuzz/invariant/symbolic testing, static analysis, deterministic deployment, and audit prep against the OWASP Smart Contract Top 10 2026. Includes patterns for validator-set, staking and system contracts.

```bash
python3 scripts/check_contracts.py src/     # tx.origin, EOA checks, unprotected implementations, open upgrades, old compiler, ...
python3 scripts/check_contracts.py --selftest
```

```
build-smart-contracts/
├── SKILL.md
├── scripts/     check_contracts.py
└── references/  toolchain.md · patterns.md · security-checklist.md · validator-set-contracts.md
```

Tool and library versions checked 2026-11-25. Part of the chainskills suite ([install](../../README.md#install)). MIT license.
