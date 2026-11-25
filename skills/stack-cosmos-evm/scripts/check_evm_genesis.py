#!/usr/bin/env python3
"""Sanity-check a cosmos/evm chain genesis.json for launch-breaking mistakes.

Usage:
    python3 check_evm_genesis.py <genesis.json>
    python3 check_evm_genesis.py --selftest

Prints ERROR / WARN / INFO lines. Exit 1 if any ERROR.
Field names follow cosmos/evm v0.6 (module "evm"); missing optional fields are skipped.
Note: replay protection is a node setting ([json-rpc] allow-unprotected-txs in app.toml), checked here only if a genesis param exists.
"""
import json
import sys


def check(g):
    out = []
    err = lambda m: out.append(("ERROR", m))
    warn = lambda m: out.append(("WARN", m))
    info = lambda m: out.append(("INFO", m))

    app = g.get("app_state", {})
    if not g.get("chain_id"):
        err("chain_id missing")

    evm_params = app.get("evm", {}).get("params", {})
    denom = evm_params.get("evm_denom")
    if not denom:
        err("app_state.evm.params.evm_denom missing")
    elif denom == "stake":
        warn("evm_denom is 'stake' (scaffold default) — set your real base denom")

    # bank metadata for the EVM denom
    metas = app.get("bank", {}).get("denom_metadata", []) or []
    meta = next((m for m in metas if m.get("base") == denom), None)
    if denom and not meta:
        err(f"no bank denom_metadata with base '{denom}'")
    elif meta:
        units = meta.get("denom_units", []) or []
        names = [u.get("denom") for u in units]
        if len(names) != len(set(names)):
            err(f"denom_metadata '{denom}' has duplicate unit names {names} (ignite evm init does this for non-'u' denoms)")
        if not any(int(u.get("exponent", 0)) == 18 for u in units):
            err(f"denom_metadata '{denom}' has no unit with exponent 18")
        if meta.get("display") not in names:
            err(f"display '{meta.get('display')}' is not one of the units {names}")
        if not meta.get("symbol"):
            warn(f"denom_metadata '{denom}' has no symbol")

    # consensus block gas limit
    cons = (g.get("consensus") or {}).get("params") or g.get("consensus_params") or {}
    max_gas = (cons.get("block") or {}).get("max_gas")
    if max_gas is None:
        warn("consensus block.max_gas not found")
    elif int(max_gas) <= 0:
        err(f"consensus block.max_gas is {max_gas} — EVM chains need a finite block gas limit")

    if evm_params.get("allow_unprotected_txs") is True:
        err("allow_unprotected_txs=true — disables EIP-155 replay protection")

    fm = app.get("feemarket", {}).get("params", {})
    if fm.get("no_base_fee") is True:
        warn("feemarket no_base_fee=true — EIP-1559 base fee disabled")

    bond = app.get("staking", {}).get("params", {}).get("bond_denom")
    if denom and bond and bond != denom:
        warn(f"staking bond_denom '{bond}' differs from evm_denom '{denom}' (fine only if intentional)")

    pcs = evm_params.get("active_static_precompiles")
    if pcs is not None:
        info(f"{len(pcs)} active static precompile(s): {', '.join(pcs) or 'none'} — keep only what you need")
    return out


def selftest():
    good = {
        "chain_id": "mychain-1",
        "consensus": {"params": {"block": {"max_gas": "100000000"}}},
        "app_state": {
            "evm": {"params": {"evm_denom": "amychain", "active_static_precompiles": []}},
            "bank": {"denom_metadata": [{
                "base": "amychain", "display": "mychain", "symbol": "MYC",
                "denom_units": [{"denom": "amychain", "exponent": 0}, {"denom": "mychain", "exponent": 18}],
            }]},
            "staking": {"params": {"bond_denom": "amychain"}},
            "feemarket": {"params": {"no_base_fee": False}},
        },
    }
    assert not [l for l, _ in check(good) if l != "INFO"], check(good)

    bad = json.loads(json.dumps(good))
    bad["consensus"]["params"]["block"]["max_gas"] = "-1"
    bad["app_state"]["bank"]["denom_metadata"][0]["denom_units"][1]["denom"] = "amychain"
    bad["app_state"]["evm"]["params"]["allow_unprotected_txs"] = True
    errors = [m for l, m in check(bad) if l == "ERROR"]
    assert len(errors) == 4, errors  # max_gas, duplicate units, display not a unit, unprotected txs
    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
        sys.exit(0)
    with open(sys.argv[1], encoding="utf-8") as f:
        results = check(json.load(f))
    for level, msg in results:
        print(f"{level}: {msg}")
    if not results:
        print("OK")
    sys.exit(1 if any(l == "ERROR" for l, _ in results) else 0)
