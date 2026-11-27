# Caveman mode for pi (Linux, any distro)

Portable install of [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — makes the pi coding agent speak caveman, cutting ~75% of output tokens while keeping full technical accuracy. Works on any distro with pi installed; no host-specific dependencies, no API keys beyond pi's own auth. This note's path mirrors the pi skill path (`~/.pi/agent/skills/caveman/`).

Provides both:

- **Skill** `caveman` — auto-triggers on "caveman mode", "talk like caveman", "use caveman", "less tokens", "be brief"; force with `/skill:caveman`.
- **Modes** — `/caveman` (standard), `/caveman ultra` (maximum compression), `/caveman wenyan` (Classical Chinese), `/megacave` (alias for wenyan).

Code blocks, technical terms, error messages and commands stay verbatim — only prose compresses.

## 1. Prerequisites

- pi installed and authenticated (see distro pi note, e.g. `computer/debian/ai/pi/README.md`).

## 2. Install

### Option A: Manual Skills Installation (Recommended)

```bash
# Clone JuliusBrussee/caveman
mkdir -p ~/.pi/agent/skills/caveman-source
cd ~/.pi/agent/skills/caveman-source
git clone https://github.com/JuliusBrussee/caveman.git .

# Copy skills to agents skills directory
mkdir -p ~/.agents/skills
cp -r skills/caveman ~/.agents/skills/caveman-caveman
cp -r skills/ultracave ~/.agents/skills/caveman-ultracave
cp -r skills/megacave ~/.agents/skills/caveman-megacave
cp -r skills/caveman-compress ~/.agents/skills/caveman-compress

# Clean up
rm -rf ~/.pi/agent/skills/caveman-source

# Add to Pi settings
nano ~/.pi/agent/settings.json
```

Add `~/.agents/skills` to `skills` array:

```json
{
  "skills": [
    "~/.agents/skills"
  ]
}
```

Then reload: `/reload`

### Option B: Legacy v2nic Package (Fallback)

If manual installation fails, use the v2nic package as fallback:

```bash
pi install git:github.com/v2nic/pi-caveman
pi list          # shows: git:github.com/v2nic/pi-caveman
```

This clones the package into `~/.pi/agent/git/github.com/v2nic/pi-caveman/` and adds it to `packages` in `~/.pi/agent/settings.json`. Skills/extensions from the package are discovered automatically; restart pi or `/reload` after install.

Temporary try without installing: `pi -e ~/.pi/agent/git/github.com/v2nic/pi-caveman/extensions/caveman`.

## 3. Use

```bash
# interactive pi session:
/caveman                 # toggle caveman mode
/caveman ultra           # maximum compression
/caveman wenyan          # Classical Chinese mode
/skill:caveman           # force-load the skill
# or just say: "caveman mode" / "less tokens" — auto-triggers
```

## 4. Verify

```bash
# For manual skills installation:
ls ~/.agents/skills/caveman-caveman/SKILL.md
ls ~/.agents/skills/caveman-ultracave/SKILL.md
ls ~/.agents/skills/caveman-megacave/SKILL.md
ls ~/.agents/skills/caveman-compress/SKILL.md

# For v2nic package installation:
pi list | grep pi-caveman
ls ~/.pi/agent/git/github.com/v2nic/pi-caveman/skills/caveman/SKILL.md
```

In a session, ask pi to explain something with caveman mode on — reply should be terse fragments with exact technical terms and untouched code blocks.

## Troubleshooting

- Skill/extension not visible after install — restart pi or run `/reload`; skills path must be in `~/.pi/agent/settings.json` under `skills`.
- Want memory-file compression via `/caveman-compress`? That is the separate skill from JuliusBrussee/caveman — included in manual installation above.
- Issues with v2nic package — see [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) for fallback-specific issues.

## Source

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (primary)
- [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) (legacy fallback)
- [Pi docs — Skills](https://pi.dev/docs/latest/skills)
- Inspired by original [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
