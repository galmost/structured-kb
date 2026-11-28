# Research Summary: Local AI Model Recommendations

**Checkpoint 2026-11-28**: 7 GGUF models downloaded (40GB), all benchmarked on Steam Deck. See [CHECKPOINT_2026-11-28.md](CHECKPOINT_2026-11-28.md).

## What Was Done

### 1. structured-kb Assessment
- **Layout**: `computer/<distro|domain>/<topic>/README.md` - clean, hierarchical
- **Conventions**: AGENTS.md defines strict formatting (numbered steps, exact commands, troubleshooting)
- **Strengths**: Well-organized, copy-paste commands, existing youtube-transcript guide
- **Gap**: No AMD-specific or model recommendation content

### 2. YouTube Transcript Extraction
- **Channel**: @kaiexplainsYT
- **Period**: Past month (2026-10-26 to 2026-11-26)
- **Videos**: 31 total identified, 10 key transcripts downloaded
- **Location**: `research/youtube-transcripts/kaiexplainsYT/2026-11/`

**Key Videos Analyzed**:
1. `j-VqPVjztJE` - I Tested Every Uncensored Local AI Model (8GB to 32GB VRAM)
2. `W9-fXb1lqos` - Radiance Made AMD's 32GB GPU Run LLM 4x Faster
3. `kTmUbRVsamo` - What's the Best AI Model Your GPU Can Actually Run? 16GB to 1TB VRam
4. `0F63pTS8Gt0` - Avalon Just Beat Strata by 47% on AMD (9x Faster)
5. `CSRrqRC9QJA` - 10 GPUs You Should Get for Local AI Before Qwen 4's Release

### 3. Software Installed

| Tool | Version | Location | Status |
|------|---------|----------|--------|
| **Strata** | 0.2.22 | `~/.local/bin/strata` | ✅ Installed |
| **llama.cpp** | b12757 | `~/.local/bin/llama.cpp/` | ✅ Installed |
| **pipx** | 1.19.1 | `~/.local/bin/pipx` | ✅ Installed |
| **pip** | 26.3 | `~/.local/bin/pip` | ✅ Installed |
| **huggingface-hub** | latest | Python package | ✅ Installed |

**Install Commands Used**:
```bash
# pipx (no system breakage)
python3 -m pip install --user --break-system-packages pipx

# Strata
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh | bash

# llama.cpp (Ubuntu pre-built)
curl -L -o llama.tar.gz https://github.com/ggml-org/llama.cpp/releases/download/b12757/llama-b12757-bin-ubuntu-x64.tar.gz
tar -xzf llama.tar.gz
mv llama-b12757 ~/.local/bin/llama.cpp
```

### 4. Documentation Created

#### Core Documents
1. **ASSESSMENT.md** - Detailed assessment + model tables
2. **MODEL_RECOMMENDATIONS_AMD_7900XT.md** - AMD 7900 XT specific recommendations
3. **TABLES_AND_TWEAKS.md** - All tables + test matrix
4. **SETUP_GUIDE.md** - Installation and setup instructions
5. **README.md** - Research folder overview

#### Hardware-Specific Documents
1. **HARDWARE_DOCS/STEAM_DECK.md** - Current hardware (AMD Custom GPU 0405, 14GB RAM)
2. **HARDWARE_DOCS/AMD_7900_XT.md** - AMD 7900 XT 24G recommendations

#### Transcripts
- 10 YouTube video transcripts in markdown + plain text format
- Located in `research/youtube-transcripts/kaiexplainsYT/2026-11/`

---

## Current Hardware Setup

**Machine**: AMD Custom APU 0932 / 0405 (Sephiroth)
- **CPU**: 8 cores (4C/8T), Zen 2
- **GPU**: AMD Custom GPU 0405 (Sephiroth), RDNA 2
- **RAM**: 14GB
- **OS**: CachyOS Linux (Arch-based)
- **Architecture**: Shared memory (APU)

**Previous Context**: Inkling-2-Mini-GGUF options assessed. UD-IQ1_M selected: 8.02GB, 90.2% top-1 accuracy, 0.0867 KLD. UD-IQ1_M fits in 14GB RAM for CPU inference.

### Compatible Models for Current Hardware

| Model | Params | Quant | Size | Tokens/sec (CPU) | Memory Used | Status |
|-------|--------|-------|------|------------------|-------------|--------|
| **Inkling-2-Mini** | 12B | SQ-10 | 11GB | 5-10 | ~11GB | Strata format |
| **Phi-3.5-mini** | 3.8B | Q4_K | 4.5GB | 10-15 | ~5GB | ✅ Recommended |
| **Gemma 4 9B** | 9B | Q4_K | 5.5GB | 5-10 | ~6GB | ✅ Recommended |
| **Gemma 4 9B** | 9B | UD-IQ1_M | 8.02GB | 3-8 | ~8GB | 90.2% accuracy |
| **Gemma 4 12B** | 12B | Q4_K | 7.4GB | 3-7 | ~8GB | Tight fit |
| **Llama 3.3 8B** | 8B | Q4_K | 4.7GB | 8-12 | ~5GB | Good alternative |

**Note**: Strata does NOT support AMD Custom GPU 0405 (Steam Deck) yet. Use llama.cpp in CPU mode.

---

## AMD 7900 XT 24G Recommendations

### Quick Picks

