**English** | [中文](README.zh-CN.md)

# OK-RM Design · 有意义的秩序

<table>
  <tr>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/poster-programme.jpg" alt="A programme poster where the weekday is the largest word on each row and one row is marked in yellow"></td>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/catalogue-spread.jpg" alt="A catalogue spread with a full-page plate on the left and a giant page number over bilingual numbered captions on the right"></td>
  </tr>
  <tr>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/archive-index-web.jpg" alt="An archive website whose navigation is an A–Z index and whose list is a table with large entry numbers"></td>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/reader-mobile.jpg" alt="Two reading-app screens: a contents list with large chapter numbers and a chapter page where the number fills the first screen"></td>
  </tr>
</table>

A method for graphic and UI design, distilled from a study of one London studio's
published work and interviews. In one sentence: **find one device in the project's own
content, exaggerate it through dry, systematic typography, let the economy of production
shape the form, and design reading as a sequence.** It is a way of working, not a style
library. The package contains none of the studio's artwork and reproduces none of its
layouts; the four examples above are fictional projects made with the method.

## The five rules

1. **Found structure.** The device comes from the project itself: the literal meaning of a
   name, a process, a craft, an object, a convention, a constraint. Never from a mood board.
2. **One device, exaggerated.** Find the key point and push it. One device per project;
   everything else recedes into system.
3. **Type is the backbone.** A neutral grotesk as the main voice, a text serif or monospace as
   the second. Expression comes from extreme scale contrast and from page furniture (page
   numbers, numbering, captions, punctuation), not from display faces.
4. **Economy as form.** Budget, paper, folds, postal formats, print processes, screen sizes and
   system fonts are generators. Every constraint must leave a visible decision.
5. **Reading is a sequence.** Books, websites and exhibitions are orders of reading. Interleave,
   juxtapose, jump scale, fold out, change paper. Let context change content.

Plus one tension rule: dry type against emotive material.

## What you get

- A seven-step workflow in [SKILL.md](../../plugins/okrm-design/skills/okrm-design/SKILL.md):
  list the found material, write the device statement, set the order, set the economy,
  sequence the reading, make, check.
- [Order system](../../plugins/okrm-design/skills/okrm-design/references/design-system.md):
  typography, scale ladder, grid derived from folds, furniture, colour, material, imagery,
  sequence, and how each shifts by medium.
- [UI translation](../../plugins/okrm-design/skills/okrm-design/references/ui-translation.md):
  index navigation, tables as lists, furniture counters, responsive design as folding, dry
  states and motion, accessibility as part of the order, an HTML/CSS skeleton.
- [Recipes](../../plugins/okrm-design/skills/okrm-design/references/recipes.md): device
  statement and spec templates, a poster skeleton, image-model prompts per medium, and a
  correction table.
- [Acceptance gates](../../plugins/okrm-design/skills/okrm-design/references/qa.md): three
  main gates (device, economy, sequence), order gates, interface gates, instant failures.
- `scripts/tokens.py`: generates an order sheet (CSS custom properties and JSON) from a few
  decisions and checks any sheet against the gates: at most two type families, three
  magnitudes of scale, one accent, legible contrast, fold-derived columns, 45–75 character
  measure.

## Start

Install from the LabArt marketplace using the Codex CLI:

```sh
codex plugin marketplace add haorantang97/LabArt --ref main
codex plugin add okrm-design@labart
```

For a standalone Skill installation with GitHub CLI 2.90 or newer:

```sh
gh skill install haorantang97/LabArt plugins/okrm-design/skills/okrm-design@main --agent codex
```

For manual installation, copy the [whole skill folder](../../plugins/okrm-design/skills/okrm-design).
The token script needs only Python 3. Start a new task after installation.

Try:

> Use $okrm-design to design a poster and identity for a six-evening lecture series on book design. Find the device in the brief first.

> 用 $okrm-design 把这个藏品档案网站做成以编号为导航的排印界面，输出 tokens.css 和一页 HTML。

> Use $okrm-design to lay out this ceramics catalogue as a reading sequence: interleave historic and contemporary pieces, one change of paper.

## Study basis

The method was distilled from public material about [OK-RM](https://www.ok-rm.co.uk/), the
London studio founded in 2008 by Oliver Knight and Rory McGrath: design-press coverage of
their identities, books, magazines and exhibition graphics; their interviews and talks; book
design award citations; and the public texts of their 2024–2025 retrospective *A Meaningful
Order*, whose title quotes Victor Papanek's definition of design. Representative sources:

- [Eye Magazine, "They work with words"](https://eyemagazine.com/feature/article/they-work-with-words-3) — "find the key point and exaggerate it".
- [It's Nice That on the Untitled art fair identity](https://www.itsnicethat.com/articles/ok-rm-untitled-art-010216) — the caption as device; comma and full stop as identity.
- [BP&O hands-on review of Real Review](https://bpando.org/2017/09/25/hands-real-review/) and the [Design Museum Q&A](https://designmuseum.org/exhibitions/california-designing-freedom/product-z/flax-chair/qa-with-jack-self-real-foundation-and-rory-mcgrath-ok-rm) — fold, large page numbers, cost as brief.
- [Creative Review on the Strelka grid](https://www.creativereview.co.uk/ok-rms-grid-based-system-for-strelka/) — grid as public space, bilingual.
- [Creative Review on Fear and Love](https://www.creativereview.co.uk/work/work-fear-and-love-graphics-and-exhibition-design-by-ok-rm-and-sam-jacobs-studio/) — dry system type against emotive material.
- [The Met on the Manus × Machina catalogue](https://www.metmuseum.org/perspectives/making-of-manus-x-machina-catalogue) — a craft made literal in production.
- [Tokyo TDC 2020](https://tokyotypedirectorsclub.org/en/award/2020_tdc_02/) and [2026](https://tokyotypedirectorsclub.org/en/award/2026_book/) book design prizes — interleaving, the book as object.
- [Nieuwe Instituut profile](https://nieuweinstituut.nl/en/projects/ontwerpplatform/okrm) and [Maximillian William press release](https://static1.squarespace.com/static/65201415e0904740920e39c7/t/67922c5c1f8ec126ff7e3923/1737632860573/OKRM_PressRelease_MW.pdf) — "design is a conversation"; *A Meaningful Order*.

The package is an independent study. It is not affiliated with, endorsed by, or an official
style of the studio. Do not use the studio's or designers' names in prompts, credits or
promotion of work made with it.

## Inside the package

[Main skill](../../plugins/okrm-design/skills/okrm-design/SKILL.md) · [Order system](../../plugins/okrm-design/skills/okrm-design/references/design-system.md) · [UI translation](../../plugins/okrm-design/skills/okrm-design/references/ui-translation.md) · [Recipes](../../plugins/okrm-design/skills/okrm-design/references/recipes.md) · [Gates](../../plugins/okrm-design/skills/okrm-design/references/qa.md) · [Study notes](../../plugins/okrm-design/skills/okrm-design/references/study-notes.md)

Example sources are under [assets/okrm-design/examples](../../assets/okrm-design/examples) and are
rendered with `node scripts/render_okrm_examples.mjs`. Structural checks and example
validation are recorded in the [validation notes](VALIDATION.md).

## License

[PolyForm Noncommercial 1.0.0](../../plugins/okrm-design/LICENSE).

[Back to LabArt](../../README.md)
