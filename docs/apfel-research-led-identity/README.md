# APFEL Research-Led Identity

[← LabArt](../../README.md) · [中文介绍](README.zh-CN.md)

A six-step method for research-led visual identities, distilled from the working
method of the London studio A Practice for Everyday Life (APFEL), not from the look
of its projects. APFEL has said it does not want a signature style; its projects
look different from each other, and what they share is a path.

The path: research the object, choose one fact you can point at, write a one-line
thesis, draw a custom letterform and one dominant grid rule from that fact, allow
one traceable tension per piece, carry the rule across media, and score the result
before calling it finished.

## Examples

Both sets were made by the Skill from a written brief, with real web research. The
institutions and the brand are fictional test briefs.

<table>
  <tr>
    <td width="50%">
      <img src="../../plugins/apfel-research-led-identity/assets/examples/sun-prints.jpg" alt="Exhibition identity for Anna Atkins: Sun Prints in translucent strip letters on Prussian blue">
      <br><strong>Anna Atkins: Sun Prints</strong><br>
      Seed: every word in her 1843 cyanotype book was written on oiled paper and
      printed in sunlight, so it sits on a paler sheet. The letters are cut strips of
      that paper; where two strips cross, the tone steps up.
    </td>
    <td width="50%">
      <img src="../../plugins/apfel-research-led-identity/assets/examples/shenguang-enamel.jpg" alt="Identity for a Shanghai enamelware workshop, with a hanging point on the character 申">
      <br><strong>申光搪瓷 · Shenguang Enamel</strong><br>
      Seed: each enamel piece hangs on a hook in the kiln and keeps one small unglazed
      point. The stem of 申 ends in that point, and every layout hangs from one line.
    </td>
  </tr>
</table>

Cyanotype scans in the first set are public-domain NYPL images. Product and workshop
photographs in the second set are AI-generated stand-ins and are labelled as such
in the pieces.

## The Six Steps

1. **Conceptual thesis.** List 3–5 concrete facts from four sources: site, objects,
   materials and making, archive. Choose one seed and write "X is Y, so every
   element Z."
2. **Typographic hierarchy.** L0 is a custom letterform grown from the seed; L1 is
   display; L2 is a quiet existing text face; L3 is an optional second voice.
3. **Grid system.** One dominant rule from the seed, with a fixed ratio or physical
   size, over an ordinary 4–6 column grid.
4. **Controlled visual tension.** One source of tension per piece, traceable to the
   research.
5. **Test across media.** Identity sheet, poster, signage, website, book cover.
6. **Evaluate originality and coherence.** Eight tests scored 0–2. Below 12/16, go
   back to step 1 and change the seed.

## What Is Included

- `.codex-plugin/plugin.json`: Codex plugin metadata.
- `skills/apfel-research-led-identity/SKILL.md`: the method, in Chinese.
- `skills/apfel-research-led-identity/agents/openai.yaml`: Codex UI metadata.
- `assets/examples/`: two selected outputs declared as plugin interface screenshots.
- `LICENSE`: the existing license, also included in the standalone Skill.

## Install As An Agent Skill

With GitHub CLI 2.90 or newer:

```bash
gh skill install haorantang97/LabArt plugins/apfel-research-led-identity/skills/apfel-research-led-identity@main --agent codex
```

The repository also supports the open `skills` installer:

```bash
npx skills add haorantang97/LabArt --skill apfel-research-led-identity
```

## Install In Codex

```bash
codex plugin marketplace add haorantang97/LabArt --ref main
codex plugin add apfel-research-led-identity@labart
```

Start a new Codex task after installation so the new skill is loaded.

## Example Requests

- Build a research-led identity for a small museum: identity sheet, poster, sign, website, and book cover.
- Find one fact in this workshop's process and grow a wordmark and grid rule from it.
- Score this identity with the six-step evaluation and tell me which seed to change.

## Originality

The Skill reuses APFEL's path — take a form, make it a letter, make it a rule —
not its letterforms or layouts. Do not copy its existing projects (the Hepworth
bevels, the Venice eye, the CAM A), and do not present outputs as APFEL's work.

## License

Distributed under the PolyForm Noncommercial License 1.0.0. See [LICENSE](../../LICENSE).

## Validation

See [how the method was tested](VALIDATION.md) and the [current package checks](../VALIDATION.md).
