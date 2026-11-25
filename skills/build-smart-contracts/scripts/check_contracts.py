#!/usr/bin/env python3
"""Quick Solidity checks that complement Slither/Aderyn/forge lint.

Targets issues that are recent or easy to miss (checked against sources 2026-11-25):
EIP-7702 EOA assumptions, unprotected upgradeable implementations, compiler
versions with known high-severity bugs, deprecated send/transfer, weak randomness.

Usage:
    python3 check_contracts.py <dir-or-file> [...]
    python3 check_contracts.py --selftest
Exit 1 if any ERROR. Regex-based: it finds likely problems, it cannot prove absence.
Silence a justified line with `// check:ok <reason>`.
"""
import os
import re
import sys

MIN_SAFE = (0, 8, 34)  # 0.8.34 fixed a high-severity IR storage/transient clearing bug

LINE_RULES = [
    ("ERROR", "tx-origin", re.compile(r"\btx\.origin\b"),
     "tx.origin is not an EOA proof or reentrancy guard since EIP-7702; use msg.sender + explicit auth"),
    ("WARN", "eoa-check", re.compile(r"\.code\.length\s*(==|>|!=)\s*0|\bextcodesize\b|\bisContract\s*\("),
     "code-size checks can't tell EOAs from contracts (EIP-7702 delegated EOAs have code)"),
    ("WARN", "send-transfer", re.compile(r"\.\s*(transfer|send)\s*\(\s*[^,()]*\)\s*;"),
     "address.send/transfer deprecated for 0.9 and 2300-gas stipend breaks with smart accounts; use call + reentrancy guard"),
    ("WARN", "selfdestruct", re.compile(r"\bselfdestruct\s*\("),
     "selfdestruct no longer deletes code (EIP-6780) and is deprecated"),
    ("WARN", "weak-randomness", re.compile(r"keccak256\s*\([^;]*(block\.timestamp|blockhash|block\.prevrandao|block\.difficulty)"),
     "block data is not secure randomness; use VRF/beacon (protocol-randomness)"),
    ("WARN", "packed-hash", re.compile(r"keccak256\s*\(\s*abi\.encodePacked\s*\([^;]*,[^;]*\)"),
     "abi.encodePacked with several args can collide when args are dynamic; prefer abi.encode"),
    ("INFO", "delegatecall", re.compile(r"\.delegatecall\s*\("),
     "delegatecall: verify target is trusted and storage layouts match"),
]
PRAGMA = re.compile(r"pragma\s+solidity\s+([^;]+);")
UPGRADEABLE = re.compile(r"\bcontract\s+\w+[^{]*\bis\b[^{]*\b(Initializable|UUPSUpgradeable|\w+Upgradeable)\b")
CONSTRUCTOR = re.compile(r"\bconstructor\s*\([^)]*\)[^{]*\{(.*?)\}", re.S)
AUTH_UPGRADE = re.compile(r"function\s+_authorizeUpgrade\s*\([^)]*\)([^{;]*)\{\s*\}")
NON_GUARD = re.compile(r"\b(internal|override|virtual)\b|\([^)]*\)")


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    return "\n".join(l if "check:ok" in l else re.sub(r"//.*", "", l) for l in src.splitlines())


def parse_version(s):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", s)
    return tuple(int(x) for x in m.groups()) if m else None


def check_source(src):
    out = []
    code = strip_comments(src)
    lines = code.splitlines()
    for n, line in enumerate(lines, 1):
        if "check:ok" in line:
            continue
        for level, rule, rx, hint in LINE_RULES:
            if rx.search(line):
                out.append((level, rule, n, hint))
    for m in PRAGMA.finditer(code):
        n = code[: m.start()].count("\n") + 1
        spec = m.group(1).strip()
        if spec.startswith("^") or ">" in spec:
            out.append(("WARN", "floating-pragma", n, f"pin an exact compiler version (found '{spec}')"))
        v = parse_version(spec)
        if v and v < MIN_SAFE and not re.search(r">=\s*0\.8\.(3[4-9]|[4-9]\d)", spec):
            out.append(("ERROR", "old-compiler", n, f"'{spec}' allows solc < 0.8.34 (known high-severity bug); use the latest 0.8.x"))
    if UPGRADEABLE.search(code):
        ctor = CONSTRUCTOR.search(code)
        if not ctor or "_disableInitializers" not in ctor.group(1):
            n = code[: UPGRADEABLE.search(code).start()].count("\n") + 1
            out.append(("ERROR", "unprotected-impl", n,
                        "upgradeable contract without `constructor() { _disableInitializers(); }`, so the implementation can be initialized by anyone"))
    for m in AUTH_UPGRADE.finditer(code):
        if NON_GUARD.sub("", m.group(1)).strip():  # a modifier (onlyOwner/onlyRole...) guards the empty body
            continue
        n = code[: m.start()].count("\n") + 1
        out.append(("ERROR", "open-upgrade", n, "_authorizeUpgrade has an empty body and no modifier, so anyone can upgrade; add onlyRole/onlyOwner"))
    return out


def check_path(path):
    files = []
    if os.path.isfile(path):
        files = [path]
    else:
        for dp, dns, fs in os.walk(path):
            dns[:] = [d for d in dns if d not in {"lib", "node_modules", "out", "cache", ".git"}]
            files += [os.path.join(dp, f) for f in fs if f.endswith(".sol") and not f.endswith((".t.sol", ".s.sol"))]
    errors = 0
    for f in sorted(files):
        with open(f, encoding="utf-8", errors="replace") as fh:
            for level, rule, n, hint in check_source(fh.read()):
                print(f"{f}:{n}: {level} [{rule}] {hint}")
                errors += level == "ERROR"
    return errors


def selftest():
    bad = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract Vault is Initializable, UUPSUpgradeable {
    function _authorizeUpgrade(address) internal override {}
    function f() external {
        require(tx.origin == msg.sender, "no contracts");
        require(msg.sender.code.length == 0);
        payable(msg.sender).transfer(1);
        uint r = uint(keccak256(abi.encodePacked(block.timestamp, msg.sender)));
    }
}"""
    rules = {r for _, r, _, _ in check_source(bad)}
    expected = {"tx-origin", "eoa-check", "send-transfer", "weak-randomness", "packed-hash",
                "floating-pragma", "old-compiler", "unprotected-impl", "open-upgrade"}
    assert expected <= rules, expected - rules

    good = """pragma solidity 0.8.39;
contract Vault is Initializable, UUPSUpgradeable, AccessControlUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() { _disableInitializers(); }
    function _authorizeUpgrade(address) internal override onlyRole(UPGRADER) {}
    // tx.origin in a comment is fine
    function f(address to) external nonReentrant {
        (bool ok,) = to.call{value: 1}("");
        require(ok);
        bytes32 h = keccak256(abi.encode(to, uint256(1)));
    }
}"""
    assert check_source(good) == [], check_source(good)
    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
        sys.exit(0)
    sys.exit(1 if sum(check_path(p) for p in sys.argv[1:]) else 0)
