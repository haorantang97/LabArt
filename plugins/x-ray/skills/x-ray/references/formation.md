# Formation And Reference Roles

## Physical Basis

For a narrow monoenergetic primary beam:

I / I0 = exp(-integral(mu(E, r) ds)).

For homogeneous material, this becomes exp(-(mu/rho) * rho * t).
Optical depth -ln(I/I0) adds along the ray. Composition, photon energy, density,
and path length affect attenuation; ordinary visible-light alpha blending does
not reproduce this mechanism. Real spectra, scatter, beam hardening, finite source
size, and detector response complicate the simplified model.

Source: [NIST mass attenuation coefficients](https://physics.nist.gov/PhysRefData/XrayMassCoef/chap2.html).

The equation is an explanatory constraint, not evidence that a generative model
has computed a projection. Do not invent exposure settings or coefficients to
lend authority to an artistic result.

## Display Choices

The bundled anchors use a pale field, darker attenuation, and restrained blue-grey
grading. A black field with brighter attenuation is another legitimate display
convention. Keep one ordering across the entire image. Tint and grain are not
defining physics; neither is an orthographic view.

## Research Routes

- [Xsyn](https://github.com/pILLOW-1/Xsyn/): GLIGEN-based synthesis/inpainting for
  security X-ray detection data. A relevant learned image prior, not general
  physical rendering rules.
- [InstantStyle](https://github.com/instantX-research/InstantStyle) and
  [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter): image-conditioned
  appearance control. They can support visual consistency, not a physics guarantee.
- [DiffDRR](https://github.com/eigenvivek/DiffDRR): digitally reconstructed
  radiographs from 3D volumes; relevant when real geometry and projection fidelity
  are needed. See [its documentation](https://vivekg.dev/DiffDRR/).

These sources were inspected during development; their models and code were not
run for the bundled examples.

## Bundled Anchor Limits

The shirt illustrates overlapping fabric, cuffs, and seams; it retains some
textile appearance. The player illustrates a faint shell and denser components;
its internals are generated and unverified. Neither proves physical accuracy.
Inspect them before applying their appearance and obtain a stronger reference
when the current subject requires one. Gallery anatomy is also unverified.
