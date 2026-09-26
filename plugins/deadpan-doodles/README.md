**English** | [中文](README.zh-CN.md)

# Deadpan Doodles · 沙冰

<table>
  <tr>
    <td width="33%"><img src="skills/deadpan-doodles/assets/style/high-forehead.png" alt="Watercolor portrait with long hair, round glasses, and an oversized forehead"></td>
    <td width="33%"><img src="assets/examples/portrait-short-hair.png" alt="Watercolor portrait with short hair, stubble, and two vertical-line eyes"></td>
    <td width="33%"><img src="assets/examples/portrait-blond.png" alt="Watercolor portrait with blond hair, a dark jacket, and a red tie"></td>
  </tr>
</table>

When I was in secondary school, the girl who shared my desk loved to draw. During breaks, and often during class, she would turn her notebook sideways and paint watercolors of me.

Two vertical lines for eyes, no nose, messy hair, color often bleeding beyond the outlines. She would slide the finished drawing over, and I would say, what on earth is this supposed to be?

The classroom windows were open. Wind lifted the translucent curtains, and the fierce sunlight caught the dust in the air. I would sneak mouthfuls of bagged slush brought back from the previous PE lesson. The slush melted fast; the paint on the paper was still wet. They overlapped in the same midsummer.

Later we went our separate ways, and naturally I rarely got to see her ugly drawings anymore. Somehow I ended up making art myself, drawing all sorts of things. Whenever the weather gets hot, I find myself searching my own pictures for that bleeding color. But my drawings are usually too neat, like an air-conditioned room: comfortable, but without a breeze. The breeze comes through the crooked lines. A little embarrassed, and unwilling to be entirely serious.

So I made this skill, just as the weather was about to turn cool. It comes from a selfish wish: to keep drawing those summers a little uglier.

## How it feels

- **As if a child drew it carefully.** Size and space have not quite been planned out; a few corners are awkward, while the subject takes itself completely seriously.
- **Transparent washes that sometimes escape the lines.** Paper shows through pale color, even dark areas keep their water, and ink and pigment follow their own paths through white gaps, wet edges, and local overlaps.
- **Offbeat proportions, restrained expressions.** Large masses, tiny features, and undersized supports create contrasts. The shape and the situation carry the dry humor.
- **More than portraits.** People, cats, dogs, plants, objects, and small scenes all fit. Backgrounds and detail can coexist with a childlike hand.

## Illustration example

<img src="assets/examples/illustration-scenes.png" alt="Eleven watercolor vignettes with a character, cats, flowers, and everyday objects" width="760">

The three portraits and this illustration were generated in this project and selected to show its visual direction. Gallery images are not automatically attached to every generation. The default style anchor and optional cat reference are described in the [asset index](skills/deadpan-doodles/references/style-assets.md).

## Start

Install from the LabArt marketplace using the Codex CLI:

```sh
codex plugin marketplace add haorantang97/LabArt
codex plugin add deadpan-doodles@labart
```

An image-generation-capable host is required. This package supplies instructions, reference images, and a prompt assembler; it does not bundle a model or configure API keys. For manual installation, keep the [whole skill folder](skills/deadpan-doodles), not just SKILL.md.

Attach a photo and try:

> Use $deadpan-doodles to turn this photo into a watercolor character. Keep the recognizable features, make the proportions offbeat, keep the expression deadpan, and let some color bleed beyond the lines.

Or describe a small scene:

> Use $deadpan-doodles to draw a cat sprawled over a stack of books beside a cup of tea. Its body is too large, its paws are tiny, and it is seriously doing nothing.

A [dedicated portrait module](skills/deadpan-doodles/references/portrait.md) handles likeness and character proportions. Other subjects do not inherit a fixed forehead, glasses, or long hair. For an already selected image, request a change to only the named part.

## Inside the package

[Main skill](skills/deadpan-doodles/SKILL.md) · [Fixed recipes](skills/deadpan-doodles/STYLES.md) · [Invocation protocol](skills/deadpan-doodles/PROTOCOL.md) · [Visual checks](skills/deadpan-doodles/references/qa.md)

The package retains the general Sha Bing recipe `shabing-20260925-1`. The assembler records the actual prompt, reference order, and file hashes; it does not call an image service. The same skill helps maintain a direction, but cannot guarantee identical shapes or watercolor behavior.

The public invocation is `$deadpan-doodles`; the earlier local name `deadpan-watercolor-ip` is not a second plugin. Structural checks and aesthetic results are recorded separately in the [validation notes](VALIDATION.md).

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Share only images, requests, and actual prompts you have permission to share. Keep the English and Chinese introductions aligned.

[Back to LabArt](../../README.md)
