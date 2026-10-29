# Package validation

## x-ray 0.1.0 — new plugin

On 2026-10-30, added X-ray with 13 plugin files, an 8-file standalone Skill,
and four declared interface screenshots: hand/ball, player/keys, folded shirt,
and frontal handbag. The shirt screenshot is bundled in the Skill as a labelled
generated appearance anchor; the other three are plugin-level presentation images.

- All five marketplace sources passed scripts/check_packages.py.
- The new source Skill passed the installed official quick_validate.py.
- A clean copy retained the plugin's complete inventory and SHA-256 hashes and
  passed the plugin checker.
- GitHub CLI installed the new Skill by name from the staged local checkout into
  an isolated custom directory. Its eight-file inventory, unchanged resource
  hashes, package links, and official Skill format validation passed. The CLI
  adds source-tracking metadata to SKILL.md.
- The four selected screenshot PNGs match their original generated files byte
  for byte. Repository Markdown/image links and Git whitespace checks passed.
- All 12 existing Deadpan tests passed; existing plugin contents were unchanged.

The first exact-path local install attempt did not discover the untracked Skill;
staging the files and selecting x-ray by name installed it successfully.
No global plugin installation or client activation is claimed. The visual tests
and unresolved limits are recorded in [X-ray validation](x-ray/VALIDATION.md).

## lab-graphic-design 0.1.0 — new plugin

Added `plugins/lab-graphic-design` (4 plugin files beyond the Skill: manifest,
license, two declared interface screenshots; standalone Skill: 3 files). The other
three plugins are unchanged. On 2026-10-27 `scripts/check_packages.py` passed for all
four marketplace sources, and the new Skill passed the installed official
`quick_validate.py`. No marketplace installation or client activation is claimed.

## 0.2.1 — installation boundaries

LabArt distributes three independent plugins. The marketplace continues to select
`plugins/antibes-holiday`, `plugins/tephra`, and `plugins/deadpan-doodles`. Each
manifest is version `0.2.1`; the source paths and plugin names are unchanged so
existing marketplace entries continue to identify the same plugins.

| Plugin | Plugin files | Standalone Skill files | Declared interface screenshots |
| --- | ---: | ---: | ---: |
| Antibes Holiday | 15 | 6 | 7 |
| Tephra | 25 | 17 | 7 |
| Deadpan Doodles | 18 | 13 | 4 |

A standalone Skill is `plugins/<name>/skills/<name>/`. It contains instructions,
metadata, required images, scripts, references, and its existing license. A plugin
also includes its manifest, license, and declared interface screenshots.

Repository introductions and validation history are under `docs/`. Deadpan's
repository artwork and design notes are under `assets/deadpan-doodles/`; developer
tests are under `tests/`. These directories are outside every marketplace source.

Tephra's mode-selection image is part of the Skill because `SKILL.md` uses it to
explain which rendering mode to choose. Its interface screenshot points to that
same file. The animated gallery files remain declared plugin screenshots. Antibes'
calibration image and prompt recipes, and Deadpan's fixed recipes, image manifest,
style anchors, and prompt assembler remain runtime resources.

## Checks performed on 2026-10-15

- All three Skills passed the installed official `quick_validate.py`.
- `scripts/check_packages.py` checked marketplace source paths, plugin-local UI
  image references, complete file inventories including hidden files, and local
  Markdown dependencies inside each standalone Skill.
- All three marketplace source directories were copied to an isolated temporary
  destination without exclusions. Their inventories and SHA-256 hashes matched
  the source; the same package checks passed on the copies.
- GitHub CLI 2.96.0 installed all three Skills from the local checkout into a
  temporary destination with `--from-local --all --dir`. The actual installed
  file inventories passed the Skill checks. GitHub CLI adds source-tracking
  metadata to `SKILL.md`; that is installer metadata rather than a recipe change.
- The remote `plugins/antibes-holiday/skills/antibes-holiday@main` selector was
  exercised against the pre-publication default branch. It resolved `main`,
  avoiding the old `v0.1.0` tag. This checked command/ref resolution, not the
  unpublished 0.2.1 contents.
- All 12 existing Deadpan prompt-assembler tests passed after moving the test
  file outside the package. Fixed recipes, image hashes, reference order, narrow
  edits, relocation, and overwrite protection remain covered.
- Tephra's renderer ran from the isolated copied plugin in both particle and
  dither modes, each producing a 128 × 128 PNG and a four-frame GIF from a synthetic
  fixture. No rendering algorithm or recipe changed.
- Python syntax, local documentation links, synchronized Deadpan command blocks,
  preserved runtime resource hashes, and Git whitespace were checked.

Run the repository checks from its root:

```sh
python3 -B scripts/check_packages.py
python3 -B -m unittest discover -s tests/deadpan-doodles -v
```

To inspect an actual installation, pass its directory:

```sh
python3 -B scripts/check_packages.py --plugin /path/to/installed/plugin
python3 -B scripts/check_packages.py --skill /path/to/installed/skill
```

The checker does not install, upgrade, or modify anything. Release verification
must also inspect the resulting files from the published installation command;
local copy checks do not establish marketplace activation. Existing plugin caches
were not changed during this cleanup. No fresh image-model generation or client
activation result is claimed.

Earlier visual evaluations remain in [Antibes Holiday](antibes-holiday/VALIDATION.md)
and [Deadpan Doodles](deadpan-doodles/VALIDATION.md). They describe their named
versions, not a new aesthetic acceptance of 0.2.1.
