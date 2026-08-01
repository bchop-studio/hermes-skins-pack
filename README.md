# Hermes Skins Pack — 50 Subscriber Themes

![Hero](hero.png)

A curated pack of **50 unique, drop-in skin themes** for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) CLI and TUI. Every skin is a complete YAML file using the real Hermes color keys — no inherited defaults, no silent fallbacks.

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

## Quick Start

1. Copy any YAML block from `hermes_50_skins_pack.md` into `~/.hermes/skins/<name>.yaml`
2. Switch to it: `/skin <name>`
3. Or set as default: `hermes config set display.skin <name>`

```bash
mkdir -p ~/.hermes/skins
# Example: save neon-ghost
cat > ~/.hermes/skins/neon-ghost.yaml << 'EOF'
# paste the YAML block here
EOF
```

## License

MIT. Do whatever you want with these.

Made by @BChopLXXXII

Built for vibe coders who just want their AI to feel less... corporate.

Ship it. 🚀

If this helped, ⭐ the repo — it helps others find it.