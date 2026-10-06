# AI Productivity Cube — engineering workspace

A pocketable, cube-like physical interface for a personal AI productivity agent (Pocket Mode + Desktop Mode via a
magnetic dock). This repo is the engineering knowledge base: decisions, research, BOMs, plans.

## Start here
1. `CURRENT_STATE.md` — one-page status (architecture, size, cost, risks, next milestone).
2. `PROJECT_BRIEF.md` — canonical product definition (accepted content only).
3. `DECISIONS.md` — ADR log (Accepted / Proposed / Superseded).
4. `tasks/TASK-001-…md` — the current task and its answers.

## Layout
```text
README.md · PROJECT_BRIEF.md · CURRENT_STATE.md · DECISIONS.md · OPEN_QUESTIONS.md · ROADMAP.md
research/     why: comparisons and evidence per subsystem
electronics/  what: architecture, block diagrams, pin map, power budget, wiring, bring-up, risks
bom/          buy: BOM, SHOPPING_CART (generated), BOM.csv (generated), costs, alternates, sources
mechanical/   size envelopes, internal packaging, pocketability test plan
tasks/        TASK-xxx files + BACKLOG
notes/        research_log.md (chronological)
tools/        cube_model.py — single source for size, mass, power and cost numbers
```

## Regenerating numbers
```bash
python3 tools/cube_model.py                 # print size / power / cost tables
python3 tools/cube_model.py --csv --cart    # also rewrite bom/BOM.csv and bom/SHOPPING_CART.md
```
Change assumptions or prices **in `tools/cube_model.py`**, re-run, then update the prose docs that quote the numbers.

## Rules
- Evidence over intuition; every hardware claim has a source in `bom/SOURCES.md`.
- Never edit an accepted decision in place — add a superseding ADR.
- Nothing is ordered from this workspace. No PCB design until TASK-001 is reviewed.
