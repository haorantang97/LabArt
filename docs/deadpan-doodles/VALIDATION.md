# Validation scope

## 0.2.1 — package boundary cleanup

The generation recipe, reference manifest, reference images, protocol, and prompt
assembler are unchanged. Repository presentation and development tests moved
outside the plugin package. The 12 existing assembler tests still pass; standalone
Skill installation and copied-plugin inventory checks are recorded in the
[collection package validation](../VALIDATION.md). No new image-model generation
or client activation is claimed.

## 0.2.0 — general Sha Bing package

This release packages the existing general recipe `shabing-20260925-1`.
The fixed recipe, protocol, entrypoint, portrait module, reference index,
visual checks, prompt assembler, and reference manifest are unchanged from that
baseline. Test subjects were made theme-neutral; the test logic is unchanged.

The package has one public skill. Its portrait guidance is a conditional module,
not a second entrypoint. The selected portrait (B) remains the default style
anchor; the cat is used only when that reference direction is requested. The
three new showcase files do not change generation-reference selection.

Checks performed on 2026-09-26:

- Official plugin validator and official skill structural validator: passed.
- Prompt-assembler behavior: all 12 existing tests passed, including recipe
  integrity, anchor integrity, reference order, narrow edits, path relocation,
  literal text, and output-overwrite protection.
- The supplied Chinese introduction is present verbatim exactly once on the
  Chinese plugin page. Neither language's story is on the collection homepage.
- English and Chinese code blocks and section counts are synchronized.
- All four selected showcase images match their supplied source files by
  SHA-256; no cropping, recoloring, or retouching was performed.
- Local links in the root README and plugin Markdown files were checked.
- Root and plugin pages were rendered at desktop and narrow widths and in
  light/dark themes. Images loaded without horizontal page overflow. The
  Chinese desktop, narrow, and dark previews and the collection preview
  were visually inspected.
- Whitespace validation passed.

The fixed recipes were distilled from selected examples, not recovered from
the original image-generation calls. No new image generation or end-to-end
plugin installation was run for this publication. Showcase selection is not
a controlled demonstration of deterministic reproduction. The reference
manifest therefore retains its candidacy/visual-validation status.

## Earlier versions

The following records describe their named historical versions, not current
proportion defaults or a fresh aesthetic pass.

## 0.1.1 — relative proportion targets

This revision targets a relative change of approximately 40% in one named
dimension relationship. It does not set a fixed part-to-whole share, and does not
expose a real image-tool strength parameter.

The historical high-forehead recipe said the forehead occupied nearly half the
face. That was a portrait-specific layout, not a general 50% deformation setting.
The subsequent four-subject sample batch was judged insufficiently unusual by
the user. Its prompts repeatedly softened shape changes with words such as
"slightly" and "a little."

The four-subject rerun kept the prior subjects, color choices, actions, formats,
and material roles, while replacing the proportion instructions. Four first-call
outputs were visually inspected against the preceding batch:

| Subject | Observed change | Remaining limitation |
|---|---|---|
| Portrait | Some elongation in the lower face | Still reads as a conventional bust; shoulders and neck remain substantial, and dark hair is dense |
| Dog | Ears extend much farther toward the paws | Head and body remain fairly conventional, with a soft/cute expression |
| Flower | A broader crown against the fine bent stem | Still reads as a plausible flower; unusual scale does not by itself establish humor |
| Cat and chair | More overhang at the hindquarters | The chair still accommodates much of the torso; the intended support conflict is only partial |

The results are mixed, not a universal pass. The 40% value is an approximate
prompt target; no output is claimed to have met a measured 40% geometric change.
This is a qualitative first-run comparison, not a controlled same-seed experiment.
The watercolor references remained unchanged, but material behavior can still
drift between generations. None of these outputs was promoted into the reference
library or the public gallery.

Tested SKILL.md SHA-256:
`0837a9b203bd317f31fc50e3c44c3bcab7b7eff7ee8766095fbc707f4d09c818`.
Tested portrait module SHA-256:
`93fb90e22a80cefdf6928c46a25afdc770c4e077b618efe6dde18b26cc4b8e32`.

## 0.1.0 — historical generation evidence

Earlier portrait iterations exercised photo-only inputs and photo plus generated
material references. Adding material references improved the observed transparent
wash behavior, but also carried unwanted proportion cues. A subsequent restrictive
facial layout reduced those cues and was judged too rigid.

This version separates material from subject geometry, restores moderate
subject-led proportion contrast, and places portrait-specific guidance in its own
module. The historical portrait samples demonstrate material, not acceptance of
this new version's behavior.

A fresh non-human request was executed in a separate task: a languid cat beside
a small flower, with transparent watercolor, dry humor, and proportion contrast.
It used this skill and its material reference, without the portrait module.

- One image-generation call, no retries or postprocessing.
- The only visual input was the bundled high-forehead material reference.
- The output showed a low, elongated cat beside a flower, transparent gray washes,
  exposed paper, and loose fine lines; no glasses or human clothing carried over.
- The round head and paired paws still read somewhat cute. The proportion contrast
  and deadpan humor remained mild. This is not user aesthetic acceptance.
- The original output and actual prompt were retained in the private test workspace,
  not published or added to the positive-reference library.

Tested SKILL.md SHA-256:
`b661697d653fbd84293cf0366cb4fc9486601f6b672b740df933e05b670050ae`.
Original output SHA-256:
`0517e99fdf50f74d1eb7a1416271e795fd33eb39e07fe28da457a2740e2092c5`.

After the initial cat test, four samples exercised portrait, dog, flower, and
cat-on-chair subjects. They were generated once each, without retries. The user
found the proportions insufficiently unusual; they were not added to the
positive-reference library.

## Remaining boundaries

- No end-to-end installation or client-discovery test under the new public plugin
  name is claimed.
- Consistent characters across multiple independent generations are not guaranteed.
- Examples do not establish equal reliability for people, animals, plants, objects,
  or scenes.
- User approval remains the aesthetic acceptance criterion.
