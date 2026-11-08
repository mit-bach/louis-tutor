#!/usr/bin/env python3
"""A few mechanical checks for a lesson, before Louis sees it.

usage: python3 tools/lint-lesson.py <lesson.md> [...]
       python3 tools/lint-lesson.py --all          every lesson in every course

It checks only what is easy to get wrong and cheap to fix:
  E  more than 3 questions, or an answer folded inside the questions
  E  a relative link that doesn't resolve
  E  an email address, or something shaped like a key or token
  E  a path:line link to a file that doesn't exist, or to a line past its end
  W  a table cell over 12 words (tables are for tiny content)
  W  a code block with no **[Lnn-Bk]** label (general lessons only)
  W  a lesson over its format's word budget (general: about 3,000 words of prose)

Fix the errors. Fix a warning, or leave it if you have a reason. Never mention the linter in a lesson.
Relevance, accuracy and readability are your job, not this script's: re-read the lesson against his words.
"""
import glob
import os
import re
import sys

ROOT = os.environ.get("TUTOR_HOME") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = re.compile(r"^\s*(```|~~~)")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
# A link whose target is a local file with a line, written as path:line or path#Lline.
LINE_LINK = re.compile(r"\]\(((?:file://|/|\.{1,2}/|~/)[^)\s:#]+)(?::(\d+)|#L(\d+))\)")
SECRET = re.compile(r"\b[\w.+-]+@[\w-]+\.(com|ai|io|org|net|edu)\b|\b(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|xox[abp]-[A-Za-z0-9-]{10,}|gh[pousr]_[A-Za-z0-9]{30,})\b")
BUDGET = {"general": 3000}


def course_format(path):
    d = os.path.dirname(os.path.abspath(path))
    while d.startswith(ROOT) and d != ROOT:
        f = os.path.join(d, "COURSE.md")
        if os.path.exists(f):
            m = re.search(r"^\|\s*\*\*Format\*\*\s*\|\s*([a-z-]+)", open(f, encoding="utf-8").read(), re.M)
            return m.group(1) if m else "general"
        d = os.path.dirname(d)
    return "general"


def resolve(target, base):
    t = target[len("file://"):] if target.startswith("file://") else target
    t = os.path.expanduser(t)
    return t if os.path.isabs(t) else os.path.join(base, t)


def lint(path):
    found = []
    lines = open(path, encoding="utf-8").read().splitlines()
    fmt = course_format(path)
    in_fence, prose, opens = False, [], []
    for i, ln in enumerate(lines):
        if FENCE.match(ln):
            if not in_fence:
                opens.append(i)
            in_fence = not in_fence
        elif not in_fence:
            prose.append(i)

    # questions: the last heading that starts with "Questions"
    heads = [i for i in prose if re.match(r"^#+\s*(part \d+\s*[·:.-]\s*)?questions\b", lines[i], re.I)]
    if heads:
        start = heads[-1]
        level = len(lines[start]) - len(lines[start].lstrip("#"))
        end = next((i for i in prose if i > start and lines[i].startswith("#")
                    and len(lines[i]) - len(lines[i].lstrip("#")) <= level), len(lines))
        block = lines[start + 1:end]
        n = sum(1 for l in block if re.match(r"^\d+[.)]\s", l))
        if n > 3:
            found.append(("E", start + 1, "%d questions; at most 3" % n))
        if any("<details" in l for l in block):
            found.append(("E", start + 1, "an answer is folded inside the questions"))

    base = os.path.dirname(os.path.abspath(path))
    for i in prose:
        for t in LINK.findall(lines[i]):
            t = t.split("#")[0]
            if re.match(r"^[a-z]+:", t) and not t.startswith("file://"):
                continue
            t = re.sub(r":\d+$", "", t)
            if t and not os.path.exists(resolve(t, base)):
                found.append(("E", i + 1, "link doesn't resolve: %s" % t))
        for m in LINE_LINK.finditer(lines[i]):
            f = resolve(m.group(1), base)
            n = int(m.group(2) or m.group(3) or 0)
            if os.path.isfile(f) and n and sum(1 for _ in open(f, encoding="utf-8", errors="ignore")) < n:
                found.append(("E", i + 1, "link past the end of %s: line %d" % (os.path.basename(f), n)))
    for i, ln in enumerate(lines):
        if SECRET.search(ln):
            found.append(("E", i + 1, "an email address or a key-shaped string"))

    words = 0
    for i in prose:
        ln = lines[i].strip()
        words += len(ln.split())
        if ln.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", ln):
            for cell in ln.strip("|").split("|"):
                if len(re.sub(r"`[^`]*`|\[([^\]]*)\]\([^)]*\)", "x", cell).split()) > 12:
                    found.append(("W", i + 1, "a table cell over 12 words"))
                    break
    if fmt in BUDGET and words > BUDGET[fmt]:
        found.append(("W", 1, "about %d words of prose, over the %s budget of %d" % (words, fmt, BUDGET[fmt])))
    if fmt == "general":
        for i in opens:
            before = [lines[j] for j in range(max(0, i - 3), i) if lines[j].strip()]
            after_fence = any(FENCE.match(lines[j]) for j in range(max(0, i - 3), i))
            if not after_fence and not any("**[L" in b for b in before[-2:]):
                found.append(("W", i + 1, "a code block with no **[Lnn-Bk]** label"))
    return found


def main(argv):
    paths = []
    for a in argv:
        if a == "--all":
            paths += [p for p in sorted(glob.glob(os.path.join(ROOT, "courses", "*", "lessons", "*", "*.md")))
                      if re.match(r"^\d\d-", os.path.basename(p)) and "casebook" not in p]
        else:
            paths.append(a)
    if not paths:
        print(__doc__)
        return 2
    errors = 0
    for p in paths:
        found = lint(p)
        errors += sum(1 for k, _, _ in found if k == "E")
        print("%s: %s" % (os.path.relpath(os.path.abspath(p), ROOT),
                          "ok" if not found else "%d error(s), %d warning(s)" % (
                              sum(k == "E" for k, _, _ in found), sum(k == "W" for k, _, _ in found))))
        grouped = {}
        for k, n, m in found:
            grouped.setdefault((k, m if k == "E" else m.split(":")[0]), []).append(n)
        for (k, m), ns in grouped.items():
            where = ", ".join(str(n) for n in ns[:6]) + (" …" if len(ns) > 6 else "")
            print("  %s %s (line%s %s)" % (k, m, "s" if len(ns) > 1 else "", where))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
