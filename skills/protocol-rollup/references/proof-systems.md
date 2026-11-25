# Proof systems

Facts checked 2026-11-25 are marked ✔.

## Families

| Family | How it works | Withdrawal latency | Ops | Examples (status) |
|---|---|---|---|---|
| Interactive fault proofs | Challenger and proposer bisect to a single instruction executed on L1 | challenge period (≥ 5 d for Stage 1) | proposers + challengers with bonds | OP Stack: Cannon/Kona programs; Upgrade 20 moves to Super Root dispute games for interop ✔; Upgrade 19 requires op-reth + kona-client, since op-geth/op-program don't support it ✔ |
| Bounded-time disputes | Disputes resolve within a fixed maximum time regardless of the number of challengers | bounded (BoLD designed around ~12 days worst case ✔) | permissionless validators with bonds | Arbitrum BoLD, live on One/Nova since Feb 2025 ✔ |
| Validity proofs (ZK) | Prover proves the state transition; L1 verifies a succinct proof | proving time + verification | GPU prover fleet or a proving market | ZKsync Airbender (RISC-V, replaces Boojum for new chains) ✔; SP1 (OP Succinct; Agglayer chains such as Katana) ✔ |
| ZK fault proofs (hybrid) | Optimistic by default, ZK proof settles disputes in one step | shorter than interactive | prover on demand | OP Succinct "Lite"-style designs (name and status unverified) |
| Multi-proof | Two or more independent systems must agree (or a council decides when they disagree) | max of the components | more infrastructure | reduces single-implementation bug risk |

## Choosing
- **Need short withdrawals** (bridges, exchanges): ZK, or a hybrid, or fast-withdrawal liquidity providers on top of optimistic.
- **Lowest ops complexity**: optimistic with a mature framework.
- **Stage 2 ambition**: permissionless challengers/provers and on-chain-adjudicable council powers. Multi-proofs make the "two valid contradicting proofs" emergency case well-defined.
- **Prover economics**: estimate the cost per block at target throughput. Proving markets reduce ops but add a dependency.

## Bugs happen
- Kona's fallback proof system had a vulnerability fixed in Feb 2026 and disclosed in Mar 2026 ✔.
- Celo upgraded its OP-Succinct dispute game on 28 Apr 2026 for two vulnerabilities in upstream kona crates (fixed in op-succinct v3.8.0 / v4.3.0) ✔.

Lessons: subscribe to upstream security advisories, keep an emergency upgrade path that can't steal funds, and track which proof components and versions you depend on (an SBOM for the proof stack).

Sources: https://docs.optimism.io/notices/upgrade-20 · https://gov.optimism.io/t/vulnerability-in-kona-fallback-proof-system/10650 · https://forum.celo.org/t/op-succinct-security-upgrade-on-celo-mainnet/13274 · https://www.theblock.co/post/340278/ · https://www.zksync.io/airbender · https://docs.polygon.technology/chain-development/cdk/get-started/overview
