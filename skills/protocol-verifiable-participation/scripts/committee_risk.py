#!/usr/bin/env python3
"""Size verifier committees and penalties.

  committee   P(a randomly sampled committee has >= t malicious members)
              python3 committee_risk.py committee --nodes 1000 --malicious 0.2 --size 32 --threshold 11
              python3 committee_risk.py committee --nodes 1000 --malicious 0.2 --threshold-frac 0.334 --target 1e-9
              (with --target and no --size: smallest committee size meeting the target)
  deterrence  minimum penalty so cheating is unprofitable:  penalty * P(detect) > gain
              python3 committee_risk.py deterrence --gain 10 --audit-rate 0.05 --tasks 20
  selftest    python3 committee_risk.py selftest

Sampling without replacement (hypergeometric). Assumes uniform sampling over node
identities; for stake-weighted sampling, use stake units as "nodes" (approximation).
Stdlib only, exact integer arithmetic.
"""
import argparse
import math
import sys
from fractions import Fraction


def hypergeom_tail(N, K, n, t):
    """P(X >= t) for X ~ Hypergeometric(N population, K successes, n draws). Exact."""
    if n > N or K > N:
        raise ValueError("n and K must be <= N")
    total = math.comb(N, n)
    s = sum(math.comb(K, x) * math.comb(N - K, n - x) for x in range(max(t, 0), min(K, n) + 1))
    return Fraction(s, total)


def committee(nodes, malicious_frac, size, threshold):
    K = int(math.floor(nodes * malicious_frac))
    return hypergeom_tail(nodes, K, size, threshold)


def threshold_for(size, frac):
    return max(1, math.ceil(size * frac))


def smallest_size(nodes, malicious_frac, threshold_frac, target, max_size=None):
    max_size = max_size or nodes
    for k in range(1, max_size + 1):
        p = committee(nodes, malicious_frac, k, threshold_for(k, threshold_frac))
        if p <= target:
            return k, p
    return None, None


def detection_probability(audit_rate, tasks):
    """P(at least one of `tasks` faked tasks is audited) with independent audits."""
    return 1 - (1 - audit_rate) ** tasks


def min_penalty(gain, audit_rate, tasks):
    q = detection_probability(audit_rate, tasks)
    if q <= 0:
        return math.inf, q
    return gain / q, q


def selftest():
    # Tiny exact case: N=4, K=2, n=2 -> P(X>=1) = 1 - C(2,2)/C(4,2) = 1 - 1/6 = 5/6
    assert hypergeom_tail(4, 2, 2, 1) == Fraction(5, 6)
    assert hypergeom_tail(4, 2, 2, 3) == 0
    # Committee = whole population: deterministic
    assert committee(10, 0.3, 10, 3) == 1 and committee(10, 0.3, 10, 4) == 0
    # Bigger committees are safer for the same threshold fraction
    p_small = committee(1000, 0.2, 16, threshold_for(16, 1 / 3))
    p_big = committee(1000, 0.2, 64, threshold_for(64, 1 / 3))
    assert p_big < p_small
    k, p = smallest_size(1000, 0.2, 1 / 3, 1e-6)
    assert k is not None and p <= 1e-6
    # Deterrence: one faked task, 10% audits -> penalty must exceed 10x gain
    pen, q = min_penalty(5, 0.1, 1)
    assert abs(q - 0.1) < 1e-12 and abs(pen - 50) < 1e-9
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("committee")
    c.add_argument("--nodes", type=int, required=True)
    c.add_argument("--malicious", type=float, required=True, help="fraction of malicious nodes, e.g. 0.2")
    c.add_argument("--size", type=int)
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--threshold", type=int, help="malicious members needed to break the committee")
    g.add_argument("--threshold-frac", type=float, help="e.g. 0.334 (BFT) or 0.5 (majority)")
    c.add_argument("--target", type=float, help="acceptable failure probability; finds the smallest size if --size omitted")
    d = sub.add_parser("deterrence")
    d.add_argument("--gain", type=float, required=True, help="profit from cheating per epoch")
    d.add_argument("--audit-rate", type=float, required=True)
    d.add_argument("--tasks", type=int, default=1, help="faked tasks per epoch")
    sub.add_parser("selftest")
    a = ap.parse_args()

    if a.cmd == "selftest":
        selftest()
    elif a.cmd == "deterrence":
        pen, q = min_penalty(a.gain, a.audit_rate, a.tasks)
        print(f"P(detect) = {q:.6g}; penalty must exceed {pen:.6g} (bond must cover it)")
    else:
        if a.size is None:
            if a.threshold_frac is None or a.target is None:
                sys.exit("without --size, give --threshold-frac and --target")
            k, p = smallest_size(a.nodes, a.malicious, a.threshold_frac, a.target)
            print("no committee size meets the target" if k is None else
                  f"smallest committee: {k} (threshold {threshold_for(k, a.threshold_frac)}), P(fail) = {float(p):.3e}")
        else:
            t = a.threshold if a.threshold is not None else threshold_for(a.size, a.threshold_frac)
            p = committee(a.nodes, a.malicious, a.size, t)
            print(f"P(>= {t} malicious in committee of {a.size}) = {float(p):.3e}")


if __name__ == "__main__":
    main()
