# Changelog

## okrm-design 0.4.0 - 2026-10-27

- Carried the chain through to the work. The deliverable is now the design itself with a
  derivation document beside it; type, scale, structure, colour, image and sequence are each
  written as "decision | because | the conventional move", the "because" pointing back to the key
  point, the readymade or the object.
- Added `references/form-derivation.md` (steps 5–11 with the derivation-table template) and
  `references/typography.md` (how a typeface is chosen: the readymade's own type, who is speaking,
  ubiquitous languages first, named faces and fallbacks per medium, three worked derivations).
- Reduced `genesis.md` to the upstream and a handover step; rewrote `qa.md` with derivation and
  work gates; rewrote `SKILL.md` around the chain.
- Remade the worked example end to end: a derivation sheet, a cover and a spread for one fictional
  catalogue, every visual decision on the pages traceable to a row of the sheet. The manifest's six
  screenshots now start with the derivation sheet.

## okrm-design 0.3.0 - 2026-10-26

- Moved the method's core from form to path. The deliverable is now a generation document
  written before any layout: nine steps (position, question, key point, framework, object,
  method, making, production, continuation) plus one strange decision that a conventional
  designer would reject and that follows from the content. Form comes after step 6.
- Added `references/genesis.md` (the protocol with evidence, templates and a test question
  per step), `references/cases.md` (34 project paths by type and year, each ending with its
  strange decision) and `references/deviation-operators.md` (the moves drawn from those
  decisions, grouped by what they change, with conditions and transfer examples).
- Rewrote the acceptance gates so the generation document, the strange decision and the
  object are tested before the page.
- Extended the evidence: the publisher's 41 product descriptions and full specification
  index, 376 product images and 267 press images, three reports on a 2026 brand exhibition,
  reviews and binding notes for a retrospective book, and the publishing notes of a
  three-part research programme. The case-to-source index is in `docs/okrm-design/CASES-INDEX.md`.
- Added a generation-document example; the manifest declares six screenshots.
- Ran two rounds of a blind comparison of three directions on three fictional briefs (no
  skill, 0.2.0, 0.3.0), each judged by a separate agent. Round 1 went to 0.2.0 and exposed
  three failures of the protocol (imported readymades, filler in optional fields, numbers
  that did not close); after the protocol was revised on those points, round 2 went to 0.3.0
  on all three briefs; round 3, on three new briefs in other media (a risograph poster
  series, an archive website, an anniversary book with a room), went to 0.3.0 again but
  exposed a severable strange decision and an unmeasured room, now gated. All rounds and
  the revisions are recorded in `docs/okrm-design/VALIDATION.md`.

## okrm-design 0.2.0 - 2026-10-26

- Rebuilt the method on primary sources after the session's network policy was opened:
  twelve interviews and conversations, the retrospective press release, the publisher's
  catalogue of 41 publications, about twenty project reviews, seven typeface records, the
  31 work photographs on the studio website measured with a 0.1 grid, and the website's
  own CSS. 0.1.0 had been written from search summaries only.
- Replaced the five rules with eight principles taken from the studio's own words:
  content and concept, magnified clarity, performative framework, readymades and
  ubiquitous languages, economy as form, structure and play, duality, sequence of reading.
- Corrected the scale rule to two poles (label-small or monumental, nothing in the
  headline middle), the colour rule to one flat colour used as a material rather than an
  accent, and the alignment rule to follow the readymade (labels centred and letterspaced,
  grotesk words in corners). Removed the unsupported claim about large page numbers.
- Added measured starting values to the order system: type heights relative to the cover,
  label position and width, plate borders, spine strip widths, website font sizes in vw.
- Added device statement types (readymade, system, duality), a framework paragraph
  (stage, actors, script) in place of mood boards, fixed/variable tables, and a cover
  skeleton. The UI translation now covers "the implicit made explicit": actions as text in
  brackets, counters as furniture, whole-screen colour as the change of paper.
- `scripts/tokens.py` now emits label and monument sizes, tracking, plate and poster
  borders and a field colour, and rejects middle-sized type, a second colour, a field used
  as an accent, and a field that cannot carry type. Tests grew from 12 to 15.
- Re-made the examples under the corrected rules and added a catalogue cover; the manifest
  declares five screenshots.

## okrm-design 0.1.0 - 2026-10-26

- Added **OK-RM Design · 有意义的秩序**, a graphic and UI design method distilled from a
  study of one London studio's published work and interviews: find one device in the
  content, exaggerate it through dry systematic typography, let production economy shape
  the form, and design reading as a sequence.
- The package holds a seven-step workflow, an order system (type pair, scale ladder,
  fold-derived grid, furniture, colour, material, imagery, sequence), a UI translation
  with an HTML/CSS skeleton, prompt recipes and a correction table, acceptance gates, and
  study notes stating the evidence base and boundaries.
