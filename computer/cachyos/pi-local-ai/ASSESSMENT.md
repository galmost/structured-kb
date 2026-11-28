# Research: Kai Explains YT - Local AI Model Recommendations for AMD RTX 7900 XT 24G

## structured-kb Assessment

**Layout**: `computer/<distro|domain>/<topic>/README.md` - clean, consistent
**Conventions**: AGENTS.md defines strict formatting rules (numbered steps, exact commands, troubleshooting sections)
**Strengths**: 
- Well-organized hierarchical structure
- Clear note format with copy-paste commands
- Already contains youtube-transcript extraction guide using yt-dlp
- Good conventions for technical documentation

**Gaps**: No existing AMD-specific or model recommendation content

---

## YouTube Transcripts Extracted

**Channel**: @kaiexplainsYT  
**Period**: Past month (2026-10-26 to 2026-11-26)  
**Videos**: 31 total, 10 key transcripts downloaded to `research/youtube-transcripts/kaiexplainsYT/`

**Key Research Sources**:
1. `j-VqPVjztJE` - I Tested Every Uncensored Local AI Model (8GB to 32GB VRAM)
2. `W9-fXb1lqos` - Radiance Made AMD's 32GB GPU Run LLM 4x Faster
3. `kTmUbRVsamo` - What's the Best AI Model Your GPU Can Actually Run? 16GB to 1TB VRam
4. `0F63pTS8Gt0` - Avalon Just Beat Strata by 47% on AMD (9x Faster)
5. `CSRrqRC9QJA` - 10 GPUs You Should Get for Local AI Before Qwen 4's Release

---

## AMD RTX 7900 XT 24G Hardware Profile

| Spec | Value | Notes |
|------|-------|-------|
| **Architecture** | RDNA 3 | AMD GPU |
| **VRAM** | 24GB GDDR6 | 800 GB/s bandwidth |
| **Compute Units** | 84 | 800 GB/s memory bandwidth |
| **PCIe** | 4.0 x16 | Check motherboard compatibility |
| **OS Support** | Linux (best) | Windows support improving |

**Critical Insight**: Performance bottleneck is **not compute** but **memory bandwidth** and **expert caching** for MoE models.

---

## Recommended Local AI Models for AMD RTX 7900 XT 24G

### Dense Models (Non-MoE)

| Task | Model | Quant | Size | VRAM Used | Context Room | Tokens/sec | Notes |
|------|-------|-------|------|-----------|--------------|------------|-------|
| **General/Coding** | Qwen 3.8 27B | Q4 | 16.81GB | 16.8GB | ~7.2GB | ~45-60 | Orca Router build. Best finish rate |
| **General/Coding** | Qwen 3.8 27B | Q5 | 19.54GB | 19.5GB | ~4.5GB | ~40-55 | Higher quality, less context |
| **General** | Gemma 4 31B | Q4 | 18.69GB | 18.7GB | ~5.3GB | ~50-70 | Shorter thinking (3k chars vs 12k) |
| **General** | Llama 3.3 70B | Q4 | 21.5GB | 21.5GB | ~2.5GB | ~35-50 | Tight fit, limited context |
| **Lightweight** | Gemma 4 12B | Q4 | 7.38GB | 7.4GB | ~16.6GB | ~80-100 | Fast, great for 12GB tier |

### Mixture of Experts (MoE) Models

| Task | Model | Quant | Size | VRAM Used | Tokens/sec | Engine | Notes |
|------|-------|-------|------|-----------|------------|--------|-------|
| **Coding/Agents** | Qwen 3.8B Flash Next | IQ3 | 89GB | ~20GB | **91** | Avalon | Expert cache optimized for 7900 XT |
| **Coding/Agents** | Qwen 3.8B Flash Next | IQ3 | 89GB | ~20GB | ~60 | Strata | Standard baseline |
| **General** | GLM 5.3 Flash | 4-bit | ~111GB | ~15GB | ~47-54 | Strata | 320B total, 18B active |

