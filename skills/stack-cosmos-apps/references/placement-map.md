# Placement map — Ignite Apps

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`. Concepts not changed by an app follow `stack-cosmos-ignite`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | n/a | — | Unchanged by apps (CometBFT via stack-cosmos-ignite). Evolve replaces CometBFT block production with a sequencer/aggregator |
| state-execution | extend | wasm / gnovm add a VM | CosmWasm (Rust contracts) or GnoVM next to native modules |
| staking-validators | n/a | — | stack-cosmos-ignite. `network` coordinates the genesis validator set only |
| rollup | extend | `evolve` | Sovereign rollup on a DA layer (Celestia or local-da). `evolve add-migrate` migrates a running chain |
| tokenomics | extend | `fee-abstraction` | Pay fees in IBC tokens priced through Osmosis |
| governance | n/a | — | stack-cosmos-ignite |
| randomness | n/a | — | stack-cosmos-ignite (custom) |
| verifiable-participation | n/a | — | stack-cosmos-ignite (custom) |
| data-availability | extend | `evolve` | External DA layer via ev-node |
| p2p | n/a | — | stack-cosmos-ignite |
| interop | native | `hermes` | IBC relaying for dev. Production Hermes runs standalone |
| smart-contracts | native | `wasm`, `gnovm` (EVM → stack-cosmos-evm) | Permissioned CosmWasm uploads on mainnet |
| node-software | extend | `spaceship`, `explorer`, `connect`, `cca`, custom Ignite apps | Deploys, explorers, CLI clients, frontends. Custom tooling via authoring.md |
| upgrades | n/a | — | stack-cosmos-ignite. Apps that rewrite code need an upgrade handler on live chains |
