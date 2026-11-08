# Lesson formats: the registry

A **format** is how a lesson is built and presented. Every course declares exactly one in its `COURSE.md` header, and every tutor teaches in that format until Louis changes it. This file lists the formats that exist, and the rules for choosing and changing them.

**The default is `general`, a Markdown lesson.** A course that declares nothing uses it. A tutor never picks another format on its own judgement.

## 1. The formats

**`general`** (stable) · `general.md`
- **Medium:** one Markdown lesson per folder.
- **Use it for:** anything that isn't one of the cases below: fundamentals, an explanation, a code reading.

**`general` with the `casebook` module** (stable) · `general.md` plus `casebook.md`
- **Medium:** a Markdown lesson, plus a casebook he works through with forks of the tutor.
- **Use it when:** he is investigating what's true about a system, and the investigation needs commands.

**`work-through`** (stable) · `work-through.md`
- **Medium:** one Markdown document per build step, which he builds from.
- **Use it when:** he is learning to build something, writing the code himself. A course that comes with a kit of tested guides uses this format, and the kit's guides are its lessons (`work-through.md` §6).

**`guided-project`** (stable) · `guided-project.md`
- **Medium:** Markdown, in a course whose main output is a finished piece of his own work: a feature, a tool, a project.
- **Use it when:** the course exists to get that piece done. Three sliders (hand-holding, education, exploration) set how it runs.

**The `labs` module** (stable) · `labs.md`
- **What it is:** a toggle for any format. A lesson can have a hands-on lab, set up by the tutor.

## 2. Choosing a course's format

1. **A new course starts as `general`** unless his brief names another format, or plainly describes one ("I'm going to build X and want you to walk me through writing it" is `work-through`).
2. **Record the choice in the course's `COURSE.md` header:** the format, the date, and the words of his that set it, or "default".
3. **If his brief points both ways, ask him in one line** before the first lesson. For example: "Do you want this as a Markdown lesson (the default), or as a work-through you build from?"

## 3. Changing formats, and changing this registry

The format system must not change by accident.
- **A course's format changes only when he asks, for that course.** Update the `COURSE.md` header with the date and his words, and note it in the course's `LEARNING-NOTES.md`.
- **A one-lesson exception** (a casebook for one lesson, say) is recorded in that lesson's header and the course notes. It doesn't change the course's format.
- **A format's spec changes only on his feedback about that kind of lesson,** not about one lesson's content.
  - When it's unclear which he means, ask: "Is that about this lesson, this course, or every `<format>` lesson?"
  - The change goes through Tutor Orch (`../CLAUDE.md` §11). Add a dated line to the spec's change log, with his words.
  - Never edit another format's spec on the strength of feedback about this one.
- **The registry itself changes only when he explicitly asks:** adding a format, retiring one, or changing the default. Record each change below and in `../orchestrator/RULES-LOG.md`.
- **A pilot stays a pilot.** A new kind of lesson is tried in one course, under that course's `COURSE.md`, and written into a spec only after he has judged a lesson in it good.
- **When he rejects a lesson,** ask one question about what was wrong before changing anything. Record his answer in the course notes, and, if it's about the format, in the format's spec.

## Change log

- Version 1.0.0 · Ported from the original tutor system's registry: `general`, `casebook`, `work-through` and `labs` as they were, `guided-pr` generalised to `guided-project`. The original's company formats (its development pipeline and pull-request rules) and its suspended `interactive` format weren't ported.
