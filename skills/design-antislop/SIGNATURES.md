<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->
# Slop Signatures

> The 71 machine-detectable tells `slopcheck` scans for. By default it shows **medium+ severity** and hides **high-false-positive** rules; `--strict` includes everything. Regex/heuristic rules match with IGNORECASE + MULTILINE.

Severity = how reliably this signals slop. FP = false-positive risk (high-FP rules are opt-in via `--strict`).


## Visual design  <sub>(18)</sub>

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
| `visual-icon-in-circle-centered-hero` | LOW | high | heuristic | `mx-auto[^"']{0,60}rounded-full[^"']{0,60}(flex\|items-center)` |
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
| `ux-dual-generic-cta` | LOW | high | regex | `Get Started[\s\S]{0,300}Learn More` |
| `ux-fake-name-placeholder-data` | LOW | high | regex | `\b(Jane Doe\|John Doe\|User Name\|\$0\.00)\b` |
| `ux-generic-empty-state` | LOW | high | regex | `^(No results( found)?\|No data( available)?)$` |
| `ux-happy-path-only-no-guards` | LOW | high | heuristic | `\{(\w+)\.map\(` |
| `ux-icon-only-buttons-no-secondary-variant` | LOW | high | heuristic | `class="[^"]*bg-(blue\|indigo)-500[^"]*text-white[^"]*"` |
| `ux-indeterminate-spinner-loading-text` | LOW | medi | regex | `class=["'][^"']*\b(spinner\|animate-spin)\b[^"']*["'][\s\S]{0,8…` |
| `ux-placeholder-as-primary-copy` | LOW | high | regex | `placeholder=["'](Enter text( here)?\|Click here\|Type here\|Sel…` |
| `ux-tab-order-mismatch` | LOW | high | heuristic | `style=["'][^"']*\b(float\|position:\s*absolute)\b[^"']*["'](?![…` |

## Copy & voice  <sub>(23)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `copy-fast-paced-world` | HIGH | low | regex | `in today'?s fast.paced world` |
| `copy-harness-the-power` | HIGH | low | substring | `harness the power of` |
| `copy-hedging-preamble` | HIGH | low | regex | `\bit('s\| is) (important\|worth) (to note\|noting\|mentioning) …` |
| `copy-ai-vocab-cluster` | MED | medi | regex | `\b(delves?\|delving\|tapestry\|leverage[sd]?\|leveraging\|seaml…` |
| `copy-binary-contrast` | MED | medi | regex | `\b(not (just\|only)\b[^.,;]{1,60}\bbut\b\|it'?s not\b[^.,;]{1,6…` |
| `copy-body-cliche-emotion` | MED | medi | regex | `\b(heart (pounded\|raced\|skipped a beat)\|eyes widened\|breath…` |
| `copy-explicit-moral-statement` | MED | medi | regex | `\b(the lesson (here )?is\|what this teaches us\|the takeaway (h…` |
| `copy-marketing-cliche-phrases` | MED | low | regex | `\b(unlock (your )?productivity\|next.generation platform\|boost…` |
| `copy-stock-transitions` | MED | low | regex | `^(Furthermore\|Moreover\|Additionally\|In addition\|Consequentl…` |
| `copy-vague-attribution` | MED | medi | regex | `\b(experts (argue\|say\|agree\|believe)\|studies show\|industry…` |
| `copy-copula-avoidance` | LOW | medi | regex | `\b(serves? as\|acts? as\|functions? as\|stands? as) an?\b` |
| `copy-em-dash-density` | LOW | high | regex | `(—.*){3,}` |
| `copy-false-agency` | LOW | medi | regex | `\bthe (data\|research\|evidence\|analysis) (reveals\|shows\|und…` |
| `copy-hedging-stack` | LOW | medi | regex | `\b(could\|might\|may)\s+(potentially\|possibly\|arguably\|seemi…` |
| `copy-hollow-tricolon` | LOW | high | regex | `\b\w+,\s*\w+,\s*(and\|&)\s*\w+\.(\s*\w+,\s*\w+,\s*(and\|&)\s*\w…` |
| `copy-in-conclusion-crutch` | LOW | low | regex | `^(In conclusion\|In summary\|To summarize\|To conclude),` |
| `copy-listicle-title` | LOW | medi | regex | `^\s*\d+\s+(reasons?\|ways?\|tips?\|things?\|secrets?\|steps?)\s…` |
| `copy-meta-commentary` | LOW | low | regex | `\b(as mentioned above\|as (we\|previously) discussed\|as noted …` |
| `copy-promotional-verbs` | LOW | high | regex | `\b(unlock(?:ing\|s)? (?:(?:the\|your\|its\|their\|our\|new\|ful…` |
| `copy-rhetorical-question-hook` | LOW | medi | regex | `^(Have you ever wondered\|What if I told you\|Ever wonder why)\b` |
| `copy-rule-of-three-bold-bullets` | LOW | high | regex | `^[-*]\s*\*\*[^*]{2,30}\*\*:\s` |
| `copy-throat-clearing-openers` | LOW | medi | regex | `^(Here'?s the thing:\|At its core,\|It'?s worth noting:\|In ess…` |
| `copy-vocabulary-tier2` | LOW | high | regex | `\b(cutting-edge\|empower(s\|ed\|ing)?\|streamline[sd]?\|innovat…` |

