# X-ray 0.1.0 — Validation

## Visual Evidence

The selected hand/ball, player/keys, shirt, and frontal handbag are original
AI-generated development outputs. Their original PNG bytes are retained.
The player/keys image was generated as a reference-conditioned edit of the bundled
player baseline. The other three were generated from text.
Exact selected prompts are in [generation-prompts.json](generation-prompts.json).

Development also examined:
- a metal occluder, with a same-center test that was ambiguous and an offset repair;
- mixed textile/metal overlap and whole-object acquisition motion;
- hand/ball and airborne-cat actions;
- a cyclist and drummer combining bodily and mechanical contacts.

These are qualitative examples, not repeated-sampling or physical validation.

## Observed Limits

The hand's full digit topology is unclear. Scarf and bag retain some transparent
material appearance. Mechanical internals are invented. Living subjects and
coupled scenes sometimes show lit-bone rendering, mixed polarity, uncertain
anatomy, or incorrect requested contact/strike targets. An image can retain its
subject while failing transmission realism.

The Skill records those failure modes instead of treating a gallery selection
as proof of correctness. It contains generated appearance anchors, not real
radiographic ground truth. Xsyn, InstantStyle, IP-Adapter, and DiffDRR were
researched but not run for these outputs.

## Release Checks

Packaging, standalone boundaries, official Skill format validation, local
documentation/image references, original image hashes, and a clean-copy check
passed on 2026-10-30. A real local GitHub CLI installation into an isolated custom
directory also passed the package and official Skill checks. See
[repository package validation](../VALIDATION.md).

No marketplace installation, client activation, cross-subject reproducibility,
diagnostic validity, or engineering/anatomical accuracy is claimed.
