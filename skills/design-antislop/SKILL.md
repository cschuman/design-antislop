---
name: design-antislop
description: Guardrail against "AI slop", the generic, cookie-cutter defaults (purple-to-pink gradients, Inter everywhere, three identical feature cards, "in today's fast-paced world", empty catch blocks) that make output read as machine-made. Two layers, a prevention playbook that steers new work and a `slopcheck` CLI/hook that scans built output for 66 slop signatures across visual design, UX, copy, and code. Use when building or reviewing ANY UI, site, component, dashboard, or written output that should not look like default AI. Cross-cutting layer that complements /design-apply (per-style), run the playbook while building and slopcheck before shipping.
---

<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->

# design-antislop

"AI slop" is the shared house style that every model drifts toward because every
model trained on the same corpus: the shadcn/Tailwind default palette, the
ChatGPT prose register, the centered hero with three feature cards. It is not
ugly. It is generic, and generic reads as machine-made. Escaping it costs a
deliberate decision; the default is sameness.

This skill is the **style-agnostic** anti-slop layer. It sits on top of whichever
of the 10 `design-apply` styles a build uses. Those per-style checklists judge
*style fidelity*; this one catches the generic-AI baseline no matter the style.

## When this fires

- Building or reviewing UI: landing pages, components, dashboards, app shells.
- Writing or reviewing copy: marketing, product, docs, email.
- Any "make this not look AI", "does this feel generic", or pre-ship review.
- Right after `/design-apply <style>`, and again before shipping.

## Layer 1: Prevention (before you generate)

**The one rule above all:** write a short `DESIGN.md` first. Lock a
project-specific palette (override the Tailwind/shadcn defaults), a distinctive
type pairing (not Inter for every role), and a voice. Generate against that
file, not against muscle memory.

Highest-impact moves, by dimension (full set in [playbook.md](playbook.md)):

- **Visual**: commit to a 2-3 hue brand palette and a display+body font pairing.
  No purple-to-pink hero gradient by default. Vary card count and use asymmetry
  instead of hero + three identical cards. Vary radius/shadow/spacing by
  importance. Real SVG icons, never emoji as UI.
- **UX**: build all four states for every data view (loading, empty, error,
  happy). Every icon-only control gets an `aria-label`. WCAG AA contrast, visible
  focus, semantic HTML. Real content, no lorem ipsum. Derive section order from
  the actual product, not the hero/3-features/stats/testimonials skeleton.
- **Copy**: cut the banned openers and the buzzword cluster
  (leverage/robust/seamless/delve/unlock/elevate). Ground every claim in a named
  number, date, or source. Vary sentence length. Drop stacked hedges, forced
  "not just X but Y", and rule-of-three padding.
- **Code**: no empty catch or bare except, guard every input, no floating
  promises. Delete dead branches, TODO stubs, and ellipsis-truncation comments.
  Comments say why, not what. No hardcoded secrets; the build must pass.

## Layer 2: Detection (before you ship)

`slopcheck` scans files for the 66 machine-detectable signatures in
[signatures.json](signatures.json) (full list: [SIGNATURES.md](SIGNATURES.md)).

```bash
skills/design-antislop/slopcheck                 # scan cwd, medium+ severity, low-noise
skills/design-antislop/slopcheck src/ index.html # specific paths
skills/design-antislop/slopcheck --strict        # + high-false-positive rules, prose in components
skills/design-antislop/slopcheck --dimension copy --min-severity high
skills/design-antislop/slopcheck --json          # machine output for CI
skills/design-antislop/slopcheck --list          # show the active ruleset
```

By default it shows medium-and-up severity and hides high-false-positive rules,
so the signal stays high. Exit code: `0` clean, `1` medium/low findings, `2` at
least one high-severity finding (usable as a CI gate). A match is a prompt to
look, not a verdict.

A **hook** runs slopcheck automatically on each file Claude writes. Installed as
a plugin it is on by default, scoped to `--dimension visual,ux,copy
--min-severity high`. That scoping makes it very quiet: no visual signature is
high severity, so the visual leg never fires, and the hook resolves to four
rules — one UX and three copy. It is a no-op on `.css`, `.py`, `.rs`, `.ts` and
`.js`. Treat it as a cheap backstop for the most obvious tells, not as coverage;
the code rules and everything else stay reachable through `--dimension code`,
`--strict`, or a CI step. See [hooks/README.md](../../hooks/README.md).

## Pre-ship gate

Walk [checklist.md](checklist.md) before calling a build or a written piece done.
Run `slopcheck` first; it is item 0.

## How it fits the pipeline

This is a cross-cutting layer, not a style. Whatever picks the visual direction
(a design system, a style skill, a `DESIGN.md`) handles style fidelity;
design-antislop keeps the build off the generic AI baseline: the playbook while
building, `slopcheck` before shipping.

## Provenance and honesty

Built by the `anti-slop-research` fleet (12 finders across GitHub, Reddit, and
design writing; first sweep 2026-08-18). Each later sweep is reconciled into the
shipped ruleset rather than replacing it, so the counts are cumulative: currently
66 signatures and 52 rules. These are heuristics, not laws.
slopcheck is advisory, human judgment ships. Do not repeat invented statistics
about slop. Worth remembering: Anthropic's own frontend skill now *excludes*
purple-on-white gradients. The canonical tell flipped from signature to liability
in about a year, which is exactly why this list is regenerable, not carved in.
