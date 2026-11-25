# Mistral Vibe with local Avalon model (Debian 13)

Run Mistral Vibe (CLI) on local OpenAI server. Here use [Avalon](../amd/avalon/README.md) `llama-server` at `http://127.0.0.1:8080` not hosted Mistral API. Vibe use custom providers with any OpenAI `api_base`.

Need: server running (`sg render -c 'avalon-server -c 65536'`). See Avalon note.

## 1. Backup and edit `~/.vibe/config.toml`

```bash
cp ~/.vibe/config.toml ~/.vibe/config.toml.bak
```

Add model in `models = [ ... ]` array. No second `[[models]]` block. Mixing `models = [...]` and `[[models]]` bad TOML:

```toml
models = [
    { thinking = "high", alias = "mistral-medium-3.5" },
    { name = "Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf", provider = "avalon", alias = "avalon" },
]
```

Add provider at file end:

```toml
[[providers]]
name = "avalon"
api_base = "http://127.0.0.1:8080/v1"
api_key_env_var = ""
```

- `name` must match model id from `curl http://127.0.0.1:8080/v1/models`.
- `api_key_env_var = ""` — llama-server ignore auth.

Check file parses:

```bash
python3 -c 'import tomllib; tomllib.load(open("/home/galmost/.vibe/config.toml","rb")); print("TOML OK")'
```

## 2. Use it

```bash
vibe --model avalon -p 'Reply with exactly: pong'   # one-shot
```

Or interactive: `/model avalon`, then `/reload` if config edit while running. Work: prints `pong`.

## 3. Caveats

- No vision: do not set `supports_images = true`. `@image.png` no work.
- Background helpers (titles, smart-approve) hit active model if no small hosted model. Pin them to hosted alias to keep cheap:

```toml
[utility_models]
title = "mistral-medium-3.5"
```

- Server must be up before first request. Vibe not start it.
- Context: `-c 65536` make window 64k. Vibe get compaction threshold from it.

## Troubleshooting

- `connection refused` — server not running: `sg render -c 'avalon-server -c 65536'`.
- Model not in `/model` list — alias missing from `models` array, or TOML invalid (run tomllib check). Misspelt key only warning unless `strict_config = true`.
- Wrong model answers — `name` not match `/v1/models` output. Fix string.
- Restore hosted-only: `cp ~/.vibe/config.toml.bak ~/.vibe/config.toml`.
- `Error: Jinja Exception: Unexpected reasoning effort high. Supported types are xhigh (default), medium, and low.` — model entry has `thinking = "high"` (Vibe keep thinking level when switch models). Avalon template only accept `xhigh`, `medium`, `low`. Remove `thinking` from `[[models]]` or set to one of those.

## Source

- [Mistral Vibe — providers/models config](https://docs.mistral.ai/vibe/code/overview)
- [Avalon note in this repo](../amd/avalon/README.md)