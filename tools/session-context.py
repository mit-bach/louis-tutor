#!/usr/bin/env python3
"""SessionStart hook: tell a session which course or role it serves, from its name.

Claude Code auto-loads only the CLAUDE.md files on a session's path, never a course's
COURSE.md (on purpose: one course's rules must never load into another's session).
This hook closes the gap. It runs on startup, resume, clear, compact and fork. It reads
the session's name (its Berth title), finds the course or role registered under that
name, and prints an identity block plus that course's COURSE.md. Claude Code adds the
output to the session's context, and adds it again after every compaction.

Where names are registered:
  courses/*/COURSE.md     a header row  | **Sessions** | Name A, Name B |
  orchestrator/ROLES.md   a line         **Sessions:** Name   under each "## Role" heading

Claude Code caps each hook's output at 10,000 characters, so the settings run this
script twice: `session-context.py identity` prints the identity block, and
`session-context.py course` prints the course's COURSE.md (cut at a section boundary,
with a note, if it's ever over the cap).

It also exports TUTOR_HOME (this harness's folder) into the session's shell, through
$CLAUDE_ENV_FILE when Claude Code provides it, so commands can use "$TUTOR_HOME/tools/...".

Input: the hook's JSON on stdin (session_title, source, transcript_path, cwd).
Output: plain text on stdout. Prints nothing for a session outside the harness.
Never fails loudly: any error exits 0 with a one-line note, so a session always starts.
"""
import glob
import json
import os
import re
import sys

ROOT = os.environ.get("TUTOR_HOME") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.realpath(ROOT)
BUDGET = 9800  # characters; Claude Code caps each hook's output at 10,000


def norm(name):
    # A fork is named "<parent> ⑂", sometimes followed by more text: keep the parent part.
    name = (name or "").split("⑂")[0]
    name = re.sub(r"[^0-9A-Za-z]+", " ", name)
    return " ".join(name.lower().split())


def title_from_transcript(path):
    """The last title set on the session (Berth's rename, or /rename), read from the transcript's tail."""
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 2_000_000))
            tail = f.read().decode("utf-8", "replace")
        for line in reversed(tail.splitlines()):
            if '"custom-title"' in line or '"customTitle"' in line:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                t = d.get("customTitle") or d.get("title")
                if t:
                    return t
    except Exception:
        pass
    return ""


def header_value(text, key):
    m = re.search(r"^\|\s*\*\*%s\*\*\s*\|\s*(.*?)\s*\|\s*$" % key, text, re.M)
    return m.group(1).strip() if m else ""


def registry():
    """name -> (kind, info)."""
    reg = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "courses", "*", "COURSE.md"))):
        text = open(path, encoding="utf-8").read()
        sessions = header_value(text, "Sessions")
        slug = os.path.basename(os.path.dirname(path))
        title = re.search(r"^# (.+)$", text, re.M)
        info = {"slug": slug, "path": path, "text": text,
                "title": title.group(1) if title else slug,
                "format": header_value(text, "Format") or "general (default)"}
        for name in re.split(r"[,;]", sessions):
            if norm(name) and not norm(name).startswith("none"):
                reg[norm(name)] = ("course", info)
    roles = os.path.join(ROOT, "orchestrator", "ROLES.md")
    if os.path.exists(roles):
        text = open(roles, encoding="utf-8").read()
        for block in re.split(r"^## ", text, flags=re.M)[1:]:
            head, _, body = block.partition("\n")
            m = re.search(r"^\*\*Sessions:\*\*\s*(.+)$", body, re.M)
            if not m:
                continue
            for name in re.split(r"[,;]", m.group(1)):
                if norm(name):
                    reg[norm(name)] = ("role", {"role": head.strip(), "text": "## " + block.strip()})
    return reg


def export_home():
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    if not env_file:
        return
    try:
        with open(env_file, "a", encoding="utf-8") as f:
            f.write('export TUTOR_HOME="%s"\n' % ROOT)
    except Exception:
        pass


