#!/usr/bin/env python3
"""Validate agent skills against the open Agent Skills format and chainskills conventions.

Usage:
    python3 check_skill.py <skill-dir> [<skill-dir> ...] [--local] [--max-age-days 180]
    python3 check_skill.py --selftest

--local   project-local skill: suite-only rules (layer prefix, README/LICENSE, sources) become warnings
Exit 1 if any ERROR. Stdlib only.
"""
import datetime
import os
import re
import shutil
import sys
import tempfile

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LAYERS = ("blockchain-dev", "design-", "protocol-", "build-", "stack-", "quality-", "ops-", "extra-")
NO_SOURCES_NEEDED = ("blockchain-dev", "design-protocol", "design-spec", "build-skill", "build-stack-adapter")
HARNESS_SPECIFIC = [r"\bSkill tool\b", r"~/\.claude/skills", r"\bAskUserQuestion\b", r"\bTodoWrite\b"]
PLACEHOLDER = re.compile(r"<(Skill name>|What the skill does|One paragraph:|First step>|Next step>)")
REF_RE = re.compile(r"`((?:references|scripts|assets)/[A-Za-z0-9_./-]+)`")
DATE_RE = re.compile(r"verified(?: on)?:?\s*\(?(\d{4}-\d{2}-\d{2})", re.I)


def parse_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", line):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text[m.end():]


def check(path, local=False, max_age_days=180, today=None):
    errs, warns = [], []
    suite = (lambda msg: warns.append(msg)) if local else (lambda msg: errs.append(msg))
    folder = os.path.basename(os.path.normpath(path))
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [f"missing SKILL.md"], warns
    text = open(skill_md, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        return ["SKILL.md has no YAML frontmatter (--- ... ---)"], warns

    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errs.append(f"name '{name}': 1-64 chars, lowercase letters/digits/single hyphens, no leading/trailing hyphen")
    if name != folder:
        errs.append(f"name '{name}' must equal folder name '{folder}'")
    if not desc or len(desc) > 1024:
        errs.append(f"description must be 1-1024 chars (has {len(desc)})")
    elif len(desc) < 150:
        warns.append("description is short; include what it does AND when to use it (trigger phrases), or it may never trigger")
    if desc and not re.search(r"\b(use|when)\b", desc, re.I):
        warns.append("description should say when to use the skill ('Use whenever ...')")
    if PLACEHOLDER.search(text):
        errs.append("template placeholders left in SKILL.md")
    if "license" not in fm:
        suite("frontmatter lacks 'license' (suite convention: license: MIT)")

    if not local and not name.startswith(LAYERS):
        errs.append(f"suite skills need a layer prefix: {', '.join(LAYERS)} (use --local for project skills)")

    n = len(text.splitlines())
    if n > 500:
        errs.append(f"SKILL.md has {n} lines (> 500): move detail into references/")
    elif n > 300:
        warns.append(f"SKILL.md has {n} lines; consider moving detail into references/")

    for line in body.splitlines():
        for ref in REF_RE.findall(line):
            if os.path.exists(os.path.join(path, ref.rstrip("/."))):
                continue
            if line.lstrip().startswith("|"):   # the skill's own reference table: must exist
                errs.append(f"referenced file does not exist: {ref}")
            elif "../" not in line and "→" not in line:  # cross-skill refs use ../<skill>/... or "skill → file"
                warns.append(f"referenced file not found in this skill: {ref} (fine if it belongs to another skill)")

    for rx in HARNESS_SPECIFIC:
        if re.search(rx, body):
            warns.append(f"harness-specific wording ({rx.strip(chr(92) + 'b')}); keep skills agent-neutral")

    for f in ("README.md", "LICENSE"):
        if not os.path.isfile(os.path.join(path, f)):
            suite(f"missing {f}")

    if not name.startswith(NO_SOURCES_NEEDED):
        dates = DATE_RE.findall(text)
        if not re.search(r"^#+ .*Sources", text, re.M) and not dates:
            suite("no 'Sources (verified YYYY-MM-DD)' section: version-sensitive facts must cite primary sources")
        today = today or datetime.date.today()
        for d in dates:
            age = (today - datetime.date.fromisoformat(d)).days
            if age > max_age_days:
                warns.append(f"sources verified {d} ({age} days ago): refresh facts (build-skill refresh mode)")

    sd = os.path.join(path, "scripts")
    if os.path.isdir(sd):
        for f in sorted(os.listdir(sd)):
            if f.endswith(".py") and "selftest" not in open(os.path.join(sd, f), encoding="utf-8").read():
                warns.append(f"scripts/{f} has no selftest mode")
    return errs, warns


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    tmpl = os.path.join(here, "..", "assets", "skill-template")
    with tempfile.TemporaryDirectory() as d:
        # unfilled template must fail
        t = os.path.join(d, "protocol-example")
        shutil.copytree(tmpl, t)
        os.rename(os.path.join(t, "SKILL.md.tmpl"), os.path.join(t, "SKILL.md"))
        errs, _ = check(t)
        assert any("placeholder" in e or "name" in e for e in errs), errs

        # a good minimal skill passes
        g = os.path.join(d, "protocol-good")
        os.makedirs(os.path.join(g, "references"))
        open(os.path.join(g, "references", "a.md"), "w").write("x")
        open(os.path.join(g, "README.md"), "w").write("x")
        open(os.path.join(g, "LICENSE"), "w").write("x")
        open(os.path.join(g, "SKILL.md"), "w", encoding="utf-8").write(
            "---\nname: protocol-good\ndescription: Design good things for any chain, covering A, B and C in detail. "
            "Use whenever the user asks about good things, A, B or C, even if they don't name them explicitly.\n"
            "license: MIT\n---\n# Good\nRead `references/a.md`.\n\n## Sources (verified 2026-11-01)\nx\n")
        errs, warns = check(g, today=datetime.date(2026, 11, 25))
        assert errs == [] and warns == [], (errs, warns)

        # broken refs, bad name, stale sources, harness wording
        b = os.path.join(d, "Bad_Skill")
        os.makedirs(b)
        open(os.path.join(b, "SKILL.md"), "w", encoding="utf-8").write(
            "---\nname: Bad_Skill\ndescription: short\n---\nUse the Skill tool.\n| `references/missing.md` | x |\n"
            "## Sources (verified 2025-01-01)\n")
        errs, warns = check(b, today=datetime.date(2026, 11, 25))
        joined = " ".join(errs + warns)
        for frag in ("name 'Bad_Skill'", "referenced file does not exist", "layer prefix", "missing README.md", "days ago", "harness-specific"):
            assert frag in joined, (frag, errs, warns)

        # --local relaxes suite rules
        errs_l, _ = check(b, local=True, today=datetime.date(2026, 11, 25))
        assert not any("layer prefix" in e or "README" in e for e in errs_l), errs_l
    print("selftest ok")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--selftest":
        selftest()
        return
    local = "--local" in args
    max_age = 180
    if "--max-age-days" in args:
        max_age = int(args[args.index("--max-age-days") + 1])
    paths = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--max-age-days")]
    failed = False
    for p in paths:
        errs, warns = check(p, local=local, max_age_days=max_age)
        print(f"== {p}: {'OK' if not errs else 'FAIL'}")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  WARN:  {w}")
        failed |= bool(errs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
