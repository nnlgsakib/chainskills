# Transaction ordering, MEV and censorship resistance

## Decisions to make

| Decision | Options | Consequences |
|---|---|---|
| Mempool visibility | public / private RPCs / encrypted (threshold-decrypted after ordering) | Public mempools invite front-running. Encrypted ones add latency and complexity |
| Who builds blocks | proposer builds / out-of-protocol builders (MEV-boost style) / in-protocol PBS | Ethereum moves PBS in-protocol with ePBS (EIP-7732, Glamsterdam, expected Q4 2026 per ethereum.org ✔) |
| Ordering rule | fee priority / first-come-first-served / auctions for priority / fair-ordering protocols | Arbitrum's Timeboost express-lane auction launched Apr 2025 ✔. A Jun 2026 report says per-tx priority auctions replaced it (unverified) |
| Inclusion guarantee | none / forced inclusion via another layer / inclusion lists | Ethereum FOCIL (EIP-7805) is the Hegotá headliner, expected Q2 2027 ✔. Rollups need L1 forced inclusion (protocol-rollup) |
| MEV revenue | proposer keeps / burned / redistributed to users or the treasury | Feed into protocol-tokenomics |
| App-specific ordering | ABCI++ PrepareProposal/ProcessProposal (CometBFT), custom block builders | Must be deterministic and verifiable by all validators in ProcessProposal |

## Rules
- Anything validators must agree on (an ordering rule, an inclusion rule) is checked in block validation. Otherwise it's only a recommendation.
- An ordering policy that pays the proposer more than honest behaviour does will be gamed. Model the incentives.
- Users of value-moving operations (swaps, liquidations, auctions) need slippage limits and deadlines whatever the ordering policy.

Sources (2026-11-25): https://ethereum.org/roadmap/glamsterdam/ · https://ethereum.org/roadmap/hegota/ · https://www.theblock.co/post/361058/arbitrum-timeboost-fees · https://cryptobriefing.com/arbitrum-priority-gas-auctions-replace-timeboost/
