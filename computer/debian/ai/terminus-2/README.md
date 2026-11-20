# Terminus-2 workspace setup (Debian 13)

`~/git/terminus-2` is a dedicated project workspace for terminus-2, run with
Mistral Vibe against the hosted Mistral API plus local llama.cpp servers
(Avalon on `http://127.0.0.1:8080/v1`, see
[amd/avalon](../amd/avalon/README.md), and the local models configured in
[mistral](../mistral/README.md)). The project config stays vanilla: its
`.vibe/config.toml` is all comments, so Vibe inherits `~/.vibe/config.toml`
per key (project TOML wins over user TOML for keys it sets; the project layer
only loads when the folder is trusted).

## 1. Create the repo

```bash
mkdir -p ~/git/terminus-2 && cd ~/git/terminus-2 && git init -b main
```

Conventions (branches from `main` with `feature/|fix/|docs/|refactor/`
prefixes, Conventional Commits) follow this repo's `AGENTS.md` and are
restated in the project's own `AGENTS.md`.

## 2. Keep the project config vanilla

`.vibe/config.toml` in the project root contains only comments. Tweaks ship
as commented blocks there and are documented one per section in the repo's
`docs/tweaks.md` — uncomment one at a time:

```toml
# active_model = "qwen3.8-flash-next-avalon"   # current global alias for the Avalon model
```

## 3. Trust the folder

Persisted in `~/.vibe/trusted_folders.toml`:

```toml
trusted = ["/home/galmost/git/terminus-2"]
untrusted = []
```

Interactive sessions prompt to trust unknown folders; `-p` mode never
trusts — pass `--trust` for a one-off trusted run.

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

All verified on Debian 13 (GArk) 2026-11-20: each printed `pong` (the avalon
one when the server was warm; under load its first inference page-ins the
89 GiB mmap and TTFT can exceed minutes). Aliases come from the global
`~/.vibe/config.toml` and can change — if one is unknown, the startup error
lists the available ones.

## 5. Benchmark instead of bloating config

The repo ships `bench/bench.sh`, a streaming TTFT/tok-s probe (not wired
into anything), and `docs/benchmarks.md` with baselines. Compare a tweak
before keeping it:

```bash
cd ~/git/terminus-2
bench/bench.sh avalon http://127.0.0.1:8080/v1 Qwen3.8-Flash-Next-Avalon-IQ3KS-00001-of-00033.gguf 512 128
BENCH_API_KEY="$MISTRAL_API_KEY" bench/bench.sh mistral https://api.mistral.ai/v1 mistral-large-4-0-3 512 128
```

Full setup record and the re-validation checklist live in the repo:
`docs/setup.md`, `docs/validation-todo.md`.

## Troubleshooting

- `Unknown model: <alias>` — aliases live in `~/.vibe/config.toml`; read the
  "Available:" list from any `vibe -p` error or `/model` and update the docs.
- Project config ignored — folder not trusted for that run; `-p` needs
  `--trust`, check `~/.vibe/trusted_folders.toml`.
- `connection refused` on :8080 — restart: `sg render -c 'avalon-server -c 65536'`
  (plain `nohup` process, no supervisor).
- `thinking = "high"` on the Avalon model breaks its chat template — use
  `low`/`medium`/`xhigh` (see the [mistral note](../mistral/README.md)).

## Source

- [mistral — Vibe with local models](../mistral/README.md)
- [amd/avalon — Avalon install/run](../amd/avalon/README.md)
- Mistral Vibe docs: config layers, trusted folders, `--trust` (`vibe --help`)
