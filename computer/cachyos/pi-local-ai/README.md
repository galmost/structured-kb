# Research: Kai Explains YT - Local AI Analysis

**Latest checkpoint**: [CHECKPOINT_2026-11-28.md](CHECKPOINT_2026-11-28.md) — 7 models downloaded, benchmarks done, HF CLI workflow documented.

## Overview

Research folder containing YouTube transcript analysis from [@kaiexplainsYT](https://www.youtube.com/@kaiexplainsYT) channel, focusing on local AI model recommendations and hardware optimization.

**Period**: Past month (2026-10-26 to 2026-11-26)  
**Videos Analyzed**: 31 total, 10 key transcripts extracted  
**Focus**: AMD GPU performance, model recommendations, inference engines

---

## Folder Structure

```
research/
├── README.md                    # This file
├── ASSESSMENT.md                # Detailed assessment + structured-kb analysis
├── MODEL_RECOMMENDATIONS_AMD_7900XT.md  # Model table for AMD RTX 7900 XT 24G
└── youtube-transcripts/
    └── kaiexplainsYT/
        ├── 2026-10/             # October transcripts
        └── 2026-11/             # November transcripts (10 files)
```

---

## Key Findings

### structured-kb Assessment
- Well-organized: `computer/<distro|domain>/<topic>/README.md`
- Clear conventions in AGENTS.md
- Already has youtube-transcript extraction guide (yt-dlp)
- **Gap**: No AMD-specific or model recommendation content

### YouTube Research Summary

**Channel**: Kai Explains YT  
**Focus**: Local AI, hardware benchmarks, model testing  
**Style**: Deep technical analysis, real-world testing, benchmark comparisons

**Key Videos Analyzed**:

| Date | Video | Focus | Key Insight |
|------|-------|-------|-------------|
| 2026-11-25 | 10 GPUs You Should Get for Local AI | Hardware | GPU recommendations for different budgets |
| 2026-11-23 | Radiance Made AMD's 32GB GPU Run LLM 4x Faster | AMD | RDNA 4 performance, Radiance engine |
| 2026-11-15 | I Tested Every Uncensored Local AI Model | Models | Finish rate > refusal count, context settings |
| 2026-11-14 | 54GB VRAM For $35 The Cheapest Local AI Hack | Hardware | Budget multi-GPU setups |
| 2026-11-08 | I Tested Local AI on My Mac Studio | Hardware | macOS memory limits, performance |
| 2026-11-02 | What's the Best AI Model Your GPU Can Run | Models | Memory ladder, tier analysis |
| 2026-11-01 | You Don't Need an Expensive GPU Anymore | Engine | Strata performance, context optimization |
| 2026-10-31 | Avalon Just Beat Strata by 47% on AMD | Engine | 7900 XT specific, expert caching |
| 2026-10-27 | Your GPU Is Nerfed for Local AI | Hardware | NVIDIA limitations |

---

## Main Deliverables

### 1. ASSESSMENT.md
- structured-kb folder analysis
- YouTube transcript extraction summary
- Hardware profiles
- Complete model recommendation tables
- Engine comparisons
- Task-specific recommendations

### 2. MODEL_RECOMMENDATIONS_AMD_7900XT.md
- **Quick picks** table
- **Detailed model tables** (Dense + MoE)
- **Engine performance** comparisons
- **Task-specific recommendations**
- **Performance optimization** guide
- **Setup commands**

---

## Quick Reference: AMD RTX 7900 XT 24G

### Best Models

| Use Case | Model | Engine | Speed | VRAM |
|----------|-------|--------|-------|------|
| Coding Agent | Qwen 3.8B Flash Next | Avalon | **91 tok/s** | ~20GB |
| General Reasoning | Qwen 3.8 27B | Strata | 45-60 tok/s | 16.8GB |
| Fast General | Gemma 4 31B | Strata | 50-70 tok/s | 18.7GB |
| Lightweight | Gemma 4 12B | llama.cpp | 80-100 tok/s | 7.4GB |

### Critical Settings

```bash
# Context length (DEFAULT 4,096 IS TOO LOW)
export OLLAMA_CONTEXT_LENGTH=32000

# 8-bit KV cache (doubles context)
--kv-cache-8bit

# Speculative decoding (2.5-2.9x on code)
--draft-model b-flash-2
```

### Hardware Requirements

- **OS**: Linux (Avalon/Strata best support)
- **RAM**: 64GB (32GB minimum for MoE)
- **Storage**: NVMe SSD (7GB/s+ for expert caching)
- **Engine**: Avalon for 7900 XT, Strata for general

---

## Methodology

1. **Channel Analysis**: Identified 31 videos from past month
2. **Transcript Extraction**: Downloaded 10 most relevant videos using yt-dlp
3. **Conversion**: json3 → markdown + plain text
4. **Analysis**: Extracted model recommendations, benchmark data, hardware insights
5. **Synthesis**: Created structured recommendations for AMD RTX 7900 XT 24G

---

## Tools Used

- **yt-dlp**: YouTube transcript extraction (`--write-auto-subs --sub-format json3`)
- **Python**: json3 to markdown conversion
- **Avalon/Strata/llama.cpp**: Inference engines analyzed

---

## Links

- [Kai Explains YT Channel](https://www.youtube.com/@kaiexplainsYT)
- [structured-kb Repository](../structured-kb/)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
