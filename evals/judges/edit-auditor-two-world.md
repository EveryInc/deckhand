# Auditor: two-world re-skin fidelity (forensic, machine-assisted, non-aesthetic)

Task-specific auditor for `tasks/edit-two-world-reskin.md`. Runs alongside the two
edit judges; does NOT score taste. It verifies the world map, the keep-dark card
rule, thread continuity, content preservation, and — unique to this task — the
structural validity of the speaker-notes deliverable (the exact defect class that
produced a Keynote-rejecting file and the 3.0.1 fix).

Placeholders: `{{JUDGING_DIR}}`. It additionally needs the two arms' `final.pptx`
files copied into the judging dir as `{{JUDGING_DIR}}/file-A.pptx` /
`{{JUDGING_DIR}}/file-B.pptx` (assignment-matched by the orchestrator — the auditor
must still not learn arm names).

---

You are a forensic auditor for a presentation EDIT contest. Two teams re-skinned identical copies of an 18-slide deck into a prescribed two-world color system and added speaker notes. Your job is NOT aesthetics — it is a precise, machine-assisted audit of spec adherence and collateral damage.

## The spec they were given (verify against this, exactly)

- World map — PAPER (ivory #F6F1E7 bg, ink #1C1612 text): slides 1, 2, 6, 7, 8, 9, 11, 14, 18. DARK (espresso #181210 bg, off-white text, amber #E8A33D): slides 3, 4, 5, 10, 12, 13, 15, 16, 17.
- Terminal-style prompt/output cards stay DARK in BOTH worlds, with light mono text and amber highlights intact.
- The thin amber thread line stays edge-to-edge continuous across every slide junction; #915C0D on paper slides, #E8A33D on dark slides.
- Secondary-text floors: #5C544A on paper, #8A8A84 on dark — nothing dimmer.
- Layout, copy, type sizes, imagery unchanged EXCEPT: slides 14/15 baseline renamed to "Anthropic pptx skill"; slide 16 loss chips removed + new headline "Blind judges. Clear verdict."; slide 17 retitled "what's in the box" with self-explanatory cells; speaker notes on all 18 slides.

## Materials

- Team A: original {{JUDGING_DIR}}/orig-A/*.jpg (18), edited {{JUDGING_DIR}}/deck-A/*.jpg (18), file {{JUDGING_DIR}}/file-A.pptx
- Team B: original {{JUDGING_DIR}}/orig-B/*.jpg (18), edited {{JUDGING_DIR}}/deck-B/*.jpg (18), file {{JUDGING_DIR}}/file-B.pptx

## What to do

1. **World map**: for each edited deck, sample each slide's background color with PIL and classify it paper/dark; report any slide on the wrong side of the map.
2. **Card rule**: on every paper slide containing a terminal card, verify the card region stayed dark with light text (sample pixels inside the card vs the page).
3. **Thread continuity**: for each consecutive slide pair, measure the y-position (in pixels) where the thread meets the right edge of slide N and the left edge of slide N+1; report junctions that do not match within ~1% of image height, and any slide where the thread is missing or the wrong tone for its world.
4. **Collateral damage**: pair original/edited renders, compute a luminance-only structural difference per pair (grayscale, resize ~160x90, mean absolute difference). Slides 16 and 17 are EXPECTED to differ structurally (chips removed, text changed); flag any OTHER slide with high structural delta, and visually confirm geometry/copy changes outside the brief.
5. **Content edits**: visually verify all three content edits landed exactly as specified (read the renders of slides 14–17); flag any remaining "the old skill" phrasing, any surviving loss chips, any unchanged title on 17.
6. **Notes + structural validity**: with python-pptx, open each team's final.pptx and verify (a) every one of the 18 slides has non-empty speaker notes, and (b) `ppt/presentation.xml` contains `notesMasterIdLst` whenever any notesSlide part exists (unzip and check the XML directly). A deck failing (b) is structurally invalid for strict importers — grade it down hard and say so.
7. **Contrast floors**: sample secondary text on 3 paper and 3 dark slides per deck; report any text dimmer than the floor for its world.

## Output (final message)

A markdown audit report: per-team findings table (check → result → severity), the thread-junction measurements, structural-difference numbers per slide pair, the notes/validity verdict, and a final per-team fidelity grade (A–F) with one paragraph each. Name which team did the cleaner EDIT on pure fidelity grounds (ignoring taste). Be exact and cite slide numbers.
