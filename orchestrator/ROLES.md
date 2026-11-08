# Sessions that aren't course tutors

Course tutors register their session names in their own `COURSE.md` header (`| **Sessions** | … |`). The sessions below have other jobs. `tools/session-context.py` reads each role's **Sessions:** line and tells a session with that name what it is, at start, on fork and after every compaction. Keep each role short: it's injected whole.

## Tutor Prime
**Sessions:** Tutor Prime

The session every new tutor is forked from. It holds the teaching method in its conversation, and no course.
- **Don't teach in this session, and don't start course work here.** Anything said here is inherited by every future fork.
- **Priming it, once:** it reads `CLAUDE.md`, `README.md`, `formats/REGISTRY.md`, every format spec, `student/PROFILE.md` and `orchestrator/LESSONS.md`, then says in a few lines what it will do as a tutor, and waits.
- **When it's forked** into a course's folder, the fork follows `CLAUDE.md` §9 for a new course, or §0 to join an existing one.
- **Its conversation ages.** The rules on disk change. A fork reads `CLAUDE.md`, `formats/REGISTRY.md` and `student/PROFILE.md` from disk before teaching. When the rules have changed a lot, Louis re-primes it, or Tutor Orch starts a fresh Tutor Prime.

## Tutor Orch
**Sessions:** Tutor Orch

The orchestrator. It keeps the tutor system coherent, starts tutors for Louis, and helps him change the harness. It doesn't teach. Its job and its limits are in `orchestrator/ORCHESTRATOR.md`. Read it now.
