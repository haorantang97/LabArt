# Validation scope

## Package

The package contains one public skill, two conditional/supporting references,
and two generated visual material references. The portrait reference is an
internal module, not a second discoverable skill.

The official skill and plugin structural validators passed for the 0.1.0 package.
Structural validation does not establish installation, runtime discovery, or
aesthetic acceptance.

## Generation evidence

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

The updated portrait module has been reviewed against the requested proportion
changes but has not received a new image-generation test in this release.

## Remaining boundaries

- No end-to-end installation or client-discovery test under the new public plugin
  name is claimed.
- Consistent characters across multiple independent generations are not guaranteed.
- Examples do not establish equal reliability for people, animals, plants, objects,
  or scenes.
- User approval remains the aesthetic acceptance criterion.
