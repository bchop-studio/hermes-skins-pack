# BUILDLOG — hermes-skins-pack

Reverse-chronological build history. Newest entry on top.

## 2026-08-09 — v2.0.0: expand pack from 50 to 100 skins

Branch: feat/add-50-skins (kanban task t_4337a5d0).

- Added 50 new curated skins under `skins/`, organized as 10 new visual
  families of 5: Ocean & Coastal, Desert & Canyon, Botanical & Garden,
  Cosmic & Deep Space, Industrial & Metal, Neon Nightlife, Cozy & Hearth,
  Ink & Editorial, Candy & Pop, Experimental & Avant-Garde.
- Existing 50 skins unchanged.
- Every new skin uses the identical 43-key color schema as the existing set,
  quoted lowercase `#rrggbb` values, unique `name` matching its filename, a
  unique description, and a distinct background palette.
- Contrast floors enforced at authoring time and in the validator: primary
  text >= 7:1, labels >= 4.5:1, accent and semantic colors >= 3:1 against
  the skin background, status bar text >= 4:1 against the status bar
  background. Dim/comment keys stay intentionally faint, matching the
  existing pack's style.
- Replaced `hermes_50_skins_pack.md` with `hermes_100_skins_pack.md`,
  regenerated from `skins/` so every embedded YAML block matches its source
  file byte-for-byte.
- README updated: 100 themes, 20 category rows, validator usage.
- VERSION bumped 1.0.0 -> 2.0.0.
- Added `.hermes.md` (repository lifecycle rules) and this BUILDLOG.
- Added `scripts/validate_pack.py`, a stdlib-only deterministic checker:
  skin count, unique names/filenames, exact schema key set, no unsupported
  keys, strict hex, README and catalog membership, catalog byte-parity,
  and contrast gates.

### Independent review, round 1 (NEEDS-CHANGES, addressed)

Reviewer: delegated read-only agent (Claude Code CLI unavailable, not logged
in). Three findings, all fixed in this branch:

1. major: unsupported top-level key check was broken (`TOP_RE` missing
   `re.M`); `ALLOWED_BRANDING` unused. Fixed: multiline flag added and
   branding keys are now validated against the allowlist.
2. major: the 43-key schema was inferred from the first parsed file instead
   of a pinned known-good set. Fixed: `EXPECTED_KEYS` is now hardcoded from
   the v1 schema; every skin must match it exactly.
3. major: near-duplicate palettes inside the new set (closest pair measured
   avg per-channel distance 7 over the 11 most visible colors; the existing
   pack's own floor is 16). Fixed: reworked six palettes (candlelight,
   canyon-shade, knit-wool, mesa-verde, kelp-forest, anodized); new-vs-new
   minimum is now 16 and new-vs-existing minimum is 30. Added a permanent
   distinctness gate to the validator (minimum 15).

Mutation testing: 11 sabotaged trees (duplicate name, missing key,
unsupported color/top-level key, uppercase/short hex, README omission, stale
catalog block, cloned palette, low-contrast text) all fail the validator;
the clean tree passes. A distinctness-pass crash on schema-broken files was
found and fixed during mutation testing.

### Independent review, round 2 (PASS)

Verifier measured min palette distances: new-vs-new 16.454
(ember-glow / rust-belt), new-vs-existing 30.485 (mesa-verde /
typewriter-cream). Two minor findings, both fixed in this branch:

1. minor: validator did not enforce unique descriptions. Fixed: duplicate
   descriptions now fail (the contract requires unique descriptions).
2. minor: catalog blocks were not associated with their `### N. name`
   headings. Fixed: the validator now maps each heading to its YAML block
   and requires heading set == skin set plus per-heading byte parity.

Follow-up mutations (duplicate description, swapped catalog blocks, renamed
heading with intact block) all fail; the clean tree passes.

### Confirmation review, round 3 (1 minor, fixed)

The round-2 confirmation reviewer found one more minor gap: stray extra
yaml blocks in the catalog were not rejected. Fixed: the validator now also
requires the total yaml-block count to equal the skin count. Mutation test
(appended stray block) fails; clean tree passes.

## 2026-08-02 — v1.0.0: public readiness

Reconstructed from git history.

- `chore: trim public repo to skins, README, VERSION, and catalog` (PR #6)
- `chore: restore cover image in README` (PR #7)
- `docs: add MIT license` (PR #8)

## 2026-08-02 — pack packaging

- `feat: package 50 Hermes skins` (PR #5): VERSION file and
  `hermes_50_skins_pack.md` catalog with all 50 full YAML blocks.

## 2026-08-01 — repo hygiene

- `chore: ignore private assets and Zone.Identifier junk` (PR #4)

## 2026-07-31 — initial 50-skin release

- `Add 50 Hermes CLI/TUI subscriber skin themes`
- `Add README with install guide and skin catalog`
- License-section wording and capitalization fixes
- `Add cover image to README` (PR #3)
