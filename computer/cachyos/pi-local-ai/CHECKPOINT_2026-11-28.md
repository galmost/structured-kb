# Checkpoint: 2026-11-28

## Hardware
- AMD Custom APU 0932/0405 (Sephiroth), 8 cores (4C/8T)
- 14GB RAM (9.6GB available)
- 912GB free disk
- CachyOS Linux

## Tools Installed
| Tool | Version | Path |
|------|---------|------|
| hf CLI | hf_hub/2.4.0 | /usr/bin/hf |
| llama.cpp | b12757 | ~/.local/bin/llama.cpp/ |
| Strata | 0.2.22 | ~/.local/bin/strata |
| pipx | 1.19.1 | ~/.local/bin/pipx |
| @caveman-ai/cli | 4.2.0 | via npx |

## HF Auth
- User: Galmost90
- Token: OAuth in ~/.cache/huggingface/token
- Commands used: `hf auth whoami`, `hf models list REPO -R`, `hf download REPO FILE --local-dir DIR --max-workers 4`

## Models Downloaded (40GB total)
| Model | File | Size | Gen t/s | Use |
|-------|------|------|---------|-----|
| Qwen3.5-4B | Qwen3.5-4B-UD-IQ2_XXS.gguf | 1.5GB | **7.0** | Speed |
| gemma-4-E4B | gemma-4-E4B-it-UD-IQ3_XXS.gguf | 3.5GB | 5.2 | Daily/pi |
| Qwen2.5-Coder-7B | Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf | 4.4GB | 5.3 | Coding |
| gemma-4-12b | gemma-4-12b-it-UD-IQ3_XXS.gguf | 4.4GB | 2.1 | Quality |
| Qwen3.5-9B | Qwen3.5-9B-Q4_K_S.gguf | 5.1GB | 4.3 | Quality |
| Inkling-2-Mini | Inkling-2-Mini-UD-IQ3_XXS.gguf | 11GB | 3.0 | Vision |
| Qwen3.8-27B | Qwen3.8-27B-UD-IQ3_XXS.gguf | 11GB | 0.3 | Avoid (swap) |

## Benchmarks (llama.cpp b12757, --ctx-size 4096 --threads 4 -ngl 0)
| Model | Prompt t/s | Gen t/s |
|-------|-----------|---------|
| Qwen2.5-Coder-7B | 14.3 | 5.3 |
| gemma-4-E4B | 11.6 | 5.2 |
| Qwen3.5-9B | 7.8 | 4.3 |
| Qwen3.5-4B | 6.9 | 7.0 |
| Inkling-2-Mini | 2.7 | 3.0 |
| gemma-4-12b | 2.7 | 2.1 |
| Qwen3.8-27B | 0.8 | 0.3 |

## Working Commands
```bash
# CLI chat
llama cli -m ~/.pi/research/models/qwen3.5-4b/Qwen3.5-4B-UD-IQ2_XXS.gguf --ctx-size 8192 --threads 4 -ngl 0

# Server for pi
llama serve -m ~/.pi/research/models/gemma-4-e4b/gemma-4-E4B-it-UD-IQ3_XXS.gguf --ctx-size 8192 --threads 4 -ngl 0 --port 9931 --jinja

# API test
curl http://127.0.0.1:9931/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model":"gemma-4-e4b","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'

# HF download
hf download unsloth/Qwen3.5-4B-GGUF Qwen3.5-4B-UD-IQ2_XXS.gguf --local-dir ~/.pi/research/models/qwen3.5-4b --max-workers 4
```

## Pi Config
```json
// ~/.pi/config.json
{
  "providers": {
    "llama-cpp": {
      "baseUrl": "http://localhost:9931/v1",
      "api": "openai-completions",
      "apiKey": "none",
      "models": [{ "id": "gemma-4-e4b" }]
    }
  }
}
```

## Avalon Tweaks (from structured-kb)
- `--jinja` for tool calls
- `-c 65536` max ctx, keep compact threshold below
- `--parallel 1` serialize
- thinking: low/medium/xhigh only

## Docs
```
research/
├── CHECKPOINT_2026-11-28.md     ← this file
├── README.md
├── SUMMARY.md
├── ASSESSMENT.md
├── SETUP_GUIDE.md
├── TABLES_AND_TWEAKS.md
├── HF_CLI_REFERENCE.md          ← hf CLI usage
├── HUGGINGFACE_CLI_GUIDE.md
├── MODEL_RECOMMENDATIONS_AMD_7900XT.md
├── HARDWARE_DOCS/
│   ├── STEAM_DECK.md
│   ├── STEAM_DECK_BENCHMARKS.md ← real results
│   └── AMD_7900_XT.md
├── scripts/
│   ├── download_model.py
│   └── download_steamdeck_models.sh
└── youtube-transcripts/kaiexplainsYT/2026-11/  ← 10 transcripts
```

## Pi Local Models (DONE)

- Convention `local-<model>-<quant>` in `~/.pi/agent/models.json` — 8 providers
- Systemd units `~/.config/systemd/user/local-*.service` — only `local-gemma-4-e4b-iq3xxs` enabled at boot (14GB RAM: run one at a time)
- Caveman compat mounts updated, `recovery_via_mcp: True`
- All 7 tested with pong sequentially: all respond
- Docs: `research/PI_LOCAL_MODELS.md`

## Caveman CLI + Pi + Systemd (DONE)

- `npx @caveman-ai/cli@latest setup --yes` — installed, wired pi
- Binary: `~/.caveman/cli/bin/caveman`
- Extension: `~/.pi/agent/extensions/caveman-native.js`
- Proxy: `caveman-proxy.service` on :8787 (enabled, systemd)
- Compat mounts: `~/.caveman/caveman.yaml` maps providers → llama.cpp ports
- SSRF fix: `CAVE_SSRF_ALLOWLIST` in service env (blocks 127.0.0.0/8 otherwise)
- Verified: `curl :8787/compat/local-gemma-e4b/v1/chat/completions` → "Pong!"
- Systemd: `llama-gemma-e4b` (9931), `llama-qwen-coder` (9932), `llama-qwen35-4b` (9933), `caveman-proxy` (8787)
- Pi providers: `local-gemma-e4b`, `local-qwen-coder`, `local-qwen35-4b` in `~/.pi/agent/models.json`
- Docs: `research/CAVEMAN_CLI_SETUP.md`

```bash
export PATH="$HOME/.caveman/cli/bin:$PATH"
caveman pi --provider local-gemma-e4b --model gemma-4-e4b
systemctl --user status caveman-proxy llama-gemma-e4b
```

## Next Steps
1. Test Qwen3.5-0.8B/2B for max speed
2. Benchmark larger ctx (8192, 16384)
3. Test --jinja tool calling with pi
4. caveman login for cloud routing
