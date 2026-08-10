# Hermes Skins Pack — 100 Themes

![Cover](hermes-cover.png)

A curated pack of **100 unique, drop-in skin themes** for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) CLI and TUI. Every skin is a complete YAML file using the real Hermes color keys — no inherited defaults, no silent fallbacks.

Every skin is a complete YAML file using Hermes skin keys. The pack can be installed for the default Hermes profile, for individual named profiles, or shared across all profiles while allowing each profile to use a different skin.

## What’s Inside

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

## How Hermes Profiles Affect Skins

A Hermes profile is a separate Hermes home directory. Each profile has its own configuration, sessions, memory, skills, state, and `skins` directory.

Typical locations are:

| Profile | Hermes home | Configuration file | Skin directory |
|---|---|---|---|
| Default | `~/.hermes` | `~/.hermes/config.yaml` | `~/.hermes/skins` |
| Named profile | `~/.hermes/profiles/PROFILE` | `~/.hermes/profiles/PROFILE/config.yaml` | `~/.hermes/profiles/PROFILE/skins` |

The selected default skin is stored in the profile’s own configuration:

```yaml
display:
  skin: neon-ghost
```

Because each profile has its own `config.yaml`, **different profiles can use different skins**.

---

## Clone the Repository

```bash
git clone https://github.com/bchop-studio/hermes-skins-pack.git
cd hermes-skins-pack
```

All commands in the following sections assume that your shell is currently in the cloned repository.

## Install for the Default Profile

```bash
mkdir -p "$HOME/.hermes/skins"
cp -i skins/*.yaml "$HOME/.hermes/skins/"
```

Set the default profile’s skin:

```bash
hermes -p default config set display.skin neon-ghost
```

Start a new Hermes CLI session to see the selected skin:

```bash
hermes -p default chat
```

Inside Hermes, you can also run:

```text
/skin
```

This shows the current skin and the skins available to that profile.

---

# Per-Profile Installation

There are two supported layouts:

1. **Independent copies** — copy all skin files into every profile.
2. **Shared catalog** — store one copy of the skin pack and symlink each profile’s `skins` directory to it.

The shared-catalog layout is usually easier to maintain.

## Option 1: Copy the Skins into Every Profile

First list your profiles:

```bash
hermes profile list
```

For example, to install the pack for profiles named `culinary`, `it_guy`, `personal`, and `travel`:

```bash
profiles=(culinary it_guy personal travel)

# Default profile
mkdir -p "$HOME/.hermes/skins"
cp -i skins/*.yaml "$HOME/.hermes/skins/"

# Named profiles
for profile in "${profiles[@]}"; do
  profile_home="$HOME/.hermes/profiles/$profile"

  if [[ ! -d "$profile_home" ]]; then
    printf 'Skipping missing profile: %s\n' "$profile"
    continue
  fi

  mkdir -p "$profile_home/skins"
  cp -i skins/*.yaml "$profile_home/skins/"
done
```

Each profile now has its own physical copy of the 50 YAML files.

### Assign Different Skins

Use the explicit `-p` form in scripts because it does not depend on profile aliases:

```bash
hermes -p default config set display.skin midnight-studio
hermes -p culinary config set display.skin warm-parchment
hermes -p it_guy config set display.skin netrunner
hermes -p personal config set display.skin aurora-boreal
hermes -p travel config set display.skin deep-ocean
```

Example assignment:

| Profile | Skin |
|---|---|
| Default | `midnight-studio` |
| `culinary` | `warm-parchment` |
| `it_guy` | `netrunner` |
| `personal` | `aurora-boreal` |
| `travel` | `deep-ocean` |

Replace the profile and skin names with your own choices.

---

## Option 2: Use One Shared Skin Catalog

This layout keeps one physical copy of the pack while every profile retains an independent `display.skin` selection.

### Step 1: Install the Pack into the Default Hermes Home

```bash
mkdir -p "$HOME/.hermes/skins"
cp -i skins/*.yaml "$HOME/.hermes/skins/"
```

### Step 2: Link Named Profiles to the Shared Directory

The following script safely backs up a profile’s existing real `skins` directory before creating the link:

```bash
profiles=(culinary it_guy personal travel)
shared_skins="$HOME/.hermes/skins"

for profile in "${profiles[@]}"; do
  profile_home="$HOME/.hermes/profiles/$profile"
  profile_skins="$profile_home/skins"

  if [[ ! -d "$profile_home" ]]; then
    printf 'Skipping missing profile: %s\n' "$profile"
    continue
  fi

  if [[ -L "$profile_skins" ]]; then
    rm "$profile_skins"
  elif [[ -d "$profile_skins" ]]; then
    backup="${profile_skins}.backup.$(date +%Y%m%d-%H%M%S)"
    mv "$profile_skins" "$backup"
    printf 'Backed up %s to %s\n' "$profile_skins" "$backup"
  elif [[ -e "$profile_skins" ]]; then
    printf 'Not replacing non-directory path: %s\n' "$profile_skins" >&2
    continue
  fi

  ln -s "$shared_skins" "$profile_skins"
  printf 'Linked %s -> %s\n' "$profile_skins" "$shared_skins"
done
```