| Task | Best Model | Engine | Speed | VRAM Used |
|------|------------|--------|-------|-----------|
| **Coding Agent** | Qwen 3.8B Flash Next | Avalon | **91 tok/s** | ~20GB |
| **General Reasoning** | Qwen 3.8 27B | Strata | 45-60 tok/s | 16.8GB |
| **Fast General** | Gemma 4 31B | Strata | 50-70 tok/s | 18.7GB |
| **Lightweight** | Gemma 4 12B | llama.cpp | 80-100 tok/s | 7.4GB |

### Full Tables
See `MODEL_RECOMMENDATIONS_AMD_7900XT.md` for complete model tables.

---

## Tweaks to Test

### 1. Context Length
```bash
# Test: 4096, 8192, 16384, 32768
strata launch --context SIZE
./llama -m model.gguf --ctx-size SIZE
```

### 2. Quantization
```bash
# Test: Q4_K, Q3_K, Q2_K, IQ1_M
./llama -m model-Q4_K.gguf
./llama -m model-Q3_K.gguf
```

### 3. CPU Threads
```bash
# Test: 1, 2, 4, 8, auto
strata launch --threads N
./llama -m model.gguf --threads N
```

### 4. KV Cache Compression
```bash
# 8-bit KV cache (2x context)
strata launch --kv 8
./llama -m model.gguf --kv-cache-8bit
```

### 5. Speculative Decoding
```bash
# Draft model (2-3x speedup)
strata launch --drafting auto
./llama -m model.gguf --draft-model draft.gguf
```

### 6. Parallel Requests
```bash
# 2-8 parallel
strata launch --parallel N
```

---

## Files Created

```
research/
├── README.md                    # Overview
├── SUMMARY.md                   # This file
├── ASSESSMENT.md                # Detailed assessment
├── MODEL_RECOMMENDATIONS_AMD_7900XT.md  # AMD 7900 XT table
├── TABLES_AND_TWEAKS.md         # All tables + test matrix
├── SETUP_GUIDE.md               # Installation guide
├── HARDWARE_DOCS/
│   ├── STEAM_DECK.md            # Current hardware
│   └── AMD_7900_XT.md           # AMD 7900 XT
└── youtube-transcripts/
    └── kaiexplainsYT/
        └── 2026-11/             # 10 transcripts
            ├── *.md
            └── *_plain.txt
```

**Total**: 17 documentation files + 10 transcripts (20 markdown files, 10 plain text)

---

## What's Next

### To Complete Setup

1. **Download Models**
   ```bash
   # For Steam Deck (CPU mode)
   # Phi-3.5-mini Q4_K (4.5GB)
   # Gemma 4 9B Q4_K (5.5GB)
   # Gemma 4 9B UD-IQ1_M (8.02GB)
   
   # For AMD 7900 XT
   # Qwen 3.8B Flash Next IQ3 (89GB)
   # Qwen 3.8 27B Q4 (16.8GB)
   # Gemma 4 31B Q4 (18.7GB)
   ```

2. **Run Benchmarks**
   - Test different context sizes
   - Test different quantizations
   - Test different thread counts
   - Document results

3. **Update Documentation**
   - Fill in benchmark results in `TABLES_AND_TWEAKS.md`
   - Update `HARDWARE_DOCS/STEAM_DECK.md` with actual performance
   - Update `HARDWARE_DOCS/AMD_7900_XT.md` with actual performance

### Commands to Run

```bash
# Verify installations
strata --version
llama --version
pipx --version

# Test with Phi-3.5-mini (if downloaded)
./llama -m phi-3.5-mini-Q4_K.gguf --ctx-size 4096 --threads 4 -ngl 0 --bench 100

# Test with Gemma 4 9B (if downloaded)
./llama -m gemma-4-9b-Q4_K.gguf --ctx-size 4096 --threads 4 -ngl 0 --bench 100
```

---

## Key Findings from Research

### 1. Uncensored Models
- **Finish rate > refusal count** (refusals are ~0% for all good builds)
- **Set context to 16,000+** (default 4,096 is too low)
- **Best builds**: Orca Router (38% loop rate), Trevor JS, coder 3101
- **Avoid**: Huihui (44% loop rate, most downloaded but damaged)

### 2. AMD Performance
- **Avalon**: 47% faster than Strata on 7900 XT for Qwen 3.8B Flash Next (91 tok/s)
- **Radiance**: 4x prefill speed on RDNA 4 (R9 700), not for 7900 XT
- **Strata**: Mature, multi-model support, RDNA 4 focus
- **llama.cpp**: Baseline, no MoE optimizations

### 3. Memory Ladder
- **32GB**: Qwen 3.8 27B with all bits + context (20.1 score)
- **128GB**: Qwen 3.8 Flash Next (27.8 score)
- **256GB**: DeepSeek V4.1 Flash (32.5 score)
- **1TB**: Kimi K3.1 Pro (46.0 score) - best open model

### 4. Engine Optimizations
- **Context length**: 16,000+ minimum for usable AI
- **KV cache**: 8-bit doubles context capacity
- **Speculative decoding**: 2-3x speedup on structured output
- **Expert caching**: Critical for MoE models on AMD

---

## Links

- [Strata GitHub](https://github.com/Niko1221/Strata)
- [Avalon GitHub](https://github.com/frieren-duck/avalon)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [Kai Explains YT](https://www.youtube.com/@kaiexplainsYT)
- [structured-kb](../structured-kb/)
