# Placement map — Move (Sui / Aptos)

Levels: `native` (built in), `extend` (built in, needs configuration or extension), `custom` (you write it), `n/a`.

| Concept | Level | Where in this stack | How to implement / notes |
|---|---|---|---|
| consensus | native | the platform's validator set (Sui / Aptos) | Relevant for finality assumptions only |
| state-execution | native | MoveVM; Sui objects (owned/shared), Aptos resources and objects | Resource safety; Sui shared-object versioning |
| staking-validators | custom | app-level staking modules | Native validator staking belongs to the platform |
| rollup | n/a | — | — |
| tokenomics | extend | coin / fungible-asset standards in the framework | Treasury caps and mint capabilities in multisig |
| governance | extend | capability objects, multisig, custom upgrade policies (Sui) | Restrict upgrade policies one-way as the protocol matures |
| randomness | custom | platform randomness APIs (verify availability) or oracles | protocol-randomness |
| verifiable-participation | custom | Move modules + off-chain operators | — |
| data-availability | n/a | — | — |
| p2p | n/a | — | — |
| interop | custom | bridges (platform-native or third-party) | Top-risk component |
| smart-contracts | native | Move packages (Sui edition 2024; Aptos Move) | This adapter |
| node-software | native | Sui CLI (suiup) and localnet; Aptos CLI and `run-local-testnet` | Pin mainnet tags |
| upgrades | native | Sui `UpgradeCap` + policies; Aptos package upgrade policy | One-way restrictions; digest verification |
