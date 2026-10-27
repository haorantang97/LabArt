# Audit of okrm-return-01 (stage 1, blank control)

Audited 2026-10-27 from `okrm-return-01.zip` (sha256 `fbef58a6…`) and `okrm-return-01-transcripts.zip`
(sha256 `3a4e617a…`), both rebuilt from parts whose hashes matched the owner's list. The package is kept
by the owner; nothing from it is committed except the figures quoted here.

## What was run

Six new briefs (photobook, tailoring identity and launch object, night-walk poster series, farmers'
magazine, seed-bank website, ferry-terminal wayfinding). Arms A (no skill) and C (okrm-design 0.5.0),
two runs each, all four started within six seconds of each other, Opus 5.5, Claude Code desktop,
`bypassPermissions`, each in a fresh session in its own folder outside any repository, started by an
operator-assistant session with the same one-line task and one neutral sentence of background. Both
arms had the same image-generation bridge (`tools/gen-image.sh` calling the Codex CLI bundled with the
ChatGPT app), described by the same paragraph added to both `TASK.md` files. A first attempt of all four
was stopped after five minutes because the bridge had not been provided; its transcripts and partial
outputs were returned. A fresh judge session saw only the judge room. The owner ranked the boards blind
before the key was opened.

## Integrity and isolation (checked against the transcripts, not only the manifest)

- Every part and both whole zips matched their hashes. Each final run has the twelve images at the
  required sizes, notes for every brief and `DONE.md`.
- No intervention in any final run; no web search or browsing; no message between sessions; no session
  read another run's folder, the handoff package, the key or the owner's notes. Arm A never met the skill
  or the studio's name. The skill files in both C folders were byte-identical to the package before and
  after.
- Each session listed the harness's notes folder for the starting session at the start; it was empty for
  all eight runs. Two C runs wrote handover notes there at the end; only the judge listed the folder
  afterwards and saw the two file names without opening them.
- Minor, symmetric or harmless: every folder sat under `okrm-exp/`, so arm A and the judge saw "okrm" in
  their own paths (none mentioned or searched it); a global `CLAUDE.md` about local storage made two
  runs list `~/Data`; C runs installed Playwright into their own folders.
- Tool faults found: on macOS's case-insensitive file system the judge's output `judge.md` overwrote the
  task file `JUDGE.md` (the verdict survived under that name and matches the transcript); the judge-room
  script expects a font that macOS lacks, so the operator redrew the boards from the shuffled images
  with the same layout and without opening the key.

## How much of the skill was used

| Run | Skill files read |
| --- | --- |
| C1 | SKILL.md, genesis, form-derivation, typography, cases, study-notes; ran tokens.py |
| C2 | SKILL.md, genesis, form-derivation, qa, deviation-operators, layout, material-and-line, cases, ui-translation; ran tokens.py |

Neither run read `recipes.md`, whose section 5a is the guidance on using an image tool; C1 read neither
of the two references added in 0.5.0 (layout, material and line). Both stopped first attempts had read
almost everything. Agents choose a subset of a twelve-file skill, so the experiment measured the skill as
partly read.

## Results

| Brief | Owner (blind) | Judge |
| --- | --- | --- |
| 1 Market | C2 > C1 > A2 > A1 | A1 > C2 > C1 > A2 |
| 2 Tailor | C2 > C1 > A1 > A2 | A1 > C2 > C1 > A2 |
| 3 Night Walks | C1 > C2 > A2 > A1 | C2 > C1 > A1 > A2 |
| 4 Field Notes | C2 > C1 > A1 > A2 | C2 > A1 > C1 > A2 |
| 5 Seed Bank | C2 > A2 > A1 > C1 | C1 > A1 > C2 > A2 |
| 6 Ferry Terminal | A1 > C1 > C2 > A2 | A1 > C2 > C1 > A2 |
| Mean rank | C2 1.50 · C1 2.17 · A1 3.00 · A2 3.33 | A1 1.67 · C2 1.83 · C1 2.50 · A2 4.00 |
| C above same-run A | C1 > A1: 4/6 · C2 > A2: 6/6 | C1 > A1: 2/6 · C2 > A2: 6/6 |

Against the criteria fixed before running (C above the same-run A on at least four briefs, both runs
agreeing): **met on the owner's ranking** (4/6 and 6/6); **not met on the judge's** (2/6 against 6/6, the
runs contradict). The owner's ranking is the one the criteria were written for, and the owner is the
designer the skill is for; the judge is a check, not the arbiter.

Both rankings agree that C2 is consistently strong and A2 consistently weakest. The difference between
two runs of the same condition (A1 against A2) is as large as the difference between conditions. The run
that read the layout and material references (C2) was the owner's first on five of six briefs and both of
the owner's favourite images; the run that did not (C1) was weaker. One pair of runs cannot separate this
from chance.

## What the images show

- **Two tastes.** The judge rewarded completeness and presentation polish (A1: colour-coded systems,
  chips, cards, display serifs, staged desk shots). The owner rewarded restraint and white space and
  called most of the set "too dense, too regular, like mainstream domestic design", with more white space
  expected. The C runs were quieter (system type, tables, monochrome, unstyled interfaces); the A runs
  looked like agency work. A model judge is not a proxy for the owner's taste.
- **Density.** Even the quieter C runs put whole records on the page: forty farms in a table on a
  magazine's opening spread, sixteen-row indexes. The record as a readymade pushes toward density unless
  the skill says how much of it to show.
- **Props.** Image generation brought the same styling into every arm: loupes, red pencils, film strips,
  scissors, tape measures, raking light on rustic wood. The judge named "desk flat-lays with props" as the
  most common weakness. The skill's rule against this sits in `recipes.md` 5a, which no C run read.
- **Convergence.** All four arms found the same readymades (contact sheets with grease pencil, ledgers
  and paper patterns, building plans, soil profiles, seed packets, split-flap boards). With a shared model
  and a shared image tool, the idea rarely separates the rows; execution does.
- **Scope.** The owner noted that two briefs (wayfinding in a terminal hall, posters on a hoarding) lie
  outside the studio's usual territory of print, books and their extension to the web; there the image
  tool did most of the work and the arms converged.
- **Numbers.** The judge found arithmetic and date errors across arms (frame counts that do not reconcile,
  a "driest" farm that is fifth-driest); and material ignored where the brief made it the constraint
  (full-colour photography destined for newsprint).

## Changes made as a result (0.6.0)

- `SKILL.md` names a required reading list per kind of task and carries a compact set of core rules
  inline, so the essentials hold even when references are skimmed.
- White space is made a decision: how much of a record to show, one thing per page, a measured empty
  area; tables excerpted rather than printed whole on covers and openers.
- Object views and generated imagery: no styled props or mood lighting unless the derivation table names
  them; plain surface, even light; no handwriting set in a font.
- The process named in the brief is respected in the render (newsprint, two inks, one colour on board).
- Applicability states that the evidence is strongest for print and its extension to the web, weaker for
  architectural wayfinding.

## For the next run

- Rename the judge's output to `verdict.md`; give `make_judge_room.py` a font fallback for macOS.
- Use a neutral parent folder name.
- Run three times per arm if the budget allows; the run-to-run spread is as large as the effect.
- Keep the owner's blind ranking as the primary measure; if a model judge is used, give it the owner's
  stated taste as a second rubric and report both.
