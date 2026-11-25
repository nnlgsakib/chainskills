# Deploying and operating an Arbitrum chain

From docs.arbitrum.io "launch-arbitrum-chain" pages and the chain SDK README (read 2026-11-25).

## Deployment sequence
1. **Pick the type**: Rollup or AnyTrust. **Pick the gas token**: ETH or a standard ERC-20.
2. **Custom genesis** (if you need predeploys, balances or storage at genesis): generate it with the chain SDK's Docker image (`generateGenesis` CLI command; not in the npm package).
3. **RollupCreator** (via the chain SDK) deploys the core contracts: Rollup, SequencerInbox, delayed Inbox, Outbox, Bridge. Set `confirmPeriodBlocks`, validators, batch posters, the owner, and the BoLD configuration here.
4. **Node configuration**: generate it from the deployment, then run the sequencer, batch poster, validator(s) and RPC nodes.
5. **TokenBridgeCreator**, after step 3. It takes the inbox (the SDK resolves it from the rollup address), sends retryables, and needs child-chain gas (with a custom gas token, grant an allowance first).

Factory addresses for each parent chain: docs "Canonical factory contracts".

## Validation (BoLD)
- BoLD is the dispute protocol with bounded dispute time and better delay-attack resistance.
- Docs recommendation: adopt BoLD but **keep validation permissioned** unless you accept the risks of open validation.
- Existing chains adopting BoLD need a Nitro upgrade plus new rollup contracts. The docs provide an upgrade playbook for multisig and Security Council chains.
- Bonds and validator configuration: docs "Bond and validator configurations".

## Challenge period
- Default about one week: `confirmPeriodBlocks` ≈ **45,818 L1 blocks** for chains settling to Ethereum or an Arbitrum chain. Extra challenge buffer: **200 blocks (~40 min)**.
- For L3s, the period is measured in L1 block progression.
- A shorter period means faster withdrawals and less time to respond. Never go below what your validators and monitoring can reliably meet. Rollup Stages require ≥ 5 days for Stage 1 (`protocol-rollup/references/stages.md`).

## Costs and licensing
- Fee parameters: L2 base fee, gas target, dynamic pricing, parent-chain data fee pricing (ArbOwner), priority fees (ArbOS 61).
- **AEP**: chains settling outside Arbitrum One/Nova pay **10% of Protocol Net Revenue** to the Arbitrum Foundation (2% of new-chain revenue funds the Developer Guild). Compliance is tracked through the **AEP fee router** contracts.

## Operations checklist
- [ ] Sequencer, batch poster and validator keys in HSM/KMS. Owner = multisig/Security Council with timelock (UpgradeExecutor).
- [ ] Batch poster posting blobs (Ethereum-settled), with fee tuning and balance alerts.
- [ ] At least one honest validator always online. Assertion and challenge monitoring with alerts.
- [ ] RPC/archive nodes separate from the sequencer. Sequencer feed relays.
- [ ] ArbOS upgrade runbook: node version first, then schedule the activation.
- [ ] Exchange-integration checklist for deposits and withdrawals (docs provide a version-pinned one).