---

## Inference Engine Recommendations

### For AMD RTX 7900 XT 24G:

| Engine | Best For | Tokens/sec (7900 XT) | Status | Notes |
|--------|----------|----------------------|--------|-------|
| **Avalon** | Qwen 3.8B Flash Next | **91** | Active | 47% faster than Strata for this model. RDNA 3 optimized |
| **Strata** | General MoE | ~60 | Active | Mature, multi-model support. RDNA 4 focus |
| **Radiance** | RDNA 4 only | N/A | Active | 4x prefill speed on R9 700. Not for 7900 XT |
| **llama.cpp** | Dense models | ~30-45 | Stable | Baseline. No MoE optimizations |

**Critical**: Avalon's 47% win is **model-specific** (Qwen 3.8B Flash Next) and **hardware-specific** (7900 XT). On RDNA 4 cards, Strata is faster.

---

## Task-Specific Recommendations

### Coding Agent (Primary Use Case)

| Model | Engine | Why |
|-------|--------|-----|
| **Qwen 3.8B Flash Next** | Avalon | 91 tok/s, expert cache optimized |
| **Qwen 3.8 27B** | Strata/llama.cpp | 45-60 tok/s, strong reasoning |
| **Gemma 4 31B** | Strata/llama.cpp | 50-70 tok/s, shorter thinking |

**Context**: Coding agents send long prompts (repo context). **Prefill speed** matters most on first load. **Decode speed** for subsequent turns.

### General Chat

| Model | Engine | Why |
|-------|--------|-----|
| **Qwen 3.8 27B** | llama.cpp | Best reasoning/quality |
| **Gemma 4 31B** | llama.cpp | Faster, good quality |
| **Llama 3.3 70B** | llama.cpp | Higher params, tight fit |

### Creative Writing / Roleplay

| Model | Engine | Why |
|-------|--------|-----|
| **Gemma 4 31B** | llama.cpp | Thinking mode off = minimal quality loss |
| **Gemma 4 12B** | llama.cpp | Fast, great for writers |

**Note**: With thinking OFF, Gemma loses ~2.5pts intelligence vs Qwen's ~25% loss.

### Uncensored Models

| VRAM Tier | Model | Build | Context Setting | Notes |
|-----------|-------|-------|-----------------|-------|
| 24GB | Orca Router Qwen 3.8 27B | Q4 | 16,000+ | 38% loop rate. Set `OLLAMA_CONTEXT_LENGTH` |
| 24GB | Gemma 4 31B | Heretic | 16,000+ | 10/10 willingness, 2.5pt truth loss |

**Warning**: Uncensored = higher loop rates. **Finish rate** > refusal count.

---

## Performance Optimization Tips

### 1. Context Length
- **Ollama default**: 4,096 (too low for 24GB)
- **Recommended**: 16,000 minimum, 32,000+ if possible
- **Check**: `ollama ps` → context column
- **Set**: `export OLLAMA_CONTEXT_LENGTH=32000`

### 2. KV Cache
- **8-bit KV cache**: Doubles context capacity
- **Flag**: `--kv-cache-8bit` (llama.cpp)
- **Impact**: 70k tokens on 16GB card

### 3. Speculative Decoding
- **Draft model**: B-Flash-2 (7 tokens ahead)
- **Gain**: 2.5-2.9x on code/JSON, 1.4x on prose
- **Cost**: One verification pass per 7 tokens

### 4. Expert Caching (MoE)
- **Avalon**: Uses unused VRAM for expert cache
- **Hit rate**: 80%+ keeps experts on GPU
- **RAM**: 64GB recommended (32GB minimum)

---

## Hardware-Specific Notes for RTX 7900 XT

### What Works Well:
✅ **Dense models** up to 21-22GB (70B params at Q4)
✅ **MoE models** with expert caching (Qwen 3.8B Flash Next)
✅ **Coding agents** with structured output (JSON/code = 2.5-2.9x speedup)
✅ **Linux** (primary support for Avalon/Strata)

