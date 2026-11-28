# Pi Caveman Setup (JuliusBrussee/caveman)

Set up JuliusBrussee/caveman for ultra-compressed responses in Pi coding agent.

## 1. Prerequisites

- Pi coding agent installed (see [Pi Coding Agent Setup for Linux](../) or [Arch-specific guide](../../arch/pi/))
- Node.js 22.13+ (for caveman CLI tools, optional)
- Git

## 2. Install JuliusBrussee/caveman Skills

### Option A: Manual Skills Installation (Recommended)

Clone JuliusBrussee/caveman repository and extract skills:

```bash
# Clone repo
mkdir -p ~/.pi/agent/skills/caveman-source
cd ~/.pi/agent/skills/caveman-source
git clone https://github.com/JuliusBrussee/caveman.git .

# Copy skills to agents skills directory (Pi auto-discovers from ~/.agents/skills/)
mkdir -p ~/.agents/skills
cp -r skills/caveman ~/.agents/skills/caveman-caveman
cp -r skills/ultracave ~/.agents/skills/caveman-ultracave
cp -r skills/megacave ~/.agents/skills/caveman-megacave
cp -r skills/caveman-compress ~/.agents/skills/caveman-compress

# Clean up
rm -rf ~/.pi/agent/skills/caveman-source
```

### Option B: Legacy v2nic Package (Fallback)

If manual installation fails, use the v2nic package as fallback:

```bash
pi install git:github.com/v2nic/pi-caveman
pi list          # shows: git:github.com/v2nic/pi-caveman
```

This clones the package into `~/.pi/agent/git/github.com/v2nic/pi-caveman/` and adds it to `packages` in `~/.pi/agent/settings.json`. Skills/extensions from the package are discovered automatically; restart pi or `/reload` after install.

Temporary try without installing: `pi -e ~/.pi/agent/git/github.com/v2nic/pi-caveman/extensions/caveman`.

## 3. Configure Pi Settings

Add skills directory to Pi settings:

```bash
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

## 4. Reload Pi

```bash
/reload
```

## 5. Verify

Test caveman modes:

```
/caveman
/caveman ultra
/caveman wenyan
/caveman-compress <file>
/caveman status
/stop caveman
```

For v2nic package installation:
```bash
pi list | grep pi-caveman
ls ~/.pi/agent/git/github.com/v2nic/pi-caveman/skills/caveman/SKILL.md
```

## 6. Commands Reference

| Command | Description |
|---|---|
| `/caveman` | Activate standard caveman mode |
| `/ultracave` or `/caveman ultra` | Maximum compression, telegraphic |
| `/megacave` or `/caveman wenyan` | Classical Chinese mode |
| `/caveman-compress <file>` | Compress memory files with backup |
| `/caveman status` | Report current mode |
| `/stop caveman` or `/normal mode` | Deactivate caveman mode |

## 7. Compression Levels

| Mode | Description | Token Reduction |
|------|-------------|-----------------|
| caveman | Standard: drop articles, filler, fragments ok | 30-45% |
| ultracave | Maximum: telegraphic, fragments | 40-60% |
| megacave | Classical Chinese: 文言文 | 30-50% |

## 8. Rules Summary

### Always Remove
- Articles: a, an, the
- Filler: just, really, basically, actually, simply
- Pleasantries: sure, certainly, of course, happy to
- Hedging: might, could, perhaps, maybe, possibly
- Connectives: because, therefore, however

### Always Keep
- Technical terms (exact)
- Numbers and quantifiers
- Names, titles
- Negations: not, never, no, only, except
- Code blocks, commands, paths, errors (verbatim)

### Formatting
- Answer first, then reason, then next step
- Pattern: `[thing] [action] [reason]. [next step].`
- One idea per sentence
- 20 words max per sentence
- Active voice
- Imperative for instructions

## 9. When to Break Rules

Use full sentences for:
- Security warnings
- Irreversible actions
- Step order that fragments could scramble
- Confused users
- Anything persisted outside chat (code, commits, docs)
- Questions to user

## 10. Troubleshooting

- Skill not visible after install — restart pi or run `/reload`; skills path must be in `~/.pi/agent/settings.json` under `skills`.
- Issues with v2nic package — see [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) for fallback-specific issues.

## See Also

- [caveman-compress](./compress/) - Compress memory files
- [Pi Caveman CLI Integration Assessment](./cli/) - Assessment of using `@caveman-ai/cli` with Pi

## Source

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (primary)
- [v2nic/pi-caveman](https://github.com/v2nic/pi-caveman) (legacy fallback)
- [Pi Coding Agent](https://github.com/earendil-works/pi-coding-agent)
