# caveman-compress on pi (Debian 13)

Port of the Vibe `caveman-compress` skill to the pi coding agent, configured to
compress with **Mistral `mistral-large-latest`, reasoning effort low**. Compresses
natural-language memory files (AGENTS.md, README notes, todos) into caveman-speak
to cut input tokens; the human-readable original is backed up out-of-tree.

Related: [pi harness note](../pi/README.md), [pi user-skills note](../pi/README-skills.md).

## 1. Layout

- Skill: `~/.pi/agent/skills/caveman-compress/` (`SKILL.md`, `README.md`,
  `SECURITY.md`, `scripts/`), copied from `~/.vibe/skills/caveman-compress/`
  with the trigger rewritten `/caveman-compress` → `/skill:caveman-compress`.
- Run from the skill dir: `python3 -m scripts <absolute_filepath>`
  (or `/skill:caveman-compress <filepath>` in an interactive pi session).
- Backups: `$XDG_DATA_HOME/caveman-compress/backups/<parent-dir>-<hash>/<file>.original.md`
  — never beside the source file, so skill auto-loaders don't re-ingest them.

## 2. Provider config (Mistral, no secret on disk)

`~/.config/environment.d/caveman-compress.conf` (tracked in home_config):

```bash
CAVEMAN_COMPRESS_PROVIDER=openai-compat
CAVEMAN_COMPRESS_ENDPOINT=https://api.mistral.ai/v1
CAVEMAN_COMPRESS_MODEL=mistral-large-latest
CAVEMAN_COMPRESS_REASONING_EFFORT=low
```

`~/.zshrc` exports `CAVEMAN_COMPRESS_API_KEY` at shell start by reading
`mistral.key` from `~/.pi/agent/auth.json` (the same credential pi uses), so the
key is never persisted in a tracked file. Re-login with
`pi auth login mistral --api-key` if the key goes stale.

## 3. Local patches to `scripts/compress.py`

Required for the Mistral endpoint; without them the call fails:

- `reasoning_effort` is sent as a top-level body field for
  `api.mistral.ai` — Mistral rejects `chat_template_kwargs` with HTTP 422
  `extra_forbidden`. Other endpoints keep `chat_template_kwargs`.
- `choices[0].message.content` may be a list of typed segments on Mistral;
  they are joined into a single string before validation.

## 4. Why not the local servers

- Avalon (Qwen3.8-Flash-Next, 88.3 GiB) on 30 GiB RAM: OOM-kills when a
  compression prompt is processed, even at `-c 8192`; empty responses at
  small context. Also note: background servers started without `setsid`
  die with the launching shell — use
  `sg render -c 'setsid nohup avalon-server -c 65536 </dev/null >/tmp/avalon-server.log 2>&1 &'`,
  then wait for `/v1/models` to return `"object":"list"` (503 while loading).
- qwen-coder-7b on 8081 answers but fails marker validation
  (`@@CAVEMAN_PRESERVED_CODE_...@@` altered) on KB-sized files.

## 5. Workflow

```bash
# compress
cd ~/.pi/agent/skills/caveman-compress && python3 -m scripts /abs/path/FILE.md
# edit: restore, edit, re-compress (skill refuses while a backup exists)
cp "$XDG_DATA_HOME/caveman-compress/backups/<dir>/FILE.original.md" /abs/path/FILE.md
$EDITOR /abs/path/FILE.md
rm "$XDG_DATA_HOME/caveman-compress/backups/<dir>/FILE.original.md"
cd ~/.pi/agent/skills/caveman-compress && python3 -m scripts /abs/path/FILE.md
```

Validation failures (lost inline code, altered preserved markers) leave the
original untouched — just re-run. Compressed on this host so far:
`computer/debian/ai/pi/README.md` and `README-skills.md` (branch
`docs/pi-caveman-skill`).

## 6. Boundaries (from the upstream skill)

- Only natural-language files: .md, .txt, .typ, .typst, .tex, extensionless.
- Never .env/credentials-looking names — refused before reading.
- Code blocks, inline code, URLs, paths, commands, env vars, dates: verbatim.
- The file's full text leaves the machine to the configured provider
  (here: Mistral) — see `SECURITY.md` in the skill dir.

## Source

- Upstream Vibe skill: `~/.vibe/skills/caveman-compress/`
- [pi user-skills note](../pi/README-skills.md)
- [Mistral note](../mistral/README.md)
- Mistral API: https://docs.mistral.ai/api/
