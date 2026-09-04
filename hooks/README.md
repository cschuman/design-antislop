<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->

# design-antislop hook (opt-in)

`slopcheck-hook.sh` runs `slopcheck` automatically on every file Claude writes or
edits, and surfaces a heads-up **only** when it finds a HIGH-severity slop
signature. It never blocks (always exits 0). A HIGH match is a near-certain tell
(`in today's fast-paced world`, `harness the power of`, empty catch / bare
except, lorem ipsum, hardcoded secret).

## Why it is opt-in, not global

Some HIGH code rules (empty catch, bare except) fire on normal backend work, so
wiring this into your **global** `~/.claude/settings.json` would nag during
non-design coding. Enable it **per project** where you care about slop, in that
project's `.claude/settings.json`.

## Enable it in a project

Add to `<project>/.claude/settings.json` (merge into any existing `hooks` block):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/Projects/design-antislop/hooks/slopcheck-hook.sh"
          }
        ]
      }
    ]
  }
}
```

That is it. Edit a file with a HIGH slop tell and you will see a
`design-antislop:` heads-up in the transcript, and Claude gets a nudge to fix it.

## Tune it

- **Catch more:** edit the hook and change `--min-severity high` to `medium`
  (noisier, more coverage).
- **Design files only:** the script already exits silently on non-existent paths;
  to scope by type, add a guard on `$file`'s extension near the top.
- **CI instead of a hook:** skip this and run `slopcheck --json` in a CI step;
  exit code `2` fails the build on any high-severity finding.

## Disable it

Remove the block above from the project's `.claude/settings.json`. Nothing else
persists.
