# Local AI Model Recommendations: AMD RTX 7900 XT 24G

> Source: Kai Explains YT channel research (Nov 2026)  
> Hardware: AMD Radeon RX 7900 XT - 24GB GDDR6, 800 GB/s, RDNA 3

---

## Quick Picks

| Use Case | Best Model | Engine | Speed | VRAM Used | Notes |
|----------|------------|--------|-------|-----------|-------|
| **Coding Agent** | Qwen 3.8B Flash Next | Avalon | **91 tok/s** | ~20GB | Expert cache optimized |
| **General Reasoning** | Qwen 3.8 27B | Strata/llama.cpp | 45-60 tok/s | 16.8-19.5GB | Orca Router build |
| **Fast General** | Gemma 4 31B | Strata/llama.cpp | 50-70 tok/s | 18.7GB | Shorter thinking drafts |
| **Budget/Testing** | Gemma 4 12B | llama.cpp | 80-100 tok/s | 7.4GB | Fast, low VRAM |

---

## Detailed Model Table

### Dense Models (Standard Transformers)

| Model | Params | Quant | File Size | VRAM Used | Context Room | Tokens/sec | Engine | Use Case | Quality Score |
|-------|--------|-------|-----------|-----------|--------------|------------|--------|----------|----------------|
| Qwen 3.8 27B | 27B | Q4 | 16.81GB | 16.8GB | ~7.2GB | 45-60 | Strata/llama.cpp | General/Coding | 20.1 |
| Qwen 3.8 27B | 27B | Q5 | 19.54GB | 19.5GB | ~4.5GB | 40-55 | Strata/llama.cpp | General/Coding | 20.1 (higher quality) |
| Gemma 4 31B | 31B | Q4 | 18.69GB | 18.7GB | ~5.3GB | 50-70 | Strata/llama.cpp | General | ~19.5 |
| Llama 3.3 70B | 70B | Q4 | 21.5GB | 21.5GB | ~2.5GB | 35-50 | llama.cpp | General | ~21.0 |
| Gemma 4 12B | 12B | Q4 | 7.38GB | 7.4GB | ~16.6GB | 80-100 | llama.cpp | Lightweight | ~18.0 |

**Context Room Calculation**: 24GB - model size - ~1GB overhead. With 8-bit KV cache: ~2x more tokens.

### Mixture of Experts (MoE) Models

| Model | Total Params | Active Params | Quant | File Size | VRAM Used | Tokens/sec | Engine | Use Case | Notes |
|-------|--------------|---------------|-------|-----------|-----------|------------|--------|----------|-------|
| Qwen 3.8B Flash Next | 177B | 125B | IQ3 | 89GB | ~20GB | **91** | Avalon | Coding/Agents | Expert cache optimized |
| Qwen 3.8B Flash Next | 177B | 125B | IQ3 | 89GB | ~20GB | ~60 | Strata | Coding/Agents | Baseline |
| GLM 5.3 Flash | 320B | 18B | 4-bit | ~111GB | ~15GB | 47-54 | Strata | General | 320B total, 18B active |

**MoE Note**: Only ~10-48 experts active per token (out of 24,576 total). Expert caching keeps hot experts in VRAM.

---

## Engine Performance on RTX 7900 XT

| Engine | Type | Qwen 3.8B Flash Next | Qwen 3.8 27B | Status | OS | Notes |
|--------|------|----------------------|--------------|--------|----|-------|
| **Avalon** | llama.cpp fork | **91 tok/s** | ~45-60 | Active | Linux | 47% faster than Strata for MoE. RDNA 3 optimized |
| **Strata** | Specialist | ~60 tok/s | ~45-60 | Active | Linux/Win | Mature, multi-model. RDNA 4 focus |
| **Radiance** | Specialist | N/A | N/A | Active | Linux | RDNA 4 only (R9 700+). 4x prefill speed |
| **llama.cpp** | General | ~30 tok/s | ~45 tok/s | Stable | Linux/Win | Baseline. No MoE optimizations |

---

## Task-Specific Recommendations

### 🎯 Coding Agents (Best Performance)

**Primary Pick**: Qwen 3.8B Flash Next + Avalon
- **Speed**: 91 tok/s on 7900 XT
- **Why**: Expert cache optimized for RDNA 3, speculative decoding
- **Context**: 8k-16k tokens
- **RAM**: 64GB recommended (32GB minimum)

**Alternative**: Qwen 3.8 27B + Strata
- **Speed**: 45-60 tok/s
- **Why**: Strong reasoning, proven performance
- **Context**: 16k+ tokens
- **VRAM**: 16.8-19.5GB

**Fast Alternative**: Gemma 4 31B + Strata
- **Speed**: 50-70 tok/s
- **Why**: Shorter thinking (3k chars vs 12k for Qwen)
- **Trade-off**: Slightly lower reasoning

