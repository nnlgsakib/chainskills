#!/usr/bin/env python3
"""Deterministic token supply / issuance / reward-split projection (baseline model).

Use it to sanity-check a monetary policy before agent-based simulation (cadCAD, radCAD, Mesa).
It is an off-chain planning model, not consensus code.

Usage:
    python3 emission_sim.py config.json            # prints a yearly table
    python3 emission_sim.py config.json --csv out.csv
    python3 emission_sim.py --example > config.json
    python3 emission_sim.py --selftest

Config (JSON; the # comments below are explanations only, generate a valid file with --example):
{
  "years": 10,
  "initial_supply": 1000000000,
  "max_supply": null,                         # optional hard cap
  "issuance": {"model": "disinflation",       # "disinflation" | "staking-target" | "fixed-amount"
               "initial_rate": 0.08, "decay": 0.15, "terminal_rate": 0.015,
               # staking-target: "target_bonded": 0.67, "min_rate": 0.07, "max_rate": 0.20,
               #                 "max_change_per_year": 0.13, "initial_rate": 0.10
               # fixed-amount:   "amount_per_year": 50000000
              },
  "bonded_ratio": [0.5, 0.55, 0.6],          # per year; last value repeats
  "fees_per_year": [1000000, 2000000],        # tokens; last value repeats
  "fee_burn_fraction": 0.5,                   # rest of fees joins the reward pool
  "split": {"validators": 0.50, "delegators": 0.25, "community_services": 0.15, "reserve": 0.10},
  "staker_roles": ["validators", "delegators"]   # roles whose rewards count toward staking yield
}
"""
import csv
import json
import sys

EXAMPLE = {
    "years": 10,
    "initial_supply": 1_000_000_000,
    "max_supply": None,
    "issuance": {"model": "disinflation", "initial_rate": 0.08, "decay": 0.15, "terminal_rate": 0.015},
    "bonded_ratio": [0.5, 0.55, 0.6, 0.65],
    "fees_per_year": [1_000_000, 3_000_000, 6_000_000],
    "fee_burn_fraction": 0.5,
    "split": {"validators": 0.50, "delegators": 0.25, "community_services": 0.15, "reserve": 0.10},
    "staker_roles": ["validators", "delegators"],
}


def at(seq, i):
    return seq[min(i, len(seq) - 1)] if isinstance(seq, list) else seq


def validate(cfg):
    split = cfg["split"]
    total = sum(split.values())
    if abs(total - 1) > 1e-9:
        raise ValueError(f"split must sum to 1, got {total}")
    if any(v < 0 for v in split.values()):
        raise ValueError("split fractions must be >= 0")
    if not 0 <= cfg.get("fee_burn_fraction", 0) <= 1:
        raise ValueError("fee_burn_fraction must be in [0,1]")
    for r in cfg.get("staker_roles", []):
        if r not in split:
            raise ValueError(f"staker role '{r}' not in split")
    b = cfg["bonded_ratio"]
    if any(not 0 < x <= 1 for x in (b if isinstance(b, list) else [b])):
        raise ValueError("bonded_ratio values must be in (0,1]")


def rate_for_year(iss, year, prev_rate, bonded):
    m = iss["model"]
    if m == "disinflation":
        return max(iss["terminal_rate"], iss["initial_rate"] * (1 - iss["decay"]) ** year)
    if m == "staking-target":
        if year == 0:
            r = iss["initial_rate"]
        else:
            # Cosmos-style: move rate toward max when under-bonded, toward min when over-bonded
            step = (1 - bonded / iss["target_bonded"]) * iss["max_change_per_year"]
            r = prev_rate + step
        return min(iss["max_rate"], max(iss["min_rate"], r))
    if m == "fixed-amount":
        return None
    raise ValueError(f"unknown issuance model {m}")


