# deckhand

**Agent-native PowerPoint manipulation.** One CLI — `deck.py` — lets AI agents inspect, edit, create, and verify `.pptx` files with the fidelity of a human operator: atomic JSON patches in, linted decks out.

**→ [everyinc.github.io/deckhand](https://everyinc.github.io/deckhand/)**

Packaged as an [Agent Skill](https://www.anthropic.com/news/skills), so it drops into Claude Code, claude.ai, and any other agent platform that supports the skills format — and because the tool itself is just a CLI, *any* agent that can run a shell command can use it.

```bash
# the whole edit loop, in four commands
python deck.py deck.pptx inspect --slide 3 --brief         # what's there (one line per shape)
python deck.py deck.pptx apply patch.json -o out.pptx --fix --render img/
python deck.py out.pptx diff deck.pptx                     # what changed
python deck.py docs                                        # the full reference, no file needed
```

## Why this exists

A `.pptx` is a zip of XML. Agents that edit it directly hand-write OOXML — fragile, token-hungry, and one namespace typo from a corrupt file. Agents that regenerate decks from scratch lose everything a template encodes: brand, layout craft, image treatments.

deckhand takes a third path: **the agent writes a declarative patch; the tool executes it.**

```json
{"ops": [
  {"op": "replace-text", "scope": "master", "from": "Globex", "to": "Acme"},
  {"op": "set-text",  "slide": 3, "shape": "s12", "text": ["Q3 results", "Tokens down 84%"]},
  {"op": "swap-image", "slide": 4, "shape": "s9", "image": "screenshot.png"},
  {"op": "duplicate", "slide": 5, "shape": "s31", "offset": [0, 1.2], "text": ["Fourth pillar"]}
]}
```

New text inherits the old text's formatting automatically. Image swaps keep aspect ratio. The duplicate keeps every bit of styling and gets fresh ids. And if any op is invalid, *nothing* is written.

## Built around how agents actually fail

The interesting part isn't that it's a CLI — it's that every design choice targets a known LLM failure mode:

**Errors teach instead of scold.** Reference a shape that doesn't exist and the error includes the slide's real shape inventory — ids, types, geometry, text previews — so the agent can correct *without another round trip*:

```
PATCH REJECTED — 2 validation error(s), nothing was modified:
  - op[0] set-text: shape 's9999' not found on slide 0.
shapes on slide 0:
  s16    PICTURE      [-1.25,-0.91 15.0x8.44in]  (image image3.png)
  s18    AUTO_SHAPE   [7.00,5.17 2.6x0.25in]  Session Management
  s19    TEXT_BOX     [0.60,1.00 4.0x0.4in]  USING CLAUDE CODE
  ...
  - op[1] add-slide: layout 'Nonexistent' not found — available: 'DEFAULT', 'Blank'
```

**All errors at once, atomically.** Every op is pre-validated; a 9-op patch with 9 mistakes returns 9 actionable errors and writes zero bytes. No partially-edited decks, ever — runtime failures abort the whole patch too.

**The linter watches the agent's hands.** After every apply, the deck is re-measured and only *new or worsened* geometry problems are reported — text overflowing its box, shapes off the slide, text-on-text overlaps — each with exact inch values and the exact `fix` command to run.

**Repair is honest.** `fix` deterministically grows boxes, shrinks fonts (with a readability floor), and nudges shapes back on-slide — then *re-measures*. Anything still broken is reported as *residue* with a suggested op, not claimed as fixed. Pictures bleeding off-slide are never auto-moved (it might be intentional design).

**Tokens are a budget.** `inspect --brief` gives one line per shape for orientation; full JSON only when writing a patch. `docs` prints the complete op reference so agents never read source. `render --slide 3 --crop 1,2,6,1.5 --scale 2` zooms into the exact region under suspicion instead of re-rendering everything. `diff` verifies edits with no rendering at all.

**Verification is visual.** Slides render to `slide-<index>.jpg` (0-based, matching every other index in the tool) so the agent can *look at* what it changed — the same way a human would check their work.

## What it covers

| | |
|---|---|
| **Read** | `inspect` — shape ids, geometry (inches), text + formatting + per-run breakdowns, image rIds + media names, table contents, fills/gradients/borders, rotation, detected issues; `--master` for masters/layouts |
| **Edit** | `set-text` (formatting-inheriting), `replace-text` (deck/master/slide scope), `swap-image` (per-slide or deck-wide via media bytes), `set-style` (fonts, solid/gradient fills, borders, rotation), `move`, `resize`, `delete`, `set-notes` |
| **Create** | `add-slide` (by layout), `add-shape` (textbox, autoshapes, any MSO_SHAPE name, lines), `add-picture` (aspect-preserving), `add-table`, `duplicate`, `copy-shape` (across slides, relationships re-homed) |
| **Structure** | `reorder` (z-order), `add-row`/`delete-row`/`add-col`/`delete-col` (formatting-inheriting, width-rescaling, merged-cell guard), `slides` (reorder/duplicate/delete), `merge` (pull slides from another deck) |
| **Verify** | `render` (JPGs, crop + zoom), `diff` (structural changelog), post-apply lint, `fix` (deterministic repair) |
| **Escape hatch** | `xml get`/`xml set` — pretty-printed part XML, parse-checked and lint-checked on write-back |

**Out of scope by design** (escape hatch or PowerPoint): creating native charts, animations, transitions, embedded video/OLE, merged-cell table surgery.

## Install

**Claude Code** (as a plugin):

```
/plugin marketplace add EveryInc/deckhand
/plugin install deckhand@deckhand
```

**claude.ai / other apps that support Agent Skills**: zip `skills/deckhand/` and upload it as a skill.

**Any agent, any platform**: clone the repo and put the output of `deck.py docs` in front of your agent. It's just a CLI.

```bash
git clone https://github.com/EveryInc/deckhand
pip install python-pptx Pillow
python deckhand/skills/deckhand/scripts/deck.py docs
```

## Requirements

- Python 3.9+, `python-pptx`, `Pillow` (lxml, used by the xml escape hatch, ships with python-pptx)
- For `render` and thumbnail grids: LibreOffice (`soffice`) and Poppler (`pdftoppm`)
  - macOS: `brew install --cask libreoffice && brew install poppler`
  - Debian/Ubuntu: `apt-get install libreoffice-impress poppler-utils`

## Development

The test suite drives `deck.py` end-to-end through its CLI — including the adversarial cases (atomic rejection, runtime aborts, merged-cell guards, deck-wide media swaps):

```bash
pip install python-pptx Pillow pytest
pytest tests/ -v
```

No binary fixtures: tests generate their decks with python-pptx on the fly.

## Who built this

deckhand is open-sourced from real work by [Every Consulting](https://every.to/consulting). We built it to make our own decks — every training we run ships with a branded deck, and our agents build them with deckhand. Then we delivered it as client work: one client's team used to spend hours of a person's day on every deck — hundreds of human hours across the team — assembling, rebranding, and updating presentations by hand. We helped them automate that pipeline end to end, and deckhand is the engine that made the agents reliable enough to trust with it.

If you want your team's work automated like this — decks or anything else — [that's literally what we do](https://every.to/consulting).

## License

MIT
