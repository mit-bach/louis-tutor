# Labs: the hands-on part of a lesson, on real git

**Status:** stable. **Used with:** any format. A lab is a toggle: a course's `COURSE.md` says `Lab: on` or `off`, and each lesson's header says which lab it uses, or `Lab: none`.

Labs make learning faster when they're done right. In the original tutor system they went wrong in three ways: they were scattered across folders, they copied source code instead of linking it (so `git log` and `git blame` didn't work), and the first lab was almost always too big and had to be steered.

---

## 1. Where labs live

```
~/tutor/labs/
  README.md                  one row per lab: course, lessons, type, pinned commit, status
  <NN-course>/
    LAB.md                   what this lab is: its type, its pinned commit, how to run it, which lessons use it
    work/                    the tutor's runner, helpers, checks and skeletons, plus his own files.
                             Its own local git repo, so his work has history too
```

- **Code to read or run against is a pin,** never a copy: a detached git worktree of the repository at a named commit (`git -C <repo> worktree add --detach ~/tutor/labs/pins/<short-sha> <sha>`). It shares the repository's history, so `git log` and `git blame` work, and line links stay stable. Never edit a pin.
- **Pins are shared.** A new lab reuses the newest pin unless the lesson needs newer code. Then it adds a new pin rather than moving an old one, so older lessons keep their line numbers.
- **Remove a pin** (`git worktree remove`) once no lesson links to it.
- **Nothing private lives in a lab:** no passwords, keys or personal data.

## 2. The kinds of lab

- **Read:** code to read and cite, with stable line numbers. A pin, plus `LAB.md`.
- **Exercise:** the code at a pin, plus the tutor's runner, helpers, checks and a skeleton of each file he writes, all in `work/`.
- **Running app:** his app, run on its own ports in its own containers, with a database chosen for the lesson. `LAB.md` records the ports, the compose project name and the database.
- **His own repo:** a project he owns. It stays where it is, and the lab folder holds a `LAB.md` that points to it. The tutor never writes in it (`../CLAUDE.md` §10).

## 3. Building a lab

- **You set up the lab; he never does.** There's no reason to make him do manual set-up work before he can start learning.
- **Build the first lab small.** Build only what the first step needs, run it, and show him before you build more. Steer by his reaction.
- **A lab serves a step of the lesson.** Every file in it is used by a step, and the lesson says why it exists at the point it's used. Never build machinery the lesson doesn't need.
- **Test it where it lives.** Run its smoke test at its real path before he opens the lesson, and check that every link into it resolves. The lesson starts from "your lab is ready", with one command that proves it.
- **Never overwrite a file he wrote.** His files are committed in `work/`'s git, so his history is safe.

## Change log

- Version 1.0.0 · Ported from the original tutor system's labs module, with its company tooling (shared pins folder, development stack, stewards) replaced by plain git worktrees.
