# Placement map — custom chain on a BFT engine

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | CometBFT (Tendermint BFT) / Malachite (Tendermint in Rust) / Commonware consensus primitives | Tune timeouts; vote extensions for per-vote data |
| state-execution | custom | your app: FinalizeBlock (CometBFT) or Decide handler (Malachite) | Determinism rules; authenticated state commitment (JMT/IAVL/SMT) |
| staking-validators | custom | your staking logic emits validator updates (CometBFT: effective at H+2) | protocol-staking-validators design |
| rollup | n/a | — | — |
| tokenomics | custom | your fee, mint and reward logic | CheckTx for fee and anti-spam gating |
| governance | custom | your governance module or contracts | protocol-governance |
| randomness | custom | vote extensions with threshold-signature shares, or an external beacon | protocol-randomness |
| verifiable-participation | custom | your modules + off-chain operators | — |
| data-availability | custom | full nodes + your snapshot / state-sync implementation | ABCI snapshot methods |
| p2p | native | CometBFT p2p (experimental libp2p in v0.39+) / Malachite libp2p network actor / Commonware p2p | Sentry topology |
| interop | custom | light clients; IBC needs implementing the IBC spec against your state | protocol-interop |
| smart-contracts | custom | only if you embed a VM (EVM via revm, WASM) | protocol-state-execution |
| node-software | extend | engine binary + your app (separate process or in-process) | Operator CLI, RPC and indexer are yours |
| upgrades | extend | engine releases; app versioning (`app_version`), halt-height coordinated upgrades | Rehearse on a devnet |
