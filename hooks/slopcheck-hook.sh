#!/usr/bin/env bash
# design-antislop PostToolUse hook — advisory, non-blocking.
#
# Runs slopcheck on the file Claude just wrote/edited and, only when it finds a
# HIGH-severity slop signature, surfaces a heads-up. Never blocks (always exits
# 0). Scoped to visual, ux, and copy so it stays quiet on ordinary backend work;
# run `slopcheck --dimension code` or `--strict` separately for the code rules.
#
# stdin: the PostToolUse hook payload (JSON) from Claude Code.
set -u
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL_DIR="$PLUGIN_ROOT/skills/design-antislop"
payload="$(cat)"

file="$(printf '%s' "$payload" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    ti = d.get("tool_input", {}) or {}
    print(ti.get("file_path") or ti.get("path") or "")
except Exception:
    print("")
' 2>/dev/null)"

[ -n "$file" ] && [ -f "$file" ] || exit 0

out="$("$SKILL_DIR/slopcheck" --dimension visual,ux,copy --min-severity high --no-color "$file" 2>/dev/null)"
[ "$?" = "2" ] || exit 0

# Human-readable heads-up (shown in the transcript).
printf 'design-antislop: high-severity slop in %s\n%s\n' "$file" "$out" >&2

# Structured context so Claude notices and fixes it before finishing.
python3 -c '
import json, sys
f = sys.argv[1]
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "slopcheck flagged HIGH-severity AI-slop in " + f +
        ". Run slopcheck on it and fix before finishing."}}))
' "$file" 2>/dev/null || true

exit 0
