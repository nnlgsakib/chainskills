---
name: quality-security
description: Secure a blockchain end to end, independent of stack — threat modeling per component and trust boundary (malicious validators, participants, relayers, governance attackers, insiders, supply chain, signing UIs), key inventory and custody (validator remote signers such as Cosmos-KMS/Horcrux with HSM or cloud KMS, multisig signer hygiene and clear signing, rotation), secure development lifecycle (dependency and CI hardening, reproducible signed releases, frontend integrity, developer workstation security), audits and audit contests, bug bounties and SEAL Safe Harbor, monitoring and incident response (SEAL 911, runbooks, post-mortems). Use whenever the user asks for a threat model, security review, key management, audit preparation, bug bounty, incident response plan, or wants to know how chains and protocols actually get hacked.
license: MIT
---

# Quality: Security

A quality skill in chainskills (layer L5). It produces the threat model and security programme for the whole system: chain, contracts, off-chain services, keys, people and processes. Code-level checks live in the build and stack skills, and testing and verification in `quality-testing` and `quality-formal-verification`. This skill makes sure they cover the real threats.

Reality check (H1 2026, per CertiK, TRM and Blockaid; figures vary by firm): key and multisig compromises were about 15% of incidents but about 76% of losses, smart-contract bugs were the most common incidents, and DPRK-linked groups caused most of the value lost. **Keys, signing flows and people are the main attack surface, alongside code.**

Inputs: `CHAIN.md`, `docs/spec/*`, the placement table, deployment plans. Shared state rules: `../blockchain-dev/references/chain-md.md`.

| Reference | Read when |
|---|---|
| `references/threat-model.md` | Building the threat model (actor catalogue, template, per-component prompts) |
| `references/key-management.md` | Inventorying and protecting keys: validators, multisigs, deployers, operators |
| `references/secure-sdlc.md` | Dependencies, CI/CD, releases, frontends, workstations |
| `references/audits-bounties-ir.md` | Audits, contests, bounties, Safe Harbor, monitoring, incident response |

## Workflow

### 1. Assets and boundaries
List what's worth attacking: user funds (escrows, pools, bridges), consensus (finality, liveness), privileged keys, the treasury, governance, data, reputation. Draw trust boundaries: chain ↔ contracts ↔ off-chain services ↔ frontends ↔ operators' machines.

### 2. Threat model
Use `references/threat-model.md`. For each component and boundary, go through the actor catalogue, from external user up to compromised developer machine. Write `docs/security/threat-model.md` with: threat, actor, preconditions, impact, likelihood, mitigation, **evidence** (test, invariant, model, config), owner. Every high-impact threat without evidence becomes a K-risk in `CHAIN.md`.

### 3. Keys
Use `references/key-management.md` to write `docs/security/key-inventory.md`, covering every key: type, holder, custody (HSM/KMS/MPC/hardware wallet), what it can do, how it's rotated and revoked, and how its compromise is detected. Validator keys sit in a remote signer. Multisig signers verify transactions independently on a separate device (the Bybit lesson).

### 4. Secure development lifecycle
Use `references/secure-sdlc.md`: pinned and scanned dependencies, hardened CI with no long-lived secrets, reproducible signed releases, frontend integrity, and hardened developer workstations against social engineering.

### 5. Code assurance
Make sure each component has the checks its stack skill requires (state-machine audit, contract checks, static analysis), fuzzing (`go test -fuzz`, cargo-fuzz, Foundry/Echidna/Medusa), tests per invariant (`quality-testing`), and a formal model for the critical parts (`quality-formal-verification`).

### 6. Audits and bounties
Use `references/audits-bounties-ir.md`. Audit after the spec freezes and tests pass. Get two independent reviews for consensus, bridge and staking code, review the fixes, and publish the reports. Launch a bug bounty before value arrives, and adopt SEAL Safe Harbor so whitehats can rescue funds during an active exploit.

### 7. Monitoring and incident response
- **Monitoring**: on-chain invariant monitors (bridge supply ≤ escrow, total supply rules, governance proposals, large voting-power moves, validator equivocation, admin-role changes), all alerting to on-call.
- **Incident response**: runbooks for pause, coordinated halt or upgrade, key revocation, communications, and SEAL 911 contact. Rehearse at least twice a year. Write a post-mortem for every incident.

### 8. Hand off
- Write `docs/security/` (threat model, key inventory, audit tracker, IR runbooks).
- In `CHAIN.md`, add risks, and set components to `audited` only with a report link.
- Feed findings back to the owning skills.

## Rules
- Every threat with a high impact has evidence or an explicit, owned K-risk.
- No privileged key without documented custody, rotation and detection.
- Signers never trust the UI that prepared a transaction: verify the calldata independently and use clear signing.
- Security reviews include ops (keys, CI, frontends, people), not only code.

## Sources (verified 2026-11-25)
H1 2026 incident data: forklog.com/en/certik-says-crypto-hack-losses-hit-1-32b-in-h1-2026, unchainedcrypto.com (Blockaid 212 exploits) · Bybit (compromised Safe{Wallet} signing frontend, blind signing, delegatecall-enabled wallet): blog.trailofbits.com/2025/02/25/how-threat-modeling-could-have-prevented-the-1.5b-bybit-hack · Cosmos-KMS: docs.cosmos.network/sdk/latest/kms/remote-signing · SEAL Safe Harbor: frameworks.securityalliance.org/safe-harbor · SEAL frameworks and 911: frameworks.securityalliance.org, theblock.co (1,800+ tickets in 2025).