def course_part(title):
    hit = registry().get(norm(title))
    if not hit or hit[0] != "course":
        return
    c = hit[1]
    head = "--- %s, verbatim (the rules of this session's course) ---\n" % os.path.relpath(c["path"], ROOT)
    text = c["text"]
    if len(head) + len(text) > BUDGET:
        cut = text.rfind("\n## ", 0, BUDGET - len(head) - 200)
        text = text[: cut if cut > 0 else BUDGET - len(head) - 200] + \
            "\n\n… (cut to fit the hook's cap: read the rest of %s now)" % os.path.relpath(c["path"], ROOT)
    print(head + text)


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "identity"
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    cwd = os.path.realpath(data.get("cwd") or os.getcwd())
    if not (cwd == ROOT or cwd.startswith(ROOT + os.sep)):
        return
    source = data.get("source") or "startup"
    title = data.get("session_title") or title_from_transcript(data.get("transcript_path") or "")
    if part == "course":
        return course_part(title)
    export_home()
    fresh_fork = source == "fork" or "⑂" in (title or "")
    hit = registry().get(norm(title))
    rel = lambda p: os.path.relpath(p, ROOT)
    out = ["## Session identity (from tools/session-context.py, on %s)" % source, "",
           "The harness is `%s` (`$TUTOR_HOME`)." % ROOT, ""]

    if hit and hit[0] == "course":
        c = hit[1]
        fmt = c["format"]
        fmt_file = re.findall(r"`?(?:\.\./\.\./)?formats/([a-z-]+)\.md`?", fmt) or [fmt.split()[0]]
        specs = ", ".join("formats/%s.md" % f for f in fmt_file)
        if fresh_fork:
            out.append('This session is a fork of "%s". A fork of a course tutor serves the same course, '
                       "unless Louis's message says otherwise, in which case his message wins." % c["title"].split(":")[0])
        out += [
            'This session ("%s") is the tutor for **%s**, in `%s/`.' % (title, c["title"], rel(os.path.dirname(c["path"]))),
            "- **Lesson format:** %s. Spec: %s. Never use another format unless he asks (formats/REGISTRY.md)." % (fmt, specs),
            "- **The files on disk win** over any copy of them earlier in this conversation.",
            "- **Before you teach after this %s, read these in full:** `student/PROFILE.md`, %s, your "
            "`LEARNING-NOTES.md` §1, `MASTERY.md` \"Focus now\", and the newest lesson and reply." % (source, specs),
            "- **Ignore every other course's rules** unless he asks you to work on that course.",
            "",
            "- **Your course file follows** (from the second hook). If it isn't there, read `%s` in full now." % rel(c["path"]),
        ]
    elif hit and hit[0] == "role":
        r = hit[1]
        if fresh_fork and r["role"].lower().startswith("tutor prime"):
            out += [
                "This session is a **new fork of Tutor Prime**. It has no course until its brief gives it one.",
                "- If the brief starts a new course, follow `CLAUDE.md` §9. If it continues an existing course, make sure "
                "this session carries that course's session name (README.md, the course table), then read its `COURSE.md`.",
                "- Your inherited conversation and file snapshots may be older than the current rules. Read "
                "`formats/REGISTRY.md` and `student/PROFILE.md` from disk before teaching.",
                "- The lesson format is `general` unless the brief names another.",
            ]
        else:
            text = r["text"]
            out.append('This session ("%s") has the role **%s**.' % (title, r["role"]))
            out.append(text if len(text) < BUDGET - 600 else text[: BUDGET - 700] + "\n… (read orchestrator/ROLES.md)")
    elif fresh_fork and not norm(title):
        out += [
            "This session is a **new fork**, and has no name yet. It has no course until its brief gives it one.",
            "- If the brief starts a new course, follow `CLAUDE.md` §9. If it continues one, make sure this session "
            "carries that course's session name, then read that course's `COURSE.md`.",
        ]
    else:
        out += [
            'This session\'s name ("%s") isn\'t registered to a course or role.' % (title or "none"),
            "- Ask Louis which course or role this session serves (`CLAUDE.md` §0), and don't guess it from the folder.",
            "- The registered names are in `README.md` (the course table) and `orchestrator/ROLES.md`.",
        ]
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never block a session from starting
        print("(session-context hook failed: %s; follow CLAUDE.md §0)" % e)
    sys.exit(0)
