# Secure development lifecycle

## Dependencies
- Pin exact versions with lockfiles (`go.sum`, `Cargo.lock`, `package-lock.json`).
- Scan in CI: `govulncheck ./...` (Go), `cargo audit` (Rust), `npm audit` / `pnpm audit` (JS), and Slither/Aderyn for contracts.
- Generate an SBOM per release (e.g. CycloneDX or SPDX via syft) and keep it with the release.
- Review new dependencies: maintainer reputation, install scripts, transitive size. Prefer stdlib or existing dependencies.
- Subscribe to upstream advisories (CometBFT/Cosmos security advisories, framework security channels), with a written SLA for critical patches.

## CI/CD
- Pin third-party CI actions by commit SHA.
- No long-lived cloud or registry secrets in CI. Use OIDC federation.
- Protected branches, required reviews, required checks (tests, linters, scanners).
- Separate build and release roles. Releases come only from tagged commits on protected branches.

## Releases
- Reproducible builds (`-trimpath`, pinned toolchains, deterministic flags). Independent rebuild verification for consensus binaries.
- Signed artifacts and checksums (sigstore/cosign or GPG). Publish them in the release notes and verify them in deployment scripts.
- Upgrade binaries for chain upgrades include checksums in the governance proposal (e.g. Cosmovisor `info` JSON).

## Frontends and RPC
- Subresource integrity for scripts, a strict Content-Security-Policy, and no third-party scripts on signing pages.
- Immutable deployments (content-addressed, e.g. IPFS with pinned hashes) as an alternative access path.
- DNS: registrar lock, DNSSEC, monitoring for record changes.
- Wallet connection libraries pinned and reviewed. Show human-readable transaction intent.

## Workstations
- Hardened, dedicated devices for anyone with production or signing access.
- Open untrusted repositories, interview tasks and attachments only in disposable VMs or containers.
- Hardware security keys for all accounts (code hosting, cloud, registrar, email).
- Least privilege, with access reviewed quarterly.
