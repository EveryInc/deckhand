# Task: edit — full re-theme + insert one slide

Edit quality under the two hardest real-world edit asks: a complete palette re-theme
(every surface, nothing else allowed to change) and a single content insertion that
must blend into an existing design language. Used verbatim in the edit benchmark round.

Input: each arm gets a finished 15-slide deck at `{{WORKDIR}}/deck.pptx`. Two valid
setups — **own-deck** (each arm edits the deck its toolchain produced in a prior create
round; measures the realistic loop but the lift differs per arm if the originals'
palettes differ) or **same-deck** (both arms edit copies of one neutral deck; cleaner
comparison). State which setup was used in the results log.

Placeholders: `{{TOOLCHAIN_BLOCK}}`, `{{WORKDIR}}`.

---

You are a presentation editor. An existing 15-slide deck about Dynamic Workflows in Claude Code needs two specific edits. The deck is at `{{WORKDIR}}/deck.pptx`.

## Edit 1 — Re-theme the whole deck to the palette below

Restyle EVERY slide to this color scheme. This means backgrounds, text colors, accent elements, table fills, pills/chips, diagram colors — the entire visual system. Preserve the deck's layout, content, typography (typefaces/sizes), and imagery; only the colors change. Map the old palette onto the new one sensibly (old primary background → Teal Dark, old accent → the gold/amber family, etc.) and keep contrast readable everywhere.

**Theme: Consulting/Teal — core palette:**

| Name | Hex | Role |
|---|---|---|
| Teal Dark | #0F5258 | Primary background, dark accents |
| Teal Medium | #4999A0 | Secondary backgrounds, depth |
| Warm White | #FFFEFB | Primary text, cards |
| Pure White | #FFFFFF | Text, highlights |
| Muted Light Teal | #C3DCDE | Secondary text (captions, labels, annotations) — the READABILITY FLOOR on teal backgrounds. Anything dimmer becomes hard to read. Use this one value for ALL secondary text. |

**Accent colors:**

| Hex | Color | Usage |
|---|---|---|
| #BB7B19 | Gold/Amber | Accent, pill borders |
| #F8DE6E | Yellow/Gold (light) | Accent, highlights |
| #2E8D23 | Green | Accent, pill borders |

## Edit 2 — Add one new slide

Insert ONE new slide at the most narratively appropriate place in the deck (you judge where — likely in the back half, near the proof/adoption content). Its message: **dynamic workflows are likely to become a new standard, fast-adopted beyond Claude Code — by other Anthropic surfaces like claude.ai, and even by competing products like Codex — the same way Skills and MCP went from Anthropic features to industry-wide standards.** Design it in the new teal theme, matching the deck's existing design language (eyebrow/footer conventions, type roles). Keep it accurate in tone: this is a prediction, not an announced fact — frame it as such (e.g. "the pattern repeats" / precedent-based), while citing the real precedent that MCP and Skills were adopted across the industry.

The final deck must have exactly 16 slides, all in the new theme.

## Your toolchain (use ONLY this)

{{TOOLCHAIN_BLOCK}}

## Process

1. Inspect the deck first to understand its structure and current colors.
2. Make the edits.
3. Review: render every slide, look at the images, verify the re-theme is complete (no stray old-palette elements), contrast is readable, and the new slide sits well in the sequence. Fix what you find. At least one genuine review-and-fix round.

## Deliverables (in `{{WORKDIR}}`)

- `final.pptx` — the edited 16-slide deck
- `img/` — rendered JPGs of all final slides
- `contact-sheet.jpg` — thumbnail grid

Your final message: a report of what you changed and how (your approach, ops/iterations used, what review caught), where you placed the new slide and why, plus any limitations. Do not ask questions; decide everything yourself.
