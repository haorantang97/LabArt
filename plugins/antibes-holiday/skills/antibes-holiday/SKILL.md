---
name: antibes-holiday
description: Create original relaxed black-pen graphics from concepts or visual references, including sparse illustrations, narrative scenes, animals, objects, abstract relationships, icons, and logo marks. Use when the user wants quick hand-drawn line energy, causal story staging, non-equilibrium proportion, shorthand forms, open contours, structural line drift, misregistered junctions, selective retracing, physical pen texture, or a transferable illustration system that must not collapse into clean vector minimalism or polished period-sketch drawing.
license: PolyForm-Noncommercial-1.0.0
---

# Antibes Holiday

Create original graphics that feel drawn in one alert but lightly unsteady sitting with a real black pen. Prioritize stroke life, tempo, shorthand, structural instability, and the courage to stop. Semantic compression remains useful, but a clean concept never compensates for lines that look professionally controlled.

## Start With Evidence

When references are supplied:

1. Define the target style cluster from stroke material, tempo, omission, density, and composition.
2. Exclude unrelated style clusters from the same reference body.
3. Record dates inside the cluster and weight recent mature work most heavily.
4. Inspect at least three high-weight images at actual size.
5. Separate stroke behavior from recurring subjects and accessories.
6. Use references for line material and gesture only. Never reuse their subject, pose, composition, or signature motif.

Default evidence weighting:

- newest mature same-cluster works: `60%`;
- recent supporting same-cluster works: `30%`;
- early same-cluster works: `10%`;
- different styles or experiments: `0%`.

Read [style-system.md](references/style-system.md) before drawing. Read [prompt-recipes.md](references/prompt-recipes.md) before using an image-generation model.

## Define The Drawing

1. Classify the deliverable: `illustration`, `series`, `icon/badge`, or `logo`.
2. State what must be felt or recognized in one sentence.
3. Choose the subject's most telling action, mass, edge, joint, or relationship.
4. Decide where the drawing should move quickly and where the pen should briefly slow down.
5. Select one dominant sweep and one compact recognition knot.
6. For a scene, identify the `principal actor`, `counterforce`, `narrative hinge`,
   and the causal path between them.
7. Choose one deliberate scale distortion and one quiet region that carries
   distance, pause, anticipation, or release.
8. Choose one controlled structural failure: a drifting contour, missed junction,
   overshoot, displaced restart, incompatible pair of fragments, or abandoned path.

Do not default to a person, face, unrequested character traits, accessories, or anthropomorphism.

## Draw In Three Passes

### Pass 1: Gesture

Draw three fast structural variants.

- Use one to three long sweeps.
- Do not close shapes for neatness.
- Do not correct proportions yet.
- Let at least one sweep drift, lurch, overshoot, or stop before reaching its
  expected destination.
- Permit one to four residual or corrective fragments across an expressive
  illustration. They must record discovery, not decorate the page.
- Reject the prettiest or most anatomically competent variant if it feels designed,
  trained, or gracefully sketched rather than found while drawing.

### Pass 2: Recognition

Add only the shorthand needed to make the subject legible.

- Use short angular, hooked, wavy, or looping fragments.
- Concentrate fragments at the action, contact, or identity knot.
- Let large regions remain unnamed.
- Omit any boundary the viewer can infer. Do not let one connected contour
  competently explain the whole form.
- Spend conventional detail only when it carries recognition or action. Do not
  delete so aggressively that the result collapses into a stick symbol.
- Distort scale when a hand, tool, opening, joint, shell, edge, or movement carries the idea.
- Prefer an implied boundary over a complete outline.

### Pass 3: Pen Life

Restore the physical behavior that image models and vector tools remove.

- Vary pressure and direction unevenly along long sweeps.
- Let selected terminals taper, dry out, or stop bluntly.
- Add one local retrace or ink-darkened overlap at the recognition knot.
- Preserve one broad drift or visible lurch plus smaller speed kinks.
- Let one intended junction miss, overlap, or restart slightly displaced.
- Keep useful false starts and competing fragments when they show the hand losing
  and recovering the form.
- Concentrate repeated correction and scribbled density at one recognition knot.
  Outside it, prefer one imperfect attempt over several sketchy alternatives.
- Stop before the result becomes clean, balanced, or fully explained.

## Adapt Without Humanizing

- `Living form`: use posture, mass distribution, locomotion, and distinctive anatomy.
- `Object`: exaggerate the operational edge, opening, handle, joint, contact, or material path.
- `Place`: use one boundary, route, threshold, and scale cue.
- `Abstract relationship`: first choose an observable physical metaphor, then express tension, exchange, interruption, growth, or separation through its gesture. Do not draw free-floating lines when the meaning depends on explanation.
- `Logo`: begin with a relaxed pen master; derive a separate production vector only after the gesture works.

Do not transfer human facial shorthand to non-human subjects.
For human figures, preserve posture and character while withholding clean anatomy.
Build the figure from unequal, partially incompatible fragments, with enough local
specificity to remain observed rather than diagrammatic.

## Compose Story Scenes

Treat complexity as relationships, not line count.

1. Reduce the event to two or three readable beats.
2. Give each actor a different narrative weight. Scale, crop, and detail may
   violate realistic perspective when that makes the event clearer.
3. Place one compact `narrative hinge` where intention becomes consequence:
   contact, exchange, reveal, interruption, impact, or release.
4. Connect the beats with one causal sweep, shared baseline, reach, gaze, object
   path, or directional gap. Do not add arrows or motion icons.
