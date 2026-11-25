# chainskills conventions

## Format (open Agent Skills standard)
- One folder per skill containing `SKILL.md`, with YAML frontmatter then Markdown.
- `name`: 1–64 chars, lowercase letters, digits and single hyphens, no leading or trailing hyphen, **equal to the folder name**.
- `description`: 1–1024 chars, covering what the skill does and when to use it.
- Optional standard fields: `license`, `compatibility` (≤ 500 chars, environment requirements), `metadata` (string map), `allowed-tools`. The suite always sets `license: MIT`. Keep other agent-specific fields out of suite skills, because not every agent understands them.
- Optional folders: `references/` (docs loaded on demand), `scripts/` (executable helpers), `assets/` (templates, data). Templates that look like skills are stored as `*.tmpl`, so agents don't load them.

## Layers and names (suite skills)

| Prefix | Layer | Rules |
|---|---|---|
| `blockchain-dev` | L0 router | only one |
| `design-` | L1 | stack-neutral; produce architecture, spec, decisions |
| `protocol-` | L2 | stack-neutral mechanisms; options, trade-offs, attacks, spec hand-off |
| `build-` | L3 | implementation surfaces and suite extension |
| `stack-` | L4 | the only framework-specific layer; follows the adapter contract (`build-stack-adapter`) |
| `quality-` | L5 | security, testing, verification |
| `ops-` | L6 | upgrades, infrastructure, data access, launch, readiness |
| `extra-` | optional | wallets, frontends, docs |

Lower layers never depend on higher ones. A `protocol-*` skill never says "use x/staking". It says "a bounded active set with delegation", and the `stack-*` placement map supplies the framework detail.

## Structure of SKILL.md
1. Title + one paragraph: layer, purpose, which skills it receives work from and hands work to.
2. Inputs, including the shared state (`CHAIN.md`, `docs/spec/…`) when relevant.
3. Reference table: `| file | read when |`. Every file listed must exist.
4. Workflow: numbered steps in the imperative, each saying *why* it matters.
5. Hand-off: files written, IDs (R-, INV-, P-, ADR-, Q-, K-), CHAIN.md updates, next skill.
6. Rules: a few durable principles.
7. `## Sources (verified YYYY-MM-DD)`: required for any skill with version-sensitive facts.

Target under about 250 lines, with a hard limit of 500. Move catalogues, tables and long examples into `references/`. Give reference files over about 300 lines a table of contents.

## Writing style
- Explain the reasoning, not only commands. Agents handle unseen cases better when they understand why.
- Use varied examples (different chains, stacks, roles), so a skill doesn't overfit one project.
- Mark verified facts with ✔ and give unverified ones explicitly as `(unverified)`. Include dates.
- No marketing, no hedging filler. Tables for comparisons, checklists for gates.

## Scripts
- Python 3 stdlib only. Read-only on the user's project unless the skill's purpose is to write files.
- A `--selftest` (or `selftest` subcommand) that exercises the real logic and must pass.
- Write commands as `python3 …`, and put this standard line before the first command in every file. `check_skill.py` warns when it's missing.

  > **Python command:** examples use `python3`. If that isn't found (common on Windows), retry the same command with `python`, then `py -3`.
- Never execute project code from a detection or analysis script.

## IDs used across skills
`R-F/R-N/R-C` requirements, `INV-<COMP>-<n>` invariants, `P-<COMP>-<name>` parameters, `ADR-<nnnn>` decisions, `Q<n>` questions, `K<n>` risks. These are defined in `blockchain-dev/references/chain-md.md`.

## Registering a suite skill
- Main README skill table (with ✅).
- `blockchain-dev/references/routing.md` topic row (and the phase table, if it belongs to a phase).
- CHANGELOG entry. For a release, bump the version in `.claude-plugin/plugin.json`.
- `check_skill.py` passes. Scripts' self-tests pass. For adapters, `check_adapter.py` passes too.
