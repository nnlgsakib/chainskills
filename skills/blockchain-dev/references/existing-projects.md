# Working in existing projects

chainskills works the same for a greenfield idea and for a chain, rollup or protocol that already has code, docs and conventions. In an existing project, **adapt to the project; don't impose the suite's structure.**

## 1. Detect the stack

```bash
python3 <blockchain-dev-dir>/scripts/detect_stack.py <repo-root>            # human-readable
python3 <blockchain-dev-dir>/scripts/detect_stack.py <repo-root> --json     # for tooling
```

It reads manifests only (go.mod, Cargo.toml, package.json, foundry.toml, Move.toml, Anchor.toml, config.yml), and never runs project code. It reports each detected stack (with version), its evidence files, and the skill that covers it. It also says whether that skill is installed, and suggests `build-stack-adapter` when no adapter exists yet. It folds dependencies that aren't the chain's own stack (go-ethereum inside a Cosmos EVM or OP chain, CometBFT inside Cosmos SDK) into the parent stack.

Also read the project's own README, `docs/`, ADRs, CONTRIBUTING, Makefile/CI and test layout. **Their conventions win** over the suite's defaults (naming, docs location, test style, branch policy).

## 2. Choose how much process to apply

| Situation | Do |
|---|---|
| A single question or change ("add a slashing condition", "why does this upgrade fail?") | Route straight to the topic skill and the detected stack adapter. Don't create CHAIN.md |
| A feature or new component in an existing chain | Write a spec only for the new component (`design-spec`, with a short Context section describing the existing system), then build and test. Put it in the project's docs location |
| A major redesign, audit preparation, or a production push | Offer to bootstrap CHAIN.md from the code (below). Create it only with the user's agreement |

## 3. Bootstrapping CHAIN.md from code (optional)
- **Stack**: the `detect_stack.py` output, with versions.
- **Components**: one row per module, pallet, contract system or service found in the code, with status `built` (or `tested` where tests exist). Mark the Spec column `missing` where there isn't one.
- **Decisions**: link existing ADRs or design docs. Don't rewrite history.
- **Open questions**: gaps found while reading (unspecified invariants, untested paths, undocumented admin powers).
- **Location**: if the project already has a docs convention (e.g. `docs/design/`, `spec/`, a wiki), point CHAIN.md at it instead of creating a parallel `docs/spec/`.

## 4. When the stack has no adapter
Detected but not covered (for example a Sovereign SDK rollup, or any framework missing from the suite): run `build-stack-adapter` in **quick mode**. It researches the framework from primary sources and creates a project-local adapter in the repo's skills folder, then continues with the task using it. Offer to upstream the adapter afterwards.

## 5. When no skill covers the need
For a topic, mechanism or workflow that no installed skill covers, use `build-skill`. It can create a new suite skill or a **project-local** skill that captures this project's own conventions, then continue with it.
