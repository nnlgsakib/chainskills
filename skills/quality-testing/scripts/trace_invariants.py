#!/usr/bin/env python3
"""Spec ↔ test traceability: find invariants and checks that no test references.

Reads IDs from the spec (INV-<COMP>-<n>, optionally P-/R- ids) and searches test and
model files for references. Tests may write IDs with '-' or '_' (INV_STAKE_2, TestINV_STAKE_2).

Usage:
    python3 trace_invariants.py <project-root> [--spec docs/spec] [--strict]
    python3 trace_invariants.py --selftest
Exit 1 with --strict if any critical invariant (Severity 'critical' in invariants.md) is untested.
"""
import argparse
import os
import re
import sys
import tempfile

INV = re.compile(r"\bINV-([A-Z][A-Z0-9]*)-(\d+)\b")
TEST_HINT = re.compile(r"(_test\.go|\.t\.sol|test_.*\.py|_test\.py|\.spec\.ts|\.test\.ts|tests?/.*\.rs|\.qnt|\.tla)$")
SKIP_DIRS = {".git", "node_modules", "vendor", "lib", "out", "target", "cache", "build", "dist"}


def spec_invariants(spec_dir):
    ids, critical = set(), set()
    for dp, dns, fs in os.walk(spec_dir):
        for f in fs:
            if not f.endswith(".md"):
                continue
            for line in open(os.path.join(dp, f), encoding="utf-8", errors="replace"):
                found = {f"INV-{c}-{n}" for c, n in INV.findall(line)}
                ids |= found
                if f == "invariants.md" and "critical" in line.lower():
                    critical |= found
    return ids, critical


def referenced_ids(root, spec_dir):
    refs = {}
    spec_abs = os.path.abspath(spec_dir)
    for dp, dns, fs in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and os.path.abspath(os.path.join(dp, d)) != spec_abs]
        for f in fs:
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if not TEST_HINT.search(rel):
                continue
            text = open(path, encoding="utf-8", errors="replace").read()
            for c, n in re.findall(r"INV[-_]([A-Z][A-Z0-9]*)[-_](\d+)", text):
                refs.setdefault(f"INV-{c}-{n}", set()).add(rel)
    return refs


def report(root, spec_dir):
    ids, critical = spec_invariants(spec_dir)
    refs = referenced_ids(root, spec_dir)
    untested = sorted(i for i in ids if i not in refs)
    unknown = sorted(i for i in refs if i not in ids)
    return ids, critical, refs, untested, unknown


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "docs", "spec"))
        os.makedirs(os.path.join(d, "x", "stake", "keeper"))
        os.makedirs(os.path.join(d, "test"))
        open(os.path.join(d, "docs", "spec", "invariants.md"), "w").write(
            "| INV-STAKE-1 | STAKE | pool == sum | critical |\n| INV-STAKE-2 | STAKE | shares >= 0 | normal |\n"
            "| INV-GOV-1 | GOV | timelock | critical |\n")
        open(os.path.join(d, "x", "stake", "keeper", "inv_test.go"), "w").write("func TestINV_STAKE_1(t *testing.T) {}\n")
        open(os.path.join(d, "test", "Gov.t.sol"), "w").write("// covers INV-STAKE-2 and INV-FOO-9\n")
        open(os.path.join(d, "x", "stake", "keeper", "keeper.go"), "w").write("// INV-GOV-1 mentioned in non-test code\n")
        ids, critical, refs, untested, unknown = report(d, os.path.join(d, "docs", "spec"))
        assert ids == {"INV-STAKE-1", "INV-STAKE-2", "INV-GOV-1"}, ids
        assert critical == {"INV-STAKE-1", "INV-GOV-1"}, critical
        assert untested == ["INV-GOV-1"], untested          # non-test files don't count
        assert unknown == ["INV-FOO-9"], unknown
    print("selftest ok")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    spec = a.spec or os.path.join(a.root, "docs", "spec")
    ids, critical, refs, untested, unknown = report(a.root, spec)
    print(f"invariants in spec: {len(ids)}; referenced by tests/models: {len(ids) - len(untested)}")
    for i in untested:
        print(f"  UNTESTED{' (CRITICAL)' if i in critical else ''}: {i}")
    for i in unknown:
        print(f"  UNKNOWN (in tests, not in spec): {i} -> {', '.join(sorted(refs[i]))}")
    if a.strict and any(i in critical for i in untested):
        sys.exit(1)


if __name__ == "__main__":
    main()
