# Changes

Each version of the harness, newest first. An update arrives as new commits in this repository. You merge it yourself (`git pull`), one change at a time if you like, with Tutor Orch's help (`orchestrator/ORCHESTRATOR.md`). Log in `orchestrator/RULES-LOG.md` what you took, what you left, and why. Your own edits are never overwritten.

## 1.0.0 · 2026-11-08 · The first version

Ported from the tutor system Dominik uses every day, with its company parts taken out.
- **The rulebook** (`CLAUDE.md`): how every tutor starts, behaves, answers a reply, builds a lesson, scores mastery, and changes the rules. Lesson 01 is a gate, the next lesson waits for his reply, and only he changes a rule, through Tutor Orch.
- **The formats** (`formats/`): `general`, `work-through` (with a section for courses that come with a kit of tested guides), `guided-project` (with its three sliders), the `casebook` module, and the `labs` module.
- **The orchestrator** (`orchestrator/`): Tutor Orch's role, the roles of Tutor Prime and Tutor Orch, the rules log with its prediction tally, the lessons the original system learnt the hard way, and `tools/tx.py` for reading transcripts.
- **The tools** (`tools/`): `new-course.sh`, the startup hook `session-context.py`, the linter `lint-lesson.py`, and the self-check `check-harness.py`.
- **The course template** (`_template/course/`), with a prediction tally in every `MASTERY.md`.
- **The `new-course` skill,** which starts a course and its tutor through Berth.
