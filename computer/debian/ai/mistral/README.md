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

## 4. Project-scoped setup: terminus-2 (vanilla + opt-in tweaks)

`~/git/terminus-2` is a dedicated project repo that stays vanilla: its
`.vibe/config.toml` is all comments, so Vibe inherits `~/.vibe/config.toml`
per key (hosted mistral + local avalon are already defined there). Layers
merge per key — project TOML wins over user TOML for keys it sets — and the
project layer only loads when the folder is trusted.

```bash
mkdir -p ~/git/terminus-2 && cd ~/git/terminus-2 && git init -b main
# .vibe/config.toml: comments only (vanilla). Tweaks ship as commented
# blocks there and in docs/tweaks.md — uncomment one at a time.
```

Trust the folder (persistent) by adding it to `~/.vibe/trusted_folders.toml`:

```toml
trusted = ["/home/galmost/git/terminus-2"]
untrusted = []
```

Interactive sessions prompt to trust unknown folders; `-p` mode never
trusts — pass `--trust` for a one-off trusted run.

Verify both backends from the project root (Avalon server must be up — see
the Prerequisite in the intro):

```bash
cd ~/git/terminus-2
curl -fsS http://127.0.0.1:8080/v1/models
vibe --trust -p 'Reply with exactly: pong'                            # global active model → pong
vibe --trust --model qwen3.8-flash-next-avalon -p 'Reply with exactly: pong'   # local avalon → pong
```

Both verified on Debian 13 (GArk): each printed `pong`. Aliases come from
`~/.vibe/config.toml` and can change — if one is unknown, the startup error
lists the available ones.

Benchmark instead of bloating config: `bench/bench.sh` in the repo is a
streaming TTFT/tok-s probe (not wired into anything); baselines are recorded
in the repo's `docs/benchmarks.md`:

```bash
cd ~/git/terminus-2
bench/bench.sh avalon http://127.0.0.1:8080/v1 Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf 512 128
BENCH_API_KEY="$MISTRAL_API_KEY" bench/bench.sh mistral https://api.mistral.ai/v1 mistral-large-4-0-3 512 128
```

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
