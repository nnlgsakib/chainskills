# Security checklist

Map every item to code and tests before an audit. Mark each one DONE / N/A / TODO with evidence.

## OWASP Smart Contract Top 10: 2026 (scs.owasp.org/sctop10, checked 2026-11-25)

| ID | Risk | Checks |
|---|---|---|
| SC01 | Access Control Vulnerabilities | Every state-changing external function has an explicit permission or is intentionally public; roles documented; admin behind timelock; initializers protected; no `tx.origin` auth |
| SC02 | Business Logic Vulnerabilities | Spec invariants implemented as invariant tests; edge cases (zero, max, first/last user, same-block actions) tested; economic review done |
| SC03 | Price Oracle Manipulation | No spot prices from a single pool; staleness + deviation checks; manipulation cost analysed |
| SC04 | Flash Loan–Facilitated Attacks | Single-tx manipulation of balances/prices/votes considered; snapshot-based voting; time-weighted values |
| SC05 | Lack of Input Validation | Every parameter bounded; addresses non-zero where required; array lengths matched and bounded; cross-chain message fields validated |
| SC06 | Unchecked External Calls | Return values checked (`SafeERC20`); failed calls handled; callbacks considered |
| SC07 | Arithmetic Errors (Rounding & Precision) | Rounding direction specified and in the protocol's favour; decimal scaling tested; share inflation defended |
| SC08 | Reentrancy Attacks | CEI + guards; cross-function and read-only reentrancy considered; hooks (ERC-777/721/1155, 7702-delegated EOAs) considered |
| SC09 | Integer Overflow and Underflow | `unchecked` blocks justified; casts (`uint256 → uint128`) use `SafeCast` |
| SC10 | Proxy & Upgradeability Vulnerabilities | `_disableInitializers()`; initialize at deploy; ERC-7201 storage; layout diffs; `_authorizeUpgrade` restricted; upgrade timelock |

## Beyond the Top 10
- [ ] Compiler ≥ 0.8.34 (preferably the latest), exact pragma, `evm_version` matches the target chain.
- [ ] EIP-7702: no EOA-detection assumptions.
- [ ] Signature replay: nonces, chainId, contract address and deadline in signed data (EIP-712). OpenZeppelin 5.7 `EIP712` name/version ≤ 31 bytes.
- [ ] Denial of service: no unbounded loops; no reliance on a single external party's liveness; griefing via dust or tiny positions.
- [ ] Front-running / MEV: slippage limits, deadlines, commit-reveal where needed.
- [ ] Gas limits: functions fit within block and per-tx gas caps (Ethereum per-tx cap 2^24 since Fusaka; check the target chain's value).
- [ ] Cross-chain: message authenticity, replay across chains, ordering assumptions, rate limits.
- [ ] Centralisation risks documented (who can do what, and with what delay).
- [ ] Emergency: pause scope, sunset, incident runbook.
- [ ] Events for every state change that off-chain systems need.

## Process
- [ ] `scripts/check_contracts.py`, `forge lint`, Slither, Aderyn: all findings triaged.
- [ ] Invariant tests per INV-ID pass with CI-level runs.
- [ ] Coverage report reviewed (uncovered branches justified).
- [ ] Audit-ready package: spec, threat model, test and coverage reports, triage notes, deployment plan, frozen commit.
- [ ] A bug bounty planned before mainnet value arrives.

OWASP also publishes the Smart Contract Security Verification Standard (SCSVS) at scs.owasp.org/SCSVS. Use its control groups for deeper reviews (no version number was shown on the page as of 2026-11-25).

Sources: https://scs.owasp.org/sctop10/ · https://scs.owasp.org/SCSVS/ · https://ethereum.org/roadmap/pectra/7702/ · https://www.certik.com/blog/pectras-eip-7702-redefining-trust-assumptions-of-externally-owned-accounts · https://soliditylang.org/blog/category/releases/