- Added `scripts/tokens.py`, a standard-library order-sheet generator and checker
  (two families at most, three magnitudes of scale, one accent, legible contrast,
  fold-derived columns, 45–75 character measure), with 12 behavioral tests under
  `tests/okrm-design/`.
- Four declared screenshots are fictional projects made with the method, rendered from
  HTML sources under `assets/okrm-design/examples/` with `scripts/render_okrm_examples.mjs`.
  The package contains none of the studied studio's artwork and reproduces none of its
  layouts; the source list lives in the repository documentation, outside the package.
- Registered the plugin in the marketplace and added its tests to the package workflow.

## plugin packages 0.2.1 - 2026-10-15

- Moved plugin introductions and validation history to `docs/<plugin>/`, Deadpan
  repository artwork and design records to `assets/deadpan-doodles/`, and developer
  tests to `tests/`. Marketplace package sources remain `plugins/<plugin>/`.
- Retained every image declared by the plugin interface. Runtime style references,
  fixed prompt recipes, rendering helpers, and behavioral reference data stay bundled.
- Made Tephra's mode-selection image self-contained in its standalone Skill and
  updated its screenshot path. Included the existing license in each install unit.
- Updated all three plugin manifests to 0.2.1, kept both Deadpan introduction
  editions aligned, and added package inventory and dependency checks.
- Standalone gh installation selects `main` explicitly to avoid the old repository
  release tag. See `docs/VALIDATION.md` for the checks and their scope.

## deadpan-doodles 0.2.0 - 2026-09-26

- Published the general Sha Bing package with fixed recipes, an invocation protocol,
  a dedicated portrait module, a reference index, visual checks, and a local prompt assembler.
- Preserved recipe revision `shabing-20260925-1` and its checked visual anchors;
  shape allocation replaces the former uniform 40% proportion target.
- Added three selected portrait examples and one illustration sheet to the gallery.
- Added the author's introduction to the plugin pages, with the supplied Chinese
  text preserved verbatim and a full English edition. The collection homepage
  remains a short overview and gallery.
- Gallery examples do not add automatic generation references or establish
  deterministic visual reproduction. See the plugin validation notes.

## deadpan-doodles 0.1.1 - 2026-09-16

- Replaced ambiguous "slightly" exaggerated proportions with an approximately
  40% relative change in one named dimension relationship, plus a visible consequence.
- Distinguished relative deformation from a part's share of the whole; no
  universal forehead percentage or image-tool strength setting is implied.
- Added counter-scaling checks so shoulders, heads, stems, or furniture do not
  grow alongside the selected feature and cancel the intended contrast.
- Updated the specialized portrait recipes and synchronized the two README editions.
- Kept watercolor material assets unchanged. New generations remain test candidates.

## deadpan-doodles 0.1.0 - 2026-09-16

- Added **Deadpan Doodles · 沙冰**, a pen-and-watercolor illustration skill for
  people, animals, plants, objects, and small scenes.
- Bundled two generated material references and a region-based brushwork index;
  no source photographs or third-party reference images are included.
- Separated subject identity, playful proportions, and watercolor material.
  Restored moderate, subject-led proportion contrasts instead of fixed anatomy.
- Moved photo-based portrait guidance into a specialized reference module;
  portrait-specific facial rules no longer govern animals or plants.
- Added single-change editing guidance, English/Chinese documentation, and
  reference provenance. Generated examples illustrate material, not guaranteed output.
- See the plugin's validation notes for package checks and generation-test scope;
  the new public plugin name has not been installation-tested.

## tephra 0.2.0 - 2026-09-06

### Renamed, and reference material removed

The plugin was previously published under a name taken from an existing artist's
series. It is now **tephra** — the geological term for the fragmental material a
volcano throws out, which is what this renderer makes a picture do. Anyone who
installed the old name should reinstall.

Alongside the rename, every pointer to a specific artist or artwork was removed from
the package: the homage line, the catalogue of surveyed works, work titles inside the
measurement tables, source filenames, and the URLs the workflow told an agent to open.
The measurements themselves are unchanged and still drive `native_check.py` — the
tables now identify their samples by letter. What was removed is identification, not
evidence; the numbers are what the algorithm needs, the titles only ever added
exposure. `references/` now states where the numbers came from in general terms.

The legacy preset `wanderer` was renamed `anchor`, with the old spelling kept as a
silent alias so commands written against 0.1.0 still reproduce byte-for-byte.

### Two canonical modes, not one

0.1.0 shipped with a single canon ("pure particle; the mass layer was rejected").
That was true of the reference works it was modelled on, and false of the ones added
since. There are now two co-equal modes, chosen by subject:

- **Pure particle** (`--mass 0`, preset `flux`) — short strokes follow the image's own
  structure field and travel along it. Right for waves, smoke, light shafts, fire:
  anything already in motion. Unchanged from 0.1.0; every 0.1.0 command still means
  exactly what it meant.
