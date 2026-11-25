# CometBFT ABCI 2.0 application guide

From docs.cosmos.network/cometbft (ABCI Overview and Methods), read 2026-11-25. CometBFT always initiates calls. The app answers each `Request*` with a `Response*` (protobuf in `proto/tendermint/abci/types.proto`).

| Method | When | Must be deterministic? | Key rules |
|---|---|---|---|
| `InitChain` | once at genesis | yes (response fields) | An empty validator set in the response means the request's set is used |
| `Info` | startup / recovery handshake | — | Return `last_block_height` and `last_block_app_hash` persisted in Commit; `app_version` goes into headers |
| `Query` | client queries | — | `/store…` paths are key queries; height 0 = latest; proofs on request |
| `CheckTx` | before a tx enters the local mempool (`New`, `Recheck`) | no (local) | Code ≠ 0 means not broadcast or proposed. Never mutate committed state. This is your anti-spam and fee gate |
| `PrepareProposal` | on the proposer | **may be non-deterministic** | Reorder, add or drop txs. Respect `max_tx_bytes`, because an invalid response crashes the node. Dropping a tx here doesn't remove it from the mempool |
| `ProcessProposal` | every validator (incl. proposer) | **must be deterministic**, depending only on the request + last committed state | ACCEPT → prevote the block; REJECT → prevote nil. Keep candidate state. Prefer ACCEPT unless you understand the liveness impact |
| `ExtendVote` | when precommitting non-nil | may be non-deterministic | The extension is signed by CometBFT and attached to the precommit (oracle prices, beacon shares, attestations) |
| `VerifyVoteExtension` | for received precommits with a valid signature | **must be deterministic** | REJECT drops the whole vote. A zero-length extension is valid if signed |
| `FinalizeBlock` | apply a decided block (replaces BeginBlock/DeliverTx/EndBlock) | **must be deterministic** | `app_hash` depends only on the request + previous committed state. `validator_updates` at H take effect at **H+2**; `consensus_param_updates` at H+1. Per-tx `code`, `data`, `gas_*` are deterministic; `log`, `info`, `events` aren't |
| `Commit` | after FinalizeBlock | — | Persist state before returning. `retain_height` (non-deterministic) controls pruning, and too low breaks bootstrapping |
| `ListSnapshots` / `LoadSnapshotChunk` / `OfferSnapshot` / `ApplySnapshotChunk` | state sync | — | Implement these so new nodes don't replay history |

## Engine versions
Supported lines are v0.40.x (Cosmos release family 2026.1) and v0.38.x (2025.1). v1.x was retracted. v0.40.0 added `mldsa65` validator keys and raised signature size limits. The CometBFT README asks you not to depend on `main`.

## Rust
`tendermint-abci` in github.com/cometbft/tendermint-rs is "a lightweight, low-level framework for building … ABCI applications in Rust". The repo is pre-1.0, and its README cites compatibility testing with Tendermint Core v0.34.21. Verify ABCI 2.0 support for your CometBFT version before choosing it, or evaluate other Rust ABCI servers (unverified) or Malachite.