### What Doesn't:
❌ **Windows** (Avalon: no Vulkan backend. Strata: limited)
❌ **Qwen 3.8 Flash Next** at full precision (needs expert caching)
❌ **Multi-user** without second card (single user: 130 tok/s max)
❌ **Prose-heavy** workloads (only 1.4x speedup)

### Memory Calculations:
- **Qwen 3.8 27B Q4**: 16.81GB weights + ~1GB KV cache = ~18GB
- **Remaining**: ~6GB for context (~90k tokens at 16-bit)
- **With 8-bit KV**: ~12GB context (~180k tokens)

---

## Summary Table: Best Models by Task

| Task Category | Best Model | Engine | Quant | VRAM Used | Tokens/sec | Context | Notes |
|---------------|------------|--------|-------|-----------|------------|----------|-------|
| **Coding Agent** | Qwen 3.8B Flash Next | Avalon | IQ3 | ~20GB | **91** | 8k-16k | Expert cache optimized |
| **General Reasoning** | Qwen 3.8 27B | Strata | Q4 | 16.8GB | 45-60 | 16k+ | Orca Router build |
| **Fast General** | Gemma 4 31B | Strata | Q4 | 18.7GB | 50-70 | 16k+ | Shorter thinking |
| **Lightweight** | Gemma 4 12B | llama.cpp | Q4 | 7.4GB | 80-100 | 32k+ | Great for 12GB+ |
| **Uncensored Coding** | Qwen 3.8 27B | Strata | Q4 | 16.8GB | 45-60 | 16k+ | Set context length! |
| **Uncensored Fast** | Gemma 4 31B | Strata | Q4 | 18.7GB | 50-70 | 16k+ | 10/10 willingness |

---

## Setup Recommendations

### For RTX 7900 XT 24G Owner:

1. **OS**: Linux (Ubuntu 22.04+ or Debian 13)
2. **Engine**: 
   - Avalon for Qwen 3.8B Flash Next
   - Strata for other MoE models
   - llama.cpp for dense models
3. **RAM**: 64GB minimum (32GB works with slowdowns)
4. **Storage**: NVMe SSD (7GB/s+ for expert caching)
5. **Context**: Set to 16,000-32,000
6. **KV Cache**: Enable 8-bit

### Installation:
```bash
# Avalon (for Qwen 3.8B Flash Next on 7900 XT)
git clone https://github.com/frieren-duck/avalon
cd avalon
make
./avalon-server --model /path/to/qwen3-8b-flash-next-iq3

# Strata (general MoE)
pip install strata-engine
strata-server --model /path/to/model

# llama.cpp (dense models)
./llama-server --model /path/to/model.gguf --ctx-size 32000 --kv-cache-8bit
```

---

## Sources

- [I Tested Every Uncensored Local AI Model](research/youtube-transcripts/kaiexplainsYT/2026-11/j-VqPVjztJE_I_Tested_Every_Uncensored_Local_AI_Model_8GB_to_32GB_VRAM.md)
- [Radiance Made AMD's 32GB GPU Run LLM 4x Faster](research/youtube-transcripts/kaiexplainsYT/2026-11/W9-fXb1lqos_Radiance_Made_AMDs_32GB_GPU_Run_LLM_4x_Faster.md)
- [What's the Best AI Model Your GPU Can Actually Run](research/youtube-transcripts/kaiexplainsYT/2026-11/kTmUbRVsamo_Whats_the_Best_AI_Model_Your_GPU_Can_Actually_Run_16GB_to_1TB_VRam.md)
- [Avalon Just Beat Strata by 47% on AMD](research/youtube-transcripts/kaiexplainsYT/2026-11/0F63pTS8Gt0_Avalon_Just_Beat_Strata_by_47_on_AMD_9x_Faster.md)
