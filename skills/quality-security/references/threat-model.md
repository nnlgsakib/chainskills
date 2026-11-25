# Threat model

## Actor catalogue (go through every actor for every component)

| # | Actor | Capabilities | Typical goals |
|---|---|---|---|
| A1 | External user | send any tx, call any public function, frontrun, spam | steal funds, grief, extract MEV |
| A2 | Malicious validator (< 1/3 power) | propose blocks, order txs, withhold votes, equivocate | MEV, censorship, slashing others |
| A3 | Validator coalition (≥ 1/3 or ≥ 2/3) | halt finality / finalise conflicting blocks | ransom, double-spend via bridges |
| A4 | Malicious participant (community/verifier/service node, oracle, relayer) | fake work, collude, withhold, lie in reports | rewards without work; corrupt results |
| A5 | Sequencer / operator (rollups, services) | censor, reorder, go offline | MEV, extortion |
| A6 | Governance attacker | buy or borrow votes, propose malicious payloads | treasury drain, parameter abuse |
| A7 | Privileged key holder (admin, council member) | anything their role allows | insider theft, coercion |
| A8 | Compromised signer environment | alter what a signer sees or signs (UI, wallet, machine) | get a malicious tx signed (Bybit pattern) |
| A9 | Supply-chain attacker | malicious dependency, compromised CI, poisoned release or frontend, DNS hijack | backdoor nodes, contracts or UIs |
| A10 | Infrastructure attacker | DDoS, BGP/DNS attacks, cloud account takeover | outages, eclipse, key theft |
| A11 | Social engineer (incl. state actors) | fake job offers, malicious repos and npm packages, impersonation | developer machine compromise, then keys |

## Per-component prompts
- **Consensus/staking**: equivocation, long-range attack, unbond-before-slash, concentration, key theft, a stalled beacon (protocol-consensus/attacks.md, protocol-staking-validators/attacks.md).
- **Execution/contracts**: OWASP SC Top 10 2026 (build-smart-contracts/security-checklist.md), precompile bugs, non-determinism.
- **Participation layer**: lazy or colluding verifiers, sybils, fake proofs, assignment prediction (protocol-verifiable-participation).
- **Bridge/rollup**: invalid state roots, proof bugs, escrow mismatch, upgrade-key abuse, DA withholding (protocol-rollup/risks.md).
- **Governance/treasury**: vote buying, malicious payloads, emergency-power abuse (protocol-governance/attacks.md).
- **Off-chain services**: authentication, rate limits, key storage, dependency on a single operator.
- **Frontends/RPC**: script injection, DNS, RPC spoofing, phishing clones.
- **Operations**: CI secrets, release signing, deployer keys, workstation compromise.

## Template (`docs/security/threat-model.md`)

| ID | Component | Threat | Actor | Preconditions | Impact (H/M/L) | Likelihood (H/M/L) | Mitigation | Evidence (test / INV / model / config) | Owner | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| TM-1 | | | | | | | | | | open |

Review the threat model at each phase gate and after every architecture change. Threats with impact H and no evidence block the `ops-production-readiness` gate.
