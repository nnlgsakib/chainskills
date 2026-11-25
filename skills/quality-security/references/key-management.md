# Key management

Facts checked 2026-11-25 are marked ✔.

## Inventory (`docs/security/key-inventory.md`)

| Key | Type / scheme | Can do | Holder | Custody | Rotation | Revocation | Compromise detection |
|---|---|---|---|---|---|---|---|
| Validator consensus key | ed25519 / secp256k1eth / ML-DSA-65 | sign blocks and votes | operator | remote signer + HSM/KMS | protocol key rotation if supported | rotate + tombstone risk | equivocation monitor |
| Validator operator key | account key | edit validator, withdraw rewards | operator | hardware wallet / multisig | manual | — | tx monitor |
| Node P2P key | ed25519 | peer identity | node | file on node (low value) | on rebuild | — | — |
| Multisig signer keys | secp256k1 etc. | treasury, upgrades, council actions | members | hardware wallets, separate devices | membership change | remove signer | unexpected tx proposals |
| Deployer key | account | deploy contracts (should hold no lasting power) | team | hardware wallet; drain/renounce after deploy | per deploy | renounce roles | role-change monitor |
| Oracle / relayer / keeper hot keys | account | submit data, relay | services | KMS with spending limits | scheduled | revoke role | anomaly alerts |
| Release signing key | GPG / sigstore | sign binaries | release managers | HSM / keyless (OIDC) | yearly | revoke + re-sign | transparency log |

## Validator keys (CometBFT-based chains)
- Use remote signing via privval (`priv_validator_laddr`): the node holds no secrets ✔.
- **Cosmos-KMS** (github.com/cosmos/kms, v0.1.0 released 27 Jul 2026) is recommended by the Cosmos docs over older signers ✔.
  - Backends: file (dev only), PKCS#11 HSM, AWS KMS.
  - Outbound-only connections: `tcp://` SecretConnection, or `noise://` with mutual peer pinning.
  - Signs ed25519, secp256k1eth and ML-DSA-65 over privval.
  - Double-sign protection is a per-key last-signed state, so never run two signers for one key. Connect one signer to several nodes instead ✔.
- **Horcrux**: an MPC/threshold Ed25519 signer cluster, e.g. 3 signers with threshold 2, or 5 with 3 ✔. It removes the single signer host but adds operational complexity. Key material outside the service is the operator's responsibility ✔.
- **TMKMS**: the older single-instance KMS; migrate per the Cosmos guide ✔.
- Rotation: Cosmos SDK v0.55 `MsgRotateConsPubKey` (fee, one rotation per unbonding period) ✔.
- Never restore `priv_validator_state.json` from an old backup.

## Multisig and signing hygiene (Bybit, Feb 2025: ~$1.4–1.5B)
What happened: attackers compromised the Safe{Wallet} signing frontend used by all signers. The hardware wallets showed only raw data or hashes (blind signing), and the wallet allowed `delegatecall`, so the implementation could be swapped ✔.
- **Clear signing**: signers see decoded intent on the hardware device. If they can't, they verify the hash and calldata independently on a separate machine and tool.
- **Independent verification**: two different tools or UIs, and a second person decodes every transaction before signing.
- **Restrict the wallet**: disable `delegatecall` and module changes unless needed. Use guards that allowlist targets and functions.
- **Separate devices** for signing; no browsing or email on them.
- **Timelock** large or rare operations, and monitor queued transactions.
- **Drills**: rotate signers, test the recovery procedure, keep a signer roster with backups.

## People and devices
Targeted social engineering (fake recruiters, malicious repos, packages and calendar links) is a leading path to key theft. Use dedicated hardened devices for privileged work, run untrusted code only in VMs or containers, and use hardware 2FA everywhere.

Sources: https://docs.cosmos.network/sdk/latest/kms/remote-signing.md · https://github.com/cosmos/kms · https://docs.cosmos.network/sdk/latest/kms/migrate-from-tmkms · https://github.com/strangelove-ventures/horcrux · https://blog.trailofbits.com/2025/02/25/how-threat-modeling-could-have-prevented-the-1.5b-bybit-hack/ · https://www.nccgroup.com/research/in-depth-technical-analysis-of-the-bybit-hack/
