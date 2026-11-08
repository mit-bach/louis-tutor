#!/usr/bin/env bash
# Create a new course from _template/course.
# Usage:
#   tools/new-course.sh <NN-slug> "<Title>" --session "<session name>" \
#       [--format general|work-through|guided-project] [--asked "<his words>"] [--lab on|off] [--origin "<where this tutor came from>"]
#       guided-project only: --sliders "<hand-holding>,<education>,<exploration>" (each 0-10) [--timebox "<deadline, who waits>"]
# The format defaults to general. Any other format needs --asked with his words (formats/REGISTRY.md §2).
# guided-project needs --sliders (formats/guided-project.md §1). --lab defaults to off (formats/labs.md).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
usage() { sed -n '3,8p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[ $# -ge 2 ] || usage
SLUG="$1"; TITLE="$2"; shift 2
FORMAT="general"; ASKED=""; SESSION=""; ORIGIN="a fork of Tutor Prime"; SLIDERS=""; TIMEBOX="not set"; LAB="off"
while [ $# -gt 0 ]; do
  case "$1" in
    --format) FORMAT="${2:?}"; shift 2 ;;
    --asked) ASKED="${2:?}"; shift 2 ;;
    --session) SESSION="${2:?}"; shift 2 ;;
    --origin) ORIGIN="${2:?}"; shift 2 ;;
    --sliders) SLIDERS="${2:?}"; shift 2 ;;
    --timebox) TIMEBOX="${2:?}"; shift 2 ;;
    --lab) LAB="${2:?}"; shift 2 ;;
    *) usage ;;
  esac
done
[[ "$SLUG" =~ ^[0-9]{2}-[a-z0-9-]+$ ]] || { echo "slug must look like 01-online-store"; exit 1; }
[ -n "$SESSION" ] || { echo "--session is required: the name this course's tutor session has (or will be given in Berth)"; exit 1; }
case "$FORMAT" in REGISTRY|casebook|labs) echo "'$FORMAT' isn't a lesson format: see $ROOT/formats/REGISTRY.md"; exit 1 ;; esac
[ -f "$ROOT/formats/$FORMAT.md" ] || { echo "unknown format '$FORMAT': see $ROOT/formats/REGISTRY.md"; exit 1; }
if [ "$FORMAT" = "general" ]; then
  if [ -n "$ASKED" ]; then FORMAT_SET="his words: \"$ASKED\""; else FORMAT_SET="default"; fi
else
  [ -n "$ASKED" ] || { echo "format '$FORMAT' needs --asked \"<his words>\" (formats/REGISTRY.md §2)"; exit 1; }
  FORMAT_SET="his words: \"$ASKED\""
fi
case "$LAB" in on|off) ;; *) echo "--lab is on or off"; exit 1 ;; esac
EXTRA_ROWS="| **Lab** | $LAB (\`../../formats/labs.md\`) |"
if [ "$FORMAT" = "guided-project" ]; then
  [[ "$SLIDERS" =~ ^([0-9]|10),([0-9]|10),([0-9]|10)$ ]] || { echo "guided-project needs --sliders \"H,E,X\", each 0-10 (formats/guided-project.md §1)"; exit 1; }
  IFS=, read -r H E X <<< "$SLIDERS"
  EXTRA_ROWS="| **Hand-holding** | $H/10 |
| **Education** | $E/10 (topic map: §4) |
| **Exploration** | $X/10 |
| **Time box** | $TIMEBOX |
$EXTRA_ROWS"
elif [ -n "$SLIDERS" ]; then echo "--sliders is only for --format guided-project"; exit 1; fi
DEST="$ROOT/courses/$SLUG"; [ -e "$DEST" ] && { echo "$DEST already exists"; exit 1; }
cp -R "$ROOT/_template/course" "$DEST"
find "$DEST" -name .gitkeep -delete
mkdir -p "$DEST/lessons" "$DEST/prompts"
# The startup hook: Claude Code reads .claude/settings.json only from the folder a session starts in,
# so a tutor started in its course folder needs its own copy. It's the same file as the root's: the hook's
# path is absolute ($HOME/tutor), so it works whatever Claude Code takes as the project folder.
mkdir -p "$DEST/.claude"
cp "$ROOT/.claude/settings.json" "$DEST/.claude/settings.json"
NN="${SLUG%%-*}"; DATE="$(date +%F)"
find "$DEST" -type f -name '*.md' -print0 | while IFS= read -r -d '' f; do
  python3 - "$f" "$NN" "$TITLE" "$DATE" "$ORIGIN" "$FORMAT" "$FORMAT_SET" "$SESSION" "$EXTRA_ROWS" <<'PY'
import sys; p,nn,title,date,origin,fmt,fset,session,extra=sys.argv[1:]
s=open(p).read()
for k,v in {"NN":nn,"TITLE":title,"DATE":date,"ORIGIN":origin,"FORMAT":fmt,"FORMAT_SET":fset,"SESSION":session}.items():
    s=s.replace("{{%s}}"%k,v)
s=s.replace("{{EXTRA_ROWS}}\n", extra+"\n" if extra else "")
open(p,"w").write(s)
PY
done
echo "Created $DEST (format: $FORMAT; session: $SESSION)"
echo "Next:"
echo "  1. fill in $DEST/COURSE.md (the goal in his words, sources, his own files); keep it short"
echo "  2. add the course to $ROOT/README.md's table, with its format and session name"
echo "  3. start its tutor as a Berth session in $DEST, titled \"$SESSION\" (the new-course skill says how)"
echo "  4. check: echo '{\"session_title\":\"$SESSION\",\"cwd\":\"$DEST\"}' | python3 $ROOT/tools/session-context.py | head -6"
