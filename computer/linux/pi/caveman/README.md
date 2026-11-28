# Pi Caveman Setup (JuliusBrussee/caveman)

Ultra-compressed responses for the Pi coding agent via [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) skills.

## 1. Prerequisites

- Pi installed — [Pi Coding Agent Setup for Linux](../) or [Arch-specific guide](../../arch/pi/README.md)
- Git. Node.js 22.13+ only for the optional CLI (see [cli/](cli/))

## 2. Install skills (recommended)

```bash
mkdir -p ~/.agents/skills ~/src/caveman
git clone https://github.com/JuliusBrussee/caveman.git ~/src/caveman
cp -r ~/src/caveman/skills/caveman        ~/.agents/skills/caveman-caveman
cp -r ~/src/caveman/skills/ultracave      ~/.agents/skills/caveman-ultracave
cp -r ~/src/caveman/skills/megacave       ~/.agents/skills/caveman-megacave
cp -r ~/src/caveman/skills/caveman-compress ~/.agents/skills/caveman-compress
```

Pi auto-discovers `~/.agents/skills/`. Alternatively point the `skills` array in `~/.pi/agent/settings.json` at the parent dir:

```json
{ "skills": ["~/.agents/skills"] }
```

### Fallback: legacy v2nic package

```bash
pi install git:github.com/v2nic/pi-caveman
pi list          # git:github.com/v2nic/pi-caveman
```

Clones into `~/.pi/agent/git/github.com/v2nic/pi-caveman/`, adds it to `packages` in `~/.pi/agent/settings.json`. `--reload` (or restart) after install. Try without installing: `pi -e ~/.pi/agent/git/github.com/v2nic/pi-caveman/extensions/caveman`.

## 3. Verify

```
/caveman
/caveman ultra
/caveman wenyan
/caveman-compress <file>
/caveman status
/stop caveman
```

Legacy install check: `ls ~/.pi/agent/git/github.com/v2nic/pi-caveman/skills/caveman/SKILL.md`.

## 4. Commands

| Command | Description |
|---|---|
| `/caveman` | Standard caveman mode |
| `/ultracave`, `/caveman ultra` | Maximum compression, telegraphic |
| `/megacave`, `/caveman wenyan` | Classical Chinese (文言文) |
| `/caveman-compress <file>` | Compress memory files with backup |
| `/caveman status` | Report current mode |
| `/stop caveman`, `/normal mode` | Deactivate |

Compression: caveman 30-45%, ultracave 40-60%, megacave 30-50%.

## 5. Rules

Compression levels:

| Mode | Description | Token reduction |
|------|-------------|-----------------|
| caveman | Standard: drop articles, filler, fragments ok | 30-45% |
| ultracave | Maximum: telegraphic, fragments | 40-60% |
| megacave | Classical Chinese: 文言文 | 30-50% |

Always remove: articles (a, an, the); filler (just, really, basically, actually, simply); pleasantries (sure, certainly, of course, happy to); hedging (might, could, perhaps, maybe, possibly); connectives (because, therefore, however).

Always keep: technical terms exact; numbers and quantifiers; names and titles; negations (not, never, no, only, except); code blocks, commands, paths and errors verbatim.

Format: answer first, then reason, then next step; one idea per sentence; ≤20 words; active voice; imperative for instructions.

Full sentences for: security warnings, irreversible actions, step order fragments could scramble, confused users, anything persisted outside chat (code, commits, docs), questions to the user.

## 6. Troubleshooting

- Skill not visible — restart pi or `/reload`; skills path must be in `~/.pi/agent/settings.json` under `skills`.
- v2nic-specific issues — see [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman).

## See Also

- [caveman-compress](compress/) — compress memory files
- [Pi Caveman CLI Integration Assessment](cli/) — `@caveman-ai/cli` with Pi

## Source

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (primary)
- [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) (legacy fallback)
- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
