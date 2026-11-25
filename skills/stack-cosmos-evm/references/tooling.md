# EVM dev tooling: keys, JSON-RPC, MetaMask, Foundry, Hardhat

Flag/key names come from cosmos/evm's server and keyring; confirm with `mychaind start --help | grep -i json-rpc` and `mychaind keys --help`.

## Contents
- Enable JSON-RPC
- Keys and addresses
- MetaMask
- Foundry
- Hardhat
- Smoke test checklist

## Enable JSON-RPC

app.toml (per node):

```toml
[json-rpc]
enable = true
address = "127.0.0.1:8545"
ws-address = "127.0.0.1:8546"
api = "eth,net,web3"            # add txpool,debug only on private dev/debug nodes
enable-indexer = false          # true on RPC nodes that must serve eth_getTransactionByHash history
```

For `ignite chain serve`, put the same under `validators[].app` in `config.yml`:

```yaml
validators:
  - name: alice
    bonded: 1000000000000000000amychain
    app:
      json-rpc:
        enable: true
        address: "0.0.0.0:8545"
        ws-address: "0.0.0.0:8546"
        api: "eth,net,web3,txpool,debug"
      minimum-gas-prices: "10000000000amychain"   # 10 gwei-equivalent at 18 decimals
```

Or as start flags: `mychaind start --json-rpc.enable --json-rpc.api eth,net,web3`.

## Keys and addresses

One secp256k1 key = one 20-byte address, shown two ways:

```bash
mychaind keys add alice                       # eth_secp256k1 by default (cosmos/evm keyring); explicit: --algo eth_secp256k1 --coin-type 60
mychaind keys show alice -a                   # mychain1...
mychaind debug addr mychain1...               # prints hex 0x... and bech32 forms
mychaind keys unsafe-export-eth-key alice     # hex private key → MetaMask/Foundry (dev only)
mychaind keys unsafe-import-eth-key bob <hex-privkey>
```

`unsafe-*` print or ingest raw private keys — dev only, never on machines with real funds.

Key type must be `eth_secp256k1` for Ethereum txs. Keys created with plain `secp256k1` (pre-EVM keyring) derive different addresses and can't sign `MsgEthereumTx`.

## MetaMask

Add network: RPC URL `http://localhost:8545`, chain ID = `cast chain-id --rpc-url http://localhost:8545` (decimal), currency symbol = display denom, decimals 18. Import a dev key via `unsafe-export-eth-key`.

Changing EVM chain ID or wiping state → MetaMask keeps stale nonces: Settings → Advanced → Clear activity tab data.

## Foundry

```bash
export RPC=http://localhost:8545
export PK=$(mychaind keys unsafe-export-eth-key alice --keyring-backend test)
cast balance $(cast wallet address --private-key $PK) --rpc-url $RPC
forge init counter && cd counter
forge create src/Counter.sol:Counter --rpc-url $RPC --private-key $PK --broadcast
cast send <addr> "increment()" --rpc-url $RPC --private-key $PK
cast call <addr> "number()(uint256)" --rpc-url $RPC
forge script script/Deploy.s.sol --rpc-url $RPC --private-key $PK --broadcast
```

If Foundry complains about EIP-1559 fees, pass `--legacy` or check feemarket `no_base_fee` / `min_gas_price`.

## Hardhat

```js
// hardhat.config.js
module.exports = {
  solidity: "0.8.24",
  networks: {
    local: { url: "http://localhost:8545", chainId: <evm-chain-id>, accounts: [process.env.PK] },
  },
};
```

`npx hardhat run scripts/deploy.js --network local`

## Precompiles from Solidity

Static precompile addresses (Cosmos EVM docs, checked 2026-11-25):

| Precompile | Address |
|---|---|
| P256 (secp256r1 verify) | `0x0000000000000000000000000000000000000100` |
| Bech32 (hex ↔ bech32) | `0x0000000000000000000000000000000000000400` |
| Staking | `0x0000000000000000000000000000000000000800` |
| Distribution | `0x0000000000000000000000000000000000000801` |
| ICS20 (IBC transfer) | `0x0000000000000000000000000000000000000802` |
| Bank | `0x0000000000000000000000000000000000000804` |
| Governance | `0x0000000000000000000000000000000000000805` |
| Slashing | `0x0000000000000000000000000000000000000806` |
| ICS02 (IBC light client queries) | `0x0000000000000000000000000000000000000807` |

ERC20 token pairs and WERC20 use per-token addresses. Take the ABIs from cosmos/evm `precompiles/<name>/abi.json` for your version. Which precompiles are active is a chain setting, so check genesis `active_static_precompiles`.

## Smoke test checklist

- [ ] `cast chain-id` returns the intended EVM chain ID.
- [ ] Deploy + call a contract with Foundry.
- [ ] MetaMask transfer shows up in `mychaind q bank balances <bech32>`.
- [ ] Cosmos `tx bank send` shows up in `cast balance <0x>`.
- [ ] ERC20 representation of the native/IBC coin works (`mychaind q erc20 token-pairs`).
- [ ] `eth_estimateGas` and `eth_feeHistory` return sane values.
- [ ] Node restart → JSON-RPC comes back, nonces continue.
