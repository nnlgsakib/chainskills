---
name: design-spec
description: Write implementable, stack-neutral specifications for blockchain components — state, transactions/operations, validation and authorization rules, per-block and per-epoch logic, parameters with bounds, numbered invariants, lifecycle state machines, failure modes, test vectors — plus the global parameter and invariant registries and decision records. Use this skill whenever the user wants a spec, a formal design, invariants, a state machine, a parameter table, or to turn an architecture or whitepaper section into something engineers and auditors can implement and test, for any stack (module, pallet, smart contract, precompile, off-chain service).
license: MIT
---

# Design Spec

Second design step of the chainskills suite. The spec is the contract between design and code: implementers build from it, testers derive tests from its invariants, auditors check code against it. It must stay stack-neutral so it survives a change of framework — "a map from validator ID to Validator record", not "a `collections.Map` in x/staking" or "a Solidity mapping".

Shared state: `CHAIN.md` and `docs/` as defined in `../blockchain-dev/references/chain-md.md`. Inputs: `docs/spec/architecture.md` and the Components table. If they don't exist, run `design-protocol` first (or, for a single component added to an existing chain, write a short Context section instead).

| Reference | Read when |
|---|---|
| `references/notation.md` | Writing any state or operation — types, pseudocode, determinism rules |
| `assets/component.template.md` | Starting a component spec |
| `references/review-checklist.md` | Before marking a component `specified` |
| `assets/registries.template.md` | Creating `parameters.md`, `invariants.md`, `glossary.md` |

## Workflow

### 1. Pick the component and its mechanism skill
One spec file per component: `docs/spec/<component>.md`. If a `protocol-*` skill owns the mechanism (see the Components table), load it first — it supplies the design options and known attacks; this skill turns the chosen option into a spec.

### 2. Write the spec from the template
Fill `assets/component.template.md` in order. The sections that matter most:

- **State** — every stored entity: fields, types (`references/notation.md`), key, who writes it, size bound. Unbounded collections need a growth limit or a cost.
- **Operations** — for each tx/message/call: caller and authorization, inputs, validation (each rule is a numbered check with the error it raises), effects in order, events, cost class. Write effects as pseudocode precise enough that two teams would produce the same state.
- **Hooks** — logic run per block / per epoch / on upgrade, with explicit work bounds ("processes at most `P-COMP-max_per_block` items").
- **Parameters** — `P-<COMP>-<name>`: type, default, min, max, unit, who can change it, effect of changing it at runtime.
- **Invariants** — `INV-<COMP>-<n>`: statements that are true after every operation and hook, phrased so a test or model checker can verify them ("Σ delegations to v == v.delegated_stake").
- **Lifecycles** — mermaid state diagram for every entity with status (validator, proposal, task, withdrawal).
- **Failure and adversarial cases** — what each actor can do wrong, what the component does.

### 3. Determinism and arithmetic
Apply the determinism rules in `references/notation.md` to every operation: integer/fixed-point only, rounding direction stated for every division (always in the protocol's favour), overflow behaviour, iteration order, time source (block time/height only), no external inputs except through explicit oracles.

### 4. Update the registries
- `docs/spec/parameters.md` — one table of every parameter across components.
- `docs/spec/invariants.md` — every invariant with its component and the test/model that checks it (filled later by `quality-testing` / `quality-formal-verification`).
- `docs/spec/glossary.md` — terms that could be read two ways.
Decisions taken while specifying (e.g. "round rewards down, dust to reserve") → ADRs.

### 5. Review and mark
Run `references/review-checklist.md`. Fix or record each failing item as a Q-item. Then set the component to `specified` in `CHAIN.md` and link the file. When all components are specified → phase `spec`, next step `design-stack-selection`.

## Changing a spec later
Specs change. Bump the spec version in the file header, add a changelog line, update affected parameters/invariants (never renumber — deprecate and add new IDs), and add a Q-item "code/tests need update" if the component is already `built`.

## Output to the user
Which components were specified, number of operations/parameters/invariants, open questions that block implementation, next step. Files are on disk — don't paste them in chat.
