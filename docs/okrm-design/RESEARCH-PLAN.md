# Research plan for okrm-design 0.3

This note hands the study to a local session. It records why 0.2.0 still produces
conventional work, what evidence is missing, and the protocol for the next round.

## Why 0.2.0 still reads as conventional

1. **The sample is thin and biased.** 31 photographs from the studio homepage, about 20
   projects out of several hundred. Most show closed objects or covers; only about six show
   interior spreads; none shows a full sequence, a website in use, motion, or an exhibition
   walk-through. Fashion and brand work (ALYX, T.T, Goldwin 0, JW Anderson), which is the
   studio's current core, is under-represented.
2. **The methodological book was not read.** *A Meaningful Order* (2025, 26 chapters A–Z)
   is the studio's own account of its method. Only its publisher description was available.
3. **The rules are averages.** Measuring many projects and keeping the typical value
   (two poles of scale, one flat colour, centred labels) produces the median of the
   practice. The practice's character lies in each project's one strange decision: three
   identical copies sold together, a catalogue that is a cassette, a perforated PVC cover,
   a rubber band instead of a binding, a vertical fold no newspaper machine had made. 0.2.0
   names these as examples but has no rule that forces one.
4. **The gates are mostly prohibitions.** They remove decoration and generic moves, which
   pushes outputs towards clean Swiss-style layouts. Nothing rewards a decision a
   conventional designer would reject.
5. **The examples are screen mock-ups.** They are flat HTML in placeholder fonts with
   self-referential copy about design. The studied work lives in objects, materials,
   art-directed photography, and sequence. None of that is in the examples.
6. **There is no evaluation loop.** No outputs were generated from briefs and compared
   blind against references or against a no-skill baseline.

## Evidence to collect

Store raw images and texts **outside the repository** (third-party copyright). Commit only
derived data: the annotation table, measurements, and written notes.

| Source | What to take | Target |
| --- | --- | --- |
| ok-rm.co.uk | Every project page (the site is Next.js with a Sanity CDN; the homepage alone lists 31 images) | All projects, all images |
| Instagram @okrm_london | Interiors, sequences, installation views, motion stills | 150+ images, dated |
| in-other-words.co.uk | `/collections/all/products.json` gives 41 products with image URLs and specs | All product images |
| *A Meaningful Order* | The book itself: chapter titles, the A–Z argument, measured spreads | Read in full; scan contents and 20 spreads for private study |
| Tokyo TDC 2020 and 2026 award pages, Creative Review (Strelka, Fear and Love), Design Week, the Met's catalogue article, Strelka Mag | Texts that refused automated access from the cloud session | Read in full |
| Fonts In Use, It's Nice That, BP&O galleries | Project images with typeface credits | All OK-RM entries |
| Physical copies the user owns | Real-size measurements of type, margins, paper, binding | Any available |

## Annotation schema

One row per image, in `docs/okrm-design/data/annotations.csv` (create it):

```text
project, year, medium, format_mm, view (cover|spread|object|space|screen),
device_type (readymade|system|duality|other), readymade_or_system,
strange_decision, voices, smallest_type_pct_height, largest_type_pct_height,
alignment, colour_as_material (y/n + hex), materials, image_treatment,
sequence_move, notes
```

Record distributions and outliers, not means. The `strange_decision` column is the most
important one: one sentence naming the decision a conventional designer would not make.

## Changes to make in the skill

1. **Deviation operators.** Add a reference file listing the moves found in `strange_decision`,
   grouped by what they change: format (fold, multiples, container, scale-less cover),
   substitution (the catalogue becomes a readymade object), sequence (interleave, rotate,
   three copies), context (an archived object, an exhibition as theatre), interface (the
   implicit made explicit). Each operator gets its source projects and a transfer example.
2. **A required strange decision.** Add a main gate: the output must contain one decision
   from the operators, stated in the device statement, that a conventional designer would
   reject, and it must still follow from the content.
3. **Art direction of images.** Add rules for commissioning and sequencing photography:
   objects shot flat on black or on everyday surfaces, white-bordered plates, double-black
   printing, pairs across the spread.
4. **Distributions, not defaults.** Replace single numbers in the order system with ranges
   and named outliers.
5. **Object-first examples.** Re-make the gallery as photographed or rendered objects with
   real material, generated from fictional briefs, not as screen mock-ups with meta copy.

## Evaluation protocol

1. Write six fictional briefs across media: artist catalogue, fashion lookbook, quarterly
   journal, institution identity, exhibition graphics, archive website.
2. For each brief, produce three directions with: no skill, okrm-design 0.2.0, and the new
   version. Use the host's image generation where available.
3. Judge blind, in pairs, on three questions: Does it follow from the content? Is there a
   decision a conventional designer would reject? Could it be mistaken for a specific
   published project (it must not)?
4. Keep the new version only if it wins on the first two questions and passes the third.
   Record results in `docs/okrm-design/VALIDATION.md`.

## Boundaries

- Do not commit third-party images, scans or long quotations.
- Do not copy a specific layout, mark, fold, typeface or photograph.
- Do not use the studio's or designers' names in generation prompts.
