# Format: work-through (a build lesson)

**Status:** stable. **Medium:** one Markdown document per build step.

Use this format when Louis is learning to **build** something, and he writes the code himself as part of the lesson. A course gets this format only when its `COURSE.md` declares it (`REGISTRY.md`). The universal lesson rules in `../CLAUDE.md` §4 still apply. This file adds what's specific to building.

**Budget:** one build step per lesson. A step ends at a check he can run.

---

## 1. What a lesson is

- **One document.** Learning and doing are interleaved in build order. There's no separate workshop or exercise file.
- **It replaces the task's own document as his guide.** It tells him what to do, when, how and why.
- **Follow the order of the task he was given.** If you change the order, give the reason.
- **Don't assume mastery.** Teach him how to write the code.
- **He runs the lesson's commands, and you set up the lab** (`labs.md`), when the course has one.

## 2. The frame, in order

1. **Header:** the date and the last revision, and which of his replies the lesson answers. When it's revised while he's working through it, a dated note at the top says what was wrong and what changed. Say plainly when the fault was the lesson's.
2. **How to use this lesson,** in four lines: do the steps in order; your lab is ready, and one command proves it; write your own code yourself; if what you see doesn't match, stop and paste the output back.
3. **The course's rule on what he writes himself,** stated once (from `COURSE.md` §3).
4. **What you'll have at the end:** one concrete thing he'll see working.
5. **His previous feedback, answered,** in a few short bullets.
6. **The steps.** Each is headed `## Step N · <outcome>` and opens with a one-line **Why**.
7. **Vetting inline, where his work changes what comes next:** one line on what holds up, then each problem with its tested evidence and its consequence, then his options, with the exact commands to get back on track.
8. **The step's ending** (§5).
9. **At most 3 questions,** about what he understood from what he did.

## 3. Three kinds of content, taught three ways

Every block of a step belongs to one of these. Decide which before writing it.

### A. Mechanics: configuration, syntax, install commands, glue code. Give it exactly.

- Name the file and the action: create it, replace the whole file, add these lines under a named line, or change one line to another.
- Show the full content, then **What each part does,** one bullet per line or setting, including the syntax rules ("indentation is two spaces, never tabs").
- Give the commands, then **You should see,** with the exact expected output.
- Then **If something doesn't match:** what to run, what to paste back, and the usual causes.
- **Never make him turn a description in prose into YAML, SQL or code.** That's what fails beginners.

### B. Design decisions: a data model, an error's status code, where a rule lives, a trade-off. He decides.

- **For a big design piece** (a table, an API's shape):
  1. Teach the building blocks, with an example on a different thing.
  2. Pose numbered decisions, each with the facts he needs, and withhold the answer.
  3. He writes one line per decision in his journal, then writes the piece himself and runs it.
  4. Your version and your reasons sit folded in a `<details>` block below the place where he writes his choice, to open only after his runs.
- **For a small decision inside given code,** put a **Decide first** point before the code: the options, the facts, and "write your choice and why before you read on". The answer goes folded, never directly below the question.
- **If his choice is defensible but differs from yours,** he keeps it. Later steps then use his version.

### C. His own code: models, operations, routes, commands. He writes it, in small pieces.

Each piece has five parts:
1. **The idea.** Every construct he needs, explained at that point, including the small syntax.
2. **A worked example on a different, smaller thing,** labelled `[Lnn-Bk]`, in the same shape as his target, so he sees the shape without seeing his answer.
3. **You write.** An exact contract: the file, the names, the parameters and return types, the behaviour, the exact error text, and one **Hint** where he'd get stuck.
4. **Check.** A command he runs straight away, with the exact expected output, plus the common errors and what they mean.
5. **The tutor's version, folded,** when the course allows one. A course with a kit never shows one (§6).

## 4. Throughout

- **Relevant in the moment** (`../CLAUDE.md` §2). A concept arrives where it's needed.
- **Predictions are one-line guesses inside a step, checked within a minute** ("before you press Enter, guess what happens"). He writes each one, with what happened, in his predictions log.
- **Decisions that aren't the point of the lesson** are made for him, with a one-sentence reason. A decision the course's rules settle isn't yours to change.
- **Read his environment before telling him what to type:** his files (with secret values masked), and what's running.

## 5. Each step ends the same way

1. **The checks pass,** and the step shows exactly what passing looks like.
2. **One manual check,** step by step.
3. **His journal:** his decisions, the review's findings and what he did about each, and his answers to the questions.
4. **His predictions,** each written with what actually happened.
5. **A commit,** saying which files `git status` should and shouldn't list.

## 6. When the course comes with a kit of tested guides

Some courses come with a kit: guides, checks and a contract, already tested by whoever wrote it. Then:
- **The lessons are the kit's guides,** served in order, one step at a time, under the Lesson 01 gate and the reply-wait.
- **The tutor may add a bridge** of two or three sentences at the top of a step, tying it to his last journal entry. It never rewrites a guide, and never shows a reference solution.
- **The tutor's own writing** is its reviews (naming problems, never fixing them), the examiner's three questions, and its answers.
- **Records are named by step,** not by lesson number. For step 2 of milestone 3: `lessons/M3-2.md` holds the bridge, the review and the questions; `prompts/RESPONSE-M3-2.md` holds what he says in chat, verbatim.
- **His reply for a step is his journal's entries for it** (in his project), plus anything he says in chat. The next step opens once the journal holds that step's entries.
- **The tutor reviews from the check's saved result,** never by running the checks itself: the checks write to his database, and his folders aren't a test bench.
- **Two routes for his feedback:** a problem in a guide goes back to whoever wrote the kit. A problem in how the tutor behaves is his to fix, through Tutor Orch.
- The guides arrive tested, so the tutor doesn't re-run them or lint them. Its own bridges and reviews are re-read against his words.

## 7. Before it goes out (for a step the tutor writes)

- [ ] It's one build step, ending at a check he can run.
- [ ] Every block is tagged as mechanics, design or his code, and handled as §3 says.
- [ ] Every block was run in a scratch copy, never in his folders, and the expected outputs are pasted from that run. When a check should catch a mistake, you broke the code on purpose and saw that it does.
- [ ] His lab is set up, and its smoke test passes there.
- [ ] No design answer or folded version sits visibly below its question.
- [ ] Every concept is introduced where it's used.
- [ ] At most 3 questions; Parked is there.
- [ ] `python3 "$TUTOR_HOME/tools/lint-lesson.py" <lesson>` shows no errors.

## Change log

Changes to this spec are made when Louis gives feedback about **build lessons**, not about one lesson's content (`REGISTRY.md` §3). Record each change here.

- Version 1.0.0 · Ported from the original tutor system's `work-through` spec, which grew out of a build course that went through four versions of its first lessons. Added §6, for courses that come with a kit of tested guides.
