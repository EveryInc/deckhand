# Task: create — Dynamic Workflows deck

From-scratch creation under a real brief: web research, real downloaded assets, an
expert audience, and a hard slide count. This is the brief used verbatim in benchmark
rounds 1–3 (round 3 added the "real assets, not recreations" clause — keep it; both
arms must get it identically).

Placeholders, filled by the orchestrator (see [RUNBOOK.md](../RUNBOOK.md)):
`{{TOOLCHAIN_BLOCK}}` — the arm's toolchain instructions; `{{WORKDIR}}` — the arm's
private working directory.

---

You are a presentation designer-builder. Build a finished PowerPoint deck.

## The brief

Create a **15-slide deck about Dynamic Workflows in Claude Code**, announced here: https://claude.com/blog/introducing-dynamic-workflows-in-claude-code

- **Audience**: people who already use skills in Claude Code daily. They know what skills, subagents, and slash commands are — don't waste slides explaining basics. They want to know what dynamic workflows are, why they matter, how they differ from what they already do, and how to start.
- **Quality bar**: a deck so good you can't stop flipping. Every slide earns the page turn.
- **You are free to use the web**: fetch the announcement post, related Claude/Anthropic blog posts and docs for accurate content. Download images from the announcement post (or other relevant posts) and include them in the deck where they genuinely help — screenshots, diagrams, illustrations. Use real, accurate content; do not invent features.
- **Real assets, not recreations**: download the actual images from the blog post (check the page's `<img>` tags / og:image) and use at least one genuine screenshot in the deck. Recreated mockups are allowed in addition, but at least one real downloaded asset must appear.
- **Exactly 15 slides.**

## Your toolchain (use ONLY this)

{{TOOLCHAIN_BLOCK}}

## Process (do all three phases)

1. **Plan** — research the content on the web, then write a deck plan: narrative arc across 15 slides, plus your design plan, before building anything.
2. **Implement** — build the full deck per your plan.
3. **Review** — render every slide, look at the images, critique the deck as a sequence (consistency, overflow, collisions, pacing, anything ugly), and fix what you find using the skill's tooling. Do at least one genuine review-and-fix round.

## Working directory and deliverables

Work entirely in `{{WORKDIR}}`. Deliver there:
- `final.pptx` — the finished 15-slide deck
- `img/` — rendered JPGs of all final slides
- `contact-sheet.jpg` — a thumbnail grid of the whole deck
- `report.md` — brief build report: your plan, what you changed in review, any known limitations

Your final message: a short summary of the deck (narrative arc, design system, what review caught) and confirmation of the deliverable paths. Do not ask questions; make all decisions yourself.
