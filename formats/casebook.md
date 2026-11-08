# Module: the casebook (an investigation track)

**Status:** stable. **Used with:** `general`.

Use a casebook when Louis is investigating what's true about a system (why a query is slow, why a page shows the wrong number), and the investigation needs commands: queries, greps, the running app. The lesson stays free of commands, and the casebook holds them. He works through it with **forks of the tutor**, in small steps, learning rather than offloading. A one-shot dossier of everything at once doesn't work: it isn't adaptive.

---

## 1. Layout

```
lessons/NN/
  NN-lesson-<topic>.md      the lesson (general.md)
  NN-casebook.md            the casebook
  casebook/LEDGER.md        append-only findings, one entry per mission run
  resources/                verbatim evidence the casebook cites
```

## 2. What the casebook contains

1. **How a fork starts, and the rules it follows:**
   - one mission at a time;
   - a checkpoint question for him before each query, which he answers first;
   - queries and outputs verbatim;
   - read-only;
   - never pick the fix;
   - hand back when access or a decision is needed.
2. **The instruments:** each tool (the repo, a database, the running app, logs), what it can see, and what it can't.
3. **A ladder of missions.** Each mission has its question, prerequisites, instrument, a starter query, what to look for, its checkpoint, and what to record. Add a rule for picking the next mission.
4. **What's known,** and **the board:** the claims under test (his and anyone else's), each with its status.
5. **A ledger template,** and the instruments' pitfalls.

## 3. When he asks a fork to run the investigation itself

That's his call. The fork records the request in the ledger, keeps every query and output verbatim so he can read the work afterwards, and the checkpoint questions then apply to what he does himself.

## Change log

- Version 1.0.0 · Ported from the original tutor system's casebook module.
