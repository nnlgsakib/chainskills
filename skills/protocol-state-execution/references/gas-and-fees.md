# Gas and fees

## Pricing method

1. **List resources**: CPU, state reads, state writes, new state (growth), bandwidth (tx bytes), signature/proof verification, events/logs, cross-chain messages.
2. **Benchmark** each operation on the reference validator hardware from R-N, single-threaded, worst case (cold caches, max input sizes).
3. **Set a target block budget**: how much of the block interval execution may use. Leave headroom for consensus, gossip and disk flush (often ≤ 30–50% of the block time).
4. **Price**: `gas(op) = ceil(cost(op) / cost(unit)) × margin`. A margin of 1.2–2 covers hardware variance. Price worst cases, not averages.
5. **Cap**: a per-tx gas limit (Ethereum added 2^24 in Fusaka ✔, which bounds the worst single-tx time), a per-block gas limit, and maximum sizes for txs, events and calldata.
6. **Re-benchmark** each release. Mispriced operations are DoS vectors.

## Multi-dimensional fees

Single-number gas mixes resources with very different scarcity. Consider separate prices or limits for: execution, state growth, data (calldata/blobs), and proofs. Ethereum already prices blob data separately (EIP-4844 and the Fusaka blob changes).

## Fee market

| Model | Behaviour | Notes |
|---|---|---|
| First-price auction | users bid, the proposer picks | poor UX, overpaying |
| EIP-1559-style | protocol base fee adjusts to a target utilisation; priority tip to the proposer; base fee burned or redistributed | standard choice. Parameters: target, max change per block, minimum base fee |
| Fixed / subsidised | constant fee or paid by a sponsor/paymaster | needs another anti-spam mechanism |
| Fees in multiple tokens | pay in IBC/ERC20 tokens converted via an oracle or AMM | oracle risk (see the fee-abstraction pattern) |

Decide where fees go (burn, validators, treasury, other roles) together with `protocol-tokenomics`.

## Storage costs
- A **deposit** per stored byte or object, refunded on deletion, is simplest and fair.
- **Rent** charges continuously. It's complex for users and needs eviction logic.
- **Expiry** archives inactive state, which needs a resurrection-proof mechanism.

Sources: https://blog.ethereum.org/2025/10/21/fusaka-gascap-update · https://ethereum.org/roadmap/fusaka/
