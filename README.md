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
| **visual** | 17 (0 high, 3 med, 14 low) | css, scss, less, html, jsx, tsx, vue, svelte, astro | The default look of a generated interface: the same two-stop gradient, the accent strip down the left edge of every card, frosted-glass panels, a glow where an elevation shadow belongs, one radius on everything |
| **ux** | 11 (1 high, 2 med, 8 low) | html, jsx, tsx, vue, svelte, astro | Interfaces that only work when nothing goes wrong: filler text left in place, icon buttons with no accessible name, errors that name no cause and no recovery, lists that render but never handle being empty |
| **copy** | 20 (3 high, 5 med, 12 low) | md, mdx, txt, html (+ jsx/tsx/vue/svelte under `--strict`) | Prose with the register of a press release and the specificity of none: cliche openers, promotional verbs, hedging preambles, clusters of the abstract vocabulary models reach for, claims attributed to nobody |
| **code** | 18 (3 high, 6 med, 9 low) | js, ts, jsx, tsx, py, go, rs, java, rb, php, c, cpp, cs, swift, kt, vue, svelte | Code that was written to look finished: swallowed exceptions, credential-shaped literals, comments marking work that was elided, stub bodies that return nothing real |

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
| `--include-nonshipped` | Also apply structural rules inside `tests/`, `examples/`, `fixtures/`, `docs/` |
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

### What it does not scan

Build output is skipped outright (`node_modules`, `dist`, `target`, and the
rest). Beyond that, the **visual, UX and code rules are skipped inside
non-shipped directories** — `tests/`, `__tests__/`, `spec/`, `fixtures/`,
`examples/`, `samples/`, `demo/`, `stories/`, `snapshots/`, `docs/` — at any
depth. A placeholder in an example file *is* the example, and a fixture is
supposed to look wrong; flagging either is flagging the test rather than the
product.

**Copy rules still run there.** A repeated writing tic in a draft is live prose
no matter which directory holds it, and drafts are where those tics are most
worth catching. Pass `--include-nonshipped` to apply everything everywhere.

