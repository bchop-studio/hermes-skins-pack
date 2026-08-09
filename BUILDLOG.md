# BUILDLOG.md — Hermes Skins Pack

The real build record. No fake milestones, no invented drama.

## 2026-08-09 — Expanded from 50 to 100 skins

### What changed
Added 50 new skins in 10 visual families, bringing the pack to 100. Updated the README, full YAML catalog, and VERSION to 2.0.0. Added a deterministic validator for counts, schema, color format, contrast, palette distance, and README/catalog parity.

### What broke
The first pass had six palettes that were too similar and several validator holes around malformed structure, duplicate keys, and missing names. Those were caught in review, fixed, then rechecked with malformed-tree mutations.

### Current status
All 100 skins load through Hermes from an isolated home. The original 50 remain byte-identical. Fresh validator, malformed-tree mutation checks, whitespace checks, and full-history plus worktree secret scans pass.

---

## 2026-08-02 — Public release: MIT license + final cleanup

### What changed
Trimmed the public repo to skins, README, VERSION, and catalog. Added MIT license. The repo is now fully public-ready.

### What broke
Nothing. Cleanup pass after the launch.

### Current status
Live on GitHub. 50 skins, MIT licensed, public.

---

## 2026-08-02 — 50 skins packaged and shipped

### What changed
All 50 Hermes CLI/TUI subscriber skin themes packaged into the repo. Every skin is a complete YAML file using the real Hermes color keys. Included README with install guide and full skin catalog.

### What broke
Initial packaging included private assets and Windows Zone.Identifier junk. Scrubbed those before the public push.

### Current status
Shipped. First OSS project, biggest X post ever (49 likes, 8 reposts).

---

## 2026-07-31 — First commit: 50 skin themes

### What changed
Created the initial batch of 50 Hermes Agent CLI/TUI themes. Cyberpunk, synthwave, OLED dark, retro terminal, and more. Every skin uses real Hermes color keys, not generic theme values.

### What broke
Nothing yet — this was the creation pass.

### Current status
All 50 skins created and ready for packaging.
