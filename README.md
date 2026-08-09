# Hermes Skins Pack — 100 Themes

![Cover](hermes-cover.png)

A curated pack of **100 unique, drop-in skin themes** for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) CLI and TUI. Every skin is a complete YAML file using the real Hermes color keys — no inherited defaults, no silent fallbacks.

## What's Inside

| Category | Skins |
|---|---|
| Cyberpunk / Synthwave | neon-ghost, chrome-rain, glitch-punk, void-sunset, netrunner |
| Modern Dark / OLED | obsidian, deep-void, graphite, midnight-studio, eclipse |
| Earth & Nature | redwood, sandstone, deep-ocean, moss-stone, aurora-boreal |
| Retro / Vintage | amber-terminal, green-screen, typewriter-cream, commodore-64, newsprint-noir |
| Monochromatic / Minimalist | bone-white, slate-mist, warm-ash, steel-thread, single-malt |
| High Contrast | white-flash, solar-flare, black-canary, red-alert, high-noon |
| Pastel / Soft | lavender-dream, peach-fuzz, seafoam-silk, dusty-rose, baby-blue |
| Light / Paper Modes | warm-parchment, rice-paper, blueprint, linen-sage, alabaster |
| Fantasy / Gaming | dragon-blood, arcane-tome, shadow-thief, enchanted-forest, forge-master |
| Abstract / Artistic | vaporwave-mall, brutalist-concrete, stained-glass, desert-neon, liquid-silver |
| Ocean & Coastal | abyssal-plain, tidal-pool, coral-reef, lighthouse-beam, kelp-forest |
| Desert & Canyon | sahara-dusk, mesa-verde, canyon-shade, cactus-bloom, mirage |
| Botanical & Garden | fern-hollow, wildflower, bonsai, ivy-wall, sunflower-field |
| Cosmic & Deep Space | nebula-drift, event-horizon, pulsar, starlight-ash, comet-tail |
| Industrial & Metal | rust-belt, brushed-steel, copper-patina, carbon-fiber, anodized |
| Neon Nightlife | ultraviolet, glow-stick, blacklight-poster, neon-koi, laser-lemon |
| Cozy & Hearth | candlelight, knit-wool, ember-glow, cocoa-nib, hearth-stone |
| Ink & Editorial | manuscript, fountain-pen, pencil-sketch, sepia-archive, marginalia |
| Candy & Pop | bubblegum, sorbet, taffy, jellybean, cotton-candy |
| Experimental & Avant-Garde | datamosh, vapor-trail, phosphor-burn, chromatic-drift, terminal-bloom |

## Install

Download or clone the repository, then copy the skins into Hermes:

```bash
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/skins"
cp -i skins/*.yaml "${HERMES_HOME:-$HOME/.hermes}/skins/"
```

The `-i` flag asks before replacing any skin with the same filename.

Switch skins inside Hermes with `/skin <name>`, or set one as the default:

```bash
hermes config set display.skin neon-ghost
```

To install one skin by hand:

```bash
mkdir -p ~/.hermes/skins
cp skins/neon-ghost.yaml ~/.hermes/skins/
```

## Repository Contents

- `skins/`, 100 ready-to-use YAML skin files
- `README.md`, installation and skin list
- `VERSION`, current pack version
- `hermes_100_skins_pack.md`, browsable catalog with every full YAML block
- `scripts/validate_pack.py`, stdlib-only checker for the whole pack

## Validate

```bash
python3 scripts/validate_pack.py
```

Checks the skin count, unique names, the complete 43-key color schema, hex
format, contrast floors, and that README and catalog stay in sync with the
files on disk.

Every skin defines the pack's complete 43-key palette, including syntax colors and `shell_dollar`, so its supported roles do not silently inherit the default theme.

## License

MIT. See `LICENSE`.

Made by @BChopLXXXII

Built for vibe coders who just want their AI to feel less... corporate.

If this helped, ⭐ the repo — it helps others find it.
