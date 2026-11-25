# EVM L1 production checklist

## All routes
- [ ] Route decision ADR (A–E) with the trust model: who validates, how validators join and leave, and the halt and recovery behaviour.
- [ ] Unique chain ID registered (chainlist), with genesis frozen and its hash published.
- [ ] Hardfork schedule in genesis matches the EVM features your contracts need. A tracking process exists for upstream hardforks and security releases.
- [ ] Validators across independent operators, regions and providers. Validator keys in HSM/KMS or remote signers. Sentry or bootnode topology so validators aren't publicly exposed.
- [ ] RPC/archive nodes separate from validators, behind rate-limited proxies. Debug, admin and personal namespaces off publicly.
- [ ] Monitoring: block production, missed proposals/rounds, peer counts, finality lag, disk growth. Alerting on-call.
- [ ] Upgrade runbook: release, coordinated activation height or time, canary nodes first.
- [ ] Bridge(s) reviewed as the top risk (`quality-security`).

## Route A: Besu QBFT
- [ ] ≥ 4 validators (BFT minimum), ideally more, across organisations. Never more than 1/3 under one operator.
- [ ] Validator management method chosen (header votes vs contract). If contract, the contract is audited and governed (multisig/timelock).
- [ ] `blockperiodseconds`, `requesttimeoutseconds` and `epochlength` tuned via a load test. `pertxgaslimit` decided.
- [ ] Network permissioning (node/account allowlists) if consortium.

## Route B: own PoS beacon chain
- [ ] ≥ 2 execution and ≥ 2 consensus client implementations in production.
- [ ] Deposit contract, genesis validators and the withdrawal credentials process documented.
- [ ] Slashing protection on every validator client. No duplicate keys across machines.
- [ ] Checkpoint sync endpoints for new nodes.

## Route C/D: custom or forked client
- [ ] Fork diff minimised and documented. Upstream merge cadence defined.
- [ ] System or validator contracts audited to consensus-code standards.
- [ ] Differential tests against upstream for unchanged behaviour.

## Route E: Avalanche L1
- [ ] ValidatorManager (PoA/PoS) deployed per ACP-99 v2, with ownership on a multisig.
- [ ] P-Chain registration and balance top-ups monitored. ICM relayers operated.
