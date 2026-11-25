# config.yml (development only)

Verified 2026-11-25 against the Ignite v29.10.1 configuration reference (`docs/docs/08-configuration`). `config.yml` drives `ignite chain serve` / `chain init` (v30: `ignite cosmos chain …`). It is **not** a launch genesis. Everything here is for local dev and CI.

```yaml
version: 1
validation: sovereign            # default; "consumer" = consumer chain (inherits provider validators)
default_denom: umychain          # default staking denom (default "stake")
build:
  main: cmd/mychaind
  binary: mychaind
  ldflags:
    - -X main.Version=dev
  proto:
    path: proto                  # if proto files live elsewhere
accounts:
  - name: alice
    coins: [20000000umychain, 200000000stake]
  - name: bob
    coins: [10000000umychain, 100000000stake]
    # mnemonic: "..."   # only demo mnemonics, never real keys; cannot be combined with `address`
    # address: mychain1...   # fixed address (no key created); not allowed for validator accounts
    # cointype: 60     # HD coin type (default 118)
client:
  openapi:
    path: docs/static/openapi.json
  typescript:
    path: ts-client
  composables:
    path: vue/src/composables
faucet:
  name: bob
  coins: [5umychain, 100000stake]
  coins_max: [100umychain, 1000000stake]   # per-address cap
  rate_limit_window: 3600                  # seconds before the cap resets
  port: 4500
validators:
  - name: alice
    bonded: 100000000stake
    app:                          # merged into app.toml
      minimum-gas-prices: "0.0025umychain"
      pruning: "nothing"
    config:                       # merged into config.toml
      consensus:
        timeout_commit: "1s"
    client:                       # merged into client.toml
      keyring-backend: test
    gentx:                        # gentx options for this validator
      commission-rate: "0.10"
      commission-max-rate: "0.20"
      commission-max-change-rate: "0.01"
      min-self-delegation: "1"
genesis:                          # deep-merged into genesis.json; chain_id set here persists across init/serve
  chain_id: mychain-local-1
  app_state:
    staking:
      params:
        bond_denom: stake
    gov:
      params:
        voting_period: "60s"      # short for local testing only
    bank:
      denom_metadata:
        - base: umychain
          display: mychain
          symbol: MYC
          denom_units:
            - { denom: umychain, exponent: 0 }
            - { denom: mychain, exponent: 6 }
include:                          # optional: merge other config files (paths or URLs)
  - accounts.yml
```

## Tips

- A short `voting_period` and `expedited_voting_period` let you test governance and upgrade proposals in minutes.
- Keep a second file (e.g. `config.ci.yml`) for CI and run it with `-c/--config config.ci.yml`.
- Changing `genesis:` or `accounts:` needs a state reset: `ignite chain serve -r`.
- `keyring-backend: test` stores keys unencrypted, which is acceptable only here.
- Without a `mnemonic`, accounts get a random one on every re-init, so their addresses change. Pin a demo mnemonic if tests depend on addresses.

Sources: https://github.com/ignite/cli/blob/v29.10.1/docs/docs/08-configuration/01-config.md · https://github.com/ignite/cli/blob/v29.10.1/docs/docs/08-configuration/02-config_example.md
