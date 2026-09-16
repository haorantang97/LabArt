# Validation scope

## Package structure

The package contains one public skill, two conditional/supporting references,
and two generated visual material references. The portrait reference is an
internal module, not a second discoverable skill.

The official skill and plugin structural validators passed for the 0.1.1 package.
Structural validation does not establish installation, runtime discovery, or
aesthetic acceptance.

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
