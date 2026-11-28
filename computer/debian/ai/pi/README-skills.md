# Pi Skills (Debian 13)

User skills for [pi coding agent](README.md) live at `~/.pi/agent/skills/<name>/SKILL.md` (override dir with `PI_CODING_AGENT_DIR`). Pi lists name/description at startup and loads `SKILL.md` when a task matches. Force with `/skill:<name>`, pick up edits with `/reload`. Project alternative: `.pi/skills/` in a trusted repo.

For the `caveman` voice skill on **any** pi install prefer the manual JuliusBrussee install — [../../../linux/pi/caveman/](../../../linux/pi/caveman/README.md).

| skill | what it does |
|---|---|
| `caveman` | terse voice, on until "stop caveman" / "normal mode" |
| `caveman-compress` | compress memory files (AGENTS.md, todos) to save tokens |

`~/AGENTS.md` loads `caveman` every run.

## 1. Prerequisites

- pi installed and configured — [README.md](README.md) sections 1–4.
- `caveman-compress`: Python 3 (stdlib only for the `openai-compat` provider) plus a Mistral API key, same as pi (`~/.pi/agent/auth.json`).

## 2. Install

### Option A: JuliusBrussee skills (recommended)

Clone `JuliusBrussee/caveman`, copy the `caveman` skill dirs into `~/.agents/skills/`, then point pi's `skills` setting at that dir. Full commands: [../../../linux/pi/caveman/](../../../linux/pi/caveman/README.md).

### Option B: legacy Vibe copies (fallback)

```bash
mkdir -p ~/.pi/agent/skills
cp -r ~/.vibe/skills/caveman ~/.pi/agent/skills/caveman
cp -r ~/.vibe/skills/caveman-compress ~/.pi/agent/skills/caveman-compress
rm -rf ~/.pi/agent/skills/caveman-compress/scripts/__pycache__
sed -i 's|/caveman-compress|/skill:caveman-compress|g; s|/caveman|/skill:caveman|g' \
  ~/.pi/agent/skills/caveman/SKILL.md ~/.pi/agent/skills/caveman-compress/SKILL.md
```

`caveman-compress` bundles `scripts/` (`python3 -m scripts <file>` from skill dir) and sends the whole file to the provider. Secret-looking files are refused before reading. Backups go to `$XDG_DATA_HOME/caveman-compress/backups/<parent-dir-name>-<hash>/`, not beside the source.

## 3. Compress provider (Mistral, no key on disk)

`~/.config/environment.d/caveman-compress.conf` (tracked, non-secret):

```bash
CAVEMAN_COMPRESS_PROVIDER=openai-compat
CAVEMAN_COMPRESS_ENDPOINT=https://api.mistral.ai/v1
CAVEMAN_COMPRESS_MODEL=mistral-large-latest
CAVEMAN_COMPRESS_REASONING_EFFORT=low
```

`~/.zshrc` exports `CAVEMAN_COMPRESS_API_KEY` read from `mistral.key` in `~/.pi/agent/auth.json` at shell start. Mistral needs `scripts/compress.py` patched: top-level `reasoning_effort` (rejects `chat_template_kwargs`, HTTP 422) and list `content` joined. Local servers work but underperform: Avalon (88 GiB) OOMs on 30 GiB RAM, 7B coder fails marker check.

## 4. Track skills in home_config

`~` is default-deny; extend the `.pi` allowlist in `~/.gitignore` ([README.md](README.md) section 5):

```bash
# ~/.gitignore
!.pi/agent/skills/
!.pi/agent/skills/**
```

`auth.json` and sessions stay ignored. Verify: `git check-ignore -v ~/.pi/agent/auth.json`.

## 5. Verify

```bash
ls ~/.agents/skills/caveman-caveman/SKILL.md ~/.agents/skills/caveman-compress/SKILL.md
pi -p 'Say exactly: pong' --no-session        # skills listed in startup diagnostics
# interactive: /skill:caveman  -> terse replies until "stop caveman"
```

## Troubleshooting

- Not listed at startup — wrong layout. Must be `<dir>/<name>/SKILL.md`, not `<dir>/<name>.md`; run `/reload`.
- HTTP 401 — `CAVEMAN_COMPRESS_API_KEY` empty: new shell, or `pi auth login mistral --api-key`.
- HTTP 422 `chat_template_kwargs` — Mistral patch missing in `scripts/compress.py`; re-copy skill dir.
- File refused — extension not allowed (.md, .txt, .typ, .tex, extensionless) or name looks secret.
- Backup exists — restore from `$XDG_DATA_HOME/caveman-compress/backups/...`; the skill refuses to re-compress an already compressed file.

## Source

- [Pi docs — Skills](https://pi.dev/docs/latest/skills)
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- [Pi harness note](README.md), [Avalon note](../amd/avalon/README.md)
