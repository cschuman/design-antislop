<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->
# Slop Signatures

> The 66 machine-detectable tells `slopcheck` scans for. By default it shows **medium+ severity** and hides **high-false-positive** rules; `--strict` includes everything. Regex/heuristic rules match with IGNORECASE + MULTILINE.
>
> The visual, UX and code rules are also skipped inside non-shipped directories (`tests/`, `examples/`, `fixtures/`, `docs/` and friends); copy rules still run there. `--include-nonshipped` turns that off.
>
> Four rules marked **&dagger;** below need a *cluster*, not a single match, and are evaluated per paragraph or per file. All `copy` rules see Markdown links and bare URLs blanked out first. Their `match` column is the pattern; the grouping is scanner behaviour, documented in the README.

Severity = how reliably this signals slop. FP = false-positive risk (high-FP rules are opt-in via `--strict`).


## Visual design  <sub>(17)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `visual-glassmorphism-css-raw` | MED | medi | regex | `backdrop-filter:\s*blur\(\d+px\)[\s\S]{0,80}rgba\(255,\s*255,\s…` |
| `visual-neon-glow-card-border` | MED | medi | regex | `box-shadow:[^;]*0\s+0\s+\d+px\s+\d*px?\s*(#22d3ee\|#a855f7\|cya…` |
| `visual-purple-pink-gradient-tw` | MED | low | regex | `bg-gradient-to-[a-z]{1,2}\s+from-(purple\|violet\|indigo)-[3-9]…` |
| `visual-badge-pill-class` | LOW | high | regex | `rounded-full[^"'>]{0,30}(px-3\|px-4)[^"'>]{0,30}(py-1)[^"'>]{0,…` |
| `visual-bounce-overshoot-easing` | LOW | medi | regex | `cubic-bezier\([^)]*1\.[3-9]\d*` |
| `visual-centered-hero-cta` | LOW | high | regex | `text-center[\s\S]{0,120}mx-auto[\s\S]{0,40}<(button\|a)\b` |
| `visual-colored-left-border-strip` | LOW | high | regex | `border-l-4\s+border-(indigo\|purple\|blue\|teal\|violet)-[3-6]0…` |
| `visual-emoji-as-ui-icons` | LOW | low | regex | `^[\s]*[🚀⚡💡🔧📊✨🎯🔥💪✅🌟🎉✓✔]\s` |
| `visual-glassmorphism-navbar` | LOW | medi | regex | `backdrop-blur(-\w+)?[^"']{0,40}bg-(white\|black)\/(5\|10\|20)\b` |
| `visual-gradient-text-clip` | LOW | high | regex | `(-webkit-)?background-clip:\s*text` |
| `visual-inter-font-family` | LOW | high | regex | `font-family:\s*['"]?Inter['"]?` |
| `visual-purple-gradient-css` | LOW | low | regex | `linear-gradient\([^)]*#(7c3aed\|8b5cf6\|6366f1\|a855f7)[^)]*,\s…` |
| `visual-rounded-2xl-shadow-combo` | LOW | medi | regex | `rounded-2xl[^"']{0,40}shadow-lg\|shadow-lg[^"']{0,40}rounded-2xl` |
| `visual-shadcn-zinc-palette-unmodified` | LOW | high | regex | `(bg\|text\|border)-(zinc\|slate)-(50\|100\|900\|950)\b` |
| `visual-tailwind-indigo-500-default` | LOW | high | regex | `(bg\|text\|border\|ring)-(indigo\|blue\|violet)-(500\|600)\b(?!…` |
| `visual-three-card-grid-structure` | LOW | high | heuristic | `grid-cols-3` |
| `visual-uniform-spacing-scale` | LOW | high | heuristic | `gap-4[\s\S]{0,400}gap-4[\s\S]{0,400}gap-4` |

## UX & interaction  <sub>(11)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `ux-lorem-ipsum-content` | HIGH | low | substring | `lorem ipsum` |
| `ux-generic-error-message` | MED | high | regex | `^(Something went wrong\.?\|An error occurred\.?\|Error!?)$` |
| `ux-icon-only-button-no-label` | MED | medi | regex | `<button(?![^>]*aria-label)(?![^>]*\btitle=)[^>]*>\s*(?:<(?:svg\…` |
| `ux-placeholder-as-primary-copy` | LOW | high | regex | `placeholder=["'](Enter text( here)?\|Click here\|Type here\|Sel…` |
| `ux-dual-generic-cta` | LOW | high | regex | `Get Started[\s\S]{0,300}Learn More` |
| `ux-fake-name-placeholder-data` | LOW | high | regex | `\b(Jane Doe\|John Doe\|User Name\|\$0\.00)\b` |
| `ux-generic-empty-state` | LOW | high | regex | `^(No results( found)?\|No data( available)?)$` |
| `ux-happy-path-only-no-guards` | LOW | high | heuristic | `\{(\w+)\.map\(` |
| `ux-icon-only-buttons-no-secondary-variant` | LOW | high | heuristic | `class="[^"]*bg-(blue\|indigo)-500[^"]*text-white[^"]*"` |
| `ux-indeterminate-spinner-loading-text` | LOW | medi | regex | `class=["'][^"']*\b(spinner\|animate-spin)\b[^"']*["'][\s\S]{0,8…` |
| `ux-tab-order-mismatch` | LOW | high | heuristic | `style=["'][^"']*\b(float\|position:\s*absolute)\b[^"']*["'](?![…` |

## Copy & voice  <sub>(20)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `copy-fast-paced-world` | HIGH | low | regex | `in today'?s fast.paced world` |
| `copy-harness-the-power` | HIGH | low | substring | `harness the power of` |
| `copy-hedging-preamble` | HIGH | low | regex | `\bit('s\| is) (important\|worth) (to note\|noting\|mentioning) …` |
| `copy-ai-vocab-cluster` | MED | medi | regex | `\b(delves?\|delving\|tapestry\|leverage[sd]?\|leveraging\|seaml…` |
| `copy-binary-contrast` &dagger; | MED | medi | regex | `\b(not (just\|only)\b[^.,;]{1,60}\bbut\b\|it'?s not\b[^.,;]{1,6…` &mdash; 2+ per file |
| `copy-em-dash-density` &dagger; | MED | medi | regex | 3+ prose asides in a paragraph, 2 per 100 words; one per file |
| `copy-marketing-cliche-phrases` | MED | low | regex | `\b(unlock (your )?productivity\|next.generation platform\|boost…` |
| `copy-promotional-verbs` | MED | medi | regex | `\b(unlock(?:ing\|s)? (?:(?:the\|your\|its\|their\|our\|new\|ful…` |
| `copy-stock-transitions` | MED | low | regex | `^(Furthermore\|Moreover\|Additionally\|In addition\|Consequentl…` |
| `copy-vague-attribution` | MED | medi | regex | `\b(experts (argue\|say\|agree\|believe)\|studies show\|industry…` |
| `copy-copula-avoidance` | LOW | medi | regex | `\b(serves? as\|acts? as\|functions? as\|stands? as) an?\b` |
| `copy-false-agency` | LOW | medi | regex | `\bthe (data\|research\|evidence\|analysis) (reveals\|shows\|und…` |
| `copy-hedging-stack` | LOW | medi | regex | `\b(could\|might\|may)\s+(potentially\|possibly\|arguably\|seemi…` |
| `copy-hollow-tricolon` | LOW | high | regex | `\b\w+,\s*\w+,\s*(and\|&)\s*\w+\.(\s*\w+,\s*\w+,\s*(and\|&)\s*\w…` |
| `copy-in-conclusion-crutch` | LOW | low | regex | `^(In conclusion\|In summary\|To summarize\|To conclude),` |
| `copy-listicle-title` | LOW | medi | regex | `^\s*\d+\s+(reasons?\|ways?\|tips?\|things?\|secrets?\|steps?)\s…` |
| `copy-meta-commentary` | LOW | low | regex | `\b(as mentioned above\|as (we\|previously) discussed\|as noted …` |
| `copy-rule-of-three-bold-bullets` &dagger; | LOW | high | regex | `^[-*]\s*\*\*[^*]{2,30}\*\*:\s` &mdash; 3+ per list |
| `copy-throat-clearing-openers` | LOW | medi | regex | `^(Here'?s the thing:\|At its core,\|It'?s worth noting:\|In ess…` |
| `copy-vocabulary-tier2` &dagger; | LOW | high | regex | `\b(cutting-edge\|empower(s\|ed\|ing)?\|streamline[sd]?\|innovat…` &mdash; 2+ distinct per paragraph |

## Code output  <sub>(18)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `code-ai-builder-dom-markers` | HIGH | low | regex | `data-(v0\|lovable\|bolt\|gpte)-[\w-]+\|<!--\s*(Generated by\|Bu…` |
| `code-bare-except-python` | HIGH | low | regex | `except(\s*(Exception\|BaseException)?)\s*:\s*(\n\s*)?(pass\|ret…` |
| `code-ellipsis-truncation-comment` | HIGH | low | regex | `(//\|#)\s*(\.\.\.\s*)?(rest of (the )?(code\|file\|middleware)\…` |
| `code-dead-branch-if-true` | LOW | high | regex | `if\s*\(\s*true\s*\)\|if\s+True\s*:` |
| `code-div-role-button` | LOW | high | regex | `<div[^>]*\brole=["'](button\|checkbox\|link)["']` |
| `code-empty-catch-js` | MED | low | regex | `catch\s*\([^)]*\)\s*\{\s*\}` |
| `code-fake-jsdoc-throws` | MED | high | regex | `@throws\s*\{[^}]+\}` |
| `code-floating-promise-map-async` | MED | high | regex | `\.map\(\s*async\b` |
| `code-hardcoded-secret` | MED | high | regex | `(api[_-]?key\|secret\|password\|token)\s*[:=]\s*['"][A-Za-z0-9_…` |
| `code-mutable-default-arg` | MED | low | regex | `def\s+\w+\([^)]*=\s*(\[\]\|\{\})[^)]*\)` |
| `code-stub-placeholder-body` | MED | high | regex | `\btodo!\(\)\|raise NotImplementedError\|\bpass\s*$(?=\s*(#.*)?$…` |
| `code-console-log-leftover` | LOW | high | regex | `console\.(log\|debug)\(` |
| `code-generic-variable-names` | LOW | high | regex | `\b(const\|let\|var)\s+(data\|result\|temp\|tempVar\|output\|res…` |
| `code-inconsistent-abbreviation-casing` | LOW | high | regex | `\b[a-z][a-zA-Z]*(HTTP\|URL\|XML\|API\|ID\|JSON)[A-Z][a-zA-Z]*\b` |
| `code-mixed-default-named-exports` | LOW | high | regex | `export default[\s\S]*export const\|export const[\s\S]*export de…` |
| `code-narrative-trivial-comment` | LOW | medi | regex | `(//\|#)\s*(loop through\|iterate through\|increment (the )?coun…` |
| `code-todo-stub-comments` | LOW | high | regex | `(//\|#\|/\*)\s*(TODO\|FIXME\|HACK\|XXX)\b` |
| `code-transition-all-css` | LOW | low | regex | `transition:\s*all\b` |