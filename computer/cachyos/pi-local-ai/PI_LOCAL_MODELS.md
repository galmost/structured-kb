# Pi Local Models: Naming Convention + Services

**Convention**: `local-<model_name>-<quant>` for both provider and model id.

## models.json providers

| Provider / Model ID | Port | File | Gen t/s | Service | Boot |
|---------------------|------|------|---------|---------|------|
| local-gemma-4-e4b-iq3xxs | 9931 | gemma-4-E4B-it-UD-IQ3_XXS.gguf (3.5GB) | 5.2 | ✅ enabled | yes |
| local-qwen3-5-4b-iq2xxs | 9933 | Qwen3.5-4B-UD-IQ2_XXS.gguf (1.5GB) | 7.0 | on-demand | no |
| local-qwen2-5-coder-7b-q4km | 9932 | Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf (4.4GB) | 5.3 | on-demand | no |
| local-gemma-4-12b-iq3xxs | 9934 | gemma-4-12b-it-UD-IQ3_XXS.gguf (4.4GB) | 2.1 | on-demand | no |
| local-qwen3-5-9b-q4ks | 9935 | Qwen3.5-9B-Q4_K_S.gguf (5.1GB) | 4.3 | on-demand | no |
| local-inkling-2-mini-iq3xxs | 9936 | Inkling-2-Mini-UD-IQ3_XXS.gguf (11GB) | 3.0 | on-demand | no |
| local-qwen3-8-27b-iq3xxs | 9937 | Qwen3.8-27B-UD-IQ3_XXS.gguf (11GB) | 0.3 | on-demand | no |

**Context**: gemma-4-E4B native `context_length` = 131072 (128k). Service runs `--ctx-size 32768` (safe on 14GB RAM, KV fits). Bump to 65536/131072 if free RAM >8GB; watch `free -h`.
| local-qwen2-5-coder-7b-q4km | 9932 | Qwen2.5-Coder-7B Q4_K_M (4.4GB) | 5.3 | on-demand | no |
| local-qwen3-5-4b-iq2xxs | 9933 | Qwen3.5-4B UD-IQ2_XXS (1.5GB) | 7.0 | on-demand | no |
| local-gemma-4-12b-iq3xxs | 9934 | gemma-4-12b UD-IQ3_XXS (4.4GB) | 2.1 | on-demand | no |
| local-qwen3-5-9b-q4ks | 9935 | Qwen3.5-9B Q4_K_S (5.1GB) | 4.3 | on-demand | no |
| local-inkling-2-mini-iq3xxs | 9936 | Inkling-2-Mini UD-IQ3_XXS (11GB) | 3.0 | on-demand | no |
| local-qwen3-8-27b-iq3xxs | 9937 | Qwen3.8-27B UD-IQ3_XXS (11GB) | 0.3 | on-demand | no |
| local-qwen3-4b-q4km | 8082 | Qwen3-4B-TerminalBench Q4_K_M | — | external | no |

## Usage

```bash
# Boot default (already enabled)
systemctl --user start local-gemma-4-e4b-iq3xxs

# One at a time (14GB RAM limit)
systemctl --user stop local-*.service
systemctl --user start local-qwen2-5-coder-7b-q4km

# In pi
pi                                          # default: local-gemma-4-e4b-iq3xxs
pi --provider local-qwen2-5-coder-7b-q4km   # coding
pi --provider local-qwen3-5-4b-iq2xxs       # fastest
```

## Caveman routing

`~/.caveman/caveman.yaml` compat mounts map each `local-*` provider to its port. Proxy on :8787. Verified: all mounts present, `recovery_via_mcp: True`.

```bash
curl http://127.0.0.1:8787/compat/local-gemma-4-e4b-iq3xxs/v1/chat/completions ...
```

## Pong test results (2026-11-28)

All 7 services started and answered (sequentially, one at a time). Thinking models (qwen3.5, gemma-12b, inkling) emit reasoning before answer — use `max_tokens: 40` in tests.

## Files

- `~/.pi/agent/models.json` — 8 local-* providers
- `~/.pi/agent/settings.json` — default `local-gemma-4-e4b-iq3xxs`
- `~/.config/systemd/user/local-*.service` — 8 units
- `~/.caveman/caveman.yaml` — compat mounts
