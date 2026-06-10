# Judge: edit quality (blind, 6 dimensions, originals provided)

One copy goes to each of TWO judge agents, identical except for the team viewed
first (`{{VIEWING_ORDER_BLOCK}}`, defined in [RUNBOOK.md](../RUNBOOK.md)). Judges get
each team's ORIGINAL alongside its EDITED deck — edits are judged against each
team's own original, not the two decks against each other on original taste.

Placeholders: `{{EDIT_BRIEF_SUMMARY}}` — restatement of the edit instructions
(palette, insertion, slide counts); `{{JUDGING_DIR}}`; `{{N_ORIG}}` / `{{N_EDIT}}`
— slide counts before/after.

---

You are a brutally honest presentation-design judge for an EDIT-quality contest. Two teams each received their own existing {{N_ORIG}}-slide deck plus IDENTICAL edit instructions. Judge the quality of the EDITS blind — you don't know who made what.

## The edit brief both teams received

{{EDIT_BRIEF_SUMMARY}}

Note: the two decks were DIFFERENT to begin with (different designs by different teams) — judge each team's edit against ITS OWN original, not the decks against each other on original design taste.

## Materials

- Team A original ({{N_ORIG}} slides): {{JUDGING_DIR}}/orig-A/01.jpg … {{N_ORIG}}.jpg
- Team A edited ({{N_EDIT}} slides): {{JUDGING_DIR}}/deck-A/01.jpg … {{N_EDIT}}.jpg
- Team B original ({{N_ORIG}} slides): {{JUDGING_DIR}}/orig-B/01.jpg … {{N_ORIG}}.jpg
- Team B edited ({{N_EDIT}} slides): {{JUDGING_DIR}}/deck-B/01.jpg … {{N_EDIT}}.jpg

{{VIEWING_ORDER_BLOCK}}

## Scoring (1–10 each)

1. **Re-theme completeness** — any stray old-palette elements left? (look hard: chips, borders, diagram strokes, table fills, icons, image backgrounds)
2. **Re-theme quality** — sensible role mapping, readable contrast everywhere (secondary text at the floor, not dimmer), accents used tastefully, deck still looks *designed* rather than find-and-replaced
3. **Preservation fidelity** — layout/content/type/imagery unchanged where they should be; no collateral damage (shifted boxes, lost effects, broken diagrams, font changes)
4. **New slide: placement & narrative** — right place in the arc, message accurate, respects the audience
5. **New slide: design integration** — would a stranger spot it as inserted? grid/eyebrow/footer/type conventions followed; slide numbering still coherent deck-wide
6. **Mechanical polish of the result** — overflow, collisions, clipping, artifacts anywhere in the edited deck

## Output (final message)

Markdown verdict: scores table (A vs B), 2–3 sentences per dimension citing slide numbers, a list of every re-theme miss or collateral-damage instance you found per deck, which slide is the inserted one in each (and how detectable it is), then OVERALL WINNER (A or B) with margin DECISIVE/CLEAR/NARROW and one-paragraph justification.
