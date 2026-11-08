# Format: general (the default Markdown lesson)

**Status:** stable, and the default for every course (`REGISTRY.md`). **Medium:** one Markdown lesson per folder, `lessons/NN/NN-lesson-<topic>.md`, which he reads in his editor.

Use this format for anything that isn't a build (`work-through.md`) or a guided project (`guided-project.md`): fundamentals, an explanation of a system, a code reading. When he's investigating what's true, add the casebook module (`casebook.md`).

The universal rules in `../CLAUDE.md` (§2 behaviour, §4 lesson rules, §5 labels) apply. This file says what a general lesson contains.

---

## 1. The parts, in order

1. **Header.**
   - The date, and the path of the reply it answers (`prompts/RESPONSE-NN.md`).
   - **What changed since last time:** corrections to earlier lessons, changed facts.
2. **Part 1 · His answers and his own words, vetted.**
   - **What he got right:** one line, or nothing.
   - **What he got wrong or half right,** in depth, in this order:
     1. quote him;
     2. give a verdict (✅ / ⚠️ / ❌);
     3. say why it's tempting;
     4. show the evidence (the row, the line, the message);
     5. give the correct model;
     6. say why it matters to what he's doing.
   - **A streamed reading of code:** correct only what's wrong, claim by claim, with line numbers.
3. **The teaching parts.** One idea at a time, each anchored in a real source: a file and line, a command and its verbatim output.
   - In an investigation, teach with 🔎 clues (evidence plus a question), not verdicts.
4. **🔸 Warm-ups,** spread through the parts, not saved for the end. Each is marked *easy* or *challenge*, with the answer in `<details><summary>check</summary>…</details>`.
5. **Parked:** what you deliberately left out, and why.
6. **Questions:** at most 3, answered in chat. Point each one at the blocks it needs, by label. Never put an answer in the lesson.

A course may adapt these parts in its `COURSE.md`. It may not drop Part 1, Parked or the Questions.

## 2. How he answers, and visual aids

**He answers freeform, as he goes.** He reads a lesson top to bottom and reacts section by section, in one reply in chat or in `prompts/RESPONSE-NN.md`.
- **Write the lesson so it invites that.** Put each 🔎 clue and each warm-up where he'll want to react. Address him directly: "Before you read on, say what you expect." Keep the parts short enough that he can respond to each.
- **Never give him a form or a text box to answer in.**
- **His reply is your evidence.** Vet it in the next lesson's Part 1, in his order.

**Use visual aids where a picture teaches what prose can't.** Draw them in the lesson: a Mermaid diagram, a small ASCII diagram, or a short table where every cell is tiny. A diagram shows the real mechanism, from the code: what happens to what, in what order. Label it like any block (`[Lnn-Bk] (diagram: what it shows; source path:lines)`). Show a thing before and after a change, side by side, and ask him to predict before he looks.

## 3. What the best-received lessons have in common

- **Small, real blocks with verbatim output,** which he can run or check himself.
- **Predictions he can check** within a minute.
- **Deep vetting of what he got wrong.**
- **No fix or design before the evidence.**
- **Short sentences, and few pointers into other files.** Aim for about 18–21 words a sentence.
- **A size he can finish:** under about 3,000 words of prose, not counting `resources/`.

## 4. Skeleton

```markdown
# Lesson NN · <what he'll be able to do>

**Date:** YYYY-MM-DD. **Your reply:** `../../prompts/RESPONSE-<NN-1>.md`.
**What changed since last time:** <corrections, news; or "first lesson">.

## Part 1 · Your answers, vetted
## Part 2 · <first idea>
## Part 3 · <second idea, if it's needed now>
## Parked
## Questions
1. … (blocks: [LNN-B2], [LNN-B3])
```

## 5. Before you send

- [ ] Every fact in the prose traces to a labelled block, a resource or an F-entry (`../CLAUDE.md` §5).
- [ ] Every block is labelled `**[Lnn-Bk]**`, numbered from 1 with no gaps, and outputs are verbatim, with any cut lines counted.
- [ ] Every concept appears where it's used, and is explained there or left out.
- [ ] No table cell holds more than a few words, and nothing is written in half-sentence fragments.
- [ ] Where a mechanism matters, there's a diagram of it.
- [ ] At most 3 questions; no answer anywhere in the lesson.
- [ ] Every command was run in a scratch copy, and `python3 "$TUTOR_HOME/tools/lint-lesson.py" <lesson>` shows no errors.
- [ ] It's been re-read against his last reply: does it answer what he asked, at the depth he asked?

## Change log

Changes to this spec are made only on his feedback about **Markdown lessons in general** (`REGISTRY.md` §3). Record each change here.

- Version 1.0.0 · Ported from the original tutor system's `general` spec.
