# deckhand evals

End-to-end evals for deckhand, run the way the tool is actually used: **an agent gets a brief and a toolchain, builds or edits a real deck, and blind judges score the result.** These are not unit tests (those live in `tests/`) — they measure the thing unit tests can't: does an agent holding this tool produce better decks?

The harness is itself agent-native. There is no runner binary; an orchestrating agent executes [RUNBOOK.md](RUNBOOK.md) directly — launching builder subagents, blinding the renders, launching judge subagents, unblinding, and tallying. Any agent platform that can run subagents and shell commands can run it (we use Claude Code).

## What's here

```
evals/
├── RUNBOOK.md     # the full protocol, written for an orchestrating agent to execute
├── tasks/         # builder briefs (what the competing agents are asked to do)
│   ├── create-dynamic-workflows.md    # from-scratch: 15-slide deck, web research, real assets
│   └── edit-retheme-and-insert.md     # edit: full palette re-theme + insert one new slide
├── judges/        # judge briefs (how results are scored)
│   ├── create-judge.md   # 7-dimension blind scoring for from-scratch decks
│   ├── edit-judge.md     # 6-dimension blind scoring for edit quality
│   └── edit-auditor.md   # forensic fidelity audit (machine-assisted, non-aesthetic)
├── scripts/
│   └── blind.py   # anonymizes two arms' renders into deck-A/deck-B for the judges
└── results/       # one markdown verdict log per run (committed; heavy artifacts stay local)
```

## The protocol in one paragraph

Two builder agents receive **identical briefs** — same content task, same quality bar, same process requirements (plan → implement → review) — differing only in the toolchain block: one uses deckhand, the other uses the baseline under comparison (we benchmark against [Anthropic's pptx skill](https://github.com/anthropics/skills)). Both run in parallel with no knowledge of each other. Their finished decks are re-rendered with one neutral command, then `blind.py` randomly assigns them to `deck-A`/`deck-B` and strips every identifying name. Three judges (create) or two judges plus a forensic auditor (edit) score blind, each with a different prescribed viewing order so order bias cancels. Only after all verdicts are in is the assignment revealed.

## Why we keep these in the repo

Every defect a judge finds in the deckhand arm is a product finding, and the rule is that **findings become machinery, not prompt patches**: the text-under-picture lint, the serif re-wrap margins, the `<br>`-in-table-cell fix, the zoom-before-dismiss rule, the `replace-color` op, and the `set-theme`/`set-props`/`set-slide` universal-editor pass all came out of eval rounds. A failure class that becomes a lint or an op never recurs; a failure class addressed by prompt wording recurs every round. Committed evals make that loop repeatable: change the tool, rerun the eval, compare against `results/`.

## Running one

Point an orchestrating agent at this directory:

> Run the create eval in `evals/` per `evals/RUNBOOK.md`, comparing the deckhand skill in this repo against <baseline skill path>. Write the verdict log to `evals/results/`.

Requirements: an agent platform with parallel subagents, LibreOffice (`soffice`) + Poppler (`pdftoppm`) for rendering, and each arm's own toolchain dependencies (for deckhand: `python-pptx`, `Pillow`, and Playwright + Chromium for the HTML create path).

## Adding a task

Add one markdown brief to `tasks/`. Keep the two invariants that make verdicts meaningful: the brief must be **toolchain-blind** (both arms get the same words; only the `{{TOOLCHAIN_BLOCK}}` differs), and it must demand a **finished, verifiable deliverable** (exact slide count, rendered images, a build report) so judges score artifacts, not intentions. If the task needs a new scoring lens, add a judge brief to `judges/` rather than overloading an existing one.
