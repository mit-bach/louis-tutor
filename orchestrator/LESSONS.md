# What the original tutor system learnt the hard way

This harness is ported from a tutor system that ran about twenty courses over three weeks, with an orchestrator auditing it. These are the lessons from those audits, without the people and the projects. Read them before you change a rule, and add your own at the bottom as you learn them.

## Lessons

1. **The first lesson of a new course is the weak one.** Three of the first four courses had their first lesson criticised or rejected, and it happened again later. Each new course rebuilt its format from the rules and then took the student's corrections again. *So Lesson 01 is a gate:* short, standalone, ending with "Is this the shape you want?", and nothing else goes out until he answers.
2. **Lessons pile up unread.** One course sent three lessons in an hour and a half, and none was read. The answer rate to questions fell to zero. *So the next lesson waits for his reply,* answers included.
3. **Corrections spread to every course by accident.** In three days, 26 edits were made to the global rules, each from one course's feedback. A frontend experiment became every course's lesson format that way. *So a correction belongs to its course* unless he says "every course", and you ask when his words point both ways.
4. **One rule kept in three places drifts.** The copies disagreed within days. *So each rule lives in one file;* others link to it.
5. **Lessons had no length budget,** and ranged from under a thousand to almost ten thousand words. The ones he answered ran about 1,000 to 4,000 words, with sentences of 18–21 words. The ones he stopped answering were longer, with longer sentences and many pointers into other files. *So formats have budgets,* and the linter warns.
6. **Verdicts got lost.** "It was pretty bad" lived only in a tutor's conversation, and the next session never saw it. *So every reply and every verdict is saved verbatim first.*
7. **Mechanical drift is measurable; judgement isn't.** A lesson that passed every mechanical check was rejected outright: "this is nowhere near what I need". *So the orchestrator reads each lesson against the brief,* not only the linter.
8. **A brief that lists things to show becomes the lesson's outline.** *So a brief says what he wants to understand.*
9. **What the best-received lessons shared:** small real blocks he ran himself, with verbatim outputs; predictions he could check within a minute; deep vetting of what he got wrong; nothing ahead of the evidence; short sentences.
10. **Untested lessons ship bugs.** A build lesson went out untested, and the student hit three bugs (a lint rule, a deprecated type, a font) that a test run would have caught. *So every command in a lesson is run in a scratch copy first,* and every expected output is pasted from that run.
11. **Prose specs for syntax-heavy files fail beginners.** "Put a db service in compose, with its variables from .env" led to a broken file. *So mechanics are given exactly,* with what each line does; design is his to decide; his own code is built in small checked pieces.
12. **Handing everything over fails too.** "You can't just hand it on a silver platter." *So design decisions are his,* with the facts, and the answer folded until he has written his.
13. **Forks loaded the wrong rules.** Every tutor forked from Tutor Prime ran in one course's folder, so it loaded that course's rules, never its own. *So course rules live in `COURSE.md`, injected by name by the hook, and never inferred from the folder.* And Claude Code reads `.claude/settings.json` only from the folder a session starts in, so each course folder has its own copy of the hook's settings. Courses that lacked it never ran the hook.
14. **A pasted `/compact` isn't a compaction.** It arrives as a plain message, and a fork once read its compaction note as its job. *So compaction goes through Berth.*
15. **Labs copied code instead of linking it.** Half a gigabyte of copied source, none of it under git, so blame and history didn't work. *So a lab's code is a git worktree pinned at a commit, never a copy,* and the tutor sets the lab up, never the student.
16. **Optional questions don't get answered.** A whole build course went by with its questions unanswered, so the only evidence of understanding was the code. *So answers are part of "done".*

## Added in this harness

<!-- Add a lesson here when a change you made taught you something. Date it, and link the RULES-LOG entry. -->
