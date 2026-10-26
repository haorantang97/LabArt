**English** | [中文](README.zh-CN.md)

# OK-RM Design · 有意义的秩序

<table>
  <tr>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/catalogue-cover.jpg" alt="A catalogue bound like a library book: one flat cloth colour, a linen spine strip, a small typed label centred in the upper quarter, a shelf number top-left"></td>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/poster-programme.jpg" alt="A programme poster that is a notice: six rows on a flat spot-colour sheet, the weekday the only large word"></td>
  </tr>
  <tr>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/catalogue-spread.jpg" alt="A catalogue spread with a full-page plate on the left and a large number over bilingual numbered captions on the right"></td>
    <td width="50%"><img src="../../plugins/okrm-design/assets/examples/archive-index-web.jpg" alt="An archive website whose title is a sentence, whose actions are text in brackets, and whose current index letter is the one monumental element"></td>
  </tr>
</table>

A method for graphic and UI design, distilled from a study of one London studio's published work,
interviews and publishing catalogue. In one sentence: **attitude before form. Find a device in the
project's own content, stage it as a performative framework, re-enact a readymade or an existing
system with ubiquitous visual languages and strict production economy, and design reading as a
sequence.** It is a way of working, not a style library. The package contains none of the studio's
artwork and reproduces none of its layouts; the examples are fictional projects made with the method.

## Eight principles

1. **Content and concept.** Design builds a frame for content. Intuition first, then reasons for it,
   written down. No mood boards.
2. **Magnified clarity.** Identify the project's key point and exaggerate it. One system, one
   component enlarged. The implicit made explicit.
3. **Performative framework.** Metaphor, theatre, script: a stage, actors, a script. Dance inside
   existing systems; without constraints there is no game.
4. **Readymades and ubiquitous languages.** Historical readymades (signage alphabets, punched cards,
   library binding, stamps, cassettes, envelopes, manuals) and languages everyone owns (system
   Helvetica, Times, Courier, barcodes, labels). References are re-enacted, not borrowed for their look.
5. **Economy as form.** Minimums and constraints; every square millimetre is real estate; the fold
   gives four pages for two; covers are scaleless; imposition means seeing everything as it will be
   folded, cut, bound and remediated.
6. **Structure and play.** Consistent choices and choices in flux: the mark stays, the face changes;
   the format stays, the image changes.
7. **Duality.** Pair a thing with its opposite: hand and machine, dry type and wet material, geometry
   and brushwork, historic and contemporary.
8. **Sequence of reading.** A DJ needs a dancer: pace, anticipation, surprise; interleaved sections;
   the power of the spread; no chronology.

Plus institutional craft: get close to where decisions are made; design methods, not forms.

## What the evidence says about form

Measured on the studio's published photographs with a 0.1 grid (about ±1% of the object):

- Type lives at two poles. Spine sentences, labels and captions are about 1.5% of the cover height;
  body text about 1.2% of the page. A monumental word is about 10% of the cover height and 77% of
  its width; a single letter mark reaches 35–40%. The headline middle is almost absent.
- Voices: a Helvetica-class grotesk and a Times-class serif or typewriter monospace, or a single
  family. Custom faces re-enact a tradition (a neo-grotesk with alternates in the manner of its
  predecessors, a geometric sans derived from universal-alphabet principles). The studio's own
  website uses Helvetica/Arial, a small-size Times and a system monospace, with sizes in vw.
- Labels are centred and letterspaced; grotesk words sit in the corners at 6% margins; a monumental
  word starts at the left and sits in the upper third.
- Plates on covers carry a white border of about 10% of the width; posters about 3%; a small image
  on cloth takes about 40% of the cover width. Photography is mostly black and white.
- One flat colour is a material: a whole cover, an endpaper, a sign. Type on it is black or white.
- Materials come from the device: cloth and linen spine strips (9–14% of the cover width), parchment
  paper, kraft boxes, copper plates, washi, manila envelopes, PVC, rubber bands, foil, blind
  embossing, stickers, perforation, cassettes, playing cards.

## What you get

- An eight-step workflow in [SKILL.md](../../plugins/okrm-design/skills/okrm-design/SKILL.md):
  list the found material, write the device statement (readymade, system or duality), write the
  framework paragraph, set the order, set the economy, sequence the reading, make, check.
- [Order system](../../plugins/okrm-design/skills/okrm-design/references/design-system.md): device
  sources, framework, voices with their evidence, the two poles of scale with measurements,
  alignment, structure, furniture, colour as material, imagery, materials, imposition, sequence,
  and how each shifts by medium.
- [UI translation](../../plugins/okrm-design/skills/okrm-design/references/ui-translation.md): the
  implicit made explicit (actions as text in brackets, counters as furniture), index navigation,
  tables as lists, whole-screen colour as the change of paper, responsive design as folding, dry
  states and motion, accessibility as part of the order, an HTML/CSS skeleton.
- [Recipes](../../plugins/okrm-design/skills/okrm-design/references/recipes.md): device and
  framework templates, a spec template, a cover skeleton, image-model prompts per medium, a
  correction table.
