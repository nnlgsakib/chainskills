#!/usr/bin/env python3
"""Detect which blockchain stack(s) a repository uses and which chainskills adapter fits.

Usage:
    python3 detect_stack.py <repo-root> [--skills-dir <dir with stack-* skills>] [--json]
    python3 detect_stack.py --selftest

Reads only manifest/config files (go.mod, Cargo.toml, package.json, foundry.toml, ...).
Never executes project code. Output: detected stacks with evidence, the matching
`stack-*` adapter if installed, otherwise a hint to create one with build-stack-adapter.
"""
import json
import os
import re
import sys
import tempfile

# (stack id, file glob name, regex on content, suggested adapter)
RULES = [
    ("cosmos-sdk", "go.mod", r"github\.com/cosmos/cosmos-sdk\s+v([\d.]+)", "stack-cosmos-ignite"),
    ("cosmos-evm", "go.mod", r"github\.com/cosmos/evm\s+v([\d.]+)", "stack-cosmos-evm"),
    ("ignite", "go.mod", r"github\.com/ignite/cli/v(\d+)", "stack-cosmos-ignite"),
    ("cosmwasm-chain", "go.mod", r"github\.com/CosmWasm/wasmd\s+v([\d.]+)", "stack-cosmos-apps"),
    ("cometbft-app", "go.mod", r"github\.com/cometbft/cometbft\s+v([\d.]+)", "stack-custom-bft"),
    ("op-stack", "go.mod", r"github\.com/ethereum-optimism/(optimism|op-geth)", "stack-rollup-op"),
    ("arbitrum-nitro", "go.mod", r"github\.com/offchainlabs/nitro", "stack-rollup-orbit"),
    ("avalanche", "go.mod", r"github\.com/ava-labs/(avalanchego|subnet-evm|coreth)", "stack-avalanche-l1"),
    ("geth-fork", "go.mod", r"github\.com/ethereum/go-ethereum\s+v([\d.]+)", "stack-evm-l1"),
    ("bsc-posa", "go.mod", r"github\.com/bnb-chain/", "stack-evm-l1"),
    ("hyperledger-fabric", "go.mod", r"github\.com/hyperledger/fabric", "stack-permissioned-fabric"),
    ("substrate", "Cargo.toml", r"\b(frame-support|sp-runtime|polkadot-sdk)\b", "stack-substrate-sdk"),
    ("reth", "Cargo.toml", r"\breth[-_a-z]*\s*=", "stack-evm-l1"),
    ("malachite", "Cargo.toml", r"malachitebft|informalsystems-malachite", "stack-custom-bft"),
    ("rust-abci", "Cargo.toml", r"\b(tendermint-abci|cometbft-abci|tower-abci)\b", "stack-custom-bft"),
    ("commonware", "Cargo.toml", r"\bcommonware-[a-z]+", "stack-custom-bft"),
    ("solana", "Cargo.toml", r"\b(solana-program|anchor-lang|solana-sdk)\b", "stack-svm-solana"),
    ("sovereign-sdk", "Cargo.toml", r"\bsov-(modules|rollup)", "stack-rollup-sovereign"),
    ("cosmwasm-contracts", "Cargo.toml", r"\bcosmwasm-std\b", "stack-cosmos-apps"),
    ("arbitrum-stylus", "Cargo.toml", r"\bstylus-sdk\b", "stack-rollup-orbit"),
    ("move", "Move.toml", r"\[package\]", "stack-move-sui-aptos"),
    ("foundry", "foundry.toml", r"\[profile", "build-smart-contracts"),
    ("hardhat", "hardhat.config.ts", r".", "build-smart-contracts"),
    ("hardhat", "hardhat.config.js", r".", "build-smart-contracts"),
    ("op-stack-contracts", "package.json", r"@eth-optimism/", "stack-rollup-op"),
    ("zksync", "package.json", r"zksync-(ethers|web3)|@matterlabs/", "stack-rollup-zk"),
    ("arbitrum-chain-sdk", "package.json", r"@arbitrum/(chain-sdk|orbit-sdk)", "stack-rollup-orbit"),
    ("zksync-os", "Cargo.toml", r"zksync[-_]os", "stack-rollup-zk"),
    ("besu-qbft", "genesis.json", r"\"qbft\"\s*:", "stack-evm-l1"),
    ("anchor", "Anchor.toml", r".", "stack-svm-solana"),
    ("ignite-config", "config.yml", r"(?m)^\s*(validators|accounts):", "stack-cosmos-ignite"),
]
SKIP = {".git", "node_modules", "vendor", "target", "out", "build", "dist", "lib", ".cache"}


