# Architecture classes

## The ladder — climb only as far as requirements force

1. **Contracts on an existing chain** (Ethereum, an L2, Solana, a Cosmos chain with CosmWasm/EVM).
   Enough when: logic fits a VM, the host's throughput/fees/finality are acceptable, no custom consensus or validator roles are needed.
   Breaks when: you need custom consensus, your own validator roles, native fee/gas policy, or the host's limits.
2. **Rollup / L2 (or L3)** on an existing settlement layer.
   Enough when: you need your own execution environment, fee policy and throughput, but can inherit security from the settlement layer; a sequencer model is acceptable.
   Breaks when: you need your own validator set as a product feature, BFT finality independent of L1, or custom consensus roles.
3. **Appchain with shared/borrowed security** (Polkadot parachain, Cosmos ICS consumer chain, restaking-secured chain, Avalanche L1 with chosen validators).
   Enough when: you need sovereignty over the state machine and validators matter, but bootstrapping a full independent security budget is too expensive.
   Breaks when: the security provider's terms, cost or validator set don't fit.
4. **Sovereign L1** with its own validator set and token-secured consensus.
   Needed when: your own validator/participant roles are core to the product, or independence from any other chain is a hard requirement.
   Cost: you must bootstrap and pay for security (token value × staked share), run a validator ecosystem, and own every layer.

Also consider:
- **Permissioned / consortium chain** (known validators, often PoA/QBFT): when participants are known organisations and openness isn't a goal.
- **Sovereign rollup** (posts data to a DA layer, settles itself): own fork-choice and upgrades without a settlement contract.
- **Validium / optimium**: rollup with off-chain DA — cheaper, weaker exit guarantees.

## Comparison

| Class | Who secures it | Finality | Exit / safety guarantee | Sovereignty | Cost to secure | Ops burden |
|---|---|---|---|---|---|---|
| Contracts on host | host chain | host's | host's | low | none | low |
| Optimistic rollup | settlement L1 + 1-of-N honest verifier | soft: sequencer; hard: after challenge window (days) | can exit via L1 if DA + proofs work | medium | DA + settlement fees | medium (sequencer, provers optional) |
| ZK rollup | settlement L1 + proof validity | after proof verified on L1 (minutes–hours) | strongest of L2s | medium | proving + DA + settlement | high (provers) |
| Validium / optimium | above + DA committee | as above | depends on DA committee | medium | lower | medium |
| Sovereign rollup | its own nodes + DA layer | its own rules | social / fork choice | high | DA fees | medium |
| Shared-security appchain | provider's validators | provider's (often BFT) | provider-dependent | high | fee/rent to provider | medium |
| Sovereign PoS L1 | own staked validators | own (BFT: 1 block) | own | full | staking rewards (inflation/fees) | high |
| Permissioned chain | known operators | BFT | legal agreements | full (consortium) | low | medium |

## Hybrid designs

Many ideas combine classes, e.g. "BFT core validators + permissionless community nodes doing verification/DA". Treat the extra roles as **separate components layered on a standard class**, not as a new consensus. The core class should be fully safe without the extra layer; the extra layer adds verification, data availability or decentralisation on top, and its failure must not halt the chain.
