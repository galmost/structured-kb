# Caveman CLI + Local Models Setup

**Date**: 2026-11-28
**Version**: @caveman-ai/cli 4.2.0

---

## Caveman CLI Install

```bash
# One-time setup (downloads binaries, wires pi)
npx @caveman-ai/cli@latest setup --yes

# Result:
# - ~/.caveman/cli/bin/caveman (add to PATH)
# - ~/.caveman/cloud.json (modules config)
# - ~/.pi/agent/extensions/caveman-native.js (pi extension)
# - caveman-proxy running (local runtime)
```

**PATH**: `export PATH="$HOME/.caveman/cli/bin:$PATH"`

## Caveman Commands

| Command | Purpose |
|---------|---------|
| `caveman pi` | Run pi with caveman layer |
| `caveman status` | Show module status |
| `caveman tools` | Local tools (compress, toon, mem, etc.) |
| `caveman login` | Cloud account (optional, for routing) |
| `caveman run -- <cmd>` | Wrap any command |

**Modules on**: output, input, waste-fixes, routing, scripts, browse

---

## Systemd Services

Created in `~/.config/systemd/user/`:

| Service | Port | Model | Use |
|---------|------|-------|-----|
| `llama-gemma-e4b.service` | 9931 | gemma-4-E4B | ✅ Enabled, daily driver |
| `llama-qwen-coder.service` | 9932 | Qwen2.5-Coder-7B | Coding |
| `llama-qwen35-4b.service` | 9933 | Qwen3.5-4B | Fastest gen |

**Commands**:
```bash
systemctl --user daemon-reload
systemctl --user enable llama-gemma-e4b.service
systemctl --user start llama-gemma-e4b.service
systemctl --user status llama-gemma-e4b.service
journalctl --user -u llama-gemma-e4b.service -f

# Switch models (Conflicts auto-stops others)
systemctl --user start llama-qwen-coder.service   # stops gemma-e4b
systemctl --user start llama-gemma-e4b.service    # back to gemma
```

**Service flags** (from structured-kb avalon):
- `--jinja` — tool calling
- `--parallel 1` — serialize, less RAM
- `--ctx-size 8192` — context
- `-ngl 0` — CPU only (Steam Deck)

---

## Pi Integration

`~/.pi/agent/models.json`:
```json
{
  "providers": {
    "local-gemma-e4b": {
      "baseUrl": "http://127.0.0.1:9931/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [{ "id": "gemma-4-e4b", "name": "gemma-4-e4b", "contextWindow": 8192, "maxTokens": 4096 }]
    },
    "local-qwen-coder": {
      "baseUrl": "http://127.0.0.1:9932/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [{ "id": "qwen2.5-coder-7b", "name": "qwen2.5-coder-7b", "contextWindow": 8192, "maxTokens": 4096 }]
    },
    "local-qwen35-4b": {
      "baseUrl": "http://127.0.0.1:9933/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [{ "id": "qwen3.5-4b", "name": "qwen3.5-4b", "contextWindow": 8192, "maxTokens": 4096 }]
    }
  }
}
```

**Use in pi**: `pi --provider local-gemma-e4b --model gemma-4-e4b`

---

## Compat Mounts (Fix Pass-Through Warning)

Pi warned: `no compat mount named "local-gemma-e4b" in the local proxy`. Fix:

`~/.caveman/caveman.yaml`:
```yaml
mode: compress
compat:
  local-gemma-e4b:
    base_url: http://127.0.0.1:9931/v1
  local-qwen-coder:
    base_url: http://127.0.0.1:9932/v1
  local-qwen35-4b:
    base_url: http://127.0.0.1:9933/v1
  terminal-bench-local:
    base_url: http://127.0.0.1:8082/v1
```

**SSRF guard blocks 127.0.0.0/8**. Must set:
```bash
CAVE_SSRF_ALLOWLIST="127.0.0.1:9931,127.0.0.1:9932,127.0.0.1:9933,127.0.0.1:8082,localhost"
```

**Recovery env required** — raw `caveman-proxy serve` publishes `recovery_via_mcp: false`, pi then warns "direct mode, no compression". Service must set:
```
CAVEMAN_RECOVERY=mcp
CAVEMAN_PROXY_OWNER=wrap
CAVEMAN_MODE=compress
CAVEMAN_LISTEN=127.0.0.1:8787
```
Verify: `python3 -c "import json; print(json.load(open('~/.caveman/run/8787.json'))['recovery_via_mcp'])"` → `True`

**Local-only routing**: compat mounts exist only for local providers. Non-local providers (mistral etc.) pass through direct with a one-time warning — use normal skills for those. Pi default set to `local-gemma-e4b/gemma-4-e4b` in `~/.pi/agent/settings.json` so sessions start on a routed local model.

**Suppress mistral warning**: reverted — user accepts the warning. Do not patch the generated extension.

**Provider naming**: all local pi providers use `local-<model>-<quant>` (see `research/PI_LOCAL_MODELS.md`). Compat mounts in `caveman.yaml` match these names.

**Proxy as systemd service**: `~/.config/systemd/user/caveman-proxy.service` (enabled, running).

**Test through proxy**:
```bash
curl http://127.0.0.1:8787/compat/local-gemma-e4b/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma-4-e4b","messages":[{"role":"user","content":"Say pong"}],"max_tokens":5}'
# -> "Pong!"
```

Flow: `pi → caveman-proxy :8787/compat/<provider>/v1 → llama.cpp :9931`

---

## Test

```bash
# Service running
systemctl --user status llama-gemma-e4b.service

# API test
curl -s http://127.0.0.1:9931/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma-4-e4b","messages":[{"role":"user","content":"Say pong"}],"max_tokens":5}'
# -> "Pong!"

# Caveman + pi
caveman pi --provider local-gemma-e4b --model gemma-4-e4b
```

---

## Caveman with Local Model

Caveman proxy wraps provider traffic. Point it at local:
```bash
# Set pi provider to caveman proxy, proxy routes to local llama.cpp
# Or use caveman-native extension (already wired)
caveman pi
```
