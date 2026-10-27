# Handoff protocol

The work on this package moved from a cloud session to the owner's machine in two stages. This file is
for whichever session audits the return: it says what was handed over, what comes back, and how to
audit it. It is process documentation, not part of the skill.

## Stage 1 — blank control (handed over 2026-10-27)

`okrm-handoff-stage1.zip` (kept by the owner; not committed) contains:

- `work-A/` and `work-C/`: identical `TASK.md` and `briefs.md` (six new briefs: a photobook, a
  tailoring workshop's identity and launch object, a night-walk poster series, a farmers' magazine, a
  seed-bank website, ferry-terminal wayfinding) and a render tool; `work-C/` adds
  `.claude/skills/okrm-design/` at 0.5.0, commit `f9a4a95`. The task texts differ by one paragraph.
- `judge-kit/JUDGE.md`: the blind image-judge task.
- `operator-tools/`: `make_judge_room.py` (shuffles runs into a judge room, key kept outside),
  `pack_return.py` (checks the twelve images and their sizes per run, hashes every file, zips),
  `manifest-template.json`.
- `OPERATOR.md` (Chinese): design, isolation checklist, steps. `RETURN-SPEC.md` (Chinese): the return
  interface.

Design: arms A (no skill) and C (okrm-design 0.5.0), one run each at minimum, two recommended; same
model, tool, permission mode, image-generation availability and first message
(`Read TASK.md in this folder and do it.`); each run in a fresh session in a fresh folder outside any
repository; a fresh judge session sees only the judge room; the owner ranks the boards blind before
opening the key.

Criteria fixed before running: the skill helps if C ranks above the same-run A on at least four of
six briefs and both runs agree; no difference if wins split or runs contradict; harmful if A mostly
wins or C is judged more formulaic.

## The return

`okrm-return-<id>.zip` with `manifest.json`, `OPERATOR-NOTES.md`, `runs/<A1|C1|A2|C2>/{out,transcript}`,
`judge/judge-room/` (with `judge.md` and its transcript) and `judge/key.json`. It arrives as a chat
attachment or on a branch `handoff/okrm-return-<id>` under `handoff/`.

## Audit checklist

1. Integrity: unzip, recompute sha256 against `manifest.json`; read `checks` (missing images, sizes,
   transcripts).
2. Isolation: from the transcripts, confirm each run started fresh, read nothing outside its folder,
   made no web requests, and that arm A never encountered the skill or the studio's name; record
   interventions and any deviation the owner noted.
3. Fidelity: in arm C, which skill files were actually read, whether a derivation document exists per
   brief, and whether the images follow it; in both arms, how image generation was used (count,
   prompts, type kept in HTML or baked into images).
4. Results: decode the key; per brief, compare C against the same-run A; check agreement between runs;
   compare the judge's ranking with the owner's blind ranking and weigh the owner's above the judge's
   where they differ.
5. Patterns: the monument used in each image (number, word, image, colour, material, line); whether
   object views read as objects; legibility at use scale; record fidelity; repetition of one formula
   across briefs within a run.
6. Cost: time, turns and rework per run, from the transcripts.
7. Write `AUDIT-<id>.md` beside this file; fold confirmed findings into the skill with a version bump;
   update `VALIDATION.md` and the changelog.

## Stage 1 result

Returned as `okrm-return-01` and audited in [AUDIT-01.md](AUDIT-01.md). Tool fixes for any rerun: the
judge's output must not be named `judge.md` beside `JUDGE.md` (case-insensitive file systems), the
judge-room script needs a font fallback for macOS, and the parent folder should have a neutral name.

## Stage 2 — context transfer (2026-10-27)

The context is now in the repository rather than in a separate archive: [CONTEXT.md](CONTEXT.md) (goal,
research basis, version history, every validation round, practices tried and disproved, the owner's
taste, boundaries, open questions) and [NEXT.md](NEXT.md) (the next phase: distil the work again by
project series, with emphasis on material, paper, print technique and line; sources, dossier template,
outputs for 0.7, how to test). Fixed experiment tools are in [handoff-tools/](handoff-tools/).
`okrm-handoff-stage2.zip` (kept by the owner) holds only a start-here note for the local session and a
note for the owner. The cloud session ended after this handoff; further fetching and distillation run
locally.
