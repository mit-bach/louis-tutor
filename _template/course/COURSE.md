# Course {{NN}} · {{TITLE}}

| | |
|---|---|
| **Format** | {{FORMAT}} (`../../formats/{{FORMAT}}.md`) |
| **Format set** | {{DATE}}, {{FORMAT_SET}} |
{{EXTRA_ROWS}}
| **Sessions** | {{SESSION}} |
| **State** | Created {{DATE}}; no lesson yet |
| **Started from** | {{ORIGIN}} |

The rules for how every tutor behaves are in `../../CLAUDE.md`. His profile is `../../student/PROFILE.md`. This file adds only what is specific to this course.
- Keep it short. `tools/session-context.py` injects it into this course's sessions at every start and compaction, and its budget is about 8,000 characters.
- A rule he gives about this course goes here, not in a global file (`../../CLAUDE.md` §11).

---

## 1. The goal, in his words

<!-- Quote the brief, from prompts/RESPONSE-00.md or chat. What should he be able to do when this course is done? -->

## 2. Sources this course teaches from

<!-- Repos and paths, docs, tools, a kit of tested guides if the course has one. -->

## 3. What he writes himself, and what agents may do

<!-- The files that are his. What his agents, the tutor included, may and may not do with them (../../CLAUDE.md §10). -->

## 4. How this course's lessons differ from the format, if at all

<!-- Only the course's own adaptations. Never restate the format spec. -->

## 5. Plan

<!-- A draft; the live plan sits in LEARNING-NOTES.md §0.1. -->

## 6. Course files

- **`LEARNING-NOTES.md`:** the goal, the plan, the lesson index, Where we are, F-entries, the glossary and the answer record.
- **`MASTERY.md`:** this course's skill map, and the prediction tally.
- **`lessons/NN/`:** one folder per lesson (`../../CLAUDE.md` §4).
- **`research/_tutor-hypotheses.md`:** the tutor-only, evolving view.
- **`prompts/RESPONSE-NN.md`:** his replies, verbatim.
