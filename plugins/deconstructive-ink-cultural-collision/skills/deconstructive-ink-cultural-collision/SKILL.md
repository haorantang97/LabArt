---
name: deconstructive-ink-cultural-collision
description: Generate original monochrome Chinese-ink images that translate recognizable modern, anatomical, technological, cosmic, or landscape subjects through deconstructive brushwork. Use when the user wants dense authentic ink traces, accumulated cun strokes, broken contours, layered gray ink, meaningful paper reserve, and a traditional-modern collision without literal landscape collage.
---

# Deconstructive Ink Cultural Collision

Create an original image with the requested subject. Reproduce the visual grammar, never a source artwork's exact composition, character design, inscription, or signature.

## Core rule

Make the subject emerge from accumulated ink events. Assume there is no finished drawing underneath the ink. Do not design a complete object, render its volumes, and then apply an ink treatment.

Pursue **high mark information but low local semantic certainty**: add many disciplined small observations, then let controlled overlap, restrained paper absorption, paper reserve, and later pale layers make each observation incomplete. Local passages should be difficult to name; their ordered accumulation should make the whole subject recognizable. Ambiguity must never come from random splashing.

Use this five-pass construction order. Do not skip directly from a pale mass to a finished silhouette:

1. **Ghost scaffold:** place 3-5 recognition relations in very pale ink: gesture, weight, one turn, one joint or cavity, and one scale cue. Do not outline parts.
2. **Ordered cun fields:** divide the subject into a few structural fields. Build each field through repeated, related brush searches. A field shares a force direction but continuously changes stroke length, pressure, angle, dryness, spacing, and ending. Never count or tile strokes.
3. **Crossing revision:** cross selected packets with a second, lighter or drier family at a different angle. This pass corrects and partly conceals the first description; it must not become cross-hatching.
4. **Accumulated ink:** deepen only 2-5 structural hinges through repeated small brush deposits. Produce darkness by layering visible strokes, never by filling a black shape.
5. **Pale consolidation:** use a few restrained pale brush passes to join fields and push some detail backward. Preserve stroke evidence; do not cover the image in global fog.

Interrupt long boundaries with paper reserve, dry attenuation, overpainting, or a changed stroke family.

The result must be recognizable at thumbnail size and materially complex when enlarged.

## Non-negotiable appearance

- Use only ink black, charcoal gray, smoke gray, pale gray, and warm off-white paper. A seal or graphic accent is excluded unless requested.
- Treat detail as repeated acts of observation expressed through stroke scale, direction, wetness, pressure, overlap, and density. Do not use precise components, surface design, lighting, or rendered shadow as detail.
- Keep dark areas internally alive: several gray levels, dry gaps, paper pinholes, crossed strokes, and softened edges must remain visible.
- Let some thin lines appear as provisional traces, but never let them close the subject into a clean diagram.
- Use uneven density. Concentrate micro-detail around joints, cavities, load paths, and ink knots; keep those details partially merged and difficult to isolate. Allow quieter passages elsewhere.
- Never decorate the object's surface with contour-following texture. Marks must search across, interrupt, and sometimes contradict the apparent volume.
- Keep brushwork orderly and calligraphically controlled. Every mark needs a start, travel, pressure decision, and ending. Orderly does not mean geometric, straight, parallel, or closed.
- Define detail through **related brush searches**, not isolated decorative marks or countable packets. Begin, respond, interrupt, and revise, but never repeat a fixed unit across the image.
- Keep the subject's outer silhouette less resolved than its internal brush fields. Avoid the common AI pattern of a crisp outer creature filled with textured ink.
- Do not create haze by lowering contrast everywhere. Keep quiet pale passages, middle-gray working passages, and a few dense accumulated passages distinct.
- Vary brush character by region. Adjacent fields must not share one repeated mark shape. Change center-tip/side-brush balance, stroke scale, loading, spacing, and revision depth.
- Do not illustrate category symbols. A landscape need not contain readable trees, rocks, houses, or outlined peaks; a machine need not contain readable panels, towers, pipes, or fasteners. Recognition should come from the whole relation.
- Let subject and environment share the same brush vocabulary. Do not paste traditional mountains, clouds, or calligraphy beside a modern object.
- Favor asymmetry, oblique weight, interrupted rhythm, and active negative space.

## Select a mode

Read [references/style-spec.md](references/style-spec.md) and choose one mode:

- `anatomical-field`: high paper reserve, identifiable organ or body axis, provisional traces, cavities, irregular bilateral echoes, dense local knots.
- `modern-colossus`: readable monumental gesture, low-contrast gray field, porous dark torso, elongated dissolving limbs, no engineered background lines.
- `rotational-landscape`: circulating spatial force, multi-scale arc families, dense ridges around an irregular paper aperture, no smooth digital vortex.
- `general-modern-subject`: translate the subject's forces and load paths into cun families; do not add landscape symbols.

