# Placement map — Polkadot SDK

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | parachain: relay-chain validation via coretime, collators author blocks; solo chain: Aura/BABE + GRANDPA (unverified details) | Choose parachain vs solo in design-stack-selection |
| state-execution | native | FRAME runtime compiled to Wasm; pallets; weights | Benchmark every call. Determinism through Wasm |
| staking-validators | native | staking pallets (release notes show `pallet-staking-async`, `pallet-election-provider-multi-block`, `pallet-validator-collators`), session, collator selection | Parachains: collators, not validators, secure liveness only |
| rollup | n/a | — | Parachains are relay-chain validated, not Ethereum-style rollups |
| tokenomics | extend | balances/assets pallets, inflation or reward config, treasury pallet | Model in protocol-tokenomics |
| governance | native | OpenGov (referenda, conviction voting, origins), treasury | Remove sudo for production |
| randomness | extend | BABE / relay-chain VRF randomness (biasable, use with care), custom beacons | protocol-randomness |
| verifiable-participation | custom | custom pallets + off-chain workers or external services | Off-chain workers suit periodic tasks; verify on-chain |
| data-availability | extend | relay chain for parachains (PoV); solo: full nodes | — |
| p2p | native | libp2p networking in the node | Reserved and boot nodes; sentry topology |
| interop | native | XCM across parachains and to the relay; bridges (e.g. to Ethereum/Kusama) via dedicated chains | Restrict XCM barriers |
| smart-contracts | extend | pallet-revive (REVM + PolkaVM; Solidity via resolc) on your runtime or Polkadot Hub; ink! opt-in via Pop CLI | `build-smart-contracts` for Solidity |
| node-software | native | `polkadot-omni-node` (generic parachain node), custom node binaries, `chain-spec-builder`, Pop CLI | Pin to stable releases |
| upgrades | native | forkless runtime upgrades (`system.setCode` via governance), node releases for client changes | Bump `spec_version`; try-runtime before upgrading |
