# OP Stack production checklist

Based on docs.optimism.io "Launch a chain with fault proofs and HA sequencing" and the chain-operator best practices (read 2026-11-25). Combine it with `protocol-rollup/references/stages.md` and the `quality-*` skills.

## Before launch
- [ ] Completed a full testnet deployment with the same op-deployer intent shape and component versions.
- [ ] The decision is recorded in an ADR: rollup vs Alt-DA, custom gas token, L2 chain ID, block time, fee parameters, Superchain membership.
- [ ] Fault proofs live from day one (permissioned or permissionless game type decided; target Stage written down).
- [ ] Absolute prestate generated and verified for the chain config (kona-client). For ZK games, the ZK prestate is verified.
- [ ] Key management: batcher, proposer, challenger and admin keys under the documented signing posture (HSM/KMS for hot keys, multisig and timelock for admin), with funded balances and balance alerts.
- [ ] Contract upgrade authority: ProxyAdmin owner = multisig/Security Council per Stage target. Upgrade delay ≥ the users' exit window.

## Sequencing
- [ ] 3 sequencer nodes (op-node + op-reth) in separate regions or AZs, managed by op-conductor.
- [ ] op-conductor and admin RPCs reachable only on the private network.
- [ ] Failover drill done: kill the leader, then check continuous block production and no unsafe-head reorg beyond tolerance.
- [ ] Sequencer isolated behind a proxy. Public traffic goes to replicas, which gossip internally.

## Monitoring
- [ ] op-dispute-mon alerting on incorrect or unchallenged games.
- [ ] Batcher lag, proposer cadence, L1 gas/blob fees, sequencer liveness, safe and finalized head lag.
- [ ] Bridge invariants (L2 supply vs L1 escrow) and withdrawal pipeline health.

## Operations
- [ ] Staggered upgrades: canary nodes first, then the rest.
- [ ] Subscribed to OP Stack notices (hardforks, end-of-support dates) with a calendar for activation deadlines.
- [ ] Deployment artifacts archived (op-deployer state, versions, commits) and Superchain Registry entry prepared if joining.
- [ ] Runbooks: sequencer outage, L1 reorg, invalid proposal detected, key compromise, emergency pause (Guardian) and its scope.