## Visual calibration

Default to text-only generation. Whole-artwork references can cause built-in image models to leak composition, seals, or a uniform microscopic surface pattern across the output.

Use one technique-calibration image from `assets/calibration/` only for diagnosis or when the user explicitly wants reference-assisted generation:

- `landscape-ink-field.webp`: calibrate accumulated cun density, multi-scale brush rhythm, and irregular paper reserve.
- `anatomy-ink-field.webp`: calibrate high descriptive labor with locally uncertain structure.
- `colossus-ink-field.webp`: calibrate low-contrast monumental mass, internal gray detail, and disappearing boundaries.

Assign the image the role **technique reference only**. Explicitly prohibit copying its subject, composition, pose, silhouette, anatomy, landmark shapes, inscription, seal, mounting, and microscopic texture. Never combine calibration images by default.

- anatomy: `anatomy-ink-field.webp`
- modern colossus: `colossus-ink-field.webp`
- landscape: `landscape-ink-field.webp`
- other modern subjects: choose at most one reference whose brush behavior best matches the required force and density

Do not use calibration assets to compensate for a weak subject description. Recognition anchors must still be stated independently.

Reject reference-assisted output immediately if it develops an all-over microscopic pattern, transfers a seal, or resembles the source value map.

Reference-assisted generation is most reliable for a same-subject, local gesture or structural edit. Do not assume that it can preserve brush logic while replacing the entire subject or composition. For major subject changes, return to text-only candidate generation rather than editing a source artwork.

When editing a same-subject reference:

1. preserve paper, stroke density, gray layering, edge behavior, and empty-space ratio
2. change only the named gesture or local structural relationship
3. reconstruct changed regions with the existing brush vocabulary
4. remove transferred inscription and seal
5. reject the result if changed regions become cleaner, flatter, or more explicitly outlined than untouched regions

## Candidate protocol

Built-in image generation is stochastic. For validation or final work, generate 2-4 independent text-only candidates from the same structural recipe rather than repeatedly editing a contaminated result.

Reject candidates in this order:

1. all-over repeated micro-pattern, wave, curl, hatch, or tiled mark
2. fully resolved concept-art or diagram underneath an ink treatment
3. splashes, drips, blooms, watercolor stains, or random blot fields
4. only broad pale washes with insufficient middle and micro brushwork
5. unrecognizable subject at thumbnail scale

Select only a candidate that passes the complete acceptance gate. If none pass, change one prompt variable: subject scale, density map, or dominant force. Do not repair a patterned candidate through editing; regeneration is more reliable.

Do not claim the skill is stable from one successful same-subject edit. Stability requires passing both a same-subject test and a new-subject test without reference-content leakage.

## Prompt assembly

Describe, in order:

1. The subject and 3-5 recognition anchors.
2. The large composition and paper reserve.
3. The medium-scale directional cun families.
4. The micro-detail zones and ink knots.
5. The pale wash that partially buries explicit structure.
6. The monochrome material behavior.
7. The full avoid list.
8. When using calibration assets, state exactly which ink behavior each reference supplies and list all source-content invariants that must not transfer.

Use [references/prompt-recipes.md](references/prompt-recipes.md) for compact recipes. Do not paste research reports into prompts.

## Hard negatives

Reject or regenerate if any of these dominate:

- clean closed contour drawing
- a fully resolved concept-art object underneath an ink filter
- technical pen, manga ink, architectural drafting, or uniform cross-hatching
- contour-first watercolor fill
- water-ripple bands, fingerprint whorls, scalloped parallel arcs, repeated contour-following waves, or worm-like line fields
- explicit armor panels, designed holes, rivets, sockets, and surface components used as fake detail
- random splashes, thrown ink, droplets, drips, runs, wet-on-wet blooms, back-runs, pooled watercolor edges, or chaotic gestural blotches
- hard parallel lines, perfect rectangles, smooth concentric arcs, or regular repeated ribs
- cinematic 3D lighting, glossy rendering, or detailed cast shadows
- a few empty wet blobs presented as ink painting
- uniform paper-noise overlay used to fake materiality
- solid black masses without internal gray structure
- literal collage of modern object plus mountains, mist, pagoda, or decorative calligraphy
- illegible subject hidden behind atmospheric abstraction

## Acceptance gate

Approve only when all are true:

