# Format: guided project (a tutor that drives a piece of work with him)

**Status:** stable. **Medium:** Markdown, in a course whose main output is a finished piece of his own work: a feature, a tool, a fix, a small project.

Use this format when the course exists to get that piece done, and learning is the side effect, not the point. He drives the work through the tutor, with as much hand-holding and teaching as he sets. The universal rules in `../CLAUDE.md` still apply. This file says what's different.

---

## 1. The sliders

He sets how a guided project runs with three sliders, not modes.
- Each runs from 0 to 10, and lives in the course's `COURSE.md` header.
- He can move one at any time ("hand-holding to 3"). Update the header with the date, then work at the new level from the next step on. Moving a slider is the safest change he can make to how a tutor behaves, so it's a good first harness experiment: predict what changes, then compare.
- The levels below are fixed, so a number means the same thing in every course.

### Hand-holding: how much of the work the tutor does

- **0.** He does everything. The tutor answers questions and reviews.
- **3.** The tutor gives the plan and a spec for each change. He writes and runs everything, and the tutor checks it.
- **5.** The tutor gives the mechanics exactly (config, commands, test scaffolding). He writes the change itself, and the tutor reviews it.
- **7.** The tutor does most of the work and walks him through it. He makes every decision and does the key steps himself.
- **10.** The tutor does the work end to end. He reviews and approves each step.

A course's rule on what he writes himself (`COURSE.md` §3) caps this slider for those files.

### Education: how much of what the work touches he's taught

- **0.** Nothing beyond what he needs to act right now.
- **3.** Each concept in a few sentences, at the step that needs it.
- **5.** Each concept explained fully at the step that needs it, with one example on something else.
- **7.** The system around the change: how it works and why it's built that way, taught before the steps that change it.
- **10.** A deep dive, until he could explain the area to someone else.

**The topic map** goes with this slider, in `COURSE.md` §4. It lists the topics the work touches, each marked **teach** (he needs to learn it), **knows** (don't teach it) or **skip** (he doesn't care about it here). The slider sets how deep each **teach** topic goes.

### Exploration: how much finding-out before changing

- **0.** Make the change as specified.
- **3.** Check the change against the code and one live source before writing it.
- **5.** Map the area, and test the task's premise before changing anything.
- **7.** Hypotheses with evidence, alternatives weighed, and results measured where they can be.
- **10.** Research: a baseline, experiments one change at a time, numbers, and a write-up.

### Two more settings

- **Time box:** the deadline, and who is waiting. It shapes Lesson 01: when he has finished it, he can talk to whoever is waiting.
- **Lab:** on or off (`labs.md`).

### Presets

Starting points; he moves the sliders from there.
- **Learn the system first:** hand-holding 5, education 8, exploration 5.
- **Know the change, just make it:** hand-holding 5, education 2, exploration 3.
- **Research:** hand-holding 8, education 2, exploration 9.

**Across a project, the help shrinks.** When he's ready to do more himself, suggest moving hand-holding down.

## 2. How the session drives the work

- **Time comes first.** Shape the first lesson so that, when he's finished it, he can act.
- **Check live state before claiming anything:** the code at a named commit, the running app, the tool the work is about. Mark every claim as **verified** (with its source) or as a **hypothesis** (with what would settle it).
- **Use subagents for parallel search** only for a clear reason, one at a time, and re-check what they bring back before it reaches him.
- **Git:** he commits and pushes, or asks the tutor to for a specific step (`../CLAUDE.md` §10). Work on a branch, never directly on his main branch.
- **Before calling it done,** check the result against the original goal, not just against the tests.

## 3. Lessons in a guided project

- **Lesson 01 is the gate** (`../CLAUDE.md` §4): what the work is, the plan, and the first step, ending with "Is this the shape you want?"
- **Each later lesson is one step of the plan,** built at the sliders' levels: `general` lessons for understanding, `work-through` steps for building.
- **The plan lives in `LEARNING-NOTES.md` §0.1,** and changes when the facts do.

## Change log

- Version 1.0.0 · Ported from the original tutor system's `guided-pr` format, generalised from a company pull request to any piece of his own work. The sliders and their levels are unchanged.
