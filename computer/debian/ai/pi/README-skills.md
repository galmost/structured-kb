# Pi Skills (Debian 13)

User skills for [pi coding agent](README.md) live in `skills/` folder: `~/.pi/agent/skills/<name>/SKILL.md` (override with `PI_CODING_AGENT_DIR`). Pi shows skill name/description at startup, loads full `SKILL.md` only when task matches. Force with `/skill:<name>`, pick up edits with `/reload`. Project alt: `.pi/skills/` in trusted repo.

For the `caveman` voice skill on **any** pi install, prefer the portable package — see [../../../linux/ai/pi/pi-caveman/](../../../linux/ai/pi/pi-caveman/README.md) (`pi install git:github.com/v2nic/pi-caveman`, provides `/caveman` + `/skill:caveman`). The manual Vibe-port below is only needed for `caveman-compress` on this host.

Host installs two skills, ported from Vibe copies under `~/.vibe/skills/`, commands changed from `/caveman...` to `/skill:caveman...`:

| skill | dir | what it does |
|---|---|---|
| `caveman` | `~/.pi/agent/skills/caveman/` | terse voice, on until "stop caveman" / "normal mode" |
| `caveman-compress` | `~/.pi/agent/skills/caveman-compress/` | compress memory files (AGENTS.md, todos) save tokens |

`~/AGENTS.md` loads `caveman` every run.

## 1. Prerequisites

- pi installed/configured — see [README.md](README.md) (sections 1–4).
- `caveman-compress`: Python 3 (stdlib only for the `openai-compat` provider) + Mistral API key (same as pi, from `~/.pi/agent/auth.json` — section 3). Other providers (`claude` CLI, Anthropic API, `opencode`, local) work upstream — see `SECURITY.md` in skill dir.

## 2. Install

```bash
mkdir -p ~/.pi/agent/skills
cp -r ~/.vibe/skills/caveman ~/.pi/agent/skills/caveman
cp -r ~/.vibe/skills/caveman-compress ~/.pi/agent/skills/caveman-compress
rm -rf ~/.pi/agent/skills/caveman-compress/scripts/__pycache__
# in each SKILL.md, rewrite the trigger command for pi:
sed -i 's|/caveman-compress|/skill:caveman-compress|g; s|/caveman|/skill:caveman|g' \
  ~/.pi/agent/skills/caveman/SKILL.md ~/.pi/agent/skills/caveman-compress/SKILL.md
```

`caveman-compress` bundles `scripts/` (`python3 -m scripts <file>` from skill dir); sends full file text to provider. Never point at secret files (`.env`, credentials) — refused before reading. Backups to `$XDG_DATA_HOME/caveman-compress/backups/<parent-dir-name>-<hash>/`, not beside source.

## 3. Configure the compress provider (Mistral large-latest, low effort)

`~/.config/environment.d/caveman-compress.conf` (tracked home_config, no secrets) sets non-secret vars:

```bash
CAVEMAN_COMPRESS_PROVIDER=openai-compat
CAVEMAN_COMPRESS_ENDPOINT=https://api.mistral.ai/v1
CAVEMAN_COMPRESS_MODEL=mistral-large-latest
CAVEMAN_COMPRESS_REASONING_EFFORT=low
```

API key never on disk: `~/.zshrc` exports `CAVEMAN_COMPRESS_API_KEY` reading `mistral.key` from `~/.pi/agent/auth.json` at shell start. `scripts/compress.py` patched for Mistral: `reasoning_effort` top-level (Mistral rejects `chat_template_kwargs` HTTP 422), list `content` joined. Local servers (Avalon 8080, qwen-coder 8081) work, but 88 GiB Avalon OOMs on 30 GiB RAM, 7B coder fails marker check. Mistral reliable default.

## 4. Track the skills in home_config

`~` default-deny; extend `.pi` allowlist in `~/.gitignore` (see README.md section 6):

```bash
# ~/.gitignore
!.pi/agent/skills/
!.pi/agent/skills/**
```

`git status` in `~` shows skill files; `auth.json`/sessions ignored. Verify: `git check-ignore -v ~/.pi/agent/auth.json` matches `*` rule.

## 5. Verify

```bash
ls ~/.pi/agent/skills/caveman/SKILL.md ~/.pi/agent/skills/caveman-compress/SKILL.md
pi -p 'Say exactly: pong' --no-session        # skills listed in startup diagnostics
# interactive: /skill:caveman                  -> terse replies until "stop caveman"
# interactive: /skill:caveman-compress ~/git/structured-kb/AGENTS.md
```

## Troubleshooting

- Not listed at startup — wrong dir: must be `~/.pi/agent/skills/<name>/SKILL.md`, not `~/.pi/agent/skills/<name>.md`; run `/reload` after move.
- `caveman-compress` HTTP 401 — `CAVEMAN_COMPRESS_API_KEY` empty: new shell (key from `~/.zshrc`/`~/.pi/agent/auth.json`) or `pi auth login mistral --api-key`.
- `caveman-compress` HTTP 422 `chat_template_kwargs` — Mistral patch missing in `scripts/compress.py`; re-copy skill dir.
- `caveman-compress` refuses file — extension not in allowlist (.md, .txt, .typ, .tex, extensionless) or name looks secret; pick different file.
- Backup exists — restore from `$XDG_DATA_HOME/caveman-compress/backups/...` first; skill refuses re-compress of compressed file.

## Source

- [Pi docs — Skills](https://pi.dev/docs/latest/skills)
- [Pi docs — Configuration (agent dir layout)](https://pi.dev/docs/latest/configuration)
- Upstream Vibe skill copies: `~/.vibe/skills/caveman/`, `~/.vibe/skills/caveman-compress/`
- [Pi harness note in this repo](README.md)
- [Avalon note in this repo](../amd/avalon/README.md)
- [Mistral note in this repo](../mistral/README.md)