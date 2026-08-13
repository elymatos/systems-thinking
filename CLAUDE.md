# Project context

This repo is **Systems Thinking — Study Notes**, published at
https://elymatos.github.io/systems-thinking/ via [Quartz](https://quartz.jzhao.xyz/) v5, deployed
automatically by GitHub Actions on every push to `main` (`.github/workflows/deploy.yml`).

## Why this exists

The user is building a conceptual framework to represent "situations," roughly based on **image
schemas from Cognitive Linguistics**. This repo is step one: a systematic, faithfully-sourced
study of Systems Thinking, meant to ground that eventual framework in established systems-theory
concepts. **The image-schema mapping itself has not started yet** — everything currently in
`content/` is a pure systems-thinking review, deliberately free of cognitive-linguistics framing.
That mapping is the next phase, whenever the user is ready for it.

The user is also running a related, longer-running project at `/home/ematos/devel/fn3` (repo
`elymatos/fn3`, published at https://elymatos.github.io/fn3/) — a FrameNet/DUL ontology
project (frame semantics, scenario domains: physical, biological, social, cultural,
psychological, representational, space/time, moral). That's the likely eventual home, or at
least a close relative, of the "situations" framework this repo is meant to feed into.

## Folder structure

- **`content/`** — the published site content, git-tracked. `index.md` is the homepage
  (originally `docs/README.md`). 11 numbered chapters (`01-...md` through `11-...md`) plus
  `glossary.md`. Edit these directly — that's the working copy now (no separate `docs/` folder
  exists anymore; the old `/home/ematos/devel/SystemThinking/` working directory was retired
  once everything here was verified live).
- **`resource/`** — the original source PDFs (ebooks + slide guides from the Systems Innovation
  Network's 20-guide series). **Gitignored, local-only, no backup elsewhere** — this is the sole
  copy of the source material, so don't delete it.
- **`quartz/`, `quartz.config.yaml`, `quartz.ts`, etc.** — the Quartz site generator itself
  (upstream `jackyzha0/quartz`, v5). Not usually something to touch; content changes alone are
  enough to update the site.

## How the docs are organized

Chapters build vocabulary progressively (each assumes terms from earlier ones) — read/edit in
order:

1. Worldview and paradigm (analysis/synthesis, holism, systems awareness, reflexivity,
   perspective-taking, process-vs-substance ontology, the four paradigm shifts)
2. System fundamentals (sets vs. systems, function)
3. Boundary and environment (autonomy, agency, autopoiesis/allopoiesis, protocols)
4. Relations, synergy, and emergence (synergy/interference, game theory, differentiation/
   integration, emergence, weak/strong emergence via downward causation)
5. Hierarchy and abstraction (encapsulation, integrative levels, bottom-up/top-down causality)
6. Dynamics, feedback, and homeostasis (feedback loops, stocks/flows, cybernetics, requisite
   variety)
7. Efficiency, energy, and entropy
8. Systems science
9. Networks (nodes/edges, centrality, topology, weak ties, contagion)
10. Complex adaptive systems (self-organization, edge of chaos, evolution, iterated games)
11. Models and modeling (what makes a model effective — self-referential to this whole project)

`glossary.md` consolidates every defined term alphabetically, cross-referenced back to its
chapter — treat it as the single source of truth for terminology, and keep it in sync whenever a
chapter adds/changes a term.

## Working conventions established so far

- **Keep it tight.** The user has explicitly said they don't want lengthy documentation — a
  summary of the main ideas needed for further work, not exhaustive coverage. When adding
  content, favor short additions/cross-references over new sprawling sections; only add a new
  numbered chapter when a topic is genuinely distinct and substantial (that's how 09–11 came to
  exist, out of 7 source guides that were mostly redundant with 01–08).
  - **This applies while editing existing documents.** It does not apply as a constraint on
    writing brand-new artifacts (e.g. the image-schema framework itself, once that phase starts)
    unless the user says otherwise for that specific deliverable.
- **Avoid duplication across chapters.** When a concept spans two chapters, one canonical
  treatment plus a cross-reference beats restating it (this was fixed once already — ch. 4 and
  ch. 10 briefly had a duplicated game-theory passage, resolved by deepening ch. 10 with Nash
  equilibrium/iterated games instead of repeating ch. 4).
  - The user is comfortable with rewrites to existing definitions when new source material
    sharpens them (e.g. weak/strong emergence was redefined around downward causation), not just
    with additive changes.
- **Cite sources.** Each chapter opens with which ebook chapter/slide numbers it's drawn from.
- **Publishing loop.** Edit `content/*.md` → `git add` → commit → `git push origin main` →
  GitHub Actions builds and deploys automatically. No manual GitHub Pages steps needed anymore
  (Pages is already configured to build from GitHub Actions). Sanity-check with
  `npx quartz build` locally before pushing if a change feels risky.
- Two ideas already flagged as most likely to matter once the image-schema phase starts:
  **perspective-taking / partial construal** and **process vs. substance ontology**, both in
  ch. 1 — they map fairly directly onto vantage-point and PROCESS/PATH-vs-OBJECT phenomena in
  Cognitive Linguistics.
