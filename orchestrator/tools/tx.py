#!/usr/bin/env python3
"""Condense a Claude Code session transcript (.jsonl) into readable lines.

usage: python3 tx.py FILE [--since ISO] [--until ISO] [--users] [--reads] [--edits]
                          [--grep REGEX] [--full] [--max N]

  default   one line per event: time, kind, short content
            kinds: USER (his typed text), ASSIST (assistant text), TOOL (tool call),
                   COMPACT (a compaction boundary/summary), RULES (a CLAUDE.md or other rules file loaded)
  --users   only USER lines, full text (his words, verbatim)
  --reads   only Read/cat-style file reads (path), to see what the session read
  --edits   only Write/Edit calls (path + old/new excerpt)
  --grep    keep only events whose text matches REGEX (case-insensitive)
  --full    don't truncate assistant text or tool inputs
  --max N   truncate each line to N chars (default 400; ignored with --full)
"""
import json, re, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--since"); ap.add_argument("--until")
ap.add_argument("--users", action="store_true")
ap.add_argument("--reads", action="store_true")
ap.add_argument("--edits", action="store_true")
ap.add_argument("--grep")
ap.add_argument("--full", action="store_true")
ap.add_argument("--max", type=int, default=400)
a = ap.parse_args()
rx = re.compile(a.grep, re.I) if a.grep else None
RULES = re.compile(r"Contents of (/\S*?CLAUDE\.md)")

def cut(s):
    s = s.replace("\n", " ⏎ ")
    return s if a.full or len(s) <= a.max else s[: a.max] + " …"

def emit(ts, kind, text):
    if rx and not rx.search(text):
        return
    print(f"{(ts or '')[:19]} {kind:7} {text if kind == 'USER' and a.users else cut(text)}")

for line in open(a.file, errors="replace"):
    try:
        d = json.loads(line)
    except Exception:
        continue
    ts = d.get("timestamp") or ""
    if a.since and ts and ts < a.since: continue
    if a.until and ts and ts > a.until: continue
    t = d.get("type")
    if t == "attachment":
        # Newer Claude Code records the rules files it loaded as an attachment, not as text:
        # "instructions" at session start, "nested_memory" when a subfolder's CLAUDE.md loads later.
        att = d.get("attachment") or {}
        if att.get("type") in ("instructions", "nested_memory") and not (a.users or a.reads or a.edits):
            files = att.get("files") or ([att] if att.get("path") else [])
            for f in files:
                if f.get("path"):
                    emit(ts, "RULES", f["path"] + ("" if att.get("type") == "instructions" else "  (loaded later, from a subfolder)"))
        continue
    if t == "system" and d.get("subtype") == "compact_boundary":
        if not (a.users or a.reads or a.edits): emit(ts, "COMPACT", "---- compaction boundary ----")
        continue
    msg = d.get("message") or {}
    content = msg.get("content")
    if t == "user":
        if d.get("isCompactSummary"):
            if not (a.users or a.reads or a.edits):
                emit(ts, "COMPACT", "summary: " + (content if isinstance(content, str) else json.dumps(content))[:3000])
            continue
        texts = []
        if isinstance(content, str):
            texts = [content]
        elif isinstance(content, list):
            for c in content:
                if c.get("type") == "text":
                    texts.append(c.get("text", ""))
        for tx in texts:
            for m in RULES.findall(tx):
                if not (a.users or a.reads or a.edits): emit(ts, "RULES", m)
            clean = re.sub(r"<system-reminder>.*?</system-reminder>", "", tx, flags=re.S).strip()
            if not clean or clean.startswith("<local-command") or clean.startswith("Caveat:"):
                continue
            if clean.startswith("Base directory for this skill"):
                if not (a.reads or a.edits): emit(ts, "SKILL", clean.splitlines()[0])
                continue
            if clean.startswith("[Image:"):
                if not (a.reads or a.edits): emit(ts, "IMAGE", clean[:80])
                continue
            if a.reads or a.edits: continue
            emit(ts, "USER", clean)
    elif t == "assistant" and isinstance(content, list):
        for c in content:
            ct = c.get("type")
            if ct == "text" and not (a.users or a.reads or a.edits):
                emit(ts, "ASSIST", c.get("text", ""))
            elif ct == "tool_use":
                name, inp = c.get("name"), c.get("input", {})
                if a.users: continue
                if a.reads:
                    if name == "Read":
                        emit(ts, "READ", inp.get("file_path", ""))
                    elif name == "Bash" and re.search(r"\b(cat|sed -n|head|tail|less)\b", inp.get("command", "")):
                        emit(ts, "READ", "bash: " + inp.get("command", ""))
                    continue
                if a.edits:
                    if name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
                        p = inp.get("file_path", "")
                        body = inp.get("new_string") or inp.get("content") or json.dumps(inp.get("edits", ""))
                        old = inp.get("old_string", "")
                        emit(ts, "EDIT", f"{name} {p} | old: {old[:300]} | new: {body}")
                    elif name == "Artifact":
                        emit(ts, "EDIT", f"Artifact {json.dumps(inp)[:600]}")
                    continue
                if name == "Bash":
                    s = "Bash: " + inp.get("command", "")
                elif name in ("Read", "Write", "Edit"):
                    s = f"{name}: {inp.get('file_path','')}"
                elif name == "Agent":
                    s = f"Agent[{inp.get('subagent_type','')}]: {inp.get('description','')} :: {inp.get('prompt','')}"
                else:
                    s = f"{name}: {json.dumps(inp)}"
                emit(ts, "TOOL", s)
