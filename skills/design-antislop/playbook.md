<!-- slopcheck-ignore-file: this file quotes slop patterns as examples -->
# Anti-Slop Playbook

> Cross-cutting prevention rules that keep output from reading as default-AI. Distilled by the `anti-slop-research` fleet into 52 ranked rules. Style-agnostic: this sits *on top of* whichever design-apply style you pick.

**The one rule above all:** decide a project-specific palette, type pairing, and voice in a `DESIGN.md` *before* generating anything, then run `slopcheck` before you ship. Genericness is the default you have to actively spend a decision to escape.

Format: **the slop** -> what to do instead -> why.


---

## Visual design  <sub>(12)</sub>

### `HIGH`  Purple-to-blue/pink gradient paired with Inter font as the default hero treatment

**Instead:** Commit to a project-specific 2-3 hue palette that avoids the 200-290° blue/indigo/violet band entirely, pair a distinctive display/serif headline face against a different body face, and lock both in a DESIGN.md before generating anything  

**Why:** This exact pairing is the single most recognized AI fingerprint, appearing in an estimated 40-75% of raw AI output and readable as AI-made in under two seconds by any designer. It traces to Tailwind's indigo-500 default and Inter's ubiquity in training data — it reads as an unmade design choice, not a brand  

<sub>e.g. Slop: bg-gradient-to-r from-purple-600 to-pink-600, font-family: Inter everywhere. Better: a custom rust-and-forest palette with Fraunces headlines over IBM Plex Sans body text</sub>


### `HIGH`  A colored 3-4px left-border strip on every card

**Instead:** Differentiate containers with whitespace first, then background tint, then elevation shadow — skip the border stripe entirely  

**Why:** This single decorative pattern is copied almost verbatim from shadcn/ui and Tailwind tutorials; spotting it on 2+ elements is near-certain proof of AI generation  

<sub>e.g. Slop: every dashboard card has a 4px indigo left border. Better: cards separated by gap-8 spacing and a subtle bg-neutral-50 shift, no border at all</sub>


### `HIGH`  Centered hero + exactly three identical feature cards, repeated as the whole-page skeleton

**Instead:** Vary card count deliberately (2, 4, or 5), use an asymmetric grid, and give each card a different copy length and visual weight  

**Why:** Hero-badge-headline-then-3-cards is a memorized template sequence, not a layout decision — it appears in 70-90% of raw AI output regardless of content  

<sub>e.g. Slop: 3 equal-width white cards, same icon position, same copy length. Better: a 2-column + 1-spanning-card grid where the spanning card carries more detail because it's the most important feature</sub>


### `HIGH`  Shipping the raw, unedited Tailwind/shadcn palette (zinc-900, indigo-500, gray-700)

**Instead:** Override tailwind.config.js theme.extend.colors with brand-specific hex values before writing any component  

**Why:** Every AI-generated project starts from the same default file; not touching it is the fastest visible signal of zero design intent  

<sub>e.g. Slop: bg-white text-zinc-900. Better: define brand-primary: #0F766E and brand-ink: #1a1a1a, then use those exclusively</sub>


### `HIGH`  Glassmorphism (backdrop-blur + low-opacity panels) applied to every surface — navbars, cards, modals alike

**Instead:** Reserve blur/transparency for at most one high-impact element (a hero overlay or single modal); make everything else solid  

**Why:** Blanket glass effects tank contrast (often below 4.5:1) and read as visual noise rather than depth, and blanket application specifically (not the effect itself) is the AI tell  

<sub>e.g. Slop: nav, cards, and buttons all use backdrop-blur-md bg-white/10. Better: solid bg-gray-900 nav, opaque cards, blur used only on one onboarding overlay</sub>


### `MED`  Rounded-2xl radius and shadow-lg applied identically to buttons, cards, and inputs with no differentiation

**Instead:** Vary radius and shadow by element importance — e.g. 16px on primary cards, 8px on secondary, 0 with a border stroke on feature blocks  

**Why:** Uniform heavy rounding across every element type is a statistical-mean default, not a design decision, and flattens the hierarchy  

<sub>e.g. Slop: every element gets rounded-2xl shadow-lg. Better: primary card 16px radius + soft shadow; secondary card 8px radius, no shadow; feature block square with 1px border</sub>


