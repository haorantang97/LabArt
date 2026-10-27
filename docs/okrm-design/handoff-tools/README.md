# Handoff and experiment tools

Tools for a blind control experiment with the okrm-design skill, fixed after the first local run
(see `../AUDIT-01.md`). Not part of the skill package.

- `render.mjs` — render `*.html` with `<meta name="size" content="WxH">` to PNG (Node + Playwright).
- `make_judge_room.py` — shuffle finished runs into a blind judge room under blinded file names; the key
  is written outside the room. Boards are drawn with Pillow (font fallback for macOS, Windows, Linux) or
  written as HTML to render.
- `JUDGE.md` — the blind image-judge task; the judge writes `verdict.md` (not `judge.md`, which would
  overwrite `JUDGE.md` on a case-insensitive file system).
- `pack_return.py`, `manifest-template.json` — pack a run's results with hashes and checks. The twelve
  expected image sizes in `pack_return.py` belong to the stage-1 briefs; edit `SIZES` for new briefs.

Lessons from the first run: give the parent folder a neutral name; run each arm at least three times;
give both arms the same image-generation bridge and the same task text apart from the skill paragraph;
take the owner's blind ranking before opening the key and treat it as the primary measure.