### Step 3: Verify the Links

```bash
for profile in culinary it_guy personal travel; do
  ls -ld "$HOME/.hermes/profiles/$profile/skins"
done
```

Expected output will resemble:

```text
/Users/yourname/.hermes/profiles/culinary/skins -> /Users/yourname/.hermes/skins
```

### Step 4: Set a Different Skin for Each Profile

```bash
hermes -p default config set display.skin midnight-studio
hermes -p culinary config set display.skin warm-parchment
hermes -p it_guy config set display.skin netrunner
hermes -p personal config set display.skin aurora-boreal
hermes -p travel config set display.skin deep-ocean
```

The skin files are shared, but the selected skin remains profile-specific because the setting is saved in each profile’s own `config.yaml`.

### Shared-Catalog Tradeoffs

Advantages:

- Only one copy of each YAML file is stored.
- Updating the pack updates the skin catalog for every linked profile.
- Each profile can still select a different default skin.

Considerations:

- Deleting or renaming a shared skin affects every linked profile.
- Backups that intentionally exclude symlink targets may not include the shared YAML files.
- Copying a linked profile to another computer requires recreating the symlink or copying the skins into the profile.

---

# Working with Profile Aliases

When Hermes creates a named profile, it normally creates a command wrapper under:

```text
~/.local/bin/PROFILE_NAME
```

A profile command such as:

```bash
culinary config set display.skin warm-parchment
```

is a convenient wrapper for:

```bash
hermes -p culinary config set display.skin warm-parchment
```

## Create or Repair a Missing Alias

Confirm the exact profile name:

```bash
hermes profile list
```

Create or repair the alias:

```bash
hermes profile alias PROFILE_NAME
```

Example:

```bash
hermes profile alias travel
```

If your installed Hermes release supports a custom alias name, use:

```bash
hermes profile alias PROFILE_NAME --name ALIAS_NAME
```

Check the command syntax available in your installed version with:

```bash
hermes profile alias --help
```

## Verify the Alias

```bash
ls -l "$HOME/.local/bin/PROFILE_NAME"
```

Refresh the shell’s command cache:

```bash
rehash
```

Then test it:

```bash
PROFILE_NAME doctor
PROFILE_NAME config get display.skin
```

## Add `~/.local/bin` to `PATH`

If the wrapper exists but the shell reports `command not found`, check your path:

```bash
printf '%s\n' "$PATH" | tr ':' '\n' | grep -F "$HOME/.local/bin"
```

If no match is returned, add this to `~/.zshrc`:

```bash
printf '\nexport PATH="$HOME/.local/bin:$PATH"\n' >> "$HOME/.zshrc"
source "$HOME/.zshrc"
rehash
```

Aliases are optional. The explicit form always works and is preferable in automation:

```bash
hermes -p PROFILE_NAME config set display.skin SKIN_NAME
```

---

# Verify Per-Profile Skin Settings

Use `config get` for each profile:

```bash
printf 'default:   '
hermes -p default config get display.skin

printf 'culinary: '
hermes -p culinary config get display.skin

printf 'it_guy:   '
hermes -p it_guy config get display.skin

printf 'personal: '
hermes -p personal config get display.skin

printf 'travel:   '
hermes -p travel config get display.skin
```

You can also inspect the YAML directly:

```bash
printf '\n=== default ===\n'
grep -A5 '^display:' "$HOME/.hermes/config.yaml"

for profile in culinary it_guy personal travel; do
  printf '\n=== %s ===\n' "$profile"
  grep -A5 '^display:' "$HOME/.hermes/profiles/$profile/config.yaml"
done
```

Do not add a second `display:` block manually. If one already exists, add or update the `skin:` key inside that block. Using `hermes config set` avoids this problem.

## Verify That the Skin File Exists

For the default profile:

```bash
skin_name="$(hermes -p default config get display.skin)"
test -f "$HOME/.hermes/skins/$skin_name.yaml" \
  && echo "Found: $skin_name" \
  || echo "Missing: $HOME/.hermes/skins/$skin_name.yaml"
```

For a named profile:

```bash
profile="travel"
skin_name="$(hermes -p "$profile" config get display.skin)"
skin_file="$HOME/.hermes/profiles/$profile/skins/$skin_name.yaml"

test -f "$skin_file" \
  && echo "Found: $skin_file" \
  || echo "Missing: $skin_file"
```