## Code output  <sub>(19)</sub>

| id | sev | FP | type | matches |
|---|---|---|---|---|
| `code-ai-builder-dom-markers` | HIGH | low | regex | `data-(v0\|lovable\|bolt\|gpte)-[\w-]+\|<!--\s*(Generated by\|Bu…` |
| `code-bare-except-python` | HIGH | low | regex | `except(\s*(Exception\|BaseException)?)\s*:\s*(\n\s*)?(pass\|ret…` |
| `code-ellipsis-truncation-comment` | HIGH | low | regex | `(//\|#)\s*(\.\.\.\s*)?(rest of (the )?(code\|file\|middleware)\…` |
| `code-stray-markdown-fence-in-source` | HIGH | medi | regex | `(^\|\n)'''[a-zA-Z]*\s*\n` |
| `code-empty-catch-js` | MED | low | regex | `catch\s*\([^)]*\)\s*\{\s*\}` |
| `code-fake-jsdoc-throws` | MED | high | regex | `@throws\s*\{[^}]+\}` |
| `code-floating-promise-map-async` | MED | high | regex | `\.map\(\s*async\b` |
| `code-hardcoded-secret` | MED | high | regex | `(api[_-]?key\|secret\|password\|token)\s*[:=]\s*['"][A-Za-z0-9_…` |
| `code-mutable-default-arg` | MED | low | regex | `def\s+\w+\([^)]*=\s*(\[\]\|\{\})[^)]*\)` |
| `code-stub-placeholder-body` | MED | high | regex | `\btodo!\(\)\|raise NotImplementedError\|\bpass\s*$(?=\s*(#.*)?$…` |
| `code-console-log-leftover` | LOW | high | regex | `console\.(log\|debug)\(` |
| `code-dead-branch-if-true` | LOW | high | regex | `if\s*\(\s*true\s*\)\|if\s+True\s*:` |
| `code-div-role-button` | LOW | high | regex | `<div[^>]*\brole=["'](button\|checkbox\|link)["']` |
| `code-generic-variable-names` | LOW | high | regex | `\b(const\|let\|var)\s+(data\|result\|temp\|tempVar\|output\|res…` |
| `code-inconsistent-abbreviation-casing` | LOW | high | regex | `\b(?-i:[a-z][a-zA-Z]*(?:HTTP\|URL\|XML\|API\|ID\|JSON)[A-Z][a-z…` |
| `code-mixed-default-named-exports` | LOW | high | regex | `export default[\s\S]*export const\|export const[\s\S]*export de…` |
| `code-narrative-trivial-comment` | LOW | medi | regex | `(//\|#)\s*(loop through\|iterate through\|increment (the )?coun…` |
| `code-todo-stub-comments` | LOW | high | regex | `(//\|#\|/\*)\s*(TODO\|FIXME\|HACK\|XXX)\b` |
| `code-transition-all-css` | LOW | low | regex | `transition:\s*all\b` |