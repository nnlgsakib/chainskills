# Rollup risk review

| Risk | Impact | Mitigation |
|---|---|---|
| Sequencer outage | No soft confirmations; users stuck | Forced inclusion via L1 with a documented delay; sequencer failover; status page |
| Sequencer censorship | Targeted txs excluded | Forced inclusion; plan for shared or based sequencing |
| Proof-system bug | Invalid state accepted or valid withdrawals blocked | Audits, bounty, multi-proofs, conservative emergency path, version pinning + advisory monitoring |
| Malicious or compromised upgrade key | Theft via a contract upgrade | Timelock ≥ exit window; Security Council ≥ 8 / 75%; publish upgrade procedures |
| DA withholding (validium/optimium) | Users can't prove balances to exit | Committee size/independence; fallback to L1 DA; state the exit guarantee honestly |
| Blob fee spikes | Posting cost explodes | Fee model passes DA cost through; batch compression; DA fallback policy |
| L1 reorg / finality delay | Deposits or withdrawals reverted | Wait for L1 finality on deposits; don't treat unsafe L2 heads as final |
| Bridge escrow mismatch | Unbacked tokens on L2 | Invariant monitoring (L2 supply ≤ L1 escrow); rate limits; pause scope limited to deposits |
| Challenger liveness | Invalid root finalises (optimistic) | ≥ 5 independent challengers (Stage 0 requirement); bonds; monitoring with alerts well before deadlines |
| Prover liveness (ZK) | Withdrawals delayed | Prover redundancy or a proving market; permissionless proving fallback |
| Gas-token or fee config errors | Broken fee accounting | Test the L1 data fee formula against real blob prices; invariant tests |
| Upstream framework breaking changes | Node or proofs stop working after an upgrade | Track framework upgrade notices (e.g. OP Upgrade 19/20 client requirements); rehearse on testnet |
