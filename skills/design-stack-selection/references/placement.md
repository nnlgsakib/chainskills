# Component placement

## Surfaces

| Surface | What it is | Pick when | Avoid when |
|---|---|---|---|
| Native module / pallet | Code compiled into the chain's state machine | Consensus-critical, runs every block/epoch, needs privileged access (minting, validator updates), performance-sensitive | Logic changes weekly; third parties must extend it |
| Precompile | Native code exposed at a fixed address to a VM | Contracts need native functionality (staking, crypto, IBC) | The stack has no VM, or there's no need for contract access |
| System contract | Contract deployed at genesis with protocol privileges (block hooks, validator-set authority) | EVM-only stacks that need protocol logic (BSC-style staking, Avalanche ValidatorManager, L2 predeploys) | A native module is available and simpler |
| Smart contract | Ordinary deployed contract | App logic, composability, fast iteration, governance-upgradable via proxy | Must run every block or needs privileges the VM doesn't give |
| L1 contract | Contract on the settlement layer | Rollup bridge, proof verification, sequencer/validator registry secured by L1, forced inclusion | Logic that doesn't need L1 security (cost) |
| Off-chain service | Process run by operators (sequencer, prover, relayer, oracle, keeper, verifier) | Heavy compute, network/data work, anything not provable cheaply on-chain. Pair it with on-chain verification or challenges | It holds authority that isn't checked on-chain |
| Client logic | Node or wallet behaviour (sync, light-client checks, DA sampling, mempool policy) | Per-node behaviour that doesn't change consensus state | It changes consensus outcomes (then it belongs in the state machine) |

A single component often spans surfaces. For example, "community verification" might be an off-chain verifier service, plus a native module or contract that assigns tasks, takes commitments and pays rewards, plus a challenge contract. Put each part in its own placement row.

## What each stack supports natively

| Stack | Native module | Precompile | System contract | Smart contract | Off-chain services typical |
|---|---|---|---|---|---|
| Cosmos SDK | ✅ Go modules | with cosmos/evm | n/a (modules instead) | CosmWasm or EVM if added | relayers, oracles, price feeders |
| Cosmos EVM | ✅ | ✅ | possible (genesis contracts) | ✅ Solidity | + JSON-RPC nodes |
| Substrate | ✅ pallets | ✅ (Frontier) | n/a (pallets) | ink! / EVM | off-chain workers built in |
| Avalanche L1 (Subnet-EVM) | via custom VM only | ✅ stateful precompiles | ✅ ValidatorManager etc. | ✅ | ICM relayers |
| geth / reth fork | via client fork (hard to maintain) | ✅ via fork | ✅ (BSC-style) | ✅ | — |
| OP Stack | fork op-geth (high maintenance) | via op-geth fork | ✅ predeploys | ✅ | sequencer, batcher, proposer, challenger |
| Arbitrum Orbit | fork Nitro (high maintenance) | via Nitro fork | ✅ | ✅ + Stylus | sequencer, validators, batch poster |
| ZK Stack | fork (high maintenance) | limited | ✅ system contracts | ✅ | sequencer, prover |
| Custom | ✅ everything | if you build a VM | — | if you build a VM | anything |

## Common placements

| Component | Cosmos-like | EVM L1 | L2 rollup |
|---|---|---|---|
| Validator set / staking | native module | system contract (+ client hook) | L1 contract for sequencer/validator set, or none (single sequencer) |
| Rewards / distribution | native module | system contract | L2 contract funded by fees |
| Governance | native module | contracts (Governor + timelock) | L1 + L2 contracts (security council) |
| Randomness beacon | native module (vote extensions / VRF) | contract + off-chain VRF/beacon | contract + oracle |
| Verification layer (community nodes) | module (assign, commit, reward) + off-chain verifier | contracts + off-chain verifier | contracts + off-chain verifier |
| Data availability sampling | client logic + off-chain service | client logic | DA layer (external) + client logic |
| Bridge | IBC module / light-client module | contracts + relayers | native rollup bridge (L1 + L2 contracts) |
