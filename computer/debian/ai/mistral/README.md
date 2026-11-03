# Mistral Vibe with local Avalon model (Debian 13)

Run Mistral Vibe (this CLI) against a local OpenAI-compatible server — here the
[Avalon](../amd/avalon/README.md) `llama-server` on `http://127.0.0.1:8080` —
instead of the hosted Mistral API. Vibe supports custom providers with any
OpenAI-compatible `api_base`.

Prerequisite: the server is running (`sg render -c 'avalon-server -c 65536'`,
see the Avalon note).

## 1. Backup and edit `~/.vibe/config.toml`

```bash
cp ~/.vibe/config.toml ~/.vibe/config.toml.bak
```

Add a model entry inside the existing `models = [ ... ]` array (do not add a
second `[[models]]` block — mixing `models = [...]` with `[[models]]` is invalid
TOML):

```toml
models = [
    { thinking = "high", alias = "mistral-medium-3.5" },
    { name = "Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf", provider = "avalon", alias = "avalon" },
]
```

Append the provider at the end of the file:

```toml
[[providers]]
name = "avalon"
api_base = "http://127.0.0.1:8080/v1"
api_key_env_var = ""
```

- `name` in the model must match the model id from `curl http://127.0.0.1:8080/v1/models`.
- `api_key_env_var = ""` — llama-server ignores authentication.

Validate the file parses:

```bash
python3 -c 'import tomllib; tomllib.load(open("/home/galmost/.vibe/config.toml","rb")); print("TOML OK")'
```

## 2. Use it

```bash
vibe --model avalon -p 'Reply with exactly: pong'   # one-shot
```

or in an interactive session: `/model avalon`, then `/reload` if config was
edited while running. Verified: prints `pong`.

## 3. Caveats

- No vision: do not set `supports_images = true`; `@image.png` mentions won't work.
- Background helpers (session titles, smart-approve) also hit the active model
  when no small hosted model is available — pin them to a hosted alias to keep
  them cheap:

```toml
[utility_models]
title = "mistral-medium-3.5"
```

- The server must be up before the first request; Vibe does not start it.
- Context: with `-c 65536` the model window is 64k — Vibe derives the compaction
  threshold from it.

## Troubleshooting

- `connection refused` — server not running: `sg render -c 'avalon-server -c 65536'`.
- Model not in `/model` list — alias missing from `models` array, or TOML invalid
  (run the tomllib check); a misspelt key is only a startup warning unless
  `strict_config = true`.
- Wrong model answers — `name` does not match `/v1/models` output; fix the string.
- Restore hosted-only setup: `cp ~/.vibe/config.toml.bak ~/.vibe/config.toml`.
- `Error: Jinja Exception: Unexpected reasoning effort high. Supported types are xhigh (default), medium, and low.`
  — the model entry has `thinking = "high"` (Vibe persists a thinking level when you
  switch models in-session). The Avalon chat template only accepts `xhigh`, `medium`,
  `low`. Remove `thinking` from the `[[models]]` entry, or set it to one of those.

## Source

- [Mistral Vibe — providers/models config](https://docs.mistral.ai/vibe/code/overview)
- [Avalon note in this repo](../amd/avalon/README.md)
