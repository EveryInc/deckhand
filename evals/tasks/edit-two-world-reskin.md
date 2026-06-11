# Task: edit — two-world re-skin + content edits + speaker notes

The hardest edit task in the suite, and the only one replayed from a **real user
request** (June 11, 2026): a finished 18-slide deck whose flat near-black design read
as "AI-generated hacker vibes" had to be re-skinned into a deliberate two-world
system — warm paper for the human-story slides, warm gallery dark for the
machine-proof slides — without touching layout or copy, plus three targeted content
edits and speaker notes throughout. The original request was executed with
hands-on-deck; this task replays the brief against any toolchain.

What it stresses that the other edit task doesn't: a **partial, per-slide-mapped**
re-theme (not uniform), elements that must KEEP their colors while everything around
them flips (the dark prompt cards), a cross-slide continuity feature (the amber
thread), per-world contrast floors, and a structural-validity trap — the speaker-notes
deliverable is the exact path that produced a Keynote-rejecting file and became the
3.0.1 fix (`p:notesMasterIdLst`).

Input: `evals/assets/two-world-reskin-input.pptx` (committed; sha256 starts
`dbb48f7bd0331e37`). Both arms edit fresh copies placed at `{{WORKDIR}}/deck.pptx`.
This is a **same-deck** setup by construction.

Heads-up for the orchestrator: the input deck's *content* is a walkthrough of
hands-on-deck itself, including benchmark claims. This is symmetric (both arms get
identical content) but judges must be told to score the EDIT EXECUTION, not the
deck's copy — the extra judge line for this task is in the RUNBOOK.

Placeholders: `{{TOOLCHAIN_BLOCK}}`, `{{WORKDIR}}`.

---

You are a presentation editor. An existing 18-slide deck needs a design re-skin and
a few targeted content edits. The deck is at `{{WORKDIR}}/deck.pptx`. Slide numbers
below are 1-based.

## Edit 1 — Re-skin the deck into a two-world system

The deck is currently flat near-black throughout. Re-skin it so the deck alternates
between two visual worlds. **Layout, copy, type sizes, and imagery do not change —
only colors and backgrounds** (exceptions in Edit 2).

**World map:**

- **PAPER world** (warm editorial print): slides 1, 2, 6, 7, 8, 9, 11, 14, 18
- **DARK world** (warm gallery dark): slides 3, 4, 5, 10, 12, 13, 15, 16, 17

**PAPER world palette:**

| Role | Value |
|---|---|
| Background | warm ivory #F6F1E7 (a subtle warmth vignette toward #EFE7D8 at edges is welcome but optional) |
| Primary text | warm ink #1C1612 |
| Secondary text | #5C544A — the readability floor on paper; nothing lighter |
| Accent (on the paper itself) | #915C0D — never use #E8A33D directly on paper, it fails contrast |
| Hairlines / footer text | #915C0D / #8A8073 |

**DARK world palette:**

| Role | Value |
|---|---|
| Background | deep espresso #181210 (a soft warm glow / subtle large contour pattern is welcome but optional — flat espresso is acceptable) |
| Primary text | warm off-white #FFFEFB (unchanged) |
| Secondary text | #C9BDA6 / #8A8A84 (unchanged) |
| Accent | amber #E8A33D (unchanged) |

**Rules that make this hard — read carefully:**

1. **The prompt/output cards stay DARK in BOTH worlds.** The deck contains dark
   terminal-style cards (labels like "THE PROMPT — IN FULL"). On dark slides they
   lift slightly (#221A14, border #3A2E22). On paper slides they stay a dark ink
   panel (#171310, border #D8CDBA) with their light mono text and #E8A33D amber
   highlights INTACT — they should pop like printed code blocks in a fine book.
2. **The amber thread.** A thin amber line runs through the entire deck, entering
   each slide's left edge at the height where it left the previous slide's right
   edge. Recolor it per world — #915C0D on paper slides, #E8A33D on dark slides —
   and PRESERVE its edge-to-edge continuity. Do not delete or break it.
3. **Slides 3 and 5 have baked background images** (an XML-text texture; a dot
   field). Restyle them to the dark-world palette. Regenerating the background art
   is allowed; preserving each background's design conceit earns fidelity credit.
4. **Ghost act numerals** (the huge faint Roman numerals behind act-opener titles)
   stay ghosts in both worlds: barely-there ink on paper, barely-there lift on dark.

## Edit 2 — Three content edits

1. **Slide 14 and slide 15** refer to a baseline toolchain vaguely (e.g. "the old
   skill"). Rename those references to **"Anthropic pptx skill"** so a first-time
   viewer knows what is meant. Do not change anything else on those slides.
2. **Slide 16**: remove the two small loss-record chips (top-left) entirely, change
   the eyebrow to `THE VERDICT`, and replace the headline with **"Blind judges.
   Clear verdict."** (left-aligned, full content width). Replace the small mono line
   mid-slide with: `three blind judges · rotated viewing orders · arms revealed only
   after every verdict was in`. The slide must read as a clean win — no mention of
   losses anywhere on it.
3. **Slide 17**: retitle to **"hands-on-deck, v3 — what's in the box"** and make
   each capability cell self-explanatory: EDIT `tiny JSON patches, lint, auto-fix` ·
   CREATE `write HTML → compiles to a patch` · VERIFY `render, diff — it checks its
   work` · EVALS `blind-judged benchmark, in the repo` · TRANSITIONS `opt-in only —
   never uninvited` · CI cell unchanged.

## Edit 3 — Speaker notes

Add presenter speaker notes to ALL 18 slides — a concise talk track (2–4 sentences
each) a presenter could speak over the slide. Derive them from each slide's visible
content. The noted file must remain a structurally valid .pptx that strict importers
(e.g. Apple Keynote) accept.

## Your toolchain (use ONLY this)

{{TOOLCHAIN_BLOCK}}

## Process

1. Inspect the deck first: structure, current colors, where the thread and cards are.
2. Make the edits.
3. Review: render every slide, look at the images, verify the world map is followed
   exactly, the cards stayed dark with amber intact, the thread is continuous and
   two-tone, contrast floors hold, and nothing outside the brief changed. Fix what
   you find. At least one genuine review-and-fix round.

## Deliverables (in `{{WORKDIR}}`)

- `final.pptx` — the edited 18-slide deck (notes included)
- `img/` — rendered JPGs of all final slides
- `contact-sheet.jpg` — thumbnail grid

Your final message: a report of what you changed and how (approach, ops/iterations,
what review caught), plus any limitations. Do not ask questions; decide everything
yourself.