### 💬 General Chat / Q&A

| Model | Why | Speed | Context |
|-------|-----|-------|----------|
| Qwen 3.8 27B Q4 | Best reasoning/quality | 45-60 tok/s | 16k+ |
| Gemma 4 31B Q4 | Faster, good quality | 50-70 tok/s | 16k+ |
| Llama 3.3 70B Q4 | Higher params | 35-50 tok/s | 8k-16k |

### ✍️ Creative Writing / Roleplay

| Model | Why | Speed | Note |
|-------|-----|-------|------|
| Gemma 4 31B | Minimal quality loss with thinking OFF | 50-70 tok/s | -2.5pts intelligence |
| Gemma 4 12B | Fast, great for writers | 80-100 tok/s | Fits easily |

**Important**: With thinking mode OFF:
- Qwen 3.6 heretic: -25% intelligence
- Gemma 4 31B heretic: -2.5pts intelligence
→ **Gemma is better for writing without thinking**

### 🔓 Uncensored Models

| Model | Build | Context Setting | Loop Rate | Truth Loss | Notes |
|-------|-------|-----------------|-----------|------------|-------|
| Qwen 3.8 27B | Orca Router | 16,000+ | 38% | Minimal | Best finish rate |
| Qwen 3.8 27B | Huihui | 16,000+ | 44% | Moderate | Most downloaded (4M) |
| Gemma 4 31B | Heretic | 16,000+ | Low | 2.5pts | 10/10 willingness |
| Gemma 4 12B | Trevor JS | 16,000+ | Low | 2pts | Best 12B uncensored |

**Critical**: 
- **Finish rate > refusal count** (refusals are ~0% for all good builds)
- **Set `OLLAMA_CONTEXT_LENGTH=16000` minimum** (default 4,096 is too low)
- **Loop rate**: % of answers that never finish (thinking budget exhausted)

---

## Performance Optimization

### 1. Context Length (MOST IMPORTANT)

```bash
# Check current context
gpu-llama ps  # or ollama ps

# Set context (Ollama)
export OLLAMA_CONTEXT_LENGTH=32000

# Set context (llama.cpp)
./llama-server --ctx-size 32000
```

**Why**: Default 4,096 tokens is too low. Sapwell's test used 15,360 (1GB cache). 24GB card can handle 16k-32k+.

### 2. KV Cache Compression

```bash
# 8-bit KV cache (doubles context capacity)
./llama-server --kv-cache-8bit

# Ollama: edit config or use flag
ollama run qwen3.8:27b --kv-cache-8bit
```

**Impact**: 70k tokens on 16GB card (Qwen 3.8 27B Q4)

### 3. Speculative Decoding

| Model Type | Draft Model | Tokens Ahead | Speed Gain | Quality |
|------------|-------------|--------------|------------|---------|
| Code/JSON | B-Flash-2 | 7 | 2.5-2.9x | Identical |
| Math | B-Flash-2 | 7 | ~2x | Identical |
| Translation | B-Flash-2 | 7 | ~1.8x | Identical |
| Prose | B-Flash-2 | 7 | ~1.4x | Identical |

**How it works**: Small model proposes 7 tokens, big model verifies all 7 in one pass. Cost ~1.7x one token.

### 4. Expert Caching (MoE Only)

**Avalon's approach**:
- Uses all unused VRAM for expert cache
- Compute buffers lent to cache between phases
- KV cache unused space holds experts
- CPU handles cache misses in parallel
- Dynamic: moves experts to GPU when faster

**Result**: 80%+ hit rate = most experts served from VRAM

**Requirement**: 
- 64GB RAM recommended
- 32GB RAM minimum (with slowdowns on new prompts)
- Fast NVMe SSD (7GB/s+)

---

## Hardware Notes

### What Works on RTX 7900 XT:

✅ **Dense models** up to 21-22GB (70B params at Q4)  
✅ **MoE models** with expert caching (Qwen 3.8B Flash Next)  
✅ **Coding agents** with structured output (JSON/code)  
✅ **Linux** (primary support for Avalon/Strata)  
✅ **Speculative decoding** (2.5-2.9x on code/JSON)  

### What Doesn't:

❌ **Windows** (Avalon: no Vulkan backend. Strata: limited support)  
❌ **Qwen 3.8 Flash Next** at full precision (needs expert caching)  
❌ **Multi-user** without second card (single user: ~130 tok/s max)  
❌ **Prose-heavy** workloads (only 1.4x speedup from speculative decoding)  
❌ **RDNA 4 optimizations** (Radiance targets R9 700+, not 7900 XT)  

### Memory Breakdown (Qwen 3.8 27B Q4):

