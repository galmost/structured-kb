# Terminus-2 workspace setup (Debian 13)

`~/git/terminus-2` is terminus-2 workspace. Run Mistral Vibe with hosted Mistral API plus local llama.cpp servers (Avalon on `http://127.0.0.1:8080/v1`, see [amd/avalon](../amd/avalon/README.md), local models in [mistral](../mistral/README.md)). Project config vanilla: `.vibe/config.toml` all comments, so Vibe inherits `~/.vibe/config.toml` per key (project TOML wins over user TOML for keys it sets; project layer loads only when folder trusted).

## 1. Create the repo

```bash
mkdir -p ~/git/terminus-2 && cd ~/git/terminus-2 && git init -b main
```

Conventions (branches from `main` with `feature/|fix/|docs/|refactor/` prefixes, Conventional Commits) follow repo `AGENTS.md`, restated in project `AGENTS.md`.

## 2. Keep the project config vanilla

`.vibe/config.toml` in project root only comments. Tweaks ship as commented blocks there, documented one per section in repo `docs/tweaks.md` — uncomment one at a time:

```toml
# active_model = "qwen3.8-flash-next-avalon"   # current global alias for the Avalon model
```

## 3. Trust the folder

Persisted in `~/.vibe/trusted_folders.toml`:

```toml
trusted = ["/home/galmost/git/terminus-2"]
untrusted = []
```

Interactive sessions prompt trust unknown folders; `-p` mode never trusts — pass `--trust` for one-off trusted run.

## 4. Verify

Avalon server must be up first (see the [Avalon note](../amd/avalon/README.md)):

```bash
sg render -c 'avalon-server -c 65536'
cd ~/git/terminus-2
curl -fsS http://127.0.0.1:8080/v1/models
vibe --trust -p 'Reply with exactly: pong'                                     # global active model → pong
vibe --trust --model mistral-large-4-0-3 -p 'Reply with exactly: pong'         # hosted mistral → pong
vibe --trust --model qwen3.8-flash-next-avalon -p 'Reply with exactly: pong'   # local avalon → pong
```

All verified Debian 13 (GArk) 2026-11-20: each printed `pong` (avalon one when server warm; under load first inference page-ins 89 GiB mmap and TTFT can exceed minutes). Aliases come from global `~/.vibe/config.toml` and can change — if one unknown, startup error lists available ones.

## 5. Benchmark instead of bloating config

Repo ships `bench/bench.sh`, streaming TTFT/tok-s probe (not wired into anything), and `docs/benchmarks.md` with baselines. Compare tweak before keeping it:

```bash
cd ~/git/terminus-2
bench/bench.sh avalon http://127.0.0.1:8080/v1 Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf 512 128
BENCH_API_KEY="$MISTRAL_API_KEY" bench/bench.sh mistral https://api.mistral.ai/v1 mistral-large-4-0-3 512 128
```

Full setup record and re-validation checklist live in repo: `docs/setup.md`, `docs/validation-todo.md`.

## Troubleshooting

- `Unknown model: <alias>` — aliases live in `~/.vibe/config.toml`; read "Available:" list from any `vibe -p` error or `/model` and update docs.
- Project config ignored — folder not trusted for that run; `-p` needs `--trust`, check `~/.vibe/trusted_folders.toml`.
- `connection refused` on :8080 — restart: `sg render -c 'avalon-server -c 65536'` (plain `nohup` process, no supervisor).
- `thinking = "high"` on Avalon model breaks chat template — use `low`/`medium`/`xhigh` (see the [mistral note](../mistral/README.md)).

## Source

- [mistral — Vibe with local models](../mistral/README.md)
- [amd/avalon — Avalon install/run](../amd/avalon/README.md)
- Mistral Vibe docs: config layers, trusted folders, `--trust` (`vibe --help`)