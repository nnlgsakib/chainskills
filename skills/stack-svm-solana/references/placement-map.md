# Placement map — Solana / SVM

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | Solana validators (Alpenglow Votor live; Rotor pending) | Relevant to program devs only for confirmation and finality assumptions |
| state-execution | native | SVM; programs (sBPF), accounts declared per tx (parallel execution) | Compute budget per tx; account size and rent |
| staking-validators | custom | app-level staking programs (stake pools, restaking) | Native stake program exists for SOL staking |
| rollup | n/a | — | SVM rollups are separate frameworks (unverified) |
| tokenomics | extend | SPL Token / Token-2022 mints and extensions, program fee logic | Mint and freeze authorities: multisig or revoke |
| governance | extend | program-based DAOs, multisig upgrade authority (e.g. Squads) | Timelocked upgrades for value-bearing programs |
| randomness | custom | oracle/VRF programs; never slot hashes alone | protocol-randomness |
| verifiable-participation | custom | programs + off-chain operators (keepers, cranks) | — |
| data-availability | n/a | — | Only relevant for own SVM chains |
| p2p | n/a | — | Only relevant for own SVM chains (validator networking) |
| interop | native | bridges and messaging protocols (third-party) | Treat bridges as top risk |
| smart-contracts | native | Anchor or native Rust programs | This adapter + quality-* |
| node-software | native | Agave / Firedancer validators, RPC nodes, Surfpool for local | Use providers or your own RPC, separate from validators |
| upgrades | extend | program upgrade authority (`solana program deploy`/upgrade; `--final` for immutable) | Multisig authority; verifiable builds |
