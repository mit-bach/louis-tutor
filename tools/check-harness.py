#!/usr/bin/env python3
"""Self-check for the tutor harness. Run after an install, an update, or a change to a tool.

usage: python3 tools/check-harness.py

It works in a temporary copy of the harness, so it never changes yours. It checks:
  - every file the harness needs is there, and the settings files are valid JSON with the hook in them;
  - new-course.sh makes a course, with its own .claude/settings.json pointing at the hook;
  - the hook names that course's tutor from its session name, injects its COURSE.md, and names the roles;
  - the hook prints nothing for a session outside the harness, and asks when a name isn't registered;
  - the linter passes a clean lesson and catches four questions and an email address;
  - every Python tool compiles.
Exits 0 when everything passes; otherwise prints what failed and exits 1.
"""
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEEDED = [
    "CLAUDE.md", "README.md", "CHANGES.md", ".claude/settings.json", ".claude/skills/new-course/SKILL.md",
    "formats/REGISTRY.md", "formats/general.md", "formats/work-through.md", "formats/guided-project.md",
    "formats/casebook.md", "formats/labs.md", "student/PROFILE.md",
    "orchestrator/ORCHESTRATOR.md", "orchestrator/ROLES.md", "orchestrator/RULES-LOG.md", "orchestrator/LESSONS.md",
    "orchestrator/tools/tx.py", "_template/course/COURSE.md", "_template/course/LEARNING-NOTES.md",
    "_template/course/MASTERY.md", "tools/new-course.sh", "tools/session-context.py", "tools/lint-lesson.py",
]
failures = []


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        failures.append(what)


def hook(root, payload, part="identity"):
    env = dict(os.environ, TUTOR_HOME=root)
    env.pop("CLAUDE_ENV_FILE", None)
    r = subprocess.run([sys.executable, os.path.join(root, "tools", "session-context.py"), part],
                       input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=20)
    return r.stdout


def main():
    print("Files")
    for rel in NEEDED:
        check(os.path.exists(os.path.join(ROOT, rel)), rel)
    try:
        s = json.load(open(os.path.join(ROOT, ".claude", "settings.json")))
        cmds = [h["command"] for g in s["hooks"]["SessionStart"] for h in g["hooks"]]
        check(any("session-context.py" in c for c in cmds), ".claude/settings.json runs the startup hook")
    except Exception as e:
        check(False, ".claude/settings.json is valid JSON (%s)" % e)
    home = os.path.realpath(os.path.expanduser("~/tutor"))
    if os.path.realpath(ROOT) == home:
        check(True, "the harness is at ~/tutor, where the hooks look for it")
    else:
        print("  note  the harness isn't at ~/tutor (it's at %s). The hooks run ~/tutor/tools/session-context.py,"
              " so they'll only work once it's installed there (INSTALL.md)." % ROOT)

    print("Python tools compile")
    for rel in ["tools/session-context.py", "tools/lint-lesson.py", "tools/check-harness.py", "orchestrator/tools/tx.py"]:
        try:
            py_compile.compile(os.path.join(ROOT, rel), doraise=True)
            check(True, rel)
        except Exception as e:
            check(False, "%s (%s)" % (rel, e))

    tmp = tempfile.mkdtemp(prefix="tutor-check-")
    copy = os.path.join(tmp, "tutor")
    try:
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "courses"))
        os.makedirs(os.path.join(copy, "courses"), exist_ok=True)

        print("new-course.sh, in a temporary copy")
        r = subprocess.run(["bash", os.path.join(copy, "tools", "new-course.sh"), "01-check-course", "Check Course",
                            "--session", "Check Tutor"], capture_output=True, text=True, timeout=30)
        check(r.returncode == 0, "it creates a course (%s)" % (r.stderr.strip() or "exit 0"))
        course = os.path.join(copy, "courses", "01-check-course")
        check(os.path.exists(os.path.join(course, "COURSE.md")), "the course has its COURSE.md")
        text = open(os.path.join(course, "COURSE.md")).read() if os.path.exists(os.path.join(course, "COURSE.md")) else ""
        check("| **Sessions** | Check Tutor |" in text, "COURSE.md registers the session name")
        check("{{" not in text, "every template placeholder is filled")
        cs = os.path.join(course, ".claude", "settings.json")
        try:
            same = json.load(open(cs)) == json.load(open(os.path.join(copy, ".claude", "settings.json")))
            cmd = json.load(open(cs))["hooks"]["SessionStart"][0]["hooks"][0]["command"]
            check(same and "$HOME/tutor/tools/session-context.py" in cmd,
                  "the course's own settings run the same hook as the root, by its fixed path")
        except Exception as e:
            check(False, "the course has a valid .claude/settings.json (%s)" % e)
        r = subprocess.run(["bash", os.path.join(copy, "tools", "new-course.sh"), "02-x", "X", "--session", "X",
                            "--format", "work-through"], capture_output=True, text=True, timeout=30)
        check(r.returncode != 0, "a non-default format without --asked is refused")

        print("The startup hook, in the temporary copy")
        out = hook(copy, {"session_title": "Check Tutor", "cwd": course})
        check("is the tutor for **Course 01 · Check Course**" in out, "it names the course's tutor from its session name")
        out = hook(copy, {"session_title": "Check Tutor", "cwd": course}, "course")
        check("| **Sessions** | Check Tutor |" in out, "it injects the course's COURSE.md")
        out = hook(copy, {"session_title": "Tutor Orch", "cwd": copy})
        check("has the role **Tutor Orch**" in out, "it names Tutor Orch")
        out = hook(copy, {"session_title": "Tutor Prime ⑂", "cwd": course, "source": "fork"})
        check("new fork of Tutor Prime" in out, "it recognises a fresh fork of Tutor Prime")
        out = hook(copy, {"session_title": "Someone Else", "cwd": copy})
        check("isn't registered" in out and "Ask Louis" in out, "it asks when a name isn't registered")
        out = hook(copy, {"session_title": "Check Tutor", "cwd": tempfile.gettempdir()})
        check(out.strip() == "", "it prints nothing outside the harness")

        print("The linter, in the temporary copy")
        lesson_dir = os.path.join(course, "lessons", "01")
        os.makedirs(lesson_dir, exist_ok=True)
        good = os.path.join(lesson_dir, "01-lesson-check.md")
        open(good, "w").write("# Lesson 01\n\n**[L01-B1]** (command)\n```\necho hi\n```\n\n## Parked\n\n## Questions\n1. One?\n")
        r = subprocess.run([sys.executable, os.path.join(copy, "tools", "lint-lesson.py"), good],
                           capture_output=True, text=True, env=dict(os.environ, TUTOR_HOME=copy), timeout=20)
        check(r.returncode == 0, "a clean lesson passes")
        bad = os.path.join(lesson_dir, "01-lesson-bad.md")
        open(bad, "w").write("# Lesson\n\nMail me at someone@example.com\n\n## Questions\n1. a\n2. b\n3. c\n4. d\n")
        r = subprocess.run([sys.executable, os.path.join(copy, "tools", "lint-lesson.py"), bad],
                           capture_output=True, text=True, env=dict(os.environ, TUTOR_HOME=copy), timeout=20)
        check(r.returncode == 1 and "4 questions" in r.stdout and "email" in r.stdout,
              "it catches four questions and an email address")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if failures:
        print("%d check(s) failed." % len(failures))
        return 1
    print("Everything passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