- Thumbnail: the subject and main action are identifiable without a caption.
- Mid-size: ink mass, paper reserve, and density gradient form a deliberate composition.
- Close-up: broad, medium, and micro strokes coexist; many local observations are present but few resolve into clean named components.
- Contours: no long boundary stays uniformly hard or mechanically straight.
- Rhythm: no repeated wave band or contour-parallel motif organizes the surface.
- Control: no accidental splash or watercolor bloom substitutes for deliberate brushwork.
- Dark zones: contain internal stroke direction and at least three perceptible ink values.
- Cultural collision: comes from brush translation and viewing logic, not symbol collage.

## Prompt compression protocol

This section governs the prompt actually sent to the image generator and overrides any earlier prompt-assembly guidance when the two conflict.

Keep the five-pass construction and regional brush logic as internal reasoning. Do not paste the full process, named brush taxonomy, numeric stroke counts, or a long prohibition list into the generation prompt. Literalizing those instructions repeatedly produced worm-like strands, tiled micro-patterns, contour rendering, and decorative surface noise.

Build the final prompt in this order:

1. Give one recognizable subject and no more than two indispensable anchors of its action or anatomy.
2. State the far-view test: the subject is identifiable from mass, posture, and voids rather than a completed outline.
3. State the middle-view test: structural regions separate through changing ink density, overlapping stroke direction, and reserved paper.
4. State the close-view test: abundant deliberate details exist, but absorbent ink, broken joins, and repeated revisions prevent any single local mark from becoming a clean diagrammatic line.
5. Add one compact material sentence: monochrome Chinese ink on xuan paper, controlled brushwork, layered gray-to-black ink, no color.
6. Add at most four failure exclusions chosen for the subject. Prefer `no clean contour`, `no photorealistic shading`, `no repeated surface pattern`, and `no splash/watercolor effects`.

Do not use `archival scan`, `hundreds or thousands of strokes`, counted brush packets, `ink filter`, or detailed step-by-step painting commands in the final prompt. These phrases describe intent poorly to the generator and bias it toward realism, texture tiling, or process illustration.

Generate at least two independent text-only candidates before using a reference. Judge them at three scales. If both fail, revise the perceptual tests or subject anchors; do not respond by adding more brush-process vocabulary. Use a reference only for a tightly bounded same-subject correction, never as the default carrier of style.

## User-accepted baseline: boneless semi-wet accumulated ink

This section is the current acceptance authority and overrides stricter earlier assumptions about universal local ambiguity or mandatory cun-like texture.

The accepted baseline is assets/calibration/user-accepted-boneless-anatomy.png. Use it for visual evaluation only. Do not send it to the image generator by default.

Target these properties:

- One dominant recognizable subject emerges against generous unpainted xuan paper.
- Construct the subject mainly without a preliminary enclosing contour. Let neighboring ink values create most boundaries.
- Allow limited structural edges where hard anatomy or rigid material needs recognition. Do not turn those edges into a complete outline network.
- Use semi-wet pressure, turning, and layered gray-to-black accumulation. Dark regions should result from repeated ink layers rather than a single black fill.
- Let paper absorption soften outer edges and some internal joins. Keep the diffusion narrow and controlled, never a watercolor bloom or global haze.
- Preserve high recognizable detail in the focal interior. Details may be clearer than the earlier deconstructive target, provided they remain visibly made from ink and do not become pen drawing or photorealistic rendering.
- Reserve broad blank paper around the subject. Avoid decorative scenery, inscriptions, seals, and artificial aged-paper effects.

### Default generator logic

Use one or two recognition anchors. Say that form grows directly from semi-wet brush pressure, turning, and repeated accumulated ink without preliminary outlining. Give different regions continuous but irregular brush movement. Build darks by layering pale ink, soften joins with a later pale overlay, and require a clear distant reading with dense mutually permeating detail up close.

Do not overload the final prompt with named cun methods, counted strokes, multi-pass terminology, or long texture prohibitions. Those routes were empirically less stable than the accepted boneless semi-wet formulation.

### Framing by subject

- Anatomy: isolate one twisted anatomical mass; let the focal bones remain readable while surrounding soft tissue dissolves.
- Landscape: use a close or middle-distance crop. A near ridge should occupy most of the painted area so the image retains the accepted detail density; avoid a remote panoramic vista.
- Modern technology: isolate one action and two anchors. Translate hard parts into limited structural edges and surrounding force into layered semi-wet ink, not smoke-cloud splashes.
- Armored figure: preserve posture and weight first. Allow a few hard edges at the head and load-bearing joints, while most armor transitions remain value-built.

### Acceptance gate

Generate two independent candidates per new subject family. Pass only when both preserve monochrome ink, controlled edge softening, layered darks, one recognizable dominant subject, and dense focal detail. Reject concept-art rendering, pen-first anatomy, dry-brush hatching, repeated microtexture, splashes, blooms, and broad low-information washes.

## Hard-surface architecture branch

Architecture needs a separate composition grammar because complete facades, skylines, regular windows, and strong perspective force the generator toward architectural rendering.