```
Total VRAM:        24,000 MB
Model weights:    16,810 MB (Q4)
KV Cache:           1,000 MB (16k tokens @ 16-bit)
Overhead:             200 MB
----------------------------------
Remaining:           5,990 MB (~90k tokens @ 16-bit)

With 8-bit KV Cache:
KV Cache:             500 MB (16k tokens @ 8-bit)
Remaining:         11,490 MB (~180k tokens @ 16-bit)
```

---

## Setup Commands

### Avalon (Qwen 3.8B Flash Next on 7900 XT)

```bash
# Clone and build
git clone https://github.com/frieren-duck/avalon
cd avalon
make

# Download model (89GB IQ3 file)
wget https://huggingface.co/Qwen/Qwen3-8B-FlashNext-IQ3/resolve/main/model-iq3_xx.safetensors

# Run server
./avalon-server --model /path/to/qwen3-8b-flash-next-iq3

# Run with context
./avalon-server --model /path/to/model --ctx-size 32000
```

**Requirements**:
- Linux
- 7900 XT or XTX (RDNA 3)
- 64GB RAM recommended
- Fast NVMe SSD

### Strata (General MoE)

```bash
# Install
pip install strata-engine

# Download model
# Qwen 3.8B Flash Next IQ3 (89GB)
# or Qwen 3.8 27B Q4 (16.8GB)

# Run server
strata-server --model /path/to/model

# Run with flags
strata-server --model /path/to/model --ctx-size 32000 --draft-model b-flash-2
```

**Requirements**:
- Linux or Windows
- Python 3.10+
- CUDA (Nvidia) or ROCm (AMD)

### llama.cpp (Dense Models)

```bash
# Download pre-built
wget https://github.com/ggerganov/llama.cpp/releases/download/b11561/llama-linux-x64-avx2
chmod +x llama-linux-x64-avx2

# Run server
./llama-server --model /path/to/model.gguf --ctx-size 32000 --kv-cache-8bit

# Run with speculative decoding
./llama-server --model /path/to/model.gguf --draft-model /path/to/draft.gguf --ctx-size 32000
```

---

## Benchmark References

| Source | Model | Engine | Hardware | Tokens/sec | Notes |
|--------|-------|--------|----------|------------|-------|
| Avalon README | Qwen 3.8B Flash Next | Avalon | RX 7900 XT | **91** | IQ3, speculative decoding |
| Avalon README | Qwen 3.8B Flash Next | Strata | RX 7900 XT | 61.9 | IQ3, same conditions |
| Solcer Vienna | Qwen 3.8 27B | Radiance | R9 700 | 2,868 | Prefill @ 16k tokens (4.2x vs llama.cpp) |
| Solcer Vienna | Qwen 3.8 27B | llama.cpp | R9 700 | 888 | Prefill @ 16k tokens |
| BizFlow AI | Mixed tasks | Radiance | R9 700 | 2x | Full day: 125.5min → 61.7min |

---

## Sources

All recommendations based on transcripts from Kai Explains YT:

1. **[I Tested Every Uncensored Local AI Model](research/youtube-transcripts/kaiexplainsYT/2026-11/j-VqPVjztJE_I_Tested_Every_Uncensored_Local_AI_Model_8GB_to_32GB_VRAM.md)** - Uncensored model analysis, finish rates, tier recommendations
2. **[Radiance Made AMD's 32GB GPU Run LLM 4x Faster](research/youtube-transcripts/kaiexplainsYT/2026-11/W9-fXb1lqos_Radiance_Made_AMDs_32GB_GPU_Run_LLM_4x_Faster.md)** - RDNA 4 performance, Radiance engine, prefill vs decode
3. **[What's the Best AI Model Your GPU Can Actually Run](research/youtube-transcripts/kaiexplainsYT/2026-11/kTmUbRVsamo_Whats_the_Best_AI_Model_Your_GPU_Can_Actually_Run_16GB_to_1TB_VRam.md)** - Memory ladder, model tiers, benchmark scores
4. **[Avalon Just Beat Strata by 47% on AMD](research/youtube-transcripts/kaiexplainsYT/2026-11/0F63pTS8Gt0_Avalon_Just_Beat_Strata_by_47_on_AMD_9x_Faster.md)** - 7900 XT specific, expert caching, Avalon vs Strata

---

## Summary

**For AMD RTX 7900 XT 24G owner:**

1. **Coding Agents**: Qwen 3.8B Flash Next + Avalon (91 tok/s)
2. **General Use**: Qwen 3.8 27B Q4 + Strata (45-60 tok/s)
3. **Fast Response**: Gemma 4 31B Q4 + Strata (50-70 tok/s)
4. **Uncensored**: Orca Router Qwen 3.8 27B Q4 (38% loop rate, best finish rate)

**Always**:
- Set context to 16,000+
- Enable 8-bit KV cache
- Use Linux for best performance
- 64GB RAM for MoE models

**Avoid**:
- Windows for Avalon
- Default Ollama context (4,096)
- Prose-heavy workloads without thinking mode