### `MED`  Emoji used as feature-list bullets or icons (🚀, ⚡, 💡)

**Instead:** Use a real icon system (monoline SVG, consistent stroke weight) or a plain text bullet  

**Why:** Emoji don't align to a baseline grid, don't scale, and can't control weight — professional interfaces essentially never use them as functional UI elements  

<sub>e.g. Slop: 🚀 Fast performance. Better: a 20px outline icon at a fixed stroke width, or a simple '–' bullet</sub>


### `MED`  Perfectly centered, symmetric layouts on every section — hero, cards, footer all balanced identically

**Instead:** Introduce deliberate asymmetry: left-anchor headlines, offset images, unequal column grids, overlapping elements  

**Why:** Mathematical symmetry is the statistically 'safest' composition and is what models default to absent any other signal; asymmetry reads as an intentional human choice  

<sub>e.g. Slop: centered heading, centered image, three centered columns below. Better: headline anchored left, hero image offset and overlapping the next section</sub>


### `MED`  Flat, uniform spacing everywhere (gap-4 p-4 on hero, cards, and footer alike)

**Instead:** Build a custom spacing scale and apply it with rhythm — generous space around the hero, tighter internal card padding, intentional variation between sections  

**Why:** Uniform spacing feels robotic; real design uses tight and loose spacing deliberately to guide the eye  

<sub>e.g. Slop: p-4 gap-4 on every section. Better: hero p-12, card internals p-4 to p-6 with varying gaps, section margins my-8 to my-16 depending on content weight</sub>


### `MED`  Single generic sans-serif (Inter, Roboto, Arial) used for every text role with no pairing

**Instead:** Pair a distinctive display/serif headline face with a different, readable body font, and document the pairing  

**Why:** A single default font signals no typographic decision was made — font choice alone removes a large share of the AI signature  

<sub>e.g. Slop: font-family: Inter for headings and body. Better: Fraunces (serif, bold) for headings, IBM Plex Sans for body</sub>


### `MED`  Linear, Tailwind-inherited type scale — headings stepping 16/18/20/22px and spacing in flat 0.5rem/1rem/1.5rem increments

**Instead:** Define a multiplicative type scale (roughly a 1.25x-1.4x progression) and a custom spacing grid (4/8/12/16/24/32/40/48), enforced as tokens rather than picked ad hoc  

**Why:** Uniform linear progression in both type and spacing produces the flat, samey hierarchy readers unconsciously associate with generated pages, because it's the arithmetic default absent any typographic decision  

<sub>e.g. Slop: font sizes 16, 18, 20, 22, 24 (linear +2px steps). Better: --font-size-sm: 16px; --font-size-base: 20px; --font-size-lg: 28px; --font-size-xl: 36px (1.4x scale).</sub>


### `LOW`  Oversaturated, hyperrealistic, shadow-free stock imagery

**Instead:** Use real photography with visible grain, texture, and asymmetric practical lighting  

**Why:** AI-generated and AI-selected imagery defaults to mathematical perfection; texture and imperfection are what read as human-made in 2026  

<sub>e.g. Slop: a glossy, perfectly lit, symmetric hero photo. Better: a photo with visible grain, one harsh shadow, and an off-center subject</sub>



---

## UX & interaction  <sub>(11)</sub>

### `HIGH`  Interfaces designed only for the happy path — no empty state, loading state, or error state

**Instead:** Explicitly design and build all four states for every data view: loading skeleton, empty state with a next action, error state with recovery, and populated state  

**Why:** Production UIs are 60-70% state-handling code; shipping only the loaded view is the clearest sign nobody thought past the demo  

<sub>e.g. Slop: {items.map(item => ...)} with no guard. Better: if (isLoading) return <Skeleton/>; if (error) return <ErrorRetry/>; if (!items.length) return <EmptyState message="You haven't uploaded a document yet — create your first one to get started" cta="Add your first item"/></sub>


### `HIGH`  Icon-only buttons shipped with no accessible label

**Instead:** Add aria-label (or visible text) to every icon-only interactive element as a non-negotiable default  

**Why:** This fails WCAG AA immediately and also fails plain usability for first-time users — it's cheap to fix and expensive to ship broken  

