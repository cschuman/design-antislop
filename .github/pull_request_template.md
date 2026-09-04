## What this changes

<!-- One or two sentences. -->

## Effect on precision

<!--
For a ruleset change, this is the part that matters:
which rule, what it now catches, and what it no longer catches.
For a code change, delete this section.
-->

## Checklist

- [ ] `python3 tests/run_tests.py` passes
- [ ] `./skills/design-antislop/slopcheck skills hooks README.md` is clean
- [ ] Detection changes come with a fixture, or the PR says why none was needed
- [ ] No new dependencies (`slopcheck` is stdlib-only by design)
