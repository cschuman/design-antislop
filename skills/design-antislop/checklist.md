<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->

# Anti-Slop Pre-Ship Checklist

Cross-cutting gate. Run before calling any build or written output done. This is
the generic-AI baseline; the per-style `checklist.md` handles style fidelity on
top of it.

## 0. Automated gate (run first)

- [ ] `slopcheck <changed paths>` shows no HIGH findings
- [ ] `slopcheck --strict` reviewed for the build's key surfaces (hero, primary flow, landing copy)

## 1. Visual

- [ ] Palette is project-specific: Tailwind/shadcn defaults overridden, not raw `zinc-900` / `indigo-500`
- [ ] Type pairing chosen and recorded in `DESIGN.md`, not Inter for every role
- [ ] No purple-to-pink or purple-to-blue hero gradient unless it is a deliberate brand decision
- [ ] Layout uses deliberate asymmetry, not centered hero plus three identical cards
- [ ] Radius, shadow, and spacing vary by importance, not `rounded-2xl shadow-lg` on everything
- [ ] Real icon system (SVG, consistent stroke), not emoji as UI

## 2. UX

- [ ] All four states exist for every data view: loading, empty, error, happy path
- [ ] Every icon-only control has an `aria-label` or visible text
- [ ] WCAG AA: 4.5:1 text contrast, visible focus rings, semantic HTML
- [ ] Real, task-specific content, no lorem ipsum or "Enter text here"
- [ ] Section order derives from the actual product, not the default hero/3-features/stats/testimonials skeleton

## 3. Copy

- [ ] No banned openers ("In today's fast-paced world", "harness the power of")
- [ ] Buzzword cluster gone (leverage, robust, seamless, delve, unlock, elevate) and replaced with concrete verbs plus numbers
- [ ] Every claim grounded in a named number, date, or source, or cut
- [ ] Sentence length varies, not a metronomic 15-25 word band
- [ ] No stacked hedges, no forced "not just X, but Y", no rule-of-three padding

## 4. Code

- [ ] No empty catch or bare except; errors handled or rethrown typed
- [ ] Inputs guarded for null, empty, and failure; no floating promises
- [ ] No dead branches, TODO stubs, or "rest of the code" ellipsis comments shipped
- [ ] Comments explain why, not restate the line; no lockstep docstrings on trivial helpers
- [ ] No hardcoded secrets; imports all resolve; build passes

## Honesty gate

- [ ] Not repeating fabricated slop statistics. slopcheck is advisory: a flag means "look here", not "this is wrong". Human judgment ships the work.
