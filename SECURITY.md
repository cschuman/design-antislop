# Security

## Reporting a vulnerability

Report privately through GitHub's
[security advisory form](https://github.com/cschuman/design-antislop/security/advisories/new).
Please do not open a public issue for a vulnerability. Expect a first response
within a week; this is a solo-maintained project with no SLA.

## What this tool does on your machine

Knowing the blast radius is most of the answer here, so it is worth being
precise about it.

`slopcheck` is a single Python 3 file with no dependencies. It reads files and
writes to stdout. It makes no network calls, spawns no subprocesses, and
writes nothing to disk. It does not send your code anywhere.

The plugin also installs a `PostToolUse` hook that runs `slopcheck` against
files Claude has just written or edited, and prints high-severity findings back
into the transcript. The hook shell script is
[`hooks/slopcheck-hook.sh`](hooks/slopcheck-hook.sh), and it is 20 lines. Read
it before you install; that is a reasonable thing to expect of anything that
runs automatically in your editing loop.

## The trust boundary worth knowing about

Findings include an excerpt of the matched text, which comes from the file
being scanned. If you scan untrusted content and feed the output into an LLM
context, that excerpt is untrusted input crossing into a context that can act.
This is a general property of any linter whose output an agent reads, not
something specific to this tool, but it is worth naming.

`slopcheck` never modifies files. Fixes are for a human, or an agent a human
is supervising, to apply.

## Scope

In scope: anything that lets a scanned file cause code execution, escape the
read-only contract, or exfiltrate data. Also in scope: a catastrophically slow
pattern that a crafted file could use to hang your editing loop.

Out of scope: false positives and false negatives in the ruleset. Those are
quality bugs and belong in the issue tracker, where they are genuinely welcome.
