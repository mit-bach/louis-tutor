---
name: new-course
description: Start a new course in Louis's tutor harness, from his brief to a running tutor in Berth. Use when he says "start a course", "teach me X", "I want to learn X", "new tutor", "here's a brief", or pastes an assignment someone gave him. For Tutor Orch, at the harness root.
---

# Start a new course

You're Tutor Orch (`orchestrator/ORCHESTRATOR.md`). Do these in order, telling Louis in a line what each step does.

## 1. The brief

- Get what he wants to understand, in his words. If he pasted an assignment, that's the brief; ask what he wants out of it in one line.
- If the brief is a list of things to show, ask what he wants to understand. A list becomes a lesson's outline, and that's how lessons go wrong.
- Save it verbatim; it becomes the course's `prompts/RESPONSE-00.md` in step 2.

## 2. Create the course

1. **Choose the format** by `formats/REGISTRY.md` §2: `general` unless the brief names or plainly describes another. Building something he writes himself is `work-through`; getting a piece of his own work done is `guided-project`, which needs sliders. If it points both ways, ask him in one line.
2. **Pick the slug and session name.** NN is the next free number in `courses/`. The slug says what is learnt (`02-git-basics`). The session name is what the tutor is called in Berth ("Git Tutor").
3. **Run it:**
   ```
   tools/new-course.sh <NN-slug> "<Title>" --session "<session name>" [--format <format> --asked "<his words>"] [--sliders "H,E,X"] [--lab on]
   ```
4. **Save the brief** as `courses/<NN-slug>/prompts/RESPONSE-00.md`, verbatim.
5. **Fill in `COURSE.md`** §1 (the goal, quoting the brief), §2 (sources), and §3 (what he writes himself). Keep it short.
6. **Add the course's row to `README.md`'s table.**
7. **Check the hook finds it:**
   ```
   echo '{"session_title":"<session name>","cwd":"'"$TUTOR_HOME"'/courses/<NN-slug>"}' | python3 tools/session-context.py | head -6
   ```
   It must say "is the tutor for".

## 3. Start the tutor, through Berth

Use the `berth` MCP's `create`, never a terminal command:
- `from`: "Tutor Prime", or a recent tutor in a nearby course that went well;
- `cwd`: the course folder, `$TUTOR_HOME/courses/<NN-slug>`;
- `title`: the course's session name;
- filed in the Berth folder `Tutor/`.

If the fork carries a long conversation, compact it the way `orchestrator/ORCHESTRATOR.md` §5a says, then check its `compaction.state` before you go on.

## 4. Place the first brief, unsent

Place the first brief in the new session's prompt box (the `cmux-claude` skill says how), and **don't send it**: Louis reads it and sends it himself.
- Write it in his voice, with the details in it: the goal in his words, the sources, the sliders if any, and what Lesson 01 must give him. Lesson 01 is a gate (`CLAUDE.md` §4).
- Paste the first paragraph from a file with no line breaks, because a line break can submit the box. Keep each paste under about 850 bytes, and type the rest as short lines.

## 5. Tell him

In a few lines: the course's folder, its session in Berth, its format, and that the brief is waiting in the tutor's box for him to send.
