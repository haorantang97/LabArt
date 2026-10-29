---
name: x-ray
description: Create and edit X-ray transmission imagery from a brief or visual reference, preserving projection, material attenuation, internal structure, and display polarity across objects, textiles, living subjects, and actions. Use for radiographic visual art and style transfer; assess glass-render, cutaway, collage, and anatomy failures separately.
license: PolyForm-Noncommercial-1.0.0
---

# X-ray

Create original images in which external form and internal construction coexist as a transmission projection. Preserve the radiographic mechanism while changing subject, action, or arrangement. Read [formation.md](references/formation.md) before generating; read [prompt-recipes.md](references/prompt-recipes.md) to construct the prompt.

## Define The Image Contract

Record:
- subject and intended action or relationship;
- plausible internal structures and materials;
- one source/detector view;
- display polarity and monochrome or requested pseudocolor;
- contrast range, image softness, and framing;
- reference roles and provenance.

Keep the imaging block separate from the content block. Do not add a fantasy habitat, botanical collage, or architectural cutaway merely because the user requests more creativity. For realistic mode, creativity can come from an unusual subject, interaction, viewpoint, overlap, or captured instant. Use hybrid imagery when requested and identify its mixed mechanism.

## Preserve Transmission

1. Form the image from attenuation along rays through the intact subject. Keep a coherent projection; a front or near-parallel view is an option, not the definition of radiography.
2. Material composition, energy, density, and path length jointly affect attenuation. Surface color does not determine X-ray darkness.
3. Overlap accumulates optical depth. Dense or thick regions may hide structure; do not show every component equally clearly.
4. Choose one display convention throughout the scene. For pale fields, high transmission is light and stronger attenuation darker. The inverted black-field convention is equally usable; record a change of polarity as a changed contract.
5. Replace optical surface rendering with transmission evidence. Suppress specular glints, glass refraction, studio shading, leather grain, fur photography, floor shadows, and separately lit bones unless the brief specifically requests mixed media.
6. Make internal topology credible. A detailed skeleton or circuit board is not evidence of correct anatomy or engineering. Obtain appropriate construction/anatomy references when accuracy matters; otherwise report it as unverified.
7. Treat tint, grain, blur, and fog as display or acquisition choices. Do not use them to conceal failed structure.

## Use Visual References

Inspect references before using them. A URL or written description is not visual inspection. Prefer relevant actual radiographs when available, and distinguish them from generated approximations.

Two generated appearance anchors are bundled:
- [folded-shirt.png](assets/style/folded-shirt.png): pale-field textile overlap and seam-density cues;
- [player-baseline.png](assets/style/player-baseline.png): pale-field mechanical transmission, low-contrast shell, and denser internals.

These are synthetic visual examples with known limits, not physics ground truth or validated anatomy. Use an anchor only when its appearance matches the brief. Its subject and layout are not templates for every image. Plugin gallery screenshots are presentation examples, not automatic runtime inputs.

When a tool supports reference images, supply the selected image through its real image-input mechanism and state which properties to preserve. For one-detail changes, start from the same baseline rather than chaining edits that accumulate drift.

## Choose The Rendering Route

In Codex, use the system imagegen workflow and built-in image generation. On another platform, use an available raster generator/editor while preserving reference roles and the image contract. Do not install a model, require an API key, or send files to another service without authorization.

If no renderer is available, deliver a renderer-ready prompt and review criteria, and state that no image was generated. If the renderer cannot receive references, state that the reference was inspected but not applied.

Generative imagery is not a physical forward simulation. For quantitative projection fidelity, a CT/volume or material-labelled 3D scene and a suitable forward renderer are needed. Do not claim text-to-image has solved the attenuation equation.

## Transfer To Actions And Complex Scenes

Non-still-life requests need a changing pose, contact, pursuit, or interaction. Blurring a static device is an acquisition test, not a dynamic-content test.

- Trace limbs and joints through overlap; count only what can be justified by the projection.
- Check every meaningful contact: hand/ball, hand/handlebar, foot/pedal, stick/drum.
- Check mechanical continuity separately from bodily gesture.
- Let near/far structures superpose naturally rather than separating them for diagram-like legibility.
- Use local motion softness only where speed warrants it. Missing fingers, invalid joints, or disconnected mechanisms remain failures.
- A pose may suggest action without proving its forces or trajectory. Use contact and scene evidence when the action depends on them.

## Validate And Repair

Read [qa.md](references/qa.md). Inspect each output at a useful size and report pass, fail, or uncertain separately for projection, attenuation cues, polarity, visibility, structure, modality, and requested action.

For stability:
1. Keep the contract and reference fixed.
2. Change one named content or acquisition condition.
3. Compare against the baseline.
4. Repeat relevant cases before claiming reproducibility.

Reference-conditioned consistency, physical correctness, and unrestricted cross-subject stability are different claims. Do not infer any of them from one attractive sample.

If the image becomes a glass render, lit skeleton model, cutaway, or collage in realistic mode, mark that failure even when aesthetically strong. Make a targeted repair, then inspect again. If the repair leaves the issue unresolved, report that limit rather than adding more style adjectives or silently switching modes. Image-conditioned repair can preserve an existing structural error.

## Deliver

Show the actual result and save selected images plus exact prompts. Briefly state the intended action, applied reference, and important unresolved structure or modality limits. Keep detailed experimental records separate from runtime resources. Do not market synthetic images as diagnostic scans, physically verified projections, or another creator's work.