- **Dithered solid** (`--mass 2.6` + native-grid rendering) — the image's tone becomes
  an ordered 8x8 dither that is perfectly static frame to frame (measured inter-frame
  persistence 0.999 vs 0.83 for particles) and can be combed along a direction into
  hard-edged fracture streaks. Right for figures, sculpture, animals, architecture:
  anything whose contour and volume have to read.

Fracture streaks are only available in the second mode: `--comb` smears an existing dot
lattice, so with no mass layer there is nothing to comb. SKILL.md now says so, and says
how to pick between the two, over a side-by-side of the same subject rendered both ways
(`assets/examples/canon-modes.jpg`, animated as `canon-modes.gif`). Each side is that
route tuned to its own best, which is the comparison worth looking at: taking the
dithered command and simply setting `--mass 0` empties the frame, because that recipe
carries almost no stroke dust and the whole picture rests on the dot layer.

`--mass` is documented as what it is — a brightness threshold, not a style switch. What
the layer looks like is decided by the shape of the source image's tone distribution, so
the same value gives a graded halftone on a side-lit sculpture and a flat cut-out on a
backlit silhouette. The fix for the flat case is preprocessing (M0.5), not `--mass`.

### Fixed: the same seed stops reproducing the same file

The turbulence curl field drew from the shared RNG on every render, with no flag guarding
it. That shifted every later draw — stroke seeding, rain — so a 0.1.0 command run against
a newer script produced a different picture from the same seed (14%-74% of pixels moved,
depending on preset). It now takes its own stream. All six legacy presets are byte-identical
to 0.1.0 again.

Rain dash placement does differ: the void layer was rebuilt (2 parameters became 17, with
measured constants for dash lifetime and travel), so legacy `--rain` commands put dashes in
different places. Subject and structure are unaffected; the difference is 0.05%-0.2% of pixels.

SKILL.md now carries the rule this came from: a noise field built on every render must take
its own stream, never the shared one.

### Added

- **Fracture / dissolve** — `--dissolve`, `--escape`, `--turbulence`, `--anchor`, and the
  `--dissolve-*` family: hold part of the subject solid and let the rest erode into flying ash.
- **Comb** — `--comb` (13 fields), `--comb-emit`, `--comb-life`: the dot lattice is smeared
  along a direction into pixel bars, with divergence that grows with distance, a tail-only
  random walk, and a ragged outer boundary.
- **Void layer** — 15 new `--rain-*` parameters with constants measured off the reference
  works. `--rain-life` is one of those constants; no other module may borrow it.
- **Native-grid rule** — the reference's true grid is 512x384, so a "pixel" is 1/512 of the
  width. Dithering straight at 1400 makes each pixel 2.7x too fine and the debris reads as
  smoke. Render at 512-768 and upscale with `scripts/upscale_nearest.py`.
- **Verification scripts** — `native_check.py` (scores a GIF against the reference's measured
  numbers), `dp_fitness.py`, `m4_check.py`, `m4_erode.py`, `p4_mask.py`, `strand_check.py`.
- **references/** — the measurement notes the SKILL cites: artist survey, module table, and
  the density / edge / rain proposals.

No parameter was removed or renamed. Legacy presets are unchanged: the six new keys added to
them carry the old hard-coded defaults.

## marketplace - 2026-08-27

- Renamed the marketplace from antibes-holiday to labart (repository: LabArt).
  With a second plugin aboard, the marketplace is no longer synonymous with its
  first skill. Users who added the old marketplace name should re-add it.

## tephra 0.1.0 - 2026-08-27

- Added the Tephra plugin as the marketplace's second skill: a
  deterministic pixel-particle renderer with structure-following flow,
  long/short stroke mix with sub-segment fray, physics-planned regional motion
  (flow regions, swirl, burst-driven flow), density conservation against
  field-attractor artifacts, and seamless PNG/GIF/MP4 output.

## 0.2.0 - 2026-07-26

- Reworked the stroke system around structural drift, missed junctions, displaced
  restarts, localized correction, and visible loss and recovery of control.
- Added a bounded decontrol pass and diagnostics for overly polished period,
  fashion, and editorial sketching.
- Added safeguards against generic loose-sketch texture, stick-symbol collapse,
  and unrequested cartoon punctuation.
- Replaced the bundled calibration asset with a selected non-semantic physical
  pen sample.
- Replaced the public gallery with seven selected 4:5 example outputs.

## 0.1.0 - 2026-07-26

- Initial public release.
- Added relaxed black-pen stroke, shorthand, and stopping system.
- Added narrative staging and non-equilibrium composition.
- Added original non-semantic stroke calibration asset.
- Added renderer capability detection and honest no-renderer fallback.
- Added Codex Plugin and Marketplace packaging.
- Added English installation documentation.
- Added public validation notes and six selected original example outputs.
