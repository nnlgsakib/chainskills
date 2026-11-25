# EVM production checklist

Use together with `stack-cosmos-ignite` → `references/production.md`. Report DONE / N/A / TODO with evidence.

## 1. Identity (permanent after launch)
- [ ] EVM chain ID chosen deliberately and unique on chainlist.org. Either hard-code it in the app's `GetEVMChainID` (no hash, no genesis-path fallback) or set `[evm] evm-chain-id` identically on every node (upstream cosmos/evm, default 262144). It must never differ between nodes.
- [ ] Base denom atto-prefixed (`amychain`), display denom with exponent 18, symbol set; bank `denom_metadata` written explicitly.
- [ ] `evm_denom` param == base denom; `app/evm.go` no longer references `sdk.DefaultBondDenom`.
- [ ] `ChainCoinType = 60`; keyring default algo eth_secp256k1.
- [ ] `scripts/check_evm_genesis.py` passes on the final genesis.

## 2. Consensus and fees
- [ ] Consensus `block.max_gas` finite and equal to the EVM mempool `BlockGasLimit`.
- [ ] Feemarket params decided: `no_base_fee=false` for EIP-1559, `base_fee`, `min_gas_price`, `base_fee_change_denominator`, `elasticity_multiplier`.
- [ ] `minimum-gas-prices` in app.toml consistent with feemarket `min_gas_price` (18-decimal scale).
- [ ] `MaxTxGasWanted` set; per-tx gas cap sane.
- [ ] Replay protection: `[json-rpc] allow-unprotected-txs = false` (the default) on every RPC node, so pre-EIP-155 txs are refused.

## 3. Attack surface inside the state machine
- [ ] `active_static_precompiles` lists only what's needed. Each enabled precompile reviewed (staking/gov/bank from contracts = new attack paths, e.g. contracts that delegate and re-enter).
- [ ] Custom precompiles: deterministic, gas-metered, reentrancy-safe, audited.
- [ ] EVM access control (contract create/call permissions) decided — permissioned deployment for an early mainnet is a valid choice, governable later.
- [ ] ERC20 module: `enable_erc20`, permissionless registration decided; token pair registration via governance reviewed.
- [ ] Module accounts `evm`/`erc20` Minter+Burner permissions understood; your other module accounts still blocked from receiving.

## 4. JSON-RPC nodes
- [ ] JSON-RPC disabled on validators and sentries.
- [ ] Public RPC nodes: `api = "eth,net,web3"` only — never `personal`, `admin`, `debug`, `txpool` publicly.
- [ ] Caps set in app.toml `[json-rpc]` (defaults in brackets, verified 2026-11-25): `gas-cap` (25000000), `evm-timeout` (5s), `txfee-cap` (1), `filter-cap` (200), `logs-cap` (10000), `block-range-cap` (10000), `http-timeout` (30s), `http-idle-timeout` (120s), `max-open-connections` (0 = unlimited, so set it, e.g. 1000), `batch-request-limit` (1000), `batch-response-max-size` (25000000), `ws-origins` restricted to your domains.
- [ ] `[evm] max-tx-gas-wanted` set (default 0 = no cap).
- [ ] Behind reverse proxy with TLS, rate limiting, request-size limits, WebSocket limits.
- [ ] Archive RPC node (`pruning = "nothing"`, `enable-indexer = true`) for explorers/indexers; tracer enabled only there.

## 5. Ecosystem
- [ ] chainlist.org entry (EVM chain ID, RPCs, explorer, native currency 18 decimals).
- [ ] Cosmos chain-registry entry (both bech32 and EVM info).
- [ ] EVM block explorer (Blockscout or similar) pointed at the archive node.
- [ ] Canonical contracts deployed: Multicall3, Create2 deployer / Safe singleton factory, WETH-like wrapper for the native coin if needed — at known addresses, documented.
- [ ] Wallets tested: MetaMask, Keplr/Leap (Cosmos side), Ledger with eth app.

## 6. Testing
- [ ] Foundry test suite against a local multi-validator network (not just a single `serve` node).
- [ ] Both tx paths (Cosmos `MsgSend` and Ethereum tx) under load; mempool behaviour with nonce gaps and replacement (same nonce, higher fee).
- [ ] Precompile integration tests from Solidity.
- [ ] IBC token → ERC20 representation round-trip with a real counterparty (Hermes via `stack-cosmos-apps`).
- [ ] Upgrade rehearsal including cosmos/evm version bump on exported state.
