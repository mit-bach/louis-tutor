# Installing the harness, for your agent

**Agent:** you're installing Louis's tutor harness, in a chat that runs inside cmux with Berth already installed (its `berth` and `cmux-mcp` MCP servers connected). Explain each step to him in plain words, and ask before anything that changes his Mac.

1. **Clone it to `~/tutor`,** where it stays for good: `git clone https://github.com/mit-bach/louis-tutor ~/tutor`. If `~/tutor` already exists, ask him what it is, and if it's this harness, `git -C ~/tutor pull` instead.
2. **Run the self-check:** `python3 ~/tutor/tools/check-harness.py`. It works in a temporary copy, and must end with "Everything passed." If it doesn't, stop and tell him which check failed.
3. **Make the Berth folder `Tutor`,** through the `berth` MCP.
4. **Start Tutor Orch:** a new Claude session through the `berth` MCP's `create`, with `cwd` `~/tutor`, `title` "Tutor Orch", filed in `Tutor`. Its job is in `orchestrator/ORCHESTRATOR.md`, and the startup hook tells it so.
5. **Start and prime Tutor Prime:** another new session, `cwd` `~/tutor`, `title` "Tutor Prime", filed in `Tutor`. Send it this prompt, with his yes:

   > You're Tutor Prime, the session every tutor in this harness is forked from. Read these from disk, in full: CLAUDE.md, README.md, formats/REGISTRY.md and every spec in formats/, student/PROFILE.md, orchestrator/ROLES.md and orchestrator/LESSONS.md. Then say in five lines what you'll do as a tutor, and wait. Don't teach here and don't start a course here: every fork of you inherits this conversation.

6. **Check the hook names both:** `berth sessions` shows them in `Tutor`. In each one, the first message says "has the role **Tutor Orch**" or "**Tutor Prime**".
7. **Have him fill in `student/PROFILE.md`** §1, §2 and §4 with Tutor Orch, in his own words.
8. **Tell him how to start a course:** open "Tutor Orch" and say what he wants to learn. Its `new-course` skill does the rest.