def simulate(cfg):
    validate(cfg)
    supply = float(cfg["initial_supply"])
    cap = cfg.get("max_supply")
    iss = cfg["issuance"]
    rows, prev_rate = [], None
    for y in range(cfg["years"]):
        bonded = at(cfg["bonded_ratio"], y)
        rate = rate_for_year(iss, y, prev_rate, bonded)
        issued = iss["amount_per_year"] if rate is None else supply * rate
        if cap is not None:
            issued = max(0.0, min(issued, cap - supply))
        fees = float(at(cfg["fees_per_year"], y))
        burned = fees * cfg.get("fee_burn_fraction", 0)
        pool = issued + fees - burned
        per_role = {r: pool * f for r, f in cfg["split"].items()}
        staked = supply * bonded
        staker_income = sum(per_role[r] for r in cfg.get("staker_roles", []))
        nominal_yield = staker_income / staked if staked else 0.0
        new_supply = supply + issued - burned
        net_inflation = (new_supply - supply) / supply
        rows.append({
            "year": y + 1, "supply_start": supply, "issuance_rate": issued / supply, "issued": issued,
            "fees": fees, "burned": burned, "net_inflation": net_inflation, "bonded_ratio": bonded,
            "staking_yield_nominal": nominal_yield, "staking_yield_real": nominal_yield - net_inflation,
            **{f"to_{r}": v for r, v in per_role.items()},
        })
        if new_supply < 0:
            raise ValueError(f"supply went negative in year {y + 1}")
        supply, prev_rate = new_supply, (issued / rows[-1]["supply_start"])
    return rows


def print_table(rows):
    cols = ["year", "supply_start", "issued", "burned", "net_inflation", "bonded_ratio",
            "staking_yield_nominal", "staking_yield_real"]
    print(" | ".join(f"{c:>21}" for c in cols))
    for r in rows:
        out = []
        for c in cols:
            v = r[c]
            out.append(f"{v:>21.2%}" if c in ("net_inflation", "bonded_ratio", "staking_yield_nominal", "staking_yield_real")
                       else f"{v:>21,.0f}")
        print(" | ".join(out))
    roles = [k for k in rows[0] if k.startswith("to_")]
    print("\nyear-1 reward pool split: " + ", ".join(f"{k[3:]}={rows[0][k]:,.0f}" for k in roles))


def selftest():
    rows = simulate(EXAMPLE)
    assert len(rows) == 10
    assert abs(rows[0]["issuance_rate"] - 0.08) < 1e-12
    assert all(r["issuance_rate"] >= 0.015 - 1e-12 for r in rows)        # terminal floor holds
    pool0 = rows[0]["issued"] + rows[0]["fees"] - rows[0]["burned"]
    assert abs(sum(v for k, v in rows[0].items() if k.startswith("to_")) - pool0) < 1e-3  # split conserves pool
    capped = dict(EXAMPLE, max_supply=1_050_000_000, fee_burn_fraction=0)
    assert rows_supply_end(simulate(capped)) <= 1_050_000_000 + 1e-6      # hard cap respected
    st = dict(EXAMPLE, issuance={"model": "staking-target", "initial_rate": 0.10, "target_bonded": 0.67,
                                 "min_rate": 0.07, "max_rate": 0.20, "max_change_per_year": 0.13})
    r2 = simulate(st)
    assert all(0.07 - 1e-12 <= r["issuance_rate"] <= 0.20 + 1e-12 for r in r2)
    assert r2[1]["issuance_rate"] > r2[0]["issuance_rate"]               # under-bonded -> rate rises
    try:
        simulate(dict(EXAMPLE, split={"validators": 0.6, "delegators": 0.6}))
        raise AssertionError("bad split accepted")
    except ValueError:
        pass
    print("selftest ok")


def rows_supply_end(rows):
    r = rows[-1]
    return r["supply_start"] + r["issued"] - r["burned"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
    elif sys.argv[1] == "--example":
        print(json.dumps(EXAMPLE, indent=2))
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            rows = simulate(json.load(f))
        print_table(rows)
        if "--csv" in sys.argv:
            path = sys.argv[sys.argv.index("--csv") + 1]
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            print(f"\nwrote {path}")