5. Use unequal information density: describe the principal action, abbreviate
   supporting actors, and leave the setting largely unstated.
6. Break balance deliberately with one dominant mass, off-center crop, oversized
   operational feature, displaced small actor, or edge-reaching contour.
7. Let blank paper separate time and distance. Do not fill it with scenery.
8. Stop when the viewer can infer what just happened or is about to happen.

When a scene is humorous, put the humor in disproportion, posture, timing, and
physical consequence. Do not explain it with sweat drops, surprise ticks,
exclamation marks, speed marks, or other cartoon punctuation unless requested.

Choose a composition family from [style-system.md](references/style-system.md)
according to the event. Do not repeat one family across a series by default.

## Select Rendering Capability

Inspect the tools available in the current environment before rendering:

1. In Codex, prefer the system `imagegen` workflow and built-in `image_gen` tool.
2. On another platform, use its native raster generation or editing capability
   while preserving the reference roles, prompt rules, and validation gates here.
3. If the available tool cannot receive local reference files, use the textual
   stroke specification and state that the calibration image was not applied.
4. If no image-generation capability exists, do not claim to have rendered an
   image. Deliver a renderer-ready prompt, the intended reference roles, and the
   complete validation checklist instead.
5. Never require an API key, install a dependency, or switch to an external
   service without the user's explicit approval.

## Use Image Generation

Use the selected raster capability for exploration and illustration.

When recent reference crops are available:

1. Supply two or three as line-material references.
2. State that their subjects and compositions must be ignored.
3. Generate one direction per call.
4. Compare the result at actual size, not only as a thumbnail.
5. Edit one stroke problem at a time.

When no user references are available, supply the bundled
[stroke-calibration.png](assets/stroke-calibration.png). It controls physical pen
instability: pressure, drift, missed junctions, overshoots, displaced restarts,
broad lurches, retracing, ink deposition, dry breaks, and abrupt terminals.
Ignore every shape and layout in the asset. Never copy a swatch as an object,
symbol, border, motif, or composition. Keep structural assembly in the text prompt;
do not add a second visual reference whose cleaner lines could dilute the material.

Use a bounded decontrol pass when the first readable render remains too competent:

1. Preserve the subject, action, text, composition, hierarchy, and blank space.
2. Change only line construction: break a clean contour, displace one restart,
   remove conventional detail, and let one structural drift alter the silhouette.
3. Compare before and after at actual size.
4. Keep the edit only when readability survives and the line no longer resembles
   trained editorial, fashion, or period sketching. Otherwise keep the readable
   draft and edit one region at a time.

Ask for a photographed or scanned black-pen drawing only when physical stroke texture matters. Keep paper texture subtle and never use it to fake quality.

## Build Logos

1. Explore the mark as a relaxed pen gesture first.
2. Remove narrative detail without sterilizing the line.
3. Create two masters when appropriate:
   - `expressive master`: preserves pen irregularity for display use;
   - `production master`: optically tuned SVG for small sizes.
4. Treat generated raster marks as sketches, not finished logos.
5. Reconstruct deliberate vector paths; never auto-trace paper noise.
6. Test one color, reversed color, 24 px, 48 px, and print-size black.

Do not force an illustration line to survive at favicon size by making every stroke thick and geometric.

## Comparative Validation

Validate against at least three recent, same-cluster references. The candidate must pass every primary gate:

- `Physicality`: reads as real pen movement, not a Bézier outline or generic sketch filter.
- `Tempo`: contains visible contrast between fast sweeps and slower recognition marks.
- `Instability`: at least one structural line visibly loses and recovers control;
  intended meetings are not all perfectly registered.
- `Shorthand`: forms are inferred from decisive fragments rather than fully described.
- `Relaxation`: proportions, spacing, anatomy, and terminals feel unforced without
  turning into uniform noise.
- `Transfer`: the line behavior survives the new subject without importing human accessories or source motifs.
- `Originality`: no source composition, character, or signature device is reproduced.

For story scenes, add two primary gates:

- `Causality`: the spatial arrangement makes the action and consequence inferable.
- `Hierarchy`: scale, crop, density, and empty space clearly prioritize the story
  without defaulting to balanced staging or realistic perspective.

Secondary gates:

- the intended subject or relationship is inferable;
- the composition has a clear movement and quiet release;
- texture does not dominate;
- the output fits its intended reproduction size.

Fail the result immediately if it is vector-clean, diagrammatic, evenly polished,
uniformly wobbly, decoratively distressed, or only recognizable because of labels.
Also fail it when most contours arrive exactly where expected, figures read as
competent fashion or period illustration, faces and hands are cleanly resolved, or
the image could pass as a professional quick sketch with texture added afterward.
Visible shoelaces, fingers, pockets, complete facial features, and fully joined
limbs are warning signs unless one carries the story.
Fail generic loose sketching when duplicate contours, search marks, and darkened
corrections spread evenly across the whole subject instead of gathering at one knot.
Fail unrequested cartoon shorthand when sweat drops, emphasis ticks, exclamation
marks, or speed marks carry an emotion or action that posture and causality should
have made visible.

Do not convert these gates into a single score. A strong semantic result with weak stroke physicality still fails.

## Deliver

Include:

- the final artifact;
- a one-sentence concept rationale;
- file format and color values when relevant;
- whether it is an expressive raster master or production vector master.

Keep internal reference analysis out of the final response unless requested.
