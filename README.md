# TArt

TArt is a collection of original visual-creation skills: relaxed black-pen illustration, contemporary Chinese brush writing, and deconstructive ink translation.

The collection is organized around visual grammar and generative behavior rather than imitation of a named artist or source image.

## Skills

### Antibes Holiday

`antibes-holiday` is the flagship TArt skill for original relaxed black-pen illustrations, narrative scenes, expressive marks, and early logo exploration.

- [Skill instructions](plugins/antibes-holiday/skills/antibes-holiday/SKILL.md)
- [Plugin metadata](plugins/antibes-holiday/.codex-plugin/plugin.json)
- [Original examples](plugins/antibes-holiday/assets/examples/)

It focuses on physical stroke behavior, shorthand recognition, confident incompletion, causal story staging, active blank space, and non-equilibrium proportion.

### Contemporary Zhuo Calligraphy

`contemporary-zhuo-calligraphy` generates deliberately awkward contemporary Chinese brush writing through structural imbalance, stroke causality, and spatial pressure.

- [Skill instructions](plugins/contemporary-zhuo-calligraphy/skills/contemporary-zhuo-calligraphy/SKILL.md)
- [Style grammar](plugins/contemporary-zhuo-calligraphy/skills/contemporary-zhuo-calligraphy/references/style-grammar.md)
- [Quality gate](plugins/contemporary-zhuo-calligraphy/skills/contemporary-zhuo-calligraphy/references/quality-gate.md)

The skill uses image generation for complete compositions and does not pass source reference images into the runtime generation path.

### Deconstructive Ink Cultural Collision

`deconstructive-ink-cultural-collision` translates modern, anatomical, technological, cosmic, and landscape subjects through accumulated ink events, broken contours, layered gray ink, and meaningful paper reserve.

- [Skill instructions](plugins/deconstructive-ink-cultural-collision/skills/deconstructive-ink-cultural-collision/SKILL.md)
- [Prompt recipes](plugins/deconstructive-ink-cultural-collision/skills/deconstructive-ink-cultural-collision/references/prompt-recipes.md)
- [Style specification](plugins/deconstructive-ink-cultural-collision/skills/deconstructive-ink-cultural-collision/references/style-spec.md)

## Install in Codex

Add this repository as a local marketplace:

```bash
codex plugin marketplace add https://github.com/haorantang97/TArt.git
```

Then install the plugin you need:

```bash
codex plugin add antibes-holiday@tart
codex plugin add contemporary-zhuo-calligraphy@tart
codex plugin add deconstructive-ink-cultural-collision@tart
```

For a local checkout:

```bash
codex plugin marketplace add /absolute/path/to/TArt
```

## Compatibility

The skills are written as portable `SKILL.md` packages. Codex uses the bundled plugin metadata; other compatible agents can read the skill folder and its supporting `references/`, `scripts/`, and `assets/` directly.

Rendering behavior depends on the image-generation or raster-rendering capability available in the host agent. A skill must not claim to have rendered an image when no renderer is available.

## Originality and privacy

The collection contains original instructions and calibration assets. Do not trace third-party source images, preserve source compositions, reuse signature characters, or market outputs as an official third-party style.

Private local paths, conversation records, and personal source archives are not part of TArt.

## License

The TArt instructions and bundled original assets are distributed under the PolyForm Noncommercial License 1.0.0. Supporting resources retain any attribution or license notice included in their directory.
