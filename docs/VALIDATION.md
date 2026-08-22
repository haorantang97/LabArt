# Validation

## Release Scope

This repository distributes three Codex plugins:
`antibes-holiday`, `contemporary-zhuo-calligraphy`, and
`deconstructive-ink-cultural-collision`.

The image-quality acceptance gates below focus on the flagship
`antibes-holiday` plugin; the structural checks apply to every plugin in the
marketplace.

The release intentionally excludes:

- third-party screenshots and source-account information;
- copied compositions, characters, signatures, or logos;
- rejected generation attempts and internal comparison sheets;
- private absolute paths, credentials, task logs, and local configuration;
- a bundled image model or undeclared external service.

## Structural Checks

The following checks must pass before release:

1. Codex `quick_validate.py` accepts every Skill.
2. Codex `validate_plugin.py` accepts every Plugin.
3. `.agents/plugins/marketplace.json` parses and discovers every Plugin.
4. A clean ZIP extraction contains `SKILL.md`, both reference files, the calibration
   asset, seven selected example outputs, UI metadata, and the plugin manifest.
5. Installed Plugin files match the release source.
6. Repository-wide scans find no private paths, credentials, or source-platform URLs.

## Forward Tests

The drawing system was tested across unrelated subject families:

- a person without recurring accessories;
- a non-human living form;
- a functional object;
- an abstract physical relationship;
- an expressive display mark;
- a multi-actor narrative scene;
- a dominant-object narrative scene.

At least one isolated-subject test and one narrative-scene test used only the
bundled non-semantic stroke calibration image. No third-party image was supplied
at runtime for those tests.

## Primary Acceptance Gates

Every generated candidate must pass:

- physical pen behavior;
- contrast between fast sweeps and slower recognition marks;
- structural drift plus visible loss and recovery of control;
- at least one imperfectly registered junction or displaced restart;
- shorthand recognition through incomplete forms;
- unforced proportion, spacing, and terminals;
- transfer without imported motifs;
- original subject and composition.

Narrative scenes must also pass:

- causal readability;
- hierarchy through scale, crop, density, and active blank space.

There is no aggregate score. Weak physicality cannot be offset by strong semantics.

## Compatibility

- Codex: full Plugin and Skill loading, with built-in image generation when available.
- Other Agent Skills loaders: the portable `SKILL.md`, references, and asset remain
  usable when the loader preserves relative paths.
- Other image-capable agents: use their native renderer.
- Agents without rendering: output a renderer-ready prompt and validation checklist.

Platform-specific UI metadata under `agents/openai.yaml` may be ignored safely.

The public example gallery is documentation only. It is not loaded as style
evidence by the Skill and is not required at generation time.

## Residual Limitations

- Image quality still depends on the renderer and may require focused iterations.
- Small production logos require authored vector reconstruction and optical testing.
- Abstract relationships require a concrete physical metaphor to remain inferable.
- Claude Desktop does not discover Codex plugins directly; it needs a separate
  instruction or connector setup.