def scan(root, max_depth=4):
    found = {}
    names = {r[1] for r in RULES}
    root = os.path.abspath(root)
    for dp, dns, fs in os.walk(root):
        depth = dp[len(root):].count(os.sep)
        dns[:] = [d for d in dns if d not in SKIP and depth < max_depth]
        for f in fs:
            if f not in names:
                continue
            path = os.path.join(dp, f)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for stack, fname, rx, adapter in RULES:
                if fname != f:
                    continue
                m = re.search(rx, text)
                if m:
                    ver = m.group(1) if m.groups() and m.group(1) and re.match(r"[\d.]+$", m.group(1)) else None
                    e = found.setdefault(stack, {"adapter": adapter, "evidence": [], "version": None})
                    e["evidence"].append(os.path.relpath(path, root).replace(os.sep, "/"))
                    e["version"] = e["version"] or ver
    # a geth dependency inside a Cosmos EVM / OP / Arbitrum / Avalanche chain is not a geth fork
    if "geth-fork" in found and found.keys() & {"cosmos-evm", "op-stack", "arbitrum-nitro", "avalanche"}:
        del found["geth-fork"]
    if "cometbft-app" in found and "cosmos-sdk" in found:
        del found["cometbft-app"]
    return found


def installed_adapters(skills_dir):
    if not skills_dir or not os.path.isdir(skills_dir):
        return set()
    return {d for d in os.listdir(skills_dir) if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))}


def report(root, skills_dir):
    found = scan(root)
    have = installed_adapters(skills_dir)
    has_chain_md = os.path.isfile(os.path.join(root, "CHAIN.md")) or os.path.isfile(os.path.join(root, "docs", "CHAIN.md"))
    out = {"chain_md": has_chain_md, "stacks": []}
    for stack, e in sorted(found.items()):
        out["stacks"].append({
            "stack": stack, "version": e["version"], "evidence": sorted(set(e["evidence"]))[:5],
            "skill": e["adapter"], "skill_installed": e["adapter"] in have if have else None,
        })
    return out


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "contracts"))
        open(os.path.join(d, "go.mod"), "w").write(
            "module x\nrequire (\n\tgithub.com/cosmos/cosmos-sdk v0.53.6\n\tgithub.com/cosmos/evm v0.6.0\n"
            "\tgithub.com/ethereum/go-ethereum v1.16.2\n\tgithub.com/cometbft/cometbft v0.38.21\n)\n")
        open(os.path.join(d, "contracts", "foundry.toml"), "w").write("[profile.default]\nsolc='0.8.39'\n")
        os.makedirs(os.path.join(d, "node_modules", "x"))
        open(os.path.join(d, "node_modules", "x", "Cargo.toml"), "w").write("solana-program = '1'\n")  # skipped dir
        skills = os.path.join(d, "skills")
        os.makedirs(os.path.join(skills, "stack-cosmos-ignite"))
        open(os.path.join(skills, "stack-cosmos-ignite", "SKILL.md"), "w").write("x")
        r = report(d, skills)
        got = {s["stack"]: s for s in r["stacks"]}
        assert set(got) == {"cosmos-sdk", "cosmos-evm", "foundry"}, got.keys()   # geth + cometbft folded in
        assert got["cosmos-sdk"]["version"] == "0.53.6"
        assert got["cosmos-sdk"]["skill_installed"] is True
        assert got["cosmos-evm"]["skill_installed"] is False
        assert r["chain_md"] is False
    print("selftest ok")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        selftest()
        return
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    skills_dir = None
    if "--skills-dir" in sys.argv:
        skills_dir = sys.argv[sys.argv.index("--skills-dir") + 1]
    else:  # default: the skills folder this script ships in
        skills_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    r = report(root, skills_dir)
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
        return
    print(f"CHAIN.md present: {'yes' if r['chain_md'] else 'no'}")
    if not r["stacks"]:
        print("no known blockchain stack detected (new project, or a stack not in the rule list)")
    for s in r["stacks"]:
        status = {True: "installed", False: "MISSING -> build-stack-adapter quick mode creates a project-local adapter now", None: "unknown"}[s["skill_installed"]]
        v = f" v{s['version']}" if s["version"] else ""
        print(f"- {s['stack']}{v}: skill {s['skill']} ({status}); evidence: {', '.join(s['evidence'])}")


if __name__ == "__main__":
    main()
