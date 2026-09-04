# design-antislop

[![CI](https://github.com/cschuman/design-antislop/actions/workflows/ci.yml/badge.svg)](https://github.com/cschuman/design-antislop/actions/workflows/ci.yml)
[![plugin validate](https://github.com/cschuman/design-antislop/actions/workflows/plugin-validate.yml/badge.svg)](https://github.com/cschuman/design-antislop/actions/workflows/plugin-validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![signatures](https://img.shields.io/badge/signatures-66-8a5cf6)](skills/design-antislop/SIGNATURES.md)
[![dependencies](https://img.shields.io/badge/dependencies-none-3f8f5f)](skills/design-antislop/slopcheck)

A fast deterministic gate against AI slop: the generic, cookie-cutter defaults
that make generated output read as machine-made across **visual design, UX,
copy, and code**. Style-agnostic, dependency-free, and advisory.

It is a gate, not the review. It catches the tells a regex can catch, in
milliseconds, so human review can spend its attention somewhere else.

📖 **[The field guide](https://cschuman.github.io/design-antislop/)** walks
through every rule and the reasoning behind it.

## What it looks like

Run it against the test fixtures in this repo and you get exactly this:

```console
$ slopcheck tests/fixtures/slop_visual.html tests/fixtures/slop_ux.html tests/fixtures/slop_code.py

tests/fixtures/slop_code.py
  HIGH  code-bare-except-python  L5
        “except Exception: pass”
        → Catch specific exception types and log/handle each.

tests/fixtures/slop_ux.html
  HIGH  ux-lorem-ipsum-content  L3
        “Lorem ipsum”
        → Replace with real copy before shipping.

tests/fixtures/slop_visual.html
  MED   visual-purple-pink-gradient-tw  L2
        “bg-gradient-to-r from-purple-500 to-pink-500”
        → Replace with a brand-specific two-color pairing defined in tailwind.config, or drop the gr
  MED   visual-neon-glow-card-border  L3
        “box-shadow: 0 0 24px 2px #a855f7”
        → Use a subtle elevation shadow in a brand-neutral color instead of a saturated neon glow.

slopcheck: 4 findings (2 high, 2 medium, 0 low) across 3 files.
  (medium+ shown; high-false-positive rules hidden — add --strict for the full sweep)

$ echo $?
2
```

Every finding carries a rule id, a line, the matched text, and an instruction.
No finding is ever just a complaint.

## What it catches

The ruleset is 66 signatures across four dimensions. Each dimension only runs
against the file types it can say something about, so a `.py` file is never
graded on gradients.

| Dimension | Signatures | Runs against | The kind of thing it flags |
|---|---|---|---|
| **visual** | 17 (0 high, 4 med, 13 low) | css, scss, less, html, jsx, tsx, vue, svelte, astro | The default look of a generated interface: the same two-stop gradient, the accent strip down the left edge of every card, frosted-glass panels, a glow where an elevation shadow belongs, one radius on everything |
| **ux** | 11 (1 high, 3 med, 7 low) | html, jsx, tsx, vue, svelte, astro | Interfaces that only work when nothing goes wrong: filler text left in place, icon buttons with no accessible name, errors that name no cause and no recovery, lists that render but never handle being empty |
| **copy** | 20 (3 high, 7 med, 10 low) | md, mdx, txt, html (+ jsx/tsx/vue/svelte under `--strict`) | Prose with the register of a press release and the specificity of none: cliche openers, promotional verbs, hedging preambles, clusters of the abstract vocabulary models reach for, claims attributed to nobody |
| **code** | 18 (5 high, 7 med, 6 low) | js, ts, jsx, tsx, py, go, rs, java, rb, php, c, cpp, cs, swift, kt, vue, svelte | Code that was written to look finished: swallowed exceptions, credential-shaped literals, comments marking work that was elided, stub bodies that return nothing real |

Severity is about consequence, not confidence. `high` means never ship it;
`medium` means it is almost always wrong; `low` means it is worth a look.
Confidence is tracked separately as `false_positive_risk`, and rules marked
high-risk stay hidden until you pass `--strict`.

The full table, with every pattern and its fix, is in
[SIGNATURES.md](skills/design-antislop/SIGNATURES.md) or the
[field guide](https://cschuman.github.io/design-antislop/).

## Two layers

1. **Prevention** ([playbook.md](skills/design-antislop/playbook.md)): 52 ranked "the slop / do instead
   / why" rules to steer new work, plus the one rule above all: decide palette,
   type, and voice in a `DESIGN.md` before generating.
2. **Detection** (`slopcheck` + [signatures.json](skills/design-antislop/signatures.json)):
   a dependency-free Python 3 CLI that scans built output for 66
   machine-detectable slop signatures.

## Quick start

```bash
# from a project root
path/to/design-antislop/skills/design-antislop/slopcheck src/
```

Shows medium-and-up findings and hides high-false-positive rules.

| Flag | What it does |
|---|---|
| `--strict` | Include rules with a high false-positive risk, and scan JSX/TSX/Vue/Svelte for copy slop |
| `--min-severity low\|medium\|high` | Threshold to report at. Default `medium` |
| `--dimension visual,ux,copy,code` | Scope the run. Comma-separated |
| `--json` | Machine-readable output: `scanned`, `findings[]`, `summary` |
| `--list` | Print the active ruleset instead of scanning |
| `--no-color` | Drop ANSI codes, for logs and CI |
| `--signatures PATH` | Load a different ruleset file |

Exit codes are the contract: `0` clean, `1` findings below high, `2` at least
one high-severity finding, `3` the signatures file could not be read. So the
CI gate is just the exit status.

```yaml
- name: Check for slop
  run: slopcheck --no-color --min-severity high src/
```

To exclude a file, put `slopcheck-ignore-file` in a leading comment. The
marker is only honored as a comment at the top of the file, so a file that
merely mentions the string is still scanned.

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
from any shell with Python 3. Installed as a plugin, a `PostToolUse` hook also
runs the visual, UX, and copy rules at high severity against every file Claude
writes, and surfaces anything it finds in the transcript. See
[hooks/README.md](hooks/README.md) to change or disable that.

## Files

| Path | What it is |
|---|---|
| `skills/design-antislop/SKILL.md` | The skill entry (invocation + how the two layers work) |
| `skills/design-antislop/playbook.md` | 52 prevention rules |
| `skills/design-antislop/checklist.md` | Pre-ship gate, house-style, `slopcheck` is item 0 |
| `skills/design-antislop/signatures.json` | The 66-signature ruleset the detector loads |
| `skills/design-antislop/SIGNATURES.md` | Human-readable table of every signature |
| `skills/design-antislop/slopcheck` | The detector CLI (Python 3 stdlib, no deps) |
| `skills/design-antislop/explainer.html` | Source for the field guide page |
| `hooks/` | PostToolUse hook, on by default when installed as a plugin |
| `tests/` | Fixture suite and runner |
| `.claude-plugin/plugin.json` | Plugin manifest |

## Tests

```bash
python3 tests/run_tests.py
```

30 tests, stdlib only, no install step. They cover the exit-code contract, the
JSON shape, dimension and severity filtering, ignore-marker semantics in both
directions, directory traversal, and a structural pass over the whole ruleset
that checks for duplicate ids, invalid enum values, and patterns that do not
compile. That last one is the guard that makes the quarterly ruleset merge
safe.

`tests/fixtures/` holds paired files: `slop_*` must trip specific rule ids,
`clean_*` must stay silent even under `--strict --min-severity low`. The clean
fixtures are the false-positive guard, and they are the more important half.

CI runs the suite on Python 3.9, 3.11, and 3.13, plus the self-scan below,
`claude plugin validate --strict`, and an inverted check that fails if the slop
fixtures ever come back clean.

## What it scans on itself

`slopcheck` runs clean on this repo, and the caveats matter more than the
result.

Six files are excluded by a leading `slopcheck-ignore-file` comment, because
their subject matter *is* the slop patterns and they quote every trigger phrase
verbatim: `playbook.md`, `SIGNATURES.md`, `SKILL.md`, `checklist.md`,
`explainer.html`, and `hooks/README.md`. Scanned without the marker they
produce 93 findings, every one of them quoted rule content.

`tests/fixtures/` is deliberate slop and is meant to fail. That is why the CI
self-scan targets `skills hooks README.md` rather than the repo root.

What is left is a thin scannable surface, so "clean" here is a weak claim and
is not offered as evidence of anything. Point it at your own project instead.

## Regenerating the ruleset

The signatures and playbook come from a 12-finder research sweep across GitHub,
Reddit, and design writing (first sweep 2026-08-18). Slop tells change fast, so
it is re-run quarterly, and each sweep is merged into the shipped ruleset rather
than replacing it, which is why the counts are cumulative.

The sweep itself runs on maintainer-only tooling and is not part of this
repository. Rule proposals are welcome as issues and are folded in at the
quarterly refresh.

## Contributing

The most useful thing you can send is a false positive: a real file that a rule
fires on wrongly. That is what sets the precision bound. See
[CONTRIBUTING.md](CONTRIBUTING.md) for what a rule proposal needs, and
[SECURITY.md](SECURITY.md) for what this tool does on your machine and how to
report a vulnerability.

## Related

Paul Bakaus's Impeccable covers a wider surface and is also free. This one is
narrower on purpose: one file, no dependencies, exit codes, fast enough to run
on every write.

## Maintenance

Solo maintainer, best-effort, no SLA. Issues and rule proposals are triaged at
the quarterly refresh.

Heuristics, not laws. slopcheck is advisory. Human judgment ships.

## License

MIT. See [LICENSE](LICENSE).
