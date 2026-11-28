# caveman-compress on pi

Compress memory files (AGENTS.md, todos) into caveman format. Part of [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). On this host: Mistral `mistral-large-latest`, effort low.

## 1. Layout

- Skill: `~/.agents/skills/caveman-compress/` (installed with [main setup](../README.md))
- Run: `/caveman-compress <filepath>` in pi
- Backups: `$XDG_DATA_HOME/caveman-compress/backups/<dir>-<hash>/<file>.original.md`

## 2. Provider config (Mistral, no secret on disk)

`~/.config/environment.d/caveman-compress.conf`:

```bash
CAVEMAN_COMPRESS_PROVIDER=openai-compat
CAVEMAN_COMPRESS_ENDPOINT=https://api.mistral.ai/v1
CAVEMAN_COMPRESS_MODEL=mistral-large-latest
CAVEMAN_COMPRESS_REASONING_EFFORT=low
```

Key from `~/.zshrc` reading `~/.pi/agent/auth.json`. Never on disk. Re-login: `pi auth login mistral --api-key`.

## 3. Mistral Patches

Required in `scripts/compress.py`:
- `reasoning_effort` top-level (Mistral rejects `chat_template_kwargs`, HTTP 422)
- `choices[0].message.content` list → join to string

## 4. Why Not Local Servers

- Avalon 88 GiB: OOM on 30 GiB RAM
- qwen-coder-7b: fails marker validation on KB files

## 5. Workflow

```bash
/caveman-compress /abs/path/FILE.md
# edit: restore, edit, re-compress
cp "$XDG_DATA_HOME/caveman-compress/backups/<dir>/FILE.original.md" /abs/path/FILE.md
$EDITOR /abs/path/FILE.md
rm "$XDG_DATA_HOME/caveman-compress/backups/<dir>/FILE.original.md"
/caveman-compress /abs/path/FILE.md
```

Validation fail → original untouched, re-run.

## 6. Boundaries

- Files: .md, .txt, .typ, .tex, extensionless
- Never .env/credentials — refused before read
- Code, URLs, paths, commands, dates: verbatim
- Full text sent to provider — see `SECURITY.md` in skill dir

## Source

- [JuliusBrussee/caveman-compress](https://github.com/JuliusBrussee/caveman/tree/main/skills/caveman-compress)
- [Pi Caveman Setup](../README.md)
- [Mistral note](../../../../debian/ai/mistral/README.md)
