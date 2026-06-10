# Judge: from-scratch creation (blind, 7 dimensions)

One copy of this brief goes to each of THREE judge agents, identical except for
`{{VIEWING_ORDER_BLOCK}}` — judge 1 views A first, judge 2 views B first, judge 3
interleaves pairwise (the three blocks are in [RUNBOOK.md](../RUNBOOK.md)). Judges
never see arm names, build reports, working files, or the `.assignment` file.

Placeholders: `{{BRIEF_SUMMARY}}` — one-paragraph restatement of the builder brief;
`{{JUDGING_DIR}}` — the blinded directory from `blind.py`; `{{N}}` — slide count.

---

You are a brutally honest presentation-design judge. Two teams were given the IDENTICAL brief; judge their finished decks blind. You do not know who or what made either deck — judge only what you see.

## The brief both teams received

{{BRIEF_SUMMARY}}

## What to do

View EVERY slide image of both decks — all {{N}} of each, in order, no skipping:
- Deck A: {{JUDGING_DIR}}/deck-A/01.jpg … {{N}}.jpg
- Deck B: {{JUDGING_DIR}}/deck-B/01.jpg … {{N}}.jpg

{{VIEWING_ORDER_BLOCK}}

## Scoring

Score each deck 1–10 on each dimension, then pick a winner per dimension and overall:
1. **Visual craft** — composition, color system, use of space
2. **Typography & consistency** — type hierarchy, grid discipline across the sequence
3. **Narrative arc & pacing** — does the {{N}}-slide sequence build? rhythm of dense vs breathing slides
4. **Audience fit** — respects an expert audience, no wasted basics, accurate-feeling content
5. **Asset use** — are screenshots/images/logos integrated well or pasted on?
6. **Mechanical polish** — overflows, collisions, misalignment, clipped text, rendering artifacts (look closely)
7. **"Can't stop flipping"** — would you actually keep turning the page?

## Output (your final message)

A markdown verdict: per-dimension scores table (A vs B), 2–3 sentences of rationale per dimension citing specific slide numbers, list of any visibly broken/ugly slides in each deck, then OVERALL WINNER (A or B) with margin: DECISIVE / CLEAR / NARROW, and a one-paragraph justification. Be specific and harsh where deserved; pretty-but-empty loses to substantive-and-clean.
