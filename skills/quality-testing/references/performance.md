# Performance testing

## Method
1. **Workload**: derive the tx mix from real user flows (transfers, contract calls, staking ops, service-layer txs), with their size distribution and per-account patterns. Synthetic "empty transfer" TPS is not a result.
2. **Topology**: validator count, regions and hardware from R-N; sentries; RPC nodes separate from validators.
3. **Ramp**: increase offered load stepwise until latency targets break. Record the knee.
4. **Soak**: run at 70% of the knee for 24–72 h. Watch memory and disk growth, and compaction stalls.
5. **Repeat** ≥ 3 runs and report the variance.

## Metrics
| Metric | Definition |
|---|---|
| Throughput | committed tx/s (and gas/s) at a steady state |
| Inclusion latency | submit → included in a block (p50/p95/p99) |
| Finality latency | submit → final (p50/p95/p99) |
| Block time | interval between consecutive commits (p50/p95) |
| Rounds per height | > 1 indicates timeout or proposer problems |
| Resource use | CPU, RAM, disk IO, bandwidth per node role |
| State growth | bytes per day at the workload |
| Sync time | fresh node to tip via state sync/snapshot |

## Report template (`docs/testing/reports/<date>-perf.md`)
- Versions (commit, config), hardware, regions, validator count, workload description.
- Table of metrics versus R-N targets (pass/fail).
- Graphs: latency versus offered load; block time over the soak.
- Bottleneck analysis (consensus, execution, disk, network).
- Regression versus the previous report.

## CI regression
A small fixed benchmark (single region, fixed workload) on every main-branch merge. Fail on a > X% regression in p95 latency or throughput.