<sub>e.g. Slop: <button><MenuIcon/></button>. Better: <button aria-label="Open navigation menu"><MenuIcon/></button></sub>


### `HIGH`  Interfaces that miss the bulk of WCAG requirements — low contrast, no focus rings, non-semantic markup

**Instead:** Write explicit, measured accessibility requirements into every build spec: semantic HTML5 only, WCAG AA (4.5:1) minimum contrast, visible focus indicator and aria-label on every interactive element — then verify with an automated pass plus one manual keyboard-only run  

**Why:** Vague requests like 'make it accessible' get ignored; automated tools alone only catch 20-30% of criteria, so a manual check is required  

<sub>e.g. Prompt slop: 'make it accessible.' Better: 'Every interactive element needs a visible focus ring and an aria-label; use native <button> instead of <div role="button">; body text must pass 4.5:1 contrast; verify with keyboard-only navigation before shipping'</sub>


### `MED`  Bounce/elastic overshoot easing on hover and micro-interactions

**Instead:** Use ease-out or linear timing functions for functional animation (e.g. Material's cubic-bezier(0.4, 0, 0.2, 1))  

**Why:** Overshoot easing is a template default, not a deliberate motion choice, and real interfaces use restrained easing for anything functional  

<sub>e.g. Slop: cubic-bezier(0.34, 1.56, 0.64, 1) on every button hover. Better: cubic-bezier(0.4, 0, 0.2, 1), or no easing at all for instant feedback</sub>


### `MED`  transition: all applied broadly instead of naming specific properties

**Instead:** List only the properties you intend to animate, and prefer transform/opacity for smooth 60fps motion  

**Why:** Animating every property causes layout thrash and jank on properties that should snap instantly (display, z-index)  

<sub>e.g. Slop: transition: all 0.3s ease;. Better: transition: opacity 0.3s ease, transform 0.3s ease;</sub>


### `MED`  Cards nested inside cards inside cards as the default way to create visual grouping

**Instead:** Build hierarchy with negative space, type scale, and color instead of stacking containers  

**Why:** Nesting containers is a reach-for-the-familiar default when the model doesn't understand hierarchy; it reads as unstructured rather than organized  

<sub>e.g. Slop: outer card > middle card > inner card, all with shadow-lg. Better: one card, internal sections separated by whitespace and a type-size shift</sub>


### `MED`  Placeholder or filler content shipped as if it were final — 'Enter text here,' Lorem ipsum, generic 'Loading...'

**Instead:** Write real, task-specific copy and states before calling the UI done  

**Why:** Designing against Lorem ipsum removes the context needed to make real hierarchy and emphasis decisions, guaranteeing generic output downstream  

<sub>e.g. Slop: <input placeholder="Enter text here" />. Better: <input placeholder="First name (e.g. Jane)" /></sub>


### `MED`  Rigid landing-page skeleton repeated regardless of product — hero, 3 features, stats bar, testimonials, 3-tier pricing, CTA

**Instead:** Derive section order and presence from actual user research and business priorities, dropping sections that don't earn their place  

**Why:** This exact structure appears in 85%+ of AI-generated SaaS pages because it's a memorized template, not a decision based on this product's users  

<sub>e.g. Slop: every generated page follows the same 6-section order. Better: a technical developer tool skips testimonials and stats entirely in favor of a code sample and docs link</sub>


### `MED`  Entrance animation (slide-in, fade, bounce) applied to every element by default, with no regard for prefers-reduced-motion

**Instead:** Animate only where motion carries real meaning — reveal, feedback, affordance — keep it to roughly 50-300ms, and respect prefers-reduced-motion unconditionally  

**Why:** Blanket motion is a decoration reflex, not a design choice, and it actively harms users who've told their OS they want less of it — an accessibility miss layered on top of a visual tell  

<sub>e.g. Slop: every heading slides in on scroll, every card bounces on hover, no media query. Better: a single subtle fade on the hero only, and @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</sub>


### `LOW`  Active or selected UI states rendered lower-contrast than the disabled state, in service of a 'sleek' minimal look

**Instead:** Make active/selected states higher-contrast than idle, never lower, and reserve genuinely faded styling (60-70% opacity) for true disabled controls only  

**Why:** Over-optimizing for a minimal aesthetic sacrifices basic legibility, and a faded 'active' button reads as broken — indistinguishable from disabled — to a real user scanning the screen  

<sub>e.g. Slop: active button text #e8e8e8 on #f5f5f5, visually weaker than the actually-disabled button beside it. Better: bold primary-color fill for the active state; true disabled state gets reduced opacity instead.</sub>


### `LOW`  Layout shift from async content — ads, late-loading data, or images pushing the rest of the page down with no space reserved in advance

**Instead:** Reserve space for anything that loads asynchronously with an explicit height, aspect-ratio, or a skeleton that matches the final layout  

**Why:** Layout shift is invisible in a static screenshot but immediately felt by a real user mid-scroll, and it's one of the few slop tells that's also a hard, standardized metric (Cumulative Layout Shift, part of Core Web Vitals)  

<sub>e.g. Slop: an ad loads and shoves the article text down with nothing reserved. Better: a 200px placeholder with a fixed aspect-ratio that holds its spot until the ad resolves.</sub>



---

## Copy & voice  <sub>(14)</sub>

### `HIGH`  Hedging stacks — multiple uncertainty markers chained in one clause ('could potentially possibly suggest', 'it is important to note that... almost always... arguably')

**Instead:** State the claim directly with at most one qualifier, or commit to it outright  

**Why:** Stacked hedges are 3-5x baseline in LLM output and are one of the most mechanically detectable AI tells; they signal the model padding against a low-confidence claim rather than a writer with a point of view  

<sub>e.g. Slop: 'It is important to note that this almost always requires, as experts argue, careful consideration.' Better: 'This needs careful thought.'</sub>


### `HIGH`  Buzzword vocabulary cluster — leverage, robust, seamless, delve, paradigm, unlock, elevate, empower, garner, tapestry

**Instead:** Replace every instance with a concrete verb tied to a specific action or number  

**Why:** These roughly 40 words run at 11-28x their normal frequency in LLM output (Max Planck Institute, 2024) — statistically overused post-2022 at rates far above human baselines; three or more in five lines is a near-certain tell, and they carry no real information  

<sub>e.g. Slop: 'Robustly leverage seamless paradigm shifts to elevate your workflow.' Better: 'This cuts setup time from 20 minutes to 3.'</sub>


### `HIGH`  Corporate transition cascade opening successive paragraphs — Furthermore, Moreover, Additionally, Consequently

**Instead:** Delete the connector and let the next sentence carry its own weight, or replace with a natural spoken transition  

**Why:** These formal connectors appear 3-5x more often in AI text than in human prose and pad without adding logical flow  

<sub>e.g. Slop: 'The platform is fast. Furthermore, it is secure. Moreover, it scales.' Better: 'Fast, secure, and it scales.'</sub>


### `HIGH`  Metronomic sentence length — nearly every sentence lands in the same 15-25 word band, producing a flat, robotic rhythm

**Instead:** Deliberately alternate short punchy fragments (under 6 words) with long explanatory sentences; aim for a 2-3:1 length variance  

**Why:** Humans naturally burst between short and long sentences; uniform pacing is detectable by ear (read it aloud) and by scanning tools alike  

<sub>e.g. Slop: 'The system provides solutions. It ensures integration. It delivers reliability.' Better: 'Deploy it. It handles enterprise load, integrates with your existing auth, and doesn't fall over at 10k concurrent users.'</sub>


### `HIGH`  Generic marketing openers and claims — 'In today's fast-paced world,' 'Elevate your workflow,' 'Unlock your potential'

**Instead:** Lead with the actual problem, a concrete scenario, or a specific number instead of a temporal or aspirational cliché  

**Why:** These phrases are so overrepresented in training data they function as an instant AI signature and carry zero product-specific information  

<sub>e.g. Slop: 'In today's fast-paced world, staying competitive means embracing innovation.' Better: 'Our slowest customer still ships 3 features a week.'</sub>


### `HIGH`  Abstract claims with no concrete grounding — 'improves efficiency,' 'drives significant growth,' 'many experts agree'

**Instead:** Ground every claim in a named number, date, source, or example (specificity insertion)  

**Why:** AI defaults to unfalsifiable abstraction because it avoids commitment; named numbers and sources are expensive to fabricate and read as credible precisely because they're specific  

<sub>e.g. Slop: 'This approach will achieve significant growth in market share.' Better: 'Regional sales grew 15% year-over-year after we shipped same-day shipping.'</sub>


### `MED`  'Not just X, but Y' and other forced binary-contrast constructions

**Instead:** State a single direct claim without the contrast frame  

**Why:** AI leans on this rhetorical move as a universal elevation device even when nothing is actually being contrasted  

<sub>e.g. Slop: 'This isn't just a tool, it's a paradigm shift.' Better: 'A tool for cleaning up AI writing.'</sub>


### `MED`  Rule-of-three forced lists — exactly 3 (or 5, or 7) benefits, reasons, or steps every time

**Instead:** Let the actual content determine list length — 2, 4, 6, whatever is true — and vary structure across a document  

**Why:** LLMs default to three items due to pretraining frequency, not because three is actually the right count for this content  

<sub>e.g. Slop: 'Three reasons: speed, reliability, cost.' Better: 'It's faster, more reliable, handles growth without new infrastructure, and costs less per transaction.'</sub>


### `MED`  Throat-clearing openers that add no information — 'Here's the thing,' 'At its core,' 'It's worth noting'

**Instead:** Delete the preamble and open with the actual point  

**Why:** These phrases exist to hedge before committing to a claim; cutting them tightens prose and reads as more confident  

<sub>e.g. Slop: 'Here's the thing: the platform streamlines workflows.' Better: 'The platform streamlines workflows.'</sub>


### `MED`  Vague, unlinked attribution — 'experts argue,' 'studies show,' 'industry reports suggest'

**Instead:** Name the actual source, date, and link, or drop the claim entirely if you can't  

**Why:** Vague attribution launders an unsupported claim into apparent authority without accountability  

<sub>e.g. Slop: 'Experts suggest AI will transform everything.' Better: 'McKinsey's 2024 report projects 15-40% cost reduction across six industries.'</sub>


### `MED`  Em-dash and semicolon overuse — 2+ per paragraph, often used for every aside

**Instead:** Reduce to human baseline; favor periods and simple clause structure, reserving dashes for genuine emphasis  

**Why:** LLM output uses em-dashes at 3-5x human baseline; clustering them is a detectable structural pattern independent of vocabulary  

<sub>e.g. Slop: 'The system — built on modern architecture — provides, seamlessly, integration.' Better: 'The system integrates seamlessly. It's built on modern architecture and scales to terabytes.'</sub>


### `MED`  Relying on manual proofreading alone to catch AI phrasing

**Instead:** Run copy through a deterministic banned-phrase linter (plain-english, Slop Cop) before publishing, and read the final draft aloud once  

**Why:** Reading aloud reliably exposes metronomic rhythm that's easy to miss silently, and a regex linter catches the mechanical patterns (hedge stacks, corporate verbs) fast and for free  

<sub>e.g. plain-english check draft.md returns: 'Line 3: [warning] leverage — use "use" instead.'</sub>


### `LOW`  False-cheerful tone with emoji headers and exclamation-heavy copy ('Hey! 🎉 Let's build something amazing together! 🚀')

**Instead:** Match tone to the actual audience — formal where the audience expects formal, plainly friendly where it doesn't — and use emoji only where it adds real meaning, if at all  

**Why:** Buddy-buddy exclamatory copy was a genuine SaaS trend once; used reflexively today it reads as either AI-generated or simply inexperienced, regardless of which it actually is  

<sub>e.g. Slop: 'Hey, great job! 🎉 Let's get started! 🚀' Better: tone calibrated to the audience — formal and precise for B2B compliance software, plainly warm for a consumer journaling app.</sub>


### `LOW`  Copy that would be equally true of any competitor's product, with no claim specific enough to be falsifiable

**Instead:** Run the swap test on every core sentence: if it still reads true after replacing your product's name with a rival's, rewrite it until it doesn't  

**Why:** Universal applicability is what LLMs default to because it minimizes the risk of being specifically, checkably wrong; real differentiation requires a claim that could actually be false for someone else  

<sub>e.g. Slop: 'Improve your team's productivity with our platform.' Better: 'Jira's slow — your engineers lose 3 hours a week chasing tickets. We cut that to 20 minutes.'</sub>



---

## Code output  <sub>(15)</sub>

### `HIGH`  Empty or near-empty catch blocks that silently swallow exceptions

**Instead:** Catch specific exception types, log with context, and either handle the case explicitly or rethrow a typed error  

**Why:** Bare except/catch masks real failures (including security bugs) and makes production debugging impossible; this shows up in ~25-30% of AI-generated snippets across languages  

<sub>e.g. Slop: try { risky(); } catch (e) {}. Better: try { risky(); } catch (e) { logger.error('X failed', e); throw new ValidationError(e.message); }</sub>


### `HIGH`  Imports for packages, functions, or files that don't actually exist

**Instead:** Verify every import resolves against the actual dependency tree and file system, and run a build before declaring the task done  

**Why:** LLMs confidently hallucinate plausible-looking API surface that was never installed or written — not a typo, a fabrication  

<sub>e.g. Slop: import { extractData } from 'nonexistent-lib'; Better: confirm the package is in package.json and the export exists before using it</sub>


### `HIGH`  Fire-and-forget async calls with no await and no .catch() (floating promises)

**Instead:** Always await the call, return the promise, or attach an explicit .catch() handler  

**Why:** Unhandled promise rejections fail silently in production and are one of the most common runtime-breaking patterns in generated code  

<sub>e.g. Slop: users.map(async (u) => saveUser(u)); Better: await Promise.all(users.map(u => saveUser(u)));</sub>


### `HIGH`  Logic that assumes inputs are always present, valid, and successful — no null checks, no empty-array guards, no failure paths

**Instead:** Handle every non-ideal input explicitly: null/undefined, empty collections, and failed calls, each with its own defined behavior  

**Why:** This is the default because training examples show the demo path, not the production path; it's the leading cause of AI code that passes review but breaks on real traffic  

<sub>e.g. Slop: const first = data[0].id; Better: if (!data?.length) return handleEmpty(); const first = data[0].id;</sub>


### `HIGH`  Semantic bugs hidden inside clean, lint-passing code — off-by-one loops, wrong comparison operator, inverted condition

**Instead:** Add type hints and run strict static analysis (mypy/pyright) as a first pass, then write test cases (including edge cases and, where logic is non-trivial, property-based tests) before trusting generated logic, not after a bug report  

**Why:** Over 60% of faults in AI-generated code are semantic, not syntactic — the code runs and looks right, so linting alone won't catch it; strict type checking alone catches roughly 94% of the errors that matter, but it isn't a substitute for testing boundary conditions  

<sub>e.g. Slop: for (let i = 1; i <= arr.length; i++) { process(arr[i]); } — skips index 0, crashes on the last index. Better: for (let i = 0; i < arr.length; i++)</sub>


### `HIGH`  Treating each AI session as a blank slate with no persistent constraints, re-explaining preferences in every prompt

**Instead:** Maintain one living config file (CLAUDE.md / DESIGN.md / .plain-english.yml) listing banned patterns across all four dimensions — fonts, colors, phrases, code smells — and reference it every session  

**Why:** Negative constraints override statistical defaults far more reliably than positive adjectives ever do, and a persistent file means the fix compounds instead of resetting each conversation  

<sub>e.g. DESIGN.md: 'NEVER: purple gradients, Inter font, rounded-2xl on buttons, emoji bullets, empty catch blocks, the phrase leverage.' Read and enforced at the start of every session</sub>


### `HIGH`  No automated gate catching slop patterns before merge — relying on manual eyeballing

**Instead:** Wire a deterministic linter into CI (code: aislop / eslint-plugin-ai-guard; copy: plain-english / Slop Cop; visual: a Tailwind-class denylist) so violations fail the build, not just the code review  

**Why:** These are 50+ rule, no-LLM-at-runtime static checks — cheap, deterministic, and they catch what a tired reviewer skims past  

<sub>e.g. CI step: aislop scan ./src --hard (fails build on narrative comments, phantom imports, swallowed exceptions, dead code)</sub>


### `MED`  Narrative comments that restate exactly what the next line does

**Instead:** Delete comments on self-explanatory code; reserve comments for non-obvious business context (the 'why', not the 'what')  

**Why:** AI defaults to explaining mechanism because it lacks the surrounding business context a human author would have; this bloats files without adding maintainability  

<sub>e.g. Slop: // loop through array\nfor (const u of users) {...}. Better: // legacy accounts predate the 2023 email-verification requirement, skip them here\nfor (const u of users) { if (!u.verified) continue; ... }</sub>


### `MED`  Generic placeholder variable names — data, result, temp, output, response — used throughout non-trivial code

**Instead:** Name every variable after what it actually holds, tied to the domain  

**Why:** Generic names are a fallback for missing context and make review and maintenance harder; specific names double as documentation  

<sub>e.g. Slop: const data = fetch(); const result = transform(data); Better: const userProfiles = fetchActiveUsers(); const enrichedProfiles = addMetadata(userProfiles);</sub>


### `MED`  Unnecessary abstraction layers (factory/interface/wrapper) built for a problem with exactly one implementation

**Instead:** Challenge every abstraction during review: does it reduce duplication, enable testing, or improve readability? If not, delete it and keep the plain function  

**Why:** AI over-engineers because it optimizes for looking complete rather than being minimal; a single-currency app doesn't need a DateFormatter interface  

<sub>e.g. Slop: an AbstractPriceFormatter with USD/EUR/GBP subclasses for a single-currency product. Better: function formatPrice(x) { return `$${x.toFixed(2)}`; }</sub>


### `MED`  Dead code, unreachable branches, and TODO stubs left in place ('if (true) {...} else { // TODO: handle error }')

**Instead:** Finish the branch or delete it — don't ship scaffolding as if it were a decision  

**Why:** These are leftover generation artifacts, not intentional placeholders, and they silently disable error handling in production  

<sub>e.g. Slop: if (true) { handleSuccess(); } else { // TODO }. Better: if (success) { handleSuccess(); } else { handleError(err); }</sub>


### `MED`  Silent failure by default — using .get() fallbacks or sentinel defaults (-1, None, empty string) on fields that must exist, instead of raising when required data is missing

**Instead:** Let required-field lookups raise loudly when the field is actually missing; reserve default fallbacks for genuinely optional fields only  

**Why:** AI defaults to defensive coding that converts missing data into sentinel values instead of surfacing it, which masks data corruption at the exact point it would have been cheapest to catch and lets it surface much later as a mysterious downstream bug  

<sub>e.g. Slop: user_id = data.get('user_id', -1). Better: user_id = data['user_id'] — raises immediately if the field is actually missing.</sub>


### `MED`  Architectural bloat generated at scale — God classes owning unrelated responsibilities, 100+ line methods, and near-duplicate helper functions instead of one shared utility

**Instead:** Extract single-responsibility classes and functions, flatten wrapper-component hierarchies, and name components by what they do rather than by structure  

**Why:** Multi-file AI agents centralize logic because it's locally easy within one generation pass, not because it's good architecture — the sheer volume of code an LLM produces at once outruns its own sense of when to split it up  

<sub>e.g. Slop: a single UserManager class handling auth, database access, logging, email, and billing. Better: split into UserAuth, UserRepository, NotificationService, and BillingService.</sub>


### `LOW`  Docstrings applied in lockstep on every function (Args/Returns/Raises even on a 2-line helper)

**Instead:** Document only where the behavior isn't obvious from the signature; let simple helpers stay undocumented  

**Why:** Real codebases are heterogeneous — uniform templated documentation on trivial functions is itself an AI tell and adds noise without value  

<sub>e.g. Slop: full Args/Returns/Raises docstring on def add(x, y): return x + y. Better: def add(x, y): '''Sum two numbers.''' return x + y</sub>


### `LOW`  A single AI-authored commit that appears feature-complete with zero follow-up fixes in the next 24 hours

**Instead:** Review large single-shot commits with extra scrutiny, and require a real test pass (not just 'it compiled') before merge  

**Why:** Real iterative work leaves a trail of dead ends, small fixes, and edge-case patches; a suspiciously clean 500+ line commit is a signal to slow down review, not speed it up  

<sub>e.g. Flag: 2,500 LOC feature landing in one commit with no follow-up commits — treat as unreviewed, not done</sub>

