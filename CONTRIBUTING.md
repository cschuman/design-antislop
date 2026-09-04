# Contributing

This is a solo-maintained project. Contributions are welcome, triage is
best-effort, and there is no SLA. The most useful thing you can send is
evidence, not a patch.

## What a good contribution looks like

The ruleset lives or dies on precision. A rule that fires on real, careful
work is worse than no rule at all, because it teaches people to ignore the
tool. So the bar for adding a signature is deliberately high, and the bar for
reporting a false positive is deliberately low.

### Reporting a false positive

This is the highest-value report. Open a **False positive** issue with the
smallest file that triggers it and the rule id from the output. If you cannot
share the file, a redacted line that still trips the rule is enough:

```bash
slopcheck --no-color --json path/to/file
```

Every confirmed false positive gets one of three outcomes: the pattern is
tightened, the rule's `false_positive_risk` is raised to `high` so it only
fires under `--strict`, or the rule is removed.

### Proposing a rule

Open a **Rule proposal** issue. A proposal needs four things:

1. **The pattern**, as a regex or a literal string.
2. **Two or three real examples** of it in shipped work. Generated samples are
   not evidence; the point of the ruleset is that these patterns show up in
   the wild.
3. **A counter-example**: text or code that contains something close to the
   pattern and is *not* slop. This is what sets the precision bound.
4. **The fix**, in one sentence, phrased as an instruction. Every signature
   carries a `fix` string, and a rule that cannot say what to do instead is
   not ready.

Proposals without a counter-example usually get sent back for one, so it is
worth including up front.

## Working on the code

`slopcheck` is a single Python 3 file with no dependencies. That is a design
constraint, not an accident: it has to run inside a `PostToolUse` hook on a
machine you do not control. Do not add a dependency, and do not split it into
a package.

```bash
python3 tests/run_tests.py           # the fixture suite
./skills/design-antislop/slopcheck skills hooks README.md   # self-scan
```

Both run in CI on every push, along with `claude plugin validate --strict`.

### If you change detection behavior

Add a fixture. `tests/fixtures/` holds paired files: `slop_*` must trip
specific rule ids, `clean_*` must stay silent even under
`--strict --min-severity low`. The clean fixtures are the false-positive
guard, and they matter more than the slop ones.

Note that the fixture directory contains deliberate slop. The self-scan step
in CI targets `skills hooks README.md` for exactly that reason.

### If you change the ruleset

`signatures.json` is regenerated from the research pipeline at the quarterly
refresh, and refreshes are merge-only. A hand-edit that the merge does not
know about will be lost. If you are proposing a rule, the issue is the durable
artifact; the JSON edit is not.

`tests/run_tests.py` validates the whole ruleset structurally on every run:
unique ids, valid dimension and severity values, compiling patterns, and ids
prefixed with their dimension. That suite is what makes the quarterly merge
safe, so keep it passing.

## Commit and PR

Small, focused commits. Explain in the PR what the change does to precision:
which rule, what it now catches, and what it no longer catches. If a PR
changes the ruleset without changing a test, say why no test was needed.
