#!/usr/bin/env python3
"""Check a chainskills stack adapter against the adapter contract.

Usage:
    python3 check_adapter.py <path-to-stack-skill> [...more paths]
    python3 check_adapter.py --selftest

Exit 1 if any ERROR. WARN items are recommendations.
"""
import os
import re
import sys
import tempfile

NAME_RE = re.compile(r"^stack-[a-z0-9]+(-[a-z0-9]+)+$")
REQUIRED_SECTIONS = ["Adapter metadata", "Placement map", "Known pitfalls"]
RECOMMENDED_SECTIONS = ["When to use this adapter", "Setup", "Implement", "Test", "Production", "Updating this adapter"]
METADATA_FIELDS = ["Versions verified", "Verified on", "Sources"]
CONCEPTS = [
    "consensus", "state-execution", "staking-validators", "rollup", "tokenomics", "governance",
    "randomness", "verifiable-participation", "data-availability", "p2p", "interop",
    "smart-contracts", "node-software", "upgrades",
]
LEVELS = {"native", "extend", "custom", "n/a"}


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def sections(text):
    return {h.strip() for h in re.findall(r"^##\s+(.+)$", text, re.M)}


def check(path):
    errs, warns = [], []
    skill = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill):
        return [f"missing SKILL.md"], []
    text = open(skill, encoding="utf-8").read()
    fm = frontmatter(text)
    folder = os.path.basename(os.path.normpath(path))
    name = fm.get("name", "")
    if not NAME_RE.match(name):
        errs.append(f"name '{name}' must match stack-<family>-<name>")
    if name != folder:
        errs.append(f"name '{name}' differs from folder '{folder}'")
    if len(fm.get("description", "")) < 80:
        errs.append("description missing or too short to trigger reliably")
    if "<" in name or re.search(r"<(Stack name|family)>", text):
        errs.append("template placeholders left in SKILL.md")

    secs = sections(text)
    for s in REQUIRED_SECTIONS:
        if s not in secs:
            errs.append(f"missing section '## {s}'")
    for s in RECOMMENDED_SECTIONS:
        if s not in secs:
            warns.append(f"missing recommended section '## {s}'")
    meta = text.split("## Adapter metadata", 1)[1].split("\n## ", 1)[0] if "## Adapter metadata" in text else ""
    for f in METADATA_FIELDS:
        if f not in meta:
            errs.append(f"Adapter metadata lacks '{f}'")

    pm_path = os.path.join(path, "references", "placement-map.md")
    if not os.path.isfile(pm_path):
        errs.append("missing references/placement-map.md")
    else:
        rows = {}
        for line in open(pm_path, encoding="utf-8"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] in CONCEPTS:
                rows[cells[0]] = cells[1].strip("`").lower()
        for c in CONCEPTS:
            if c not in rows:
                errs.append(f"placement map lacks concept '{c}'")
            elif rows[c] not in LEVELS:
                errs.append(f"placement map '{c}' level '{rows[c]}' not in {sorted(LEVELS)}")

    for f in ("README.md", "LICENSE"):
        if not os.path.isfile(os.path.join(path, f)):
            errs.append(f"missing {f}")
    if len(text.splitlines()) > 300:
        warns.append("SKILL.md over 300 lines — move detail into references/")
    return errs, warns


def selftest():
    import shutil
    here = os.path.dirname(os.path.abspath(__file__))
    template = os.path.join(here, "..", "assets", "adapter-template")
    with tempfile.TemporaryDirectory() as d:
        t = os.path.join(d, "stack-x-y")
        shutil.copytree(template, t)
        os.rename(os.path.join(t, "SKILL.md.tmpl"), os.path.join(t, "SKILL.md"))
        errs, _ = check(t)
        assert any("placeholders" in e or "name" in e for e in errs), errs   # unfilled template must fail

    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "stack-demo-chain")
        os.makedirs(os.path.join(p, "references"))
        body = "\n".join(f"## {s}\nx" for s in REQUIRED_SECTIONS + RECOMMENDED_SECTIONS if s != "Adapter metadata")
        open(os.path.join(p, "SKILL.md"), "w", encoding="utf-8").write(
            "---\nname: stack-demo-chain\ndescription: " + "Demo adapter used for the self test of the checker script. " * 2 +
            "\n---\n# Demo\n## Adapter metadata\n- Versions verified: v1\n- Verified on: 2026-01-01\n- Sources: x\n" + body + "\n")
        rows = "\n".join(f"| {c} | native | x | y |" for c in CONCEPTS)
        open(os.path.join(p, "references", "placement-map.md"), "w", encoding="utf-8").write("| Concept | Level | Where | How |\n|---|---|---|---|\n" + rows)
        for f in ("README.md", "LICENSE"):
            open(os.path.join(p, f), "w").write("x")
        errs, warns = check(p)
        assert errs == [] and warns == [], (errs, warns)
    print("selftest ok")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--selftest":
        selftest()
        sys.exit(0)
    failed = False
    for p in sys.argv[1:]:
        errs, warns = check(p)
        print(f"== {p}: {'OK' if not errs else 'FAIL'}")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  WARN:  {w}")
        failed |= bool(errs)
    sys.exit(1 if failed else 0)
