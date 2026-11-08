# Changes

Each version of the harness, newest first. An update arrives as new commits in this repository. You merge it yourself (`git pull`), one change at a time if you like, with Tutor Orch's help (`orchestrator/ORCHESTRATOR.md`). Log in `orchestrator/RULES-LOG.md` what you took, what you left, and why. Your own edits are never overwritten.

## 1.0.4 · 2026-11-08 · tx.py sees which rules files a session loaded

- **`orchestrator/tools/tx.py`** prints a RULES line for every rules file a session loaded, as recorded by current Claude Code (an "instructions" attachment at start, "nested_memory" when a subfolder's file loads later). Older transcripts still work the old way. Before this, it printed none on current versions.

## 1.0.3 · 2026-11-08 · Compacting any session

- **`orchestrator/ORCHESTRATOR.md` §5a:** how to compact any session through Berth, not only a fresh fork: the note's TASK, SEAT and SOURCES, never a keep-or-drop list, and checking `compaction.state`. The `new-course` skill points to it.

## 1.0.2 · 2026-11-08 · A course's settings may carry its own permissions

- **`check-harness.py`** compares only the startup hook between a course's settings and the root's, so a course can add its own permissions, such as the store course's block on editing his backend. It also checks every existing course's settings, not just a new one.

## 1.0.1 · 2026-11-08 · One fixed path for the startup hook

- **Every `.claude/settings.json`,** in the root and in each course, runs the hook as `$HOME/tutor/tools/session-context.py`, so it works whichever folder Claude Code treats as the project. In a git clone that might be the clone's top folder rather than the course folder. `new-course.sh` now copies the root's file as it is.
- **`check-harness.py`** checks that every course's settings match the root's, and notes when the harness isn't at `~/tutor`.
- **`INSTALL.md` and `README.md`** say the harness must live at `~/tutor`.

## 1.0.0 · 2026-11-08 · The first version

Ported from the tutor system Dominik uses every day, with its company parts taken out.
- **The rulebook** (`CLAUDE.md`): how every tutor starts, behaves, answers a reply, builds a lesson, scores mastery, and changes the rules. Lesson 01 is a gate, the next lesson waits for his reply, and only he changes a rule, through Tutor Orch.
- **The formats** (`formats/`): `general`, `work-through` (with a section for courses that come with a kit of tested guides), `guided-project` (with its three sliders), the `casebook` module, and the `labs` module.
- **The orchestrator** (`orchestrator/`): Tutor Orch's role, the roles of Tutor Prime and Tutor Orch, the rules log with its prediction tally, the lessons the original system learnt the hard way, and `tools/tx.py` for reading transcripts.
- **The tools** (`tools/`): `new-course.sh`, the startup hook `session-context.py`, the linter `lint-lesson.py`, and the self-check `check-harness.py`.
- **The course template** (`_template/course/`), with a prediction tally in every `MASTERY.md`.
- **The `new-course` skill,** which starts a course and its tutor through Berth.
