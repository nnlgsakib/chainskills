#!/usr/bin/env python3
"""Flag non-determinism hazards in Cosmos SDK state-machine code.

Usage:
    python3 audit_state_machine.py <chain-root>    # scans x/ and app/
    python3 audit_state_machine.py --selftest

Scans non-test, non-generated Go files. Exit code 1 if anything is found.
Heuristic (regex) scanner: it finds likely problems, it cannot prove absence.
Silence a justified line with a trailing `// audit:ok <reason>`.
"""
import os
import re
import sys

RULES = [
    ("wall-clock", re.compile(r"\btime\.Now\("), "use sdkCtx.HeaderInfo().Time / BlockTime()"),
    ("randomness", re.compile(r'"(math/rand(/v2)?|crypto/rand)"'), "no RNG in state transitions"),
    ("float", re.compile(r"\bfloat(32|64)\b"), "use math.Int / math.LegacyDec"),
    ("goroutine", re.compile(r"\bgo\s+(func\b|[\w.]+\()"), "no concurrency in state transitions"),
    ("select", re.compile(r"\bselect\s*\{"), "no channels in state transitions"),
    ("os-io", re.compile(r"\bos\.(Getenv|LookupEnv|ReadFile|Open|Create|Hostname)\("), "no env/filesystem reads"),
    ("network", re.compile(r'"net(/http)?"'), "no network I/O"),
]

MAP_DECL = re.compile(r"\b(\w+)\s*(?::=\s*make\(\s*map\[|:=\s*map\[|map\[)")
RANGE = re.compile(r"\brange\s+(?:[\w.]+\.)?(\w+)\b")
SKIP_SUFFIXES = ("_test.go", ".pb.go", ".pb.gw.go", ".pulsar.go")
SKIP_DIRS = {"simulation", "testutil", "testdata", "mocks"}


def strip_comment(line):
    i = line.find("//")
    return line if i < 0 else line[:i]


def scan_source(text):
    """Return list of (lineno, rule, hint, code) for one Go file's text."""
    lines = text.splitlines()
    maps = set()
    for line in lines:
        for m in MAP_DECL.finditer(strip_comment(line)):
            maps.add(m.group(1))
    findings = []
    for n, raw in enumerate(lines, 1):
        if "audit:ok" in raw:
            continue
        code = strip_comment(raw)
        for rule, rx, hint in RULES:
            if rx.search(code):
                findings.append((n, rule, hint, raw.strip()))
        m = RANGE.search(code)
        if m and m.group(1) in maps:
            findings.append((n, "map-iteration", "sort keys first or use collections", raw.strip()))
    return findings


def scan_tree(root):
    total = 0
    for top in ("x", "app"):
        base = os.path.join(root, top)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in sorted(filenames):
                if not f.endswith(".go") or f.endswith(SKIP_SUFFIXES) or f == "simulation.go":
                    continue
                path = os.path.join(dirpath, f)
                with open(path, encoding="utf-8", errors="replace") as fh:
                    for n, rule, hint, code in scan_source(fh.read()):
                        print(f"{os.path.relpath(path, root)}:{n}: [{rule}] {code}  -- {hint}")
                        total += 1
    return total


def selftest():
    bad = '''package keeper
import "math/rand"
func f(ctx context.Context) {
	t := time.Now()
	var x float64
	go func() {}()
	balances := make(map[string]int64)
	for k, v := range balances { _ = k; _ = v }
	h := os.Getenv("X")
}
'''
    rules = {r for _, r, _, _ in scan_source(bad)}
    assert rules == {"randomness", "wall-clock", "float", "goroutine", "map-iteration", "os-io"}, rules

    good = '''package keeper
// time.Now() in a comment is fine
func f(ctx context.Context, ids []uint64) {
	now := sdk.UnwrapSDKContext(ctx).HeaderInfo().Time
	for _, id := range ids { _ = id }
	t := time.Now() // audit:ok used only for logging latency
	category := "goods"
}
'''
    assert scan_source(good) == [], scan_source(good)
    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
        sys.exit(0)
    n = scan_tree(sys.argv[1])
    print(f"{n} finding(s)")
    sys.exit(1 if n else 0)
