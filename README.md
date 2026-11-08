# Louis's tutor harness

Your tutor system, in one folder: `~/tutor/`. Each course is taught by a tutor, which is a Claude Code session started in that course's folder. Tutor Orch, the orchestrator, keeps the system coherent and starts tutors for you, and Tutor Prime is the session every tutor is forked from. All of them are rows in Berth, filed in the Berth folder `Tutor/`.

It's ported from the tutor system Dominik uses every day, with its company parts taken out. It's yours: read it, change it, and run it. **You're its orchestrator.** When a tutor does something you don't like, you find the rule that caused it, predict what changing it will do, change it with Tutor Orch, and check (`orchestrator/ORCHESTRATOR.md` §3). That loop is how you learn to build and change harnesses.

Every session in here follows:
- [`CLAUDE.md`](CLAUDE.md), the rulebook, which Claude Code loads automatically;
- its course's `COURSE.md`, which the startup hook injects by the session's name;
- the spec of its lesson format, in [`formats/`](formats/REGISTRY.md).

## Courses

Each tutor keeps its own row current.

| # | Course | Format | Session | State |
|---|---|---|---|---|

## Starting a course

Open the session "Tutor Orch" and tell it what you want to learn, in your own words, or paste a brief someone gave you. Its `new-course` skill creates the course, starts the tutor in Berth, and places the first brief for you to read and send. To do it by hand, `orchestrator/ORCHESTRATOR.md` §5 has the steps.

## Where things are

```
~/tutor/
  CLAUDE.md            how every tutor works (loaded automatically)
  README.md            this map
  CHANGES.md           each version of the harness, and what it changed
  formats/             REGISTRY.md (the lesson formats; the default is general) and one spec per format
  student/             PROFILE.md (who you are, how you want to be taught) and NOTEBOOK/<course>/ (your notes)
  courses/NN-slug/     COURSE.md, LEARNING-NOTES.md, MASTERY.md, lessons/NN/, prompts/, research/, .claude/
  labs/                every lab, and its pinned code
  orchestrator/        Tutor Orch's role, ROLES.md, RULES-LOG.md, LESSONS.md, research/, tools/tx.py
  _template/course/    the skeleton a new course is created from
  tools/               new-course.sh, session-context.py (the startup hook), lint-lesson.py, check-harness.py
  .claude/             settings.json (the startup hook) and skills/new-course/
```

## When things run

- **The startup hook** (`tools/session-context.py`) runs whenever a session here starts, resumes, is forked, or comes back from a compaction. It tells the session which course or role it serves, from its name, and injects that course's `COURSE.md`. Rules never come from the hook; they're in the `CLAUDE.md` files. Claude Code reads settings only from the folder a session starts in, so every course folder has its own `.claude/settings.json`. All of them run the hook by one fixed path, `~/tutor/tools/session-context.py`, which is why the harness must live at `~/tutor`.
- **The linter** (`tools/lint-lesson.py`) runs before a tutor sends a lesson.
- **The self-check** (`tools/check-harness.py`) runs after an install or an update, and whenever you change a tool.

## Words you'll meet

- **Harness:** everything around a model that shapes what it does: its rules, tools, hooks, skills, settings and records. This folder is one.
- **Session:** one conversation with Claude Code. It starts in a folder, and that folder decides which `CLAUDE.md` files and settings it loads.
- **Context:** everything the model can see at a given moment: the rules it loaded, what was said, the files it read.
- **Compaction:** when a session gets long, Claude Code replaces the earlier conversation with a summary to make room. A summary loses detail, so the files are the real memory. Compact through Berth, never by pasting `/compact`.
- **Hook:** a script Claude Code runs at a set moment, such as when a session starts or before a tool is used. It can add information, or block an action.
- **Skill:** a packaged set of instructions an agent loads when a task matches its description.
- **Transcript:** the full record of a session, saved in `~/.claude/projects/`. `orchestrator/tools/tx.py` makes one readable.
- **Fork:** a new session that starts with a copy of another session's whole conversation.
- **Berth:** the catalogue of your sessions, in folders, and the way you start, wake, fork and compact them.
- **Orchestrator:** an agent, or a person, that runs other agents: setting their rules, checking their work, and changing them when they fail. Here that's you, with Tutor Orch.
- **Slider:** a 0–10 setting in a course's header, for hand-holding, education or exploration (`formats/guided-project.md`).

In `CLAUDE.md`, "you" is the agent and "he" is you, Louis.