---

# Test Each Profile

Start each profile in a separate new CLI session:

```bash
hermes -p default chat
hermes -p culinary chat
hermes -p it_guy chat
hermes -p personal chat
hermes -p travel chat
```

Or use aliases when available:

```bash
culinary chat
it_guy chat
personal chat
travel chat
```

Inside a session:

```text
/skin
```

Temporarily switch the current session:

```text
/skin neon-ghost
```

Set a persistent profile default from the shell:

```bash
hermes -p PROFILE_NAME config set display.skin SKIN_NAME
```

Depending on the Hermes version and interface, an already-running session may need to be restarted before a changed `display.skin` setting is visible.

---

# Install Only One Skin

Default profile:

```bash
mkdir -p "$HOME/.hermes/skins"
cp skins/neon-ghost.yaml "$HOME/.hermes/skins/"
hermes -p default config set display.skin neon-ghost
```

Named profile:

```bash
profile="travel"
skin="deep-ocean"
profile_home="$HOME/.hermes/profiles/$profile"

mkdir -p "$profile_home/skins"
cp "skins/$skin.yaml" "$profile_home/skins/"
hermes -p "$profile" config set display.skin "$skin"
```

---

# Update the Skin Pack

If the repository was cloned with Git:

```bash
cd /path/to/hermes-skins-pack
git pull --ff-only
```

For independent profile copies, copy the updated files again:

```bash
cp -i skins/*.yaml "$HOME/.hermes/skins/"

for profile in culinary it_guy personal travel; do
  cp -i skins/*.yaml "$HOME/.hermes/profiles/$profile/skins/"
done
```

For the shared-catalog layout, only update the central directory:

```bash
cp -i skins/*.yaml "$HOME/.hermes/skins/"
```

All linked profiles will immediately see the updated catalog.

---

# Troubleshooting

## Skin Does Not Appear in `/skin`

Confirm the YAML file is stored under the active profile’s `skins` directory:

```bash
hermes -p PROFILE_NAME config get display.skin
ls -1 "$HOME/.hermes/profiles/PROFILE_NAME/skins"
```

For the default profile:

```bash
hermes -p default config get display.skin
ls -1 "$HOME/.hermes/skins"
```

## Hermes Falls Back to Its Default Skin

Common causes include:

- The configured skin name does not match the YAML filename.
- The file was copied into the default profile but the named profile is active.
- The profile’s `skins` symlink is broken.
- The YAML file is malformed.
- The running session has not reloaded the changed configuration.

Check a symlink with:

```bash
ls -ld "$HOME/.hermes/profiles/PROFILE_NAME/skins"
readlink "$HOME/.hermes/profiles/PROFILE_NAME/skins"
```

## Wrong Profile Was Modified

Check the active sticky profile:

```bash
hermes profile
```

Use an explicit profile selector to avoid ambiguity:

```bash
hermes -p PROFILE_NAME config set display.skin SKIN_NAME
```

## Alias Is Missing

The profile itself can still be used without an alias:

```bash
hermes -p PROFILE_NAME doctor
```

Then repair the wrapper:

```bash
hermes profile alias PROFILE_NAME
rehash
```

## Alias Exists but Is Not Found

```bash
ls -l "$HOME/.local/bin/PROFILE_NAME"
echo "$PATH" | tr ':' '\n'
```

Ensure `~/.local/bin` is on `PATH` as described earlier.

---

# What Skins Change

Skins control visual presentation in supported Hermes CLI and TUI surfaces, including items such as:

- Banner and accent colors
- Prompt and response styling
- Spinner faces and verbs
- Branding text
- Tool-output prefixes
- Status and completion-menu colors supported by the installed Hermes version

Skins do **not** change:

- The selected model
- Agent instructions or personality
- Tools or MCP configuration
- Memory providers or memory banks
- Telegram, Discord, or other messaging-platform colors
- Profile isolation or permissions

Personality controls how the agent communicates. A skin controls how supported Hermes interfaces look.

---

# Repository Contents

- `skins/` — 50 ready-to-use YAML skin files
- `README.md` — installation, profile-specific setup, verification, and troubleshooting
- `VERSION` — current pack version
- `hermes_50_skins_pack.md` — browsable catalog with every full YAML block

Every skin defines a complete palette, including syntax colors and `shell_dollar`, so it does not silently depend on unrelated user customizations.

## License

MIT. See [`LICENSE`](LICENSE).

Made by [bchop-studio](https://github.com/bchop-studio)

Built for vibe coders who want their AI to feel less corporate.

If this helped, ⭐ the repository so others can find it.

