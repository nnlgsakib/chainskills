# Randomness sources

Facts checked 2026-11-25 are marked ✔. Unmarked rows are protocol background.

| Source | Unpredictable to | Bias resistance | Liveness | Verification | Fits |
|---|---|---|---|---|---|
| Block hash / timestamp | nobody (the proposer knows it) | none: the proposer can grind or withhold | always | trivial | nothing of value |
| RANDAO / `prevrandao` (Ethereum) | others until reveal | the last proposer of a window can bias by withholding (losing the block reward); bias grows with consecutive slots controlled | always | on-chain opcode | low-value uses with lookahead. EIP-7917 (Fusaka) fixes the proposer schedule per epoch, but further epochs stay unpredictable ✔ |
| Commit-reveal among participants | everyone until reveals | the last revealer can withhold (bias of 1 bit per withholder) unless penalised | needs all or a threshold to reveal | hashes | small groups with bonds and non-reveal slashing |
| Per-proposer VRF (leader election) | everyone except the key holder for their own output | unbiasable per key | always | VRF proof | private leader election; each validator learns its own slots early |
| In-protocol threshold BLS beacon | everyone until t partial signatures combine | unbiasable if < t malicious (the signature is unique) | needs ≥ t validators online | one BLS signature check | sovereign chains: validators sign each round (e.g. in CometBFT vote extensions); needs a DKG and resharing on set changes |
| drand quicknet | everyone until the round is published | threshold BLS of the League of Entropy | external network | BLS12-381 signature; on-chain on EIP-2537 chains (future-drand contract) ✔; ~20% less gas than BN254 per drand ✔ | any chain that accepts the LoE trust assumption |
| drand evmnet | same | same | external | BN254 for chains without BLS12-381 precompiles ✔; LoE keeps it while there's interest ✔ | EVM chains without EIP-2537 |
| Oracle VRF (Chainlink VRF v2.5) | everyone until fulfilment | oracle can't bias (VRF proof) but can withhold or delay | depends on the oracle network | on-chain VRF proof check | contracts needing per-request randomness. v2.5 replaced V1/V2 on 29 Nov 2024; subscription or direct funding ✔ |
| VDF-based | everyone until computed | strong | compute delay | VDF proof | research-grade. No widely deployed standard; avoid unless you have specialists |

## Choosing
- Sovereign BFT chain where validators run the protocol: **in-protocol threshold beacon** (optionally mixed with drand).
- EVM chain or L2 contracts: **drand** (verify on-chain) or an **oracle VRF**. Mixing both removes reliance on either one's honesty but needs both to be live.
- A rollup without its own validators: **an external beacon or oracle VRF**.
- High-value lotteries: combine sources and add commit-reveal for user inputs.

## Trust and liveness notes
- An external beacon means the chain's random selection depends on that network's threshold honesty and uptime. Record it as a trust assumption (T-item) and define the fallback.
- A threshold beacon reduces liveness to the threshold. A stalled beacon must not stall consensus unless that's an explicit decision.

Sources: https://docs.drand.love/blog/2025/08/26/verifying-bls12-on-ethereum · https://github.com/future-drand · https://docs.chain.link/vrf · https://docs.chain.link/vrf/v2-5/overview/subscription · https://eips.ethereum.org/EIPS/eip-7917