This default came out of a hand audit of 741 findings across nine projects and
five public repositories: it removes 62% of total output and drops
high-severity findings from 68 to 16 without losing a single verified true
positive. See [the audit note](#calibration) below.

To exclude a file, put `slopcheck-ignore-file` in a leading comment. The
marker is only honored as a comment at the top of the file, so a file that
merely mentions the string is still scanned.

### Links are not prose

Before any `copy` rule runs, Markdown links and bare URLs are blanked out
(offsets preserved, so line numbers do not move). A link title is usually
someone else's headline and a slug is nobody's prose; two of the four
`copy-promotional-verbs` findings in the September 2026 blind audit were a
promotional verb inside a press-release URL.

### Rules that need a cluster

Four rules describe a pattern that only means something in bulk, and they are
evaluated per paragraph or per file rather than per match:

| rule | fires when |
|---|---|
| `copy-em-dash-density` | em dashes used as sentence asides reach 3 in a paragraph **and** 2 per 100 words. One finding per file, at the densest paragraph. `low` tier since v1.0.4, `--strict` only. |
| `copy-vocabulary-tier2` | 2+ **distinct** terms cluster in one paragraph. Inflections of one word (`showcases` / `showcased` / `showcasing`) count once. |
| `copy-rule-of-three-bold-bullets` | the bold-keyword-colon bullet repeats 3+ times in one list. |
| `copy-binary-contrast` | the `not X, but Y` / `it is not X. It is Y` frame appears **2+ times in one file**. One finding per file, at the first instance, with the count. A single contrast is a rhetorical choice; the blind audit's graders only called it a tic when it recurred. |

The em dash rule counts *prose* dashes only. Markdown leans on the em dash as a
structural separator — `- **Label** — definition`, table cells, checklist
`claim — verdict`, link titles someone else wrote, design-token comments — and
that is ordinary formatting, not an authorship tic. Counting every dash flags it
by the hundred.

These windows live in `slopcheck` rather than in `signatures.json`, because that
file is regenerated from the research pipeline and a regeneration that dropped a
window would quietly turn a cluster rule back into a single-hit rule. A rule's
pattern is research; how its hits are grouped is scanner behaviour.

### Calibration

Severity is a claim about how often a rule is right, and `high` severity fails
builds. Four rules were re-tiered in September 2026 after 240 findings were
opened by hand at `file:line`: `code-todo-stub-comments` and
`visual-colored-left-border-strip` moved to low/high-FP (0% and 3% measured
precision), and `code-hardcoded-secret` and `code-empty-catch-js` came off the
build-breaking tier. For real secret scanning use gitleaks or trufflehog, which
do entropy analysis and provider verification that a regex cannot.

`ux-lorem-ipsum-content` measured at zero but was *only* wrong about location,
so it kept its tier: the non-shipped default above fixes it at the root. Three
more (`code-div-role-button`, `code-dead-branch-if-true`,
`ux-placeholder-as-primary-copy`) had no true positive in the audit and produced
nothing at all on shipped surfaces once the ignore set landed, so they went to
low. Nothing measured supports a tier that appears in the default report.

### What the default report is actually right about

Measured on v1.0.3 against the audit corpus: 5,062 files across nine personal
projects and five public repositories, 205 findings at default settings, 15 of
them high. Every high finding plus 40 drawn at random (seed 20260905) from the
other 190 went to two independent graders who saw only the excerpt with the
flagged span marked. No rule name, no severity, no mention of this tool. The
question was whether a careful editor or code reviewer would ask for the marked
span to change. 54 of the 55 got two verdicts; the one that got a single verdict
was judged fine.

| tier | graded | both graders: change it | at least one grader |
|---|---|---|---|
| high (fails CI) | 15 of 15 | 14 (93%) | 15 (100%) |
| medium (default report) | 40 of 190 | 4 (10%) | 11 (28%) |
| **whole default report, weighted** | | **16%** | **33%** |

By rule, where there were enough findings to say anything:

| rule | graded | both | either | reading |
|---|---|---|---|---|
| `code-bare-except-python` | 14 | 13 | 14 | the high tier is almost entirely this rule, and it earns it |
| `copy-binary-contrast` | 18 | 4 | 11 | graders split 39% of the time: one "not X, it is Y" reads as a choice, three in a document read as a tic |
| `copy-em-dash-density` | 12 | 0 | 0 | see below |
| `copy-ai-vocab-cluster` | 6 | 0 | 0 | dense, sourced paragraphs that happen to use the words |
| `copy-promotional-verbs` | 4 | 0 | 0 | two of the four matched inside a URL |

The em dash result needed a second measurement. The graders were asked a
quality question and answered it: every flagged paragraph was substantive
analysis, and nobody asks a writer to strip dashes out of good analysis. The
rule was meant as a provenance signal, a tell that prose was machine-drafted,
so it got a provenance rubric next: 24 flagged paragraphs and 24 unflagged
control paragraphs from the same files, shuffled together, two graders asked
only whether each one reads as drafted by a language model or by a person.
Flagged paragraphs were called machine-drafted 38% of the time. So were the
controls. Lift of 1.0, grader agreement 60%. Two rubrics, no signal, so as of
v1.0.4 the rule is `low` with `false_positive_risk: high` and appears only
under `--strict`. The corpus is largely machine-drafted research kept on
purpose, which caps what any provenance test can show here, and the controls
ran shorter (71 words against 106); both caveats are real and neither rescues
a lift of 1.0.

`copy-binary-contrast` was re-measured after it became a per-file cluster
rule in v1.0.4. On the same corpus the rule went from 80 findings to 17, and
the 17 went to two fresh graders who saw every instance in the document
marked: 7 of 17 both graders (41%), 12 of 17 at least one (71%), against 22%
and 61% for single instances. Every document with three or more instances
got both graders. Link masking, also v1.0.4, removed the URL false positives
from `copy-promotional-verbs` (14 findings to 9 on this corpus).

With the em dash rule out of the default report, the v1.0.4 default run on
the same corpus is 61 findings rather than 205, 15 of them high. That is
small enough to grade as a census, so all 61 went to two fresh graders under
the same protocol:

| tier | graded | both graders: change it | at least one grader |
|---|---|---|---|
| high (fails CI) | 15 of 15 | 10 (67%) | 14 (93%) |
| medium (default report) | 46 of 46 | 12 (26%) | 23 (50%) |
| **whole default report** | 61 of 61 | **22 (36%)** | **37 (61%)** |

| rule | findings | both | either | reading |
|---|---|---|---|---|
| `copy-binary-contrast` | 17 | 11 | 15 | the cluster version, second pair of graders: 65% strict, 88% lenient |
| `code-bare-except-python` | 14 | 9 | 13 | same 14 findings as v1.0.3; this pair of graders read four "best-effort cleanup" excepts as acceptable |
| `copy-promotional-verbs` | 9 | 0 | 0 | what is left after link masking is the verb used literally in changelogs and design notes, and a 401(k) provider whose company name is one of the verbs |
| `copy-ai-vocab-cluster` | 9 | 0 | 3 | dense, sourced paragraphs that happen to use the words |
| `code-empty-catch-js` | 8 | 1 | 5 | graders split on whether an empty catch around `localStorage` or `JSON.parse` is a choice |

The whole default report went from 16% to 36% strict and 33% to 61%
lenient between v1.0.3 and v1.0.4. The high tier's strict number moved from
93% to 67% on the same 15 findings with a different pair of graders, which
is a grader-variance number, not a change in the tool: at least one grader
still wanted 14 of 15 changed in both rounds. Pairs of graders agreed with
each other 74% of the time in this round.

`copy-promotional-verbs` went to `low` with `false_positive_risk: high` in
v1.0.5 on the strength of that 0 of 9: the URL matches were gone after link
masking and nothing that remained was a finding either grader wanted changed.
It runs under `--strict`. Without it the v1.0.4 default report on the same
corpus is 52 findings.

In the v1.0.3 round graders agreed with each other 84% of the time overall
and 61% on `copy-binary-contrast`. The second grader saw the items batched and shuffled
differently from the first, so disagreement is real subjectivity rather than a
batch effect. The sample packets contain excerpts from private projects and are
not in the repo; the method above is enough to reproduce the measurement on any
corpus.

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
scans every file Claude writes and surfaces what it finds in the transcript.

Be clear about how little that hook does, because the scoping is deliberate. It
runs `--dimension visual,ux,copy --min-severity high`, and **no visual signature
carries high severity**, so the visual leg never fires. In practice the hook is
four rules: one UX (`ux-lorem-ipsum-content`) and three copy. On `.css`, `.py`,
`.rs`, `.ts` and `.js` it is a no-op by construction. That is the intended
trade — a hook that speaks on every write is a hook people mute — but it is not
the safety net "visual, UX and copy protection" would imply. The real coverage
is `slopcheck` in CI or run by hand. See [hooks/README.md](hooks/README.md).

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

33 tests, stdlib only, no install step. They cover the exit-code contract, the
JSON shape, dimension and severity filtering, ignore-marker semantics in both
directions, directory traversal, and a structural pass over the whole ruleset
that checks for duplicate ids, invalid enum values, patterns that do not
compile, and patterns that depend on case the tool never gives them. Those
last ones are the guard that makes the quarterly ruleset merge safe; writing
them turned up a shipped rule that was matching ordinary English words.

`tests/fixtures/` holds paired files: `slop_*` must trip specific rule ids,
`clean_*` must stay silent even under `--strict --min-severity low`. The clean
fixtures are the false-positive guard, and they are the more important half.

CI runs the suite on Python 3.9, 3.11, and 3.13, plus the self-scan below,
`claude plugin validate --strict`, and an inverted check that fails if the slop
fixtures ever come back clean.

## What it scans on itself

`slopcheck` runs clean on this repo, and the caveats matter far more than the
result. Here is the honest accounting.

Six files are excluded by a leading `slopcheck-ignore-file` comment, because
their subject matter *is* the slop patterns and they quote every trigger phrase
verbatim: `playbook.md`, `SIGNATURES.md`, `SKILL.md`, `checklist.md`,
`explainer.html`, and `hooks/README.md`. Scanned without the marker they
produce 93 findings, every one of them quoted rule content.

Of what remains, `signatures.json` and `hooks.json` are JSON, `slopcheck-hook.sh`
is shell, and `slopcheck` itself has no extension. None of those map to a
dimension, so none are scanned. `tests/fixtures/` is deliberate slop and is
meant to fail.

That leaves exactly one file: this README. The CI self-scan step is therefore a
prose gate on this page and nothing more, which is why it runs at
`--strict --min-severity low`. "Clean" here is close to a tautology and is not
offered as evidence of anything. Point it at your own project instead.

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
