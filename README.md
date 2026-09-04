# design-antislop

A fast deterministic gate against AI slop: the generic, cookie-cutter defaults
that make generated output read as machine-made across **visual design, UX,
copy, and code**. Style-agnostic, dependency-free, and advisory.

It is a gate, not the review. It catches the tells a regex can catch, in
milliseconds, so human review can spend its attention somewhere else.

## Two layers

1. **Prevention** ([playbook.md](skills/design-antislop/playbook.md)): 52 ranked "the slop / do instead
   / why" rules to steer new work, plus the one rule above all: decide palette,
   type, and voice in a `DESIGN.md` before generating.
2. **Detection** (`slopcheck` + [signatures.json](skills/design-antislop/signatures.json)):
   a dependency-free Python 3 CLI that scans built output for 66
   machine-detectable slop signatures ([SIGNATURES.md](skills/design-antislop/SIGNATURES.md)).

## Quick start

```bash
# from a project root
path/to/design-antislop/skills/design-antislop/slopcheck src/
```

Shows medium-and-up findings and hides high-false-positive rules. Add `--strict`
for the full sweep, `--dimension visual,ux,copy` to scope it, `--json` for CI,
`--list` to inspect the ruleset. Exit code `2` means at least one high-severity
finding, which makes it usable as a CI gate.

## Install

As a Claude Code plugin:

```bash
/plugin marketplace add anthropics/claude-plugins-community
/plugin install design-antislop
```

Or register the skill directly:

```bash
git clone https://github.com/cschuman/design-antislop.git
ln -sfn "$PWD/design-antislop/skills/design-antislop" ~/.claude/skills/design-antislop
```

Either way `/design-antislop` becomes available, and `slopcheck` runs standalone
from any shell with Python 3.

## Files

| Path | What it is |
|---|---|
| `skills/design-antislop/SKILL.md` | The skill entry (invocation + how the two layers work) |
| `skills/design-antislop/playbook.md` | 52 prevention rules |
| `skills/design-antislop/checklist.md` | Pre-ship gate, house-style, `slopcheck` is item 0 |
| `skills/design-antislop/signatures.json` | The 66-signature ruleset the detector loads |
| `skills/design-antislop/SIGNATURES.md` | Human-readable table of every signature |
| `skills/design-antislop/slopcheck` | The detector CLI (Python 3 stdlib, no deps) |
| `skills/design-antislop/explainer.html` | Standalone browsable page for the full ruleset |
| `hooks/` | PostToolUse hook, on by default when installed as a plugin |
| `.claude-plugin/plugin.json` | Plugin manifest |

## What it scans on itself

`slopcheck` runs clean on this repo, with a caveat worth stating plainly: six
files are excluded by a leading `slopcheck-ignore-file` comment, because their
subject matter *is* the slop patterns and they quote every trigger phrase
verbatim. Those are `playbook.md`, `SIGNATURES.md`, `SKILL.md`, `checklist.md`,
`explainer.html`, and `hooks/README.md`. Scanned without the marker they produce
93 findings, all of them quoted rule content.

The marker is honored only when it stands alone as a leading comment, so a file
that merely mentions the string is still scanned.

## Regenerating the ruleset

The signatures and playbook come from a 12-finder research sweep across GitHub,
Reddit, and design writing (first sweep 2026-08-18). Slop tells change fast, so
it is re-run quarterly, and each sweep is merged into the shipped ruleset rather
than replacing it, which is why the counts are cumulative.

The sweep itself runs on maintainer-only tooling and is not part of this
repository. Rule proposals are welcome as issues and are folded in at the
quarterly refresh.

## Related

Paul Bakaus's Impeccable covers a wider surface and is also free. This one is narrower on purpose: one file, no dependencies, exit
codes, fast enough to run on every write.

## Maintenance

Solo maintainer, best-effort, no SLA. Issues and rule proposals are triaged at
the quarterly refresh.

Heuristics, not laws. slopcheck is advisory. Human judgment ships.

## License

MIT. See [LICENSE](LICENSE).
