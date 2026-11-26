# Caveman mode for pi (Linux, any distro)

Portable install of [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) — makes the pi coding agent speak caveman, cutting ~75% of output tokens while keeping full technical accuracy. Works on any distro with pi installed; no host-specific dependencies, no API keys beyond pi's own auth. This note's path mirrors the pi skill path (`~/.pi/agent/skills/caveman/`).

Provides both:

- **Skill** `caveman` — auto-triggers on "caveman mode", "talk like caveman", "use caveman", "less tokens", "be brief"; force with `/skill:caveman`.
- **Extension** — `/caveman` toggle with levels: `/caveman lite` (drop filler, keep grammar), `/caveman full` (default), `/caveman ultra` (telegraphic).

Code blocks, technical terms, error messages and commands stay verbatim — only prose compresses.

## 1. Prerequisites

- pi installed and authenticated (see distro pi note, e.g. `computer/debian/ai/pi/README.md`).
- `gh` CLI authenticated (used only if you install via git URL; the package source is public GitHub so a plain clone also works).

## 2. Install

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
/skill:caveman           # force-load the skill
# or just say: "caveman mode" / "less tokens" — auto-triggers
```

## 4. Verify

```bash
pi list | grep pi-caveman
ls ~/.pi/agent/git/github.com/v2nic/pi-caveman/skills/caveman/SKILL.md
```

In a session, ask pi to explain something with caveman mode on — reply should be terse fragments with exact technical terms and untouched code blocks.

## Troubleshooting

- Skill/extension not visible after install — restart pi or run `/reload`; package must be listed in `~/.pi/agent/settings.json` under `packages`.
- `pi install` fails to clone — network/auth: repo is public, use `git clone https://github.com/v2nic/pi-caveman` fallback and `pi install <local-path>`.
- Want the old behavior (memory-file compression via `/caveman-compress`)? That is the separate Vibe-ported skill, host-specific — see `computer/debian/ai/caveman-compress/README.md` and `computer/debian/ai/pi/README-skills.md`.

## Source

- https://github.com/v2nic/pi-caveman
- https://pi.dev/docs/latest/skills
- Inspired by https://github.com/JuliusBrussee/caveman
