# Research: Kai Explains YT — Local AI Analysis (CachyOS Steam Deck)

**Latest checkpoint**: [CHECKPOINT_2026-11-28.md](CHECKPOINT_2026-11-28.md) — 7 models downloaded, benchmarks done, HF CLI workflow documented.

Transcript analysis from [@kaiexplainsYT](https://www.youtube.com/@kaiexplainsYT): local AI model recommendations and AMD hardware optimization. Period 2026-10-26 → 2026-11-26; 31 videos screened, 10 key transcripts extracted.

## Files

```
pi-local-ai/
├── README.md                              # this file
├── CHECKPOINT_2026-11-28.md                # current state
├── ASSESSMENT.md                          # detailed assessment + structured-kb analysis
├── MODEL_RECOMMENDATIONS_AMD_7900XT.md    # model table for AMD RX 7900 XT 24G
├── *.md                                   # SETUP_GUIDE, HUGGINGFACE_CLI_GUIDE, HF_CLI_REFERENCE,
│                                          # PI_LOCAL_MODELS, SUMMARY, TABLES_AND_TWEAKS, ...
├── scripts/
├── HARDWARE_DOCS/                         # benchmarks (incl. Steam Deck)
└── youtube-transcripts/kaiexplainsYT/{2026-10,2026-11}/
```

## Key videos

| Date | Video | Key insight |
|------|-------|-------------|
| 2026-11-25 | 10 GPUs You Should Get for Local AI | GPU picks per budget |
| 2026-11-23 | Radiance: 32GB AMD GPU 4x faster | RDNA 4, Radiance engine |
| 2026-11-15 | Every Uncensored Local AI Model | Finish rate > refusal count |
| 2026-11-14 | 54GB VRAM For $35 | Budget multi-GPU |
| 2026-11-08 | Local AI on Mac Studio | macOS memory limits |
| 2026-11-02 | Best AI Model Your GPU Can Run | Memory ladder |
| 2026-11-01 | You Don't Need an Expensive GPU | Strata context optimization |
| 2026-10-31 | Avalon Beats Strata by 47% on AMD | 7900 XT, expert caching |
| 2026-10-27 | Your GPU Is Nerfed for Local AI | NVIDIA limits |

## Deliverables

1. **ASSESSMENT.md** — structured-kb analysis, transcript summary, hardware profiles, model tables, engine comparisons.
2. **MODEL_RECOMMENDATIONS_AMD_7900XT.md** — quick picks, dense + MoE tables, engine performance, task-specific picks, setup commands.

## Quick reference: AMD RX 7900 XT 24G

| Use case | Model | Engine | Speed | VRAM |
|----------|-------|--------|-------|------|
| Coding agent | Qwen 3.8B Flash Next | Avalon | 91 tok/s | ~20GB |
| General reasoning | Qwen 3.8 27B | Strata | 45-60 tok/s | 16.8GB |
| Fast general | Gemma 4 31B | Strata | 50-70 tok/s | 18.7GB |
| Lightweight | Gemma 4 12B | llama.cpp | 80-100 tok/s | 7.4GB |

Critical settings:

```bash
export OLLAMA_CONTEXT_LENGTH=32000   # default 4,096 is too low
# llama.cpp flags: --kv-cache-8bit (doubles context), --draft-model b-flash-2 (2.5-2.9x on code)
```

Hardware: Linux, 64GB RAM (32GB min for MoE), NVMe (7GB/s+ for expert caching), Avalon for 7900 XT.

## Methodology

yt-dlp (`--write-auto-subs --sub-format json3`) → Python json3→markdown → extract model/benchmark/hardware claims → synthesize recommendations. Extraction recipe: [computer/debian/youtube-transcript](../../debian/youtube-transcript/README.md).

## Links

- [Kai Explains YT](https://www.youtube.com/@kaiexplainsYT)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
