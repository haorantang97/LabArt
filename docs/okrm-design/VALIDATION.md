# Validation scope

## 0.2.0 — rebuilt on primary sources

0.1.0 was written from search-engine summaries only, because the session's network policy
blocked every source site. 0.2.0 replaces it after the sources were read in full: twelve
interviews and conversations, the retrospective's press release, the publisher's catalogue
of 41 publications with specifications, about twenty project reviews, seven typeface records,
the 31 work photographs on the studio website (measured with a 0.1 grid), and the website's
own CSS. The study basis is listed in [README.md](README.md#study-basis).

What changed as a result of the evidence:

- The five rules became eight principles taken from the studio's own words: content and
  concept, magnified clarity, performative framework, readymades and ubiquitous languages,
  economy as form, structure and play, duality, sequence of reading.
- The scale rule was corrected. 0.1.0 asked for "one unreasonably large element" and a wide
  ladder; the photographs show type at two poles (label-small or monumental) with the
  headline middle almost absent. The token checker now rejects sizes between 2 and 8 times
  the body size.
- The colour rule was corrected. 0.1.0 used an accent colour for one function inside a
  layout; the photographs show one flat colour used as the material of a whole cover,
  endpaper or sign. The token now carries a field colour and the checker rejects a second
  colour or a field that cannot carry type.
- The alignment rule was corrected: labels are centred and letterspaced, grotesk words sit
  in corners; "always flush left" was removed.
- The claim that page numbers are unusually large in the folded journal was removed; the
  photographs do not support it.
- Measured starting values (type heights, label position and width, plate borders, spine
  strip widths) were added to the order system with their precision.

Checks performed on 2026-10-26:

- `scripts/check_packages.py` passed for all four marketplace plugins, including the new
  five declared screenshots and local links.
- 15 behavioral tests for the order-sheet generator and checker passed
  (`tests/okrm-design/test_tokens.py`): every medium's default sheet passes its own gates;
  three families, a headline in the middle, a small monument, a second colour, a field used
  as an accent, a field that cannot carry type, low ink contrast, a default 12-column grid,
  an out-of-range measure and an illegible mobile caption are each rejected; the CLI
  round-trips generate → check.
- The five examples were re-made under the corrected rules and checked against
  `references/qa.md`: each has one device of a stated type (readymade or system), two
  voices at most, type at two poles, one flat colour used as a material or none, actions
  written as text in brackets where the medium is an interface, no decoration. The earlier
  accent highlights were removed from all examples.
- Rendered images were visually inspected at full size.

Not claimed: no image-model generation was run for the prompt recipes. No marketplace
activation or remote installation of this plugin name was tested. Measurements were taken
from photographs with perspective and cropping, so they are starting points, not
specifications. Pages that refused automated access were not used beyond search summaries.

## 0.1.0 — first package

Superseded. Written from search summaries; its rules on scale, colour and alignment were
partly wrong and are corrected above.
