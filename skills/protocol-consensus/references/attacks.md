# Consensus attack review

For each attack, record either a mitigation in the spec or a K-risk in CHAIN.md.

| Attack | What happens | Mitigations |
|---|---|---|
| Equivocation (double sign) | A validator signs two conflicting blocks or votes | Evidence handling + slashing + tombstoning (protocol-staking-validators); remote signer with double-sign protection; never run two signers on one key |
| Long-range attack | Old keys with already-unbonded stake rewrite history for newly syncing nodes | Unbonding period longer than the weak-subjectivity window; checkpoints / trusted state sync; light clients reject headers older than the trusting period |
| Nothing-at-stake | Validators vote on many forks for free | Slashable conflicting votes (BFT), evidence windows ≥ unbonding period |
| > 1/3 offline (liveness) | BFT can't finalise and halts | Accept the halt (safety); geographic and provider diversity; downtime slashing/jailing; documented restart runbook |
| ≥ 1/3 Byzantine (safety) | Conflicting finalised blocks become possible | Economic security (stake at risk), concentration caps, monitoring of voting-power distribution |
| Proposer DoS | Attacker knows the next leader and floods it | Sentry topology, unpredictable leader election, fast round timeouts |
| Randomness grinding | Proposer biases leader or committee selection | VRF / threshold beacon (protocol-randomness), commit-reveal with penalties |
| Censorship by proposer/builder | Txs are excluded | Forced inclusion (rollups), inclusion lists (Ethereum FOCIL, EIP-7805, planned for Hegotá, ethereum.org lists Q2 2027 ✔), rotating proposers, encrypted mempools |
| Time manipulation | Proposer skews block time to affect time-based logic | BFT time (median of validator times), bounds on drift, avoid tight time-based logic |
| Eclipse / partition | Node or validator sees only attacker peers | Persistent trusted peers, peer diversity, peer scoring (protocol-p2p) |
| Bribery / cartel | Validators paid to reorder, censor or halt | Slashing for provable misbehaviour, decentralised stake, governance monitoring |
| Key compromise | Attacker signs as the validator | HSM/remote signer, key rotation (Cosmos SDK v0.55 `MsgRotateConsPubKey`: fee, one rotation per unbonding period, old address still slashable until the evidence age expires ✔) |
| Signature-size DoS (post-quantum keys) | Large signatures bloat blocks and votes | Budget block bytes; CometBFT v0.40 raised `MaxSignatureSize`/`MaxCommitSigBytes` for ML-DSA-65 ✔; IBC counterparties must support the key type first ✔ |

Sources (2026-11-25): https://docs.cosmos.network/sdk/latest/upgrade/v0.55 · https://ethereum.org/roadmap/hegota/