Use text-only generation for architecture. Do not use the accepted anatomy calibration image as a visual input; cross-subject reference editing produced uniform microtexture and weakened the ink hierarchy.

- Present architecture as one isolated structural section or close fragment on blank xuan paper, not as a building in an environment.
- Remove ground, skyline, full roof, complete facade, and photographic viewpoint.
- Use three recognition anchors: one dark load-bearing core, offset floor slabs, and one paper-white atrium or structural void.
- Let only short local slab edges remain hard. Infer the larger vertical and horizontal order from interrupted alignment and neighboring ink values, not continuous ruler lines.
- Use paper-white openings instead of repeated window grids. Vary their scale and placement.
- Build depth through overlap and layered gray-to-black ink, not cast shadows, concrete texture, or converging perspective.
- Keep the subject recognizably architectural. Borrow the presentation logic of an anatomical specimen, but never insert bones, organs, muscles, or bodily silhouettes.
- Generate at least two text-only candidates. Prefer the candidate with the clearest load path and the fewest complete outlines.

## Force-first machinery branch

Hard machinery becomes stiff when the prompt enumerates parts or asks every component to remain readable. Keep ink information dense while reducing countable component information.

Use text-only generation. Do not densify machinery with a second full-image edit; that path produced uniform microtexture.

- Describe action, load, torque, compression, or grip before naming the machine.
- Keep one focal structural hinge and no more than two action anchors. Use an incomplete arc or dark offset mass, never a complete concentric joint.
- Organize three information scales: one clear overall force-bearing mass; a few irregular middle-scale accumulated-ink clusters along the load path; small marks only inside those clusters.
- Make middle and small details non-enumerable. Do not request lists of bearings, bolts, cables, panels, fasteners, or blades.
- Concentrate the darkest contrast at the force transition. Cover secondary joins with pale ink so they merge rather than competing at equal sharpness.
- Preserve broad xuan-paper white around the cropped machine. Let the frame cut off the machine before it becomes a complete product illustration.
- Judge success by readable action and weight, not by engineering completeness.

## General-purpose subject router

This router is the current default for broad applicability. Keep one shared ink core, then choose a composition grammar from the subject's dominant visual problem. Do not stack every branch into one prompt.

### Shared ink core

Every branch keeps monochrome black-gray ink on xuan paper, semi-wet accumulated layers, narrowly softened joins, value-built form, one dominant contrast hinge, dense focal information, and intentional paper white. Generate text-only by default.

### Route by dominant problem

1. Organic body or plant
   Use the accepted boneless baseline. Preserve one clear posture or growth direction. Allow selected anatomical or branch edges while soft tissue, bark, roots, or secondary structure merge through layered ink.

2. Soft material or garment
   Organize by gravity, suspension, fold convergence, and fabric weight. Let large folds become middle-scale ink regions and keep decoration as non-enumerable marks inside them.

3. Force-bearing machinery
   Use the force-first machinery branch: one focal hinge, three information scales, non-enumerable secondary details, concentrated contrast, and a cropped incomplete machine.

4. Structural architecture or information infrastructure
   Use an isolated section, close fragment, or flow cutaway. Anchor it with a dark load core, offset slabs or equipment masses, and one paper-white circulation channel. Avoid full facades and environmental perspective.

5. Compact artifact or product
   Do not over-apply mechanical ambiguity. Allow one exact geometric anchor and a mostly recognizable silhouette. Fill much of the frame, keep a few middle-scale detail clusters around the anchor, and let only secondary edges dissolve. This route suits cameras, instruments, vessels, tools, and domestic objects.

6. Actor plus machine
   Prioritize the action contact point. Keep the human posture and one machine joint readable; merge suit, tools, and machine details into shared accumulated-ink clusters around that contact.

7. Crowded interior or circulation scene
   Choose one paper-white movement path and one dark structural core. Treat people as varied posture marks that clarify flow and scale. Infer perspective from overlap and value change rather than a complete line framework.

8. Dynamic environment
   Keep the moving subject sufficiently complete to remain recognizable. Restrict water, smoke, cloud, dust, or flame to a narrow interaction zone around the force event; do not let the medium become a full-frame watercolor field. Use this route for ships, launches, storms, impacts, and fast vehicles.

### Routing safeguards

- Route by the dominant problem, not by every noun in the request.
- Use at most one primary branch and one secondary modifier.
- If a candidate loses recognition, restore one anchor before adding detail.
- If a candidate becomes technical illustration, remove component nouns and convert details into regional ink clusters.
- If a candidate becomes low-information abstraction, restore middle-scale clusters rather than adding microscopic texture.
- If a candidate becomes watercolor scenery, shrink the environmental medium to the interaction zone and enlarge the subject.