- [Acceptance gates](../../plugins/okrm-design/skills/okrm-design/references/qa.md): three main
  gates (device, economy, sequence), order gates, interface gates, instant failures.
- `scripts/tokens.py`: generates an order sheet (CSS custom properties and JSON) and checks any sheet
  against the gates: at most two voices, two poles of scale with nothing in the middle, one field
  colour used as material, legible contrast, fold-derived columns, 45–75 character measure.

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

> Use $okrm-design to design a catalogue for 44 vessels. Find the device in the brief first and name the readymade it re-enacts.

> 用 $okrm-design 把这个藏品档案网站做成编号即导航、动作用括号写出的排印界面，输出 tokens.css 和一页 HTML。

> Use $okrm-design to lay out a quarterly journal as a folded format with a fixed mark and a cover that changes with each issue's mood.

## Study basis

The method was distilled from public material about [OK-RM](https://www.ok-rm.co.uk/), the London
studio founded in 2008 by Oliver Knight and Rory McGrath. Primary sources were read in full:

- Studio statements: the studio website; the [Maximillian William press release](https://static1.squarespace.com/static/65201415e0904740920e39c7/t/67922c5c1f8ec126ff7e3923/1737632860573/OKRM_PressRelease_MW.pdf) for *A Meaningful Order* (James Langdon); the [InOtherWords catalogue](https://in-other-words.co.uk/collections/all) of 41 publications with their specifications.
- Interviews and conversations: [Designers & Books, "Question Everything"](https://www.designersandbooks.com/blog/question-everything-conversation-with-ok-rm-rory-mcgrath) (2021); [Developments](https://developments.media/interviews/ok-rm) (2021); [System Magazine issue 15](https://system-magazine.com/issues/issue-15/ok-rm) (2020); [Eye 75, "They work with words"](https://eyemagazine.com/feature/article/they-work-with-words-3) (2010); [The Fashion Post](https://fashionpost.jp/portraits/396646) (2026); [Design Museum Q&A on Real Review](https://designmuseum.org/exhibitions/california-designing-freedom/product-z/flax-chair/qa-with-jack-self-real-foundation-and-rory-mcgrath-ok-rm) (2017); [It's Nice That on Real Review](https://www.itsnicethat.com/articles/real-review-jack-self-ok-rm-18082016) (2016); [Walker Reader, 2016 according to OK-RM](https://www.walkerart.org/reader/2016-the-year-according-to-ok-rm/); [AIGA Eye on Design on exhibition graphics](https://eyeondesign.aiga.org/great-exhibition-graphics-theyre-about-marrying-mood-mechanics/) (2017); [GRIND](https://grind-magazine.com/ok-rm/) (2023).
- Project coverage: It's Nice That on [Untitled](https://www.itsnicethat.com/articles/ok-rm-untitled-art-010216), [Antenne Books](https://www.itsnicethat.com/articles/okrm-antenne-books-identity-20316), [Manus × Machina](https://www.itsnicethat.com/articles/okrm-manus-x-machina-identity-150616), [Disobedient Bodies](https://www.itsnicethat.com/articles/okrm-disobedient-bodies-book-jw-anderson-hepworth-wakefield-jamie-hawkesworth-170317), [Naïvy](https://www.itsnicethat.com/articles/coco-capitan-okrm-inotherwords-naivy-publication-160221), [Kaleidoscope](https://www.itsnicethat.com/articles/ok-rm-kaleidoscope-africa-issue), [Footnote to a Project](https://www.itsnicethat.com/articles/ok-rm-footnote-to-a-project); BP&O on [Real Review](https://bpando.org/2017/09/25/hands-real-review/), [Antenne Books](https://bpando.org/2016/01/25/logo-design-antenne-books/), [Sancy & Regent](https://bpando.org/2013/03/12/logo-sancy-and-regent/); [Domus](https://www.domusweb.it/en/news/2016/01/14/ok_rm_untitled_art_fair_visual_identity.html) and [Mindsparkle](https://mindsparklemag.com/design/untitled-art-exhibition/) on Untitled; [Creative Boom on Naïvy](https://www.creativeboom.com/resources/okrm-coco/); [Het Nieuwe Instituut on Designing the Surface](https://grafisch-ontwerp.hetnieuweinstituut.nl/en/okrm); [magCulture](https://magculture.com/blogs/journal/real-review-8) on Real Review's covers.
- Typefaces: [Fonts In Use](https://fontsinuse.com/designers/190/ok-rm) records for Strelka Institute, Footnote to a Project, Real Review #3, Ice Lab, Karl Lagerfeld: A Line of Beauty, and Oscar Murillo: Frequencies.
- Images: the 31 work photographs published on the studio website, measured with a 0.1 grid; the website's own CSS.

Pages that refused automated access (Creative Review, Design Week, PRINT, the Met's catalogue
article, Tokyo TDC award pages, Strelka Mag) were not used beyond search summaries.

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
