#!/usr/bin/env python3
"""Deterministic validator for the hermes-skins-pack release tree.

Stdlib-only. Verifies:
  1. exactly 101 YAML files under skins/
  2. unique filenames and unique top-level `name` values, name == filename stem
  3. every skin defines the exact same 43-key color set as the canonical schema
  4. exact top-level structure with no missing, duplicate, or unsupported keys
  5. every color value is a quoted six-digit hex string (#rrggbb)
  6. every skin name appears in README.md and hermes_101_skins_pack.md
  7. every YAML block embedded in the catalog matches its source file byte-for-byte
  8. readability gates: primary text, label, accent, and semantic colors keep
     minimum contrast against the skin background; status bar text against its bg

Exit code 0 with a summary on success, 1 with a failure list otherwise.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKINS_DIR = os.path.join(ROOT, "skins")
README = os.path.join(ROOT, "README.md")
CATALOG = os.path.join(ROOT, "hermes_101_skins_pack.md")
EXPECTED_COUNT = 101

EXPECTED_TOP_LEVEL = ("name", "description", "colors", "branding", "tool_prefix")
EXPECTED_BRANDING = ("prompt_symbol",)

# Canonical 43-key color schema, pinned from the v1 pack (skins/obsidian.yaml).
EXPECTED_KEYS = (
    "background", "banner_border", "banner_title", "banner_accent", "banner_dim",
    "banner_text", "ui_accent", "ui_label", "ui_text", "ui_border", "ui_ok",
    "ui_error", "ui_warn", "ui_tool", "ui_thinking", "diff_added", "diff_removed",
    "diff_added_word", "diff_removed_word", "syntax_string", "syntax_number",
    "syntax_keyword", "syntax_comment", "prompt", "shell_dollar", "input_rule",
    "response_border", "session_label", "session_border", "status_bar_bg",
    "status_bar_text", "status_bar_strong", "status_bar_dim", "status_bar_good",
    "status_bar_warn", "status_bar_bad", "status_bar_critical", "voice_status_bg",
    "selection_bg", "completion_menu_bg", "completion_menu_current_bg",
    "completion_menu_meta_bg", "completion_menu_meta_current_bg",
)

# Palette-distinctness gate: average per-channel RGB distance over the 11 most
# visible colors. The existing pack's closest pair measures 16 (steel-thread /
# slate-mist), so 15 rejects anything weaker than the pack's own floor.
DISTINCT_KEYS = (
    "background", "ui_text", "ui_accent", "ui_label", "ui_ok", "ui_error",
    "ui_warn", "ui_tool", "syntax_string", "syntax_number", "syntax_keyword",
)
MIN_PALETTE_DISTANCE = 15.0

HEX_RE = re.compile(r'^  ([a-z_]+): "(#[0-9a-f]{6})"$', re.M)
TOP_RE = re.compile(r"^([a-z_]+):", re.M)

# Minimum contrast ratios (WCAG-style) against the skin background.
# banner_dim / syntax_comment / ui_thinking are intentionally faint and exempt.
# Semantic floor is 2.9: the existing pack's measured minimum is 2.99
# (deep-void ui_error); new skins are authored at >= 3.5.
CONTRAST_GATES = {
    "ui_text": 7.0,
    "banner_text": 7.0,
    "prompt": 7.0,
    "ui_label": 4.5,
    "ui_accent": 3.0,
    "ui_ok": 2.9,
    "ui_error": 2.9,
    "ui_warn": 2.9,
    "ui_tool": 2.9,
    "status_bar_text": 4.0,  # measured against status_bar_bg
}


def luminance(hexcolor):
    chans = [int(hexcolor[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    chans = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in chans]
    return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def parse_skin(path, errors):
    text = open(path, encoding="utf-8").read()
    stem = os.path.basename(path)[:-5]

    top_keys = TOP_RE.findall(text)
    if tuple(top_keys) != EXPECTED_TOP_LEVEL:
        errors.append(f"{stem}: top-level structure differs from pack schema "
                      f"(expected={list(EXPECTED_TOP_LEVEL)} actual={top_keys})")

    m = re.search(r"^name: (.+)$", text, re.M)
    if not m:
        errors.append(f"{stem}: missing name")
        return None, None, text, None
    name = m.group(1).strip()
    if name != stem:
        errors.append(f"{stem}: name '{name}' does not match filename")

    desc_m = re.search(r"^description: (\S.{9,})$", text, re.M)
    if not desc_m:
        errors.append(f"{stem}: missing or too-short description")
    description = desc_m.group(1).strip() if desc_m else None
    if description and " #" in description and not (
        description.startswith('"') and description.endswith('"')
    ):
        errors.append(f"{stem}: description containing # must be double quoted")

    branding_text = text.split("branding:")[-1] if "branding:" in text else ""
    branding_keys = tuple(re.findall(r"^  ([a-z_]+):", branding_text, re.M))
    if branding_keys != EXPECTED_BRANDING:
        errors.append(f"{stem}: branding structure differs from pack schema "
                      f"(expected={list(EXPECTED_BRANDING)} actual={list(branding_keys)})")
    if not re.search(r'^  prompt_symbol: ".+"$', text, re.M):
        errors.append(f"{stem}: missing branding.prompt_symbol")
    if not re.search(r'^tool_prefix: ".+"$', text, re.M):
        errors.append(f"{stem}: missing tool_prefix")

    colors_text = text.split("branding:")[0]
    pairs = HEX_RE.findall(colors_text)
    color_keys = [key for key, _ in pairs]
    if len(color_keys) != len(set(color_keys)):
        duplicates = sorted({key for key in color_keys if color_keys.count(key) > 1})
        errors.append(f"{stem}: duplicate color keys {duplicates}")
    colors = dict(pairs)

    # any color line that does not match the strict hex shape
    for line in colors_text.splitlines():
        if line.startswith("  ") and not line.startswith("   ") and ":" in line:
            if not HEX_RE.match(line):
                errors.append(f"{stem}: malformed color line: {line.strip()!r}")

    return name, colors, text, description


def main():
    errors = []
    paths = sorted(glob.glob(os.path.join(SKINS_DIR, "*.yaml")))

    if len(paths) != EXPECTED_COUNT:
        errors.append(f"expected {EXPECTED_COUNT} skin files, found {len(paths)}")

    stems = [os.path.basename(p) for p in paths]
    if len(set(stems)) != len(stems):
        errors.append("duplicate filenames detected")

    skins = {}
    descriptions = {}
    for path in paths:
        name, colors, text, description = parse_skin(path, errors)
        if name is None or colors is None:
            continue
        if name in skins:
            errors.append(f"duplicate top-level name '{name}'")
        skins[name] = (colors, text)
        if description is not None:
            if description in descriptions:
                errors.append(f"{name}: description duplicates "
                              f"'{descriptions[description]}'")
            descriptions[description] = name
        keyset = tuple(colors.keys())
        if keyset != EXPECTED_KEYS:
            missing = set(EXPECTED_KEYS) - set(keyset)
            extra = set(keyset) - set(EXPECTED_KEYS)
            errors.append(f"{name}: key set differs from schema "
                          f"(missing={sorted(missing)} extra={sorted(extra)})")

    # palette distinctness across the whole pack
    def rgb(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

    def channel_dist(a, b):
        return sum((x - y) ** 2 for x, y in zip(rgb(a), rgb(b))) ** 0.5

    names_sorted = sorted(n for n in skins
                          if tuple(skins[n][0].keys()) == EXPECTED_KEYS)
    for i, a in enumerate(names_sorted):
        for b in names_sorted[i + 1:]:
            avg = sum(channel_dist(skins[a][0][k], skins[b][0][k])
                      for k in DISTINCT_KEYS) / len(DISTINCT_KEYS)
            if avg < MIN_PALETTE_DISTANCE:
                errors.append(f"near-duplicate palettes: {a} / {b} "
                              f"(avg distance {avg:.1f} < {MIN_PALETTE_DISTANCE})")

    # contrast gates
    for name, (colors, _) in sorted(skins.items()):
        bg = colors.get("background")
        if not bg:
            continue
        for key, minimum in CONTRAST_GATES.items():
            ref = colors["status_bar_bg"] if key == "status_bar_text" else bg
            fg = colors.get(key)
            if not fg:
                continue
            ratio = contrast(fg, ref)
            if ratio < minimum:
                errors.append(f"{name}: {key} contrast {ratio:.2f} below {minimum}")

    # README and catalog membership
    readme = open(README, encoding="utf-8").read()
    if not os.path.exists(CATALOG):
        errors.append("catalog hermes_101_skins_pack.md is missing")
        catalog = ""
    else:
        catalog = open(CATALOG, encoding="utf-8").read()

    for name in sorted(skins):
        if not re.search(rf"\b{re.escape(name)}\b", readme):
            errors.append(f"{name}: not listed in README.md")

    # catalog: every '### N. <name>' heading must carry the byte-for-byte
    # YAML of skins/<name>.yaml, and the heading set must equal the skin set
    sections = re.findall(r"^### \d+\. (\S+)\n.*?```yaml\n(.*?)```",
                          catalog, re.S | re.M)
    catalog_map = dict(sections)
    total_blocks = len(re.findall(r"```yaml\n", catalog))
    if total_blocks != EXPECTED_COUNT:
        errors.append(f"catalog contains {total_blocks} yaml blocks, "
                      f"expected {EXPECTED_COUNT} (stray or missing blocks)")
    if len(sections) != EXPECTED_COUNT:
        errors.append(f"catalog contains {len(sections)} skin sections, "
                      f"expected {EXPECTED_COUNT}")
    if set(catalog_map) != set(skins):
        errors.append(f"catalog headings differ from skins on disk "
                      f"(missing={sorted(set(skins) - set(catalog_map))} "
                      f"extra={sorted(set(catalog_map) - set(skins))})")
    for name, (_, text) in sorted(skins.items()):
        block = catalog_map.get(name)
        if block is None:
            errors.append(f"{name}: no catalog section")
        elif block != text:
            errors.append(f"{name}: catalog YAML block does not match "
                          f"skins/{name}.yaml")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"PASS — {len(paths)} skins, {len(EXPECTED_KEYS)}-key schema, "
          f"README + catalog complete, contrast + distinctness gates green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
