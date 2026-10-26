# Validation scope

## 0.1.0 — first package

The package contains a method (SKILL.md and five references), one standard-library
Python script (`scripts/tokens.py`), UI metadata, and the license. The four declared
screenshots are fictional projects made with the method, rendered from the HTML sources
under `assets/okrm-design/examples/` with Chromium through Playwright. Placeholder fonts
were used for the renders (an open grotesk, a Times-metric serif, an open monospace, a
Japanese Gothic for CJK captions); the method does not depend on them.

Checks performed on 2026-10-26:

- `scripts/check_packages.py` passed for all four marketplace plugins, including the new
  package's inventory, allowed skill-root content, declared UI images, and local links.
- 12 behavioral tests for the order-sheet generator and checker passed
  (`tests/okrm-design/test_tokens.py`): every medium's default sheet passes its own gates;
  three families, a flat scale, a second accent, low ink contrast, a default 12-column grid,
  an out-of-range measure, and an illegible mobile caption are each rejected; the CLI
  round-trips generate → check and reports a failing sheet with exit code 1.
- The four examples were checked against the acceptance gates in `references/qa.md`:
  each has one device that can be stated as "X is Y, so Z"; two type families; a scale
  ladder of at least three magnitudes with one unreasonably large element; at most three
  kinds of furniture; one accent colour carrying one function (the current item); no
  gradients, shadows or decoration. One earlier draft used the accent twice on the web and
  catalogue examples; those uses were removed before the final render.
- Rendered images were visually inspected at full size. The poster's programme rows fit the
  sheet after the weekday size and row padding were reduced; nothing is clipped.

Not claimed: no image-model generation was run for the prompt recipes; they are scaffolds
whose wording follows the method's vocabulary and have not been scored against outputs. No
marketplace activation or remote installation of this new plugin name was tested. Aesthetic
acceptance of the examples is the author's; user review is recorded separately.
