# Placement map — OP Stack

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | extend | single sequencer (op-node + op-reth); op-conductor (Raft) for HA sequencing | The L2 has no BFT validator set. Safety comes from L1 + fault proofs, liveness from the sequencer, and censorship resistance from L1 forced inclusion (deposits). Shared or based sequencing isn't standard |
| state-execution | native | EVM via op-reth (op-geth end-of-support) | Track OP hardforks for EVM changes. Custom precompiles require forking op-reth **and** kona (proof program) |
| staking-validators | custom | — | No native staking. Sequencer/operator sets or app staking are contracts (`build-smart-contracts`), optionally secured on L1 |
| rollup | native | op-deployer + op-contracts (OptimismPortal, L2OutputOracle/DisputeGameFactory, SystemConfig, bridges); op-batcher, op-proposer, op-challenger | Fault proofs (Kona-based, super-root games for interop); ZK dispute games via OP Succinct |
| tokenomics | extend | fee vaults (sequencer, base, L1 fees), custom gas token option | Fee routing and revenue share are configuration plus contracts. Superchain membership has revenue-share terms, so check current terms |
| governance | extend | L1 ProxyAdmin owner, Guardian, Security Council multisigs; L2 contracts for app governance | Stage targets dictate council size, threshold and upgrade delays (protocol-rollup/stages.md) |
| randomness | custom | contracts + oracle/beacon (drand, VRF) | `prevrandao` on L2 is sequencer-controlled. Never use it for value |
| verifiable-participation | custom | contracts + off-chain operators | Pattern from protocol-verifiable-participation, implemented as L2 or L1 contracts |
| data-availability | native | Ethereum blobs (default); Alt-DA mode with a DA server | Alt-DA weakens exit guarantees. Document the trust assumption |
| p2p | native | op-node libp2p gossip for unsafe blocks; tx pool gossip | Keep the sequencer behind replicas and a proxy (best practices) |
| interop | native | standard bridge (L1↔L2), Superchain interop (op-supernode, shared dispute games) | Third-party bridges are app-level contracts |
| smart-contracts | native | Solidity/Vyper on L2 (EVM-equivalent) | `build-smart-contracts`. Set `evm_version` to the chain's active fork |
| node-software | native | op-node, op-reth, op-batcher, op-proposer, op-challenger, op-dispute-mon, op-conductor, op-supernode, kona-node | Pin versions per component tag |
| upgrades | native | op-deployer upgrade flow, OPCM (OP Contracts Manager), hardfork activations via node releases | Follow docs.optimism.io notices. Stagger node rollouts |
