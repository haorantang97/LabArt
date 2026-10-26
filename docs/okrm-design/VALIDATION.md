# Validation scope

## 0.3.0 — from form to path

0.3.0 moves the method's core from the look of the work to the way a project is conceived:
a generation document in nine steps plus one strange decision, written before any layout.
The question for validation was therefore not "does the output look right" but "does the
path produce proposals that follow from the brief and contain a decision a conventional
studio would reject — without being mistakable for a published project".

### Blind comparison

Three fictional briefs were written for the test (a catalogue of sixty unattributed ceramic
vessels for a travelling show with one print run; an identity and first-year publication for
a bilingual architecture school in a former bus depot that "does not want a brand"; a launch
object "that is not a lookbook" for a knitwear label run by a former textile engineer, with a
swatch archive and a five-year photographer). Three directions answered each brief:

- A: a competent studio agent with no skill;
- B: an agent given the 0.2.0 skill and order system (form-first);
- C: the 0.3.0 generation protocol.

The nine proposals were shuffled per brief with a seeded script and relabelled, and a fresh
agent that had seen none of the files judged them on four questions: which follows most
directly from the brief; which contains the one decision a conventional studio would reject,
and whether it follows from the brief; which is the most expected; which it would commission
and on what conditions. It also checked whether any proposal could be mistaken for a specific
published project.

**Round 1** (C written by the same agent that wrote the protocol): the judge preferred B on
all three briefs. A was "most expected" on each. No proposal was mistakable for a published
project. The judge's criticism of C was specific and correct: it imported readymades the
briefs did not contain (an accession ledger, a departure board) when the briefs already
offered a grey card, bay numbers and a test record; it filled optional template fields with
stock phrases ("the thing you cannot know without the show", "one change of pace"); and its
object decisions carried numbers that did not add up or contradicted each other (an
"interleaved signature" that is really sixty tip-ins; a "second printing" inside a one-run
constraint; eighty pages for eleven sheets).

The protocol was revised on those three points: the readymade must be taken first from
objects already in the brief, and an external one needs a sentence saying why it is more
accurate; step 4 is now two tables (order and economy) and every decision carries numbers
that are checked against each other (pages from sheets, copies × unit cost = budget, weight
against postage); optional fields stay empty rather than being filled; the continuation plan
may not violate a constraint written in step 4; the gates in `qa.md` test each of these.

**Round 2** (C written by a fresh agent from the revised protocol, which had not seen round 1;
new seed and labels; a new judge): the judge commissioned the 0.3.0 proposal on all three
briefs and named the no-skill proposal as "the safe one" on all three. On each brief it found
that the 0.3.0 proposal followed most directly from the brief's own objects and numbers (the
grey card as paper and the accession number as the only folio; 24 students, 10 evenings and
2 languages as the panel count of one folded sheet published in September before the year
runs; the engineer's sampling technique as the way the swatches are knitted) and that its
rejectable decision followed from the brief rather than from a conceit. It re-did the
arithmetic by hand and found the 0.3.0 proposals correct on every count (imposition, page
plan, weights, copies × unit cost, envelope sizes), while finding page-count, fold, binding
and weight errors in both other directions. No proposal was mistakable for a published
project.

Its remaining criticisms of 0.3.0 were specific and have been folded into the protocol:
one claimed readymade ("nothing imported") brought a role the brief did not contain; the
operator name in the strange-decision sentence reads as a filled slot; one template sentence
("we hold the publisher's hat") recurred across proposals; a ganged imposition of thirteen
different cards was counted as if it were one; a sixteen-layer cross fold and hand folding
were not costed; no design fee appeared in the economy tables. `genesis.md` now lists these
as common miscounts and false moves, the operator goes in the acceptance record rather than
the proposal, and `qa.md` fails repeated template phrasing and unchecked "nothing imported"
claims.

**Round 3** (three new briefs of different media — a twelve-week risograph poster series
for a library's poetry readings, a documentary photographer's estate website to be built by
one developer in three months, and a family quarry's 120th-anniversary book with a visitor
centre in the old weighbridge office; all three directions written by fresh agents, each
seeing only its own material; new seed, new labels, new judge): the 0.3.0 proposal was
commissioned on all three briefs and the no-skill proposal was "the safe one" on all three.
The judge found the 0.3.0 arithmetic correct throughout (2,400 sheets and 38 masters; 39,600
frames, twelve developer-weeks; 264 pages in 33 eight-page sections, 125 plates, £38.33 a
copy) and judged its interface for the estate the only one "the developer can begin from on
Monday", with a stated acceptance test. It found page-count, imposition, colour-count and
screen-scale errors in the other two directions on every brief.

It also found two failures in 0.3.0 that the earlier rounds had not: the strange decision on
the poster brief ("the poets read from the poster") does not follow from the brief and is
severable — strike it and the system is unchanged — which is precisely the "gimmick" case the
strange-decision gate exists to reject; and the quarry proposal hung all 400 core trays and
several hundred prints in a weighbridge office nobody had measured. Smaller: a fold sentence
that contradicted the column layout, an unstated week-12 split, 36 frames per roll assumed
rather than read from the data, template fields filled by denial ("Editing: nothing to
choose; the rule chose"), the optional "what you only know from being there" line filled with a
phrase despite the instruction to leave it empty, and type named only as "Times-class" and
never chosen.

Folded into the protocol after round 3: a severability test on the strange decision (strike
it; if no object, sequence or economy decision changes, it is a posture, not a decision — and
the real one is usually already in the brief, as both independent writers reaching the blank
ruled ledger pages showed); rooms and walls measured and load-checked before anything is hung;
period edges counted separately; counts taken from the data rather than assumed; the optional
Hultén line removed from the template and kept as a self-check only; filling a field by
denial listed as a false move; type to be named in step 6.

What the three rounds show: the path method does not by itself produce better proposals — the
first round's author knew the protocol best and lost — but a protocol whose steps are tied to
the brief's own objects and whose numbers must close does, in the hands of an agent reading
it cold: six commissions out of six across two rounds and six briefs, against a no-skill
proposal judged "most expected" every time. Each round is one judge on three briefs, so this
is evidence that the method produces proposals a blunt reader prefers and can check, not a
general claim; and round 3 shows the strange-decision gate can still pass a gimmick, which is
why the severability test was added.

The briefs, the nine proposals of each of the three rounds, the shuffle scripts, the keys and both judges'
notes are kept outside the package and are not committed, because they contain the
proposals' full text; the method of the test is described here so it can be re-run.

### Checks performed on 2026-10-26

- `scripts/check_packages.py` passed for all marketplace plugins, including the six declared
  screenshots and all local links.
- 15 behavioral tests for the order-sheet generator and checker passed
  (`tests/okrm-design/test_tokens.py`); the checker is unchanged from 0.2.0.
- The generation-document example was written with the protocol and checked against the
  main gates of `references/qa.md` (complete, one strange decision with its operator and
  source line, object before page with consistent numbers, readymade from the brief, economy
  list, transferable method, sequence with room for chance, continuation inside step 4's
  limits). The five form examples from 0.2.0 were kept and re-checked against the order gates.
- The case cards were written from the sources listed in `CASES-INDEX.md`; each card's
  strange decision is quoted or paraphrased from a published interview or review, not inferred
  from a photograph.

Not claimed: the studio's own book on its method was not read (not available to the session);
its social-media archive was not collected; measurements in the order system remain starting
values taken from photographs; no image-model generation was run; no marketplace activation
was tested. The blind comparison used three briefs and one judge per round, which is enough to
catch the failures listed above and not enough to claim the method wins in general.

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
