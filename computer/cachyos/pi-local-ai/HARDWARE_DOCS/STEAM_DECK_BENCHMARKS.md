# Steam Deck Benchmarks: Real Results

**Hardware**: AMD Custom APU 0932/0405 (Sephiroth), 8 cores (4C/8T), 14GB RAM, CachyOS
**Engine**: llama.cpp b12757 (CPU mode, `-ngl 0`)
**Settings**: `--ctx-size 4096 --threads 4 -ngl 0`

---

## Results Table

| Model | File | Size | Prompt t/s | Gen t/s | Status | Notes |
|-------|------|------|-----------|---------|--------|-------|
| **Qwen3.5-4B** | Qwen3.5-4B-UD-IQ2_XXS.gguf | 1.5GB | 6.9 | **7.0** | ✅ Fastest | Best speed |
| **Qwen2.5-Coder-7B** | Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf | 4.4GB | **14.3** | 5.3 | ✅ Best prompt | Coding tasks |
| **gemma-4-E4B** | gemma-4-E4B-it-UD-IQ3_XXS.gguf | 3.5GB | 11.6 | 5.2 | ✅ Best all-round | Daily driver |
| **Qwen3.5-9B** | Qwen3.5-9B-Q4_K_S.gguf | 5.1GB | 7.8 | 4.3 | ✅ Good | Better quality than 4B |
| **Inkling-2-Mini** | Inkling-2-Mini-UD-IQ3_XXS.gguf | 11GB | 2.7 | 3.0 | ✅ Vision | Tight fit |
| **gemma-4-12b** | gemma-4-12b-it-UD-IQ3_XXS.gguf | 4.4GB | 2.7 | 2.1 | ✅ OK | Slower, better quality |
| **Qwen3.8-27B** | Qwen3.8-27B-UD-IQ3_XXS.gguf | 11GB | 0.8 | 0.3 | ⚠️ Slow | Barely fits, swap risk |

---

## Server Test

```bash
# Start server
llama serve -m gemma-4-E4B-it-UD-IQ3_XXS.gguf --ctx-size 4096 --threads 4 -ngl 0 --port 9931

# API call works
curl http://127.0.0.1:9931/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma-4-e4b","messages":[{"role":"user","content":"Say hi"}],"max_tokens":10}'
```

**Result**: `Hello there friend` — API works.

---

## Pi Integration

```bash
# Server
llama serve -m ~/.pi/research/models/gemma-4-e4b/gemma-4-E4B-it-UD-IQ3_XXS.gguf --ctx-size 8192 --threads 4 -ngl 0 --port 9931 --jinja
```

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

---

## Recommendations

| Use Case | Model | Gen t/s | Why |
|----------|-------|---------|-----|
| **Fastest gen** | Qwen3.5-4B | 7.0 | 1.5GB, fits easily |
| **Coding** | Qwen2.5-Coder-7B | 5.3 | 14.3 prompt t/s, code-tuned |
| **Daily chat / pi** | gemma-4-E4B | 5.2 | 11.6 prompt, balanced |
| **Better quality** | Qwen3.5-9B | 4.3 | 5.1GB, smarter than 4B |
| Vision | Inkling-2-Mini | 3.0 | 11GB tight, images |
| Avoid | Qwen3.8-27B | 0.3 | Swap risk |

---

## Commands

```bash
# Fastest generation
llama cli -m ~/.pi/research/models/qwen3.5-4b/Qwen3.5-4B-UD-IQ2_XXS.gguf --ctx-size 8192 --threads 4 -ngl 0

# Coding (best prompt speed)
llama cli -m ~/.pi/research/models/qwen2.5-coder-7b/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf --ctx-size 8192 --threads 4 -ngl 0

# Server for pi (daily driver)
llama serve -m ~/.pi/research/models/gemma-4-e4b/gemma-4-E4B-it-UD-IQ3_XXS.gguf --ctx-size 8192 --threads 4 -ngl 0 --port 9931 --jinja
```
