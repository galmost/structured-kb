# Pi Skills (Debian 13)

User skills for the [pi coding agent](README.md) live in the agent directory's
`skills/` folder: `~/.pi/agent/skills/<name>/SKILL.md` (override the agent
directory with `PI_CODING_AGENT_DIR`). Pi advertises each skill by name and
description at startup and loads the full `SKILL.md` only when a task matches;
force one with `/skill:<name>` and pick up edits with `/reload`. Project
alternative: `.pi/skills/` in a trusted repo.

This host installs two skills, both ported from the Vibe harness copies under
`~/.vibe/skills/` with command references changed from `/caveman...` to
`/skill:caveman...`:

| skill | dir | what it does |
|---|---|---|
| `caveman` | `~/.pi/agent/skills/caveman/` | terse output voice, stays on until "stop caveman" / "normal mode" |
| `caveman-compress` | `~/.pi/agent/skills/caveman-compress/` | compresses natural-language memory files (AGENTS.md, todos) to save input tokens |

`~/AGENTS.md` loads `caveman` at the start of every run.

## 1. Prerequisites

- pi installed and configured — see [README.md](README.md) (sections 1–4).
- For `caveman-compress`: Python 3 (stdlib only for the `openai-compat`
  provider) and a reachable model endpoint. On this host use the local Avalon
  server: `CAVEMAN_COMPRESS_PROVIDER=openai-compat` with
  `CAVEMAN_COMPRESS_ENDPOINT=http://127.0.0.1:8080/v1` (avalon-server must be
  running, see [Avalon note](../amd/avalon/README.md)). Other providers
  (`claude` CLI, Anthropic API, `opencode`) work as in the upstream skill —
  see `SECURITY.md` in the skill dir.

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

`caveman-compress` bundles `scripts/` (`python3 -m scripts <file>` run from
the skill dir); it sends the file's full text to the configured provider, so
never point it at secret-looking files (`.env`, credentials) — those are
refused before reading. Backups go to
`$XDG_DATA_HOME/caveman-compress/backups/<parent-dir-name>-<hash>/`, not
beside the source file.

## 3. Configure the compress provider (local Avalon)

```bash
export CAVEMAN_COMPRESS_PROVIDER=openai-compat
export CAVEMAN_COMPRESS_ENDPOINT=http://127.0.0.1:8080/v1
# optional: export CAVEMAN_COMPRESS_MODEL=<model id from /v1/models>
```

Put the exports in `~/.config/environment.d/` so they apply to every shell.

## 4. Track the skills in home_config

`~` is default-deny; extend the `.pi` allowlist in `~/.gitignore` (see
README.md section 6):

```bash
# ~/.gitignore
!.pi/agent/skills/
!.pi/agent/skills/**
```

`git status` in `~` then shows the skill files; `auth.json` and sessions stay
ignored. Verify: `git check-ignore -v ~/.pi/agent/auth.json` still matches
the `*` rule.

## 5. Verify

```bash
ls ~/.pi/agent/skills/caveman/SKILL.md ~/.pi/agent/skills/caveman-compress/SKILL.md
pi -p 'Say exactly: pong' --no-session        # skills listed in startup diagnostics
# interactive: /skill:caveman                  -> terse replies until "stop caveman"
# interactive: /skill:caveman-compress ~/git/structured-kb/AGENTS.md
```

## Troubleshooting

- Skill not listed at pi startup — wrong directory: must be
  `~/.pi/agent/skills/<name>/SKILL.md`, not `~/.pi/agent/skills/<name>.md`
  alone; run `/reload` after moving it.
- `caveman-compress` fails with connection refused — Avalon not running:
  `sg render -c 'avalon-server -c 65536'`, then retry.
- `caveman-compress` refuses the file — extension not in the natural-language
  allowlist (.md, .txt, .typ, .tex, extensionless) or name looks like a
  secret; compress a different file.
- Backup already exists for the file — restore from
  `$XDG_DATA_HOME/caveman-compress/backups/...` first; the skill refuses to
  re-compress an already-compressed file.

## Source

- [Pi docs — Skills](https://pi.dev/docs/latest/skills)
- [Pi docs — Configuration (agent dir layout)](https://pi.dev/docs/latest/configuration)
- Upstream Vibe skill copies: `~/.vibe/skills/caveman/`, `~/.vibe/skills/caveman-compress/`
- [Pi harness note in this repo](README.md)
- [Avalon note in this repo](../amd/avalon/README.md)
