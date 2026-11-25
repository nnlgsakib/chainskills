# Contract patterns

## Access control
- Use `AccessControl` (roles) or `AccessManager` (central permission manager) from OpenZeppelin. Give every privileged function a named role.
- For a single owner, use `Ownable2Step`, so a typo can't hand ownership to a wrong address.
- Separate roles: `DEFAULT_ADMIN` (held by timelock/governance), `PAUSER` (fast multisig, pause only), `OPERATOR` (keepers, bounded actions), `UPGRADER` (timelock).
- Every role holder is documented in `docs/deployments/<network>.md`.

## Upgradeability
| Choice | When |
|---|---|
| Immutable | Cores whose rules shouldn't change: often the safest option |
| UUPS (`UUPSUpgradeable`) | Default for upgradeable logic. Upgrade logic lives in the implementation, so `_authorizeUpgrade` must be restricted |
| Transparent proxy | When admin/user call separation is wanted; slightly more gas |
| Beacon | Many proxies share one implementation |

Rules:
- Storage in **ERC-7201 namespaced structs** (OpenZeppelin 5.x upgradeable contracts do this; Solidity 0.8.35+ has an `erc7201` builtin for computing slots; Foundry 1.10 lints collisions).
- Put `_disableInitializers()` in the implementation's constructor.
- Initialize at deployment, in the same transaction. OpenZeppelin 5.6+ `ERC1967Proxy`/`TransparentUpgradeableProxy` revert without initializer data.
- Validate storage layouts between versions (OpenZeppelin Upgrades plugins or `forge inspect ... storage-layout` diffs).
- The upgrade authority goes through a timelock longer than the users' exit time.

## Reentrancy and external calls
- Checks → effects → interactions.
- `ReentrancyGuard` / `ReentrancyGuardTransient` (transient storage, cheaper) on functions that make external calls or transfer tokens.
- Use `SafeERC20` for token transfers. Handle fee-on-transfer and rebasing tokens explicitly, or reject them.
- Prefer pull payments over pushing ETH in loops.
- Don't use `send`/`transfer` (deprecated for 0.9). Use `call` with checks and reentrancy protection.

## EIP-7702 (live since Pectra)
- `tx.origin == msg.sender` no longer proves "called by an EOA without code", and it isn't a reentrancy guard.
- `extcodesize`/`code.length == 0` can't tell EOAs from contracts. A delegated EOA has code.
- Design as if every caller might be a contract. Callbacks (ERC-721/1155 receivers) may now run on delegated EOAs.

## Arithmetic
- Solidity ≥ 0.8 checks overflow. Wrap code in `unchecked` only with a written proof.
- `Math.mulDiv(a, b, c, Math.Rounding.Floor/Ceil)`: round in the protocol's favour (down on payouts, up on charges).
- Vault/share systems: defend against first-depositor inflation (virtual shares/offset, as in OpenZeppelin ERC4626).
- Keep scaling factors explicit (`1e18`) and test decimal edge cases (tokens with 6 decimals).

## Pausing and emergency
- `Pausable` scoped to specific functions. Withdrawals ideally stay open during a pause.
- Pause authority is a fast multisig. Unpause and any other power goes to governance/timelock.
- Emergency powers have a sunset (timestamp/block after which they're disabled) where the design requires it.

## Rate limiting
OpenZeppelin 5.7 `RateLimiter` (token bucket / sliding window): use it for bridges, mints and withdrawals to cap the damage from an exploit.

## Oracles
- Use multiple sources or TWAPs and staleness checks. Never use a spot price from one AMM.
- Bound how much a price can move per update. Pause on deviation.

## Deployment
- Scripted (`forge script` / Hardhat Ignition), idempotent, and reviewed like code.
- Deterministic addresses: CREATE2/CREATE3 (OpenZeppelin 5.7 `Create3`).
- Transfer admin roles to the multisig/timelock and renounce the deployer's roles in the same script.
- Verify source on the explorer, and record addresses, commit, compiler settings and constructor args.
