# Tables & Tweaks: Local AI Performance Testing

## Hardware Profiles

| Profile | GPU | VRAM | RAM | Architecture | OS | Notes |
|---------|-----|------|-----|--------------|----|-------|
| **Steam Deck** | AMD Custom GPU 0405 (Sephiroth) | 1-4GB shared | 14GB | Zen 2 + RDNA 2 | CachyOS Linux | APU, shared memory |
| **AMD 7900 XT** | Radeon RX 7900 XT | 24GB GDDR6 | N/A | RDNA 3 | Linux/Windows | 800 GB/s bandwidth |
| **AMD R9 700** | Radeon AI Pro R9 700 | 32GB GDDR6 | N/A | RDNA 4 | Linux | 640 GB/s bandwidth |

---

## Model Tables

### Dense Models (Standard Transformers)

| Model | Params | Provider | Quant | Size | VRAM Needed | RAM Needed | Tokens/sec (7900 XT) | Tokens/sec (Steam Deck) | Quality Score |
|-------|--------|----------|-------|------|-------------|------------|------------------------|-------------------------|----------------|
| **Gemma 4 9B** | 9B | Unsloth | Q4_K | 5.5GB | 1-2GB | 5-6GB | 50-70 | 5-10 | ~18.0 |
| **Gemma 4 9B** | 9B | Unsloth | IQ1_M | 8.02GB | 1-2GB | 8-9GB | 40-60 | 3-8 | ~18.0 |
| **Gemma 4 12B** | 12B | Unsloth | Q4_K | 7.4GB | 2-3GB | 7-8GB | 45-60 | 3-7 | ~18.5 |
| **Gemma 4 12B** | 12B | Unsloth | UD-IQ4_XS | 7.4GB | 2-3GB | 7-8GB | 45-60 | 3-7 | ~18.5 |
| **Phi-3.5-mini** | 3.8B | Microsoft | Q4_K | 4.5GB | 1GB | 4-5GB | 60-80 | 10-15 | ~17.5 |
| **Qwen 3.8 27B** | 27B | Orca Router | Q4 | 16.8GB | 16-17GB | N/A | 45-60 | N/A | 20.1 |
| **Qwen 3.8 27B** | 27B | Orca Router | Q3 | 12.3GB | 12-13GB | N/A | 40-55 | N/A | 20.1 |
| **Llama 3.3 70B** | 70B | Meta | Q4 | 21.5GB | 21-22GB | N/A | 35-50 | N/A | ~21.0 |
| **Llama 3.3 8B** | 8B | Meta | Q4 | 4.7GB | 1-2GB | 4-5GB | 60-80 | 8-12 | ~17.0 |

### Mixture of Experts (MoE) Models

| Model | Total Params | Active Params | Provider | Quant | Size | VRAM Needed | RAM Needed | Tokens/sec (7900 XT) | Tokens/sec (Steam Deck) | Notes |
|-------|--------------|---------------|----------|-------|------|-------------|------------|------------------------|-------------------------|-------|
| **Qwen 3.8B Flash Next** | 177B | 125B | ISTA-DASLab | Q2_0 | 37.6GB | 3-4GB | 37-38GB | 91 (Avalon) | N/A | Expert cache optimized |
| **Qwen 3.8B Flash Next** | 177B | 125B | ISTA-DASLab | IQ2_XS | 39.2GB | 3-4GB | 39-40GB | 85-90 | N/A | Faster, better quality |
| **Qwen 3.8B Flash Next** | 177B | 125B | ISTA-DASLab | IQ3_XXS | 47.0GB | 3-4GB | 47-48GB | 70-80 | N/A | Great quality |
| **Qwen 3.8B Flash Next** | 177B | 125B | ISTA-DASLab | IQ3_S | 54.8GB | 3-4GB | 54-55GB | 50-60 | N/A | Best quality |
| **Qwen 3.8B Flash Next** | 177B | 125B | Unsloth | UD-IQ4_XS | 72GB | 3-4GB | 72-73GB | 60-70 | N/A | All experts in RAM |
| **GLM 5.3 Flash** | 320B | 18B | Unsloth | 4-bit | 111GB | 2-3GB | 10-12GB | 47-54 | N/A | 320B total, 18B active |
| **Inkling-2-Mini** | 12B | 12B | Strata | SQ-10 | 11GB | 1-2GB | 8-10GB | 30-40 | 5-10 | 8-24GB GPU recommended |
| **Inkling-2-Mini** | 12B | 12B | Strata | SQ-15 | 14.35GB | 1-2GB | 10-12GB | 25-35 | 3-8 | 16GB GPU recommended |
| **Inkling-2-Mini** | 12B | 12B | Strata | SQ-20 | 19.35GB | 2-3GB | 12-14GB | 20-30 | 2-5 | 24GB GPU recommended |

---

## Engine Comparison

| Engine | Version | Type | AMD Support | Windows | Linux | Mac | Notes |
|--------|---------|------|-------------|---------|-------|-----|-------|
| **Strata** | 0.2.22 | Full-featured | ✅ RDNA 3/4 | ✅ | ✅ | ✅ | GUI + CLI, MoE optimized |
| **Avalon** | latest | llama.cpp fork | ✅ RDNA 3 | ❌ | ✅ | ❌ | 47% faster on 7900 XT for Qwen 3.8B Flash Next |
| **Radiance** | 2.x | Specialist | ✅ RDNA 4 | ❌ | ✅ | ❌ | 4x prefill speed on R9 700 |
| **llama.cpp** | b12757 | General | ✅ | ✅ | ✅ | ✅ | CPU/GPU, baseline |

### Engine Performance on AMD 7900 XT

| Engine | Model | Tokens/sec | Notes |
|--------|-------|------------|-------|
| Avalon | Qwen 3.8B Flash Next IQ3 | **91** | Expert cache optimized |
| Strata | Qwen 3.8B Flash Next IQ3 | ~60 | Baseline |
| Radiance | Qwen 3.8 27B Q4 | 2,868 | Prefill @ 16k tokens (4.2x vs llama.cpp) |
| llama.cpp | Qwen 3.8 27B Q4 | 888 | Prefill @ 16k tokens |
| Strata | Qwen 3.8 27B Q4 | 45-60 | Decode speed |

---

## Tweaks to Test

### 1. Context Length

| Setting | Impact | Recommended | Notes |
|---------|--------|-------------|-------|
| 4096 | Low memory | Minimum | Default in many tools |
| 8192 | Balanced | Default for 12B | Good for most tasks |
| 16384 | High memory | 24GB+ cards | Needed for coding agents |
| 32768 | Very high | 32GB+ cards | Large repos |
| 65536 | Maximum | 48GB+ cards | Full context |

**Test command**:
```bash
# Strata
strata launch --context SIZE

# llama.cpp
./llama-server --ctx-size SIZE

# Ollama
export OLLAMA_CONTEXT_LENGTH=SIZE
```

### 2. Quantization

| Quant | Size Reduction | Speed | Quality | Use Case |
|-------|----------------|-------|---------|----------|
| Q8_0 | 1x (full) | Slowest | Best | Quality critical |
| Q6_K | 1.33x | Slow | Very good | Balanced |
| Q5_K | 1.6x | Medium | Good | Default |
| Q4_K | 2x | Fast | Good | Recommended |
| Q3_K | 2.66x | Faster | OK | Memory constrained |
| Q2_K | 4x | Fastest | Lower | CPU mode |
| IQ4_XS | 2x | Fast | Very good | MoE models |
| IQ3_XXS | 2.66x | Faster | Good | MoE models |
| IQ2_XS | 4x | Fastest | Lower | MoE models |

**Test command**:
```bash
# Download different quantizations
strata launch --model MODEL_NAME

# llama.cpp with different files
./llama-server --model model-Q4_K.gguf
./llama-server --model model-Q3_K.gguf
```

### 3. CPU Threads

| Threads | Impact | Recommended |
|---------|--------|-------------|
| 1 | Slowest | Debugging |
| 2-4 | Slow | Light workloads |
| 4-8 | Balanced | Default |
| 8-16 | Fast | Multi-core CPU |
| auto | Automatic | Best for most |

**Test command**:
```bash
# Strata
strata launch --threads N

# llama.cpp
./llama-server --threads N
```

### 4. KV Cache Compression

| Mode | Memory Savings | Speed Impact | Quality Impact |
|------|----------------|--------------|----------------|
| 16-bit (default) | 1x | Baseline | Baseline |
| 8-bit | 2x | Minimal | None |
| 4-bit | 4x | Noticeable | Minimal |

**Test command**:
```bash
# Strata
strata launch --kv FORMAT  # 16, 8, 4

# llama.cpp
./llama-server --kv-cache-8bit
```

### 5. Speculative Decoding

| Draft Model | Tokens Ahead | Speed Gain | Quality | Best For |
|-------------|--------------|------------|---------|----------|
| B-Flash-2 | 7 | 2.5-2.9x | Identical | Code/JSON |
| B-Flash-2 | 7 | ~2x | Identical | Math |
| B-Flash-2 | 7 | ~1.8x | Identical | Translation |
| B-Flash-2 | 7 | ~1.4x | Identical | Prose |

**Test command**:
```bash
# Strata
strata launch --drafting auto  # or mtp, dflash2

# llama.cpp
./llama-server --draft-model draft.gguf
```

### 6. Parallel Requests

| Parallel | Memory Impact | Speed Impact | Notes |
|----------|---------------|--------------|-------|
| 1 | Baseline | Baseline | Default |
| 2 | +KV cache | +2x | Needs RAM |
| 4 | +2x KV cache | +4x | Needs lots of RAM |
| 8 | +4x KV cache | +8x | Server mode |

**Test command**:
```bash
# Strata
strata launch --parallel N
```

### 7. Memory Offloading (MoE Models)

| Mode | Speed | Memory Usage | Notes |
|------|-------|---------------|-------|
| RAM only | Fastest | High | All experts in RAM |
| SSD streaming | Slow | Low | Experts on SSD |
| Hybrid | Medium | Medium | Hot experts in RAM |

**Test command**:
```bash
# Strata auto-detects based on available memory
strata launch --model iq3_xxs --family qwen
```

### 8. Vision Mode

| Mode | VRAM Usage | Speed | Use Case |
|------|------------|-------|----------|
| off | 0 | Fastest | Text only |
| cpu | 0 | Medium | Any GPU |
| gpu | 1-1.4GB | Fast | 24GB+ GPU |

**Test command**:
```bash
strata launch --vision off  # or cpu, gpu
```

---

## Performance Benchmarks (Expected)

### AMD 7900 XT 24G

| Model | Quant | Context | Tokens/sec | Memory Used | Latency (ms) |
|-------|-------|---------|------------|-------------|--------------|
| Qwen 3.8B Flash Next | IQ3 | 8k | 91 | ~20GB | ~100 |
| Qwen 3.8B Flash Next | IQ3 | 16k | 85 | ~20GB | ~120 |
| Qwen 3.8B Flash Next | IQ3 | 32k | 70 | ~20GB | ~150 |
| Qwen 3.8 27B | Q4 | 8k | 60 | ~17GB | ~150 |
| Qwen 3.8 27B | Q4 | 16k | 55 | ~17GB | ~180 |
| Gemma 4 31B | Q4 | 8k | 70 | ~19GB | ~130 |
| Gemma 4 31B | Q4 | 16k | 65 | ~19GB | ~150 |

### Steam Deck (14GB RAM)

| Model | Quant | Context | Tokens/sec | Memory Used | Latency (ms) |
|-------|-------|---------|------------|-------------|--------------|
| Inkling-2-Mini | SQ-10 | 8k | 5-10 | ~11GB | ~200-400 |
| Phi-3.5-mini | Q4 | 4k | 10-15 | ~5GB | ~100-200 |
| Phi-3.5-mini | Q4 | 8k | 8-12 | ~6GB | ~150-300 |
| Gemma 4 9B | Q4 | 4k | 5-10 | ~6GB | ~200-400 |
| Gemma 4 9B | IQ1_M | 4k | 3-8 | ~8GB | ~250-500 |
| Llama 3.3 8B | Q4 | 4k | 8-12 | ~5GB | ~150-250 |

---

## Test Matrix

### Test 1: Context Length Impact
- Models: Gemma 4 12B, Qwen 3.8 27B
- Context sizes: 4096, 8192, 16384, 32768
- Measure: Tokens/sec, memory usage, latency

### Test 2: Quantization Impact
- Models: Qwen 3.8 27B
- Quantizations: Q4_K, Q3_K, Q2_K
- Measure: Tokens/sec, quality (perplexity), memory

### Test 3: Thread Count Impact
- Models: Gemma 4 12B
- Threads: 1, 2, 4, 8, auto
- Measure: Tokens/sec, CPU usage

### Test 4: KV Cache Compression
- Models: Qwen 3.8 27B Q4
- KV Cache: 16-bit, 8-bit, 4-bit
- Measure: Tokens/sec, context capacity, quality

### Test 5: Speculative Decoding
- Models: Qwen 3.8 27B
- Draft: B-Flash-2 (7 tokens)
- Tasks: Code, JSON, Math, Prose
- Measure: Tokens/sec, quality

### Test 6: Parallel Requests
- Models: Gemma 4 12B
- Parallel: 1, 2, 4
- Measure: Total tokens/sec, memory usage

### Test 7: MoE Expert Caching
- Models: Qwen 3.8B Flash Next
- Cache: RAM only, SSD streaming, Hybrid
- Measure: Tokens/sec, memory usage

### Test 8: Vision Mode
- Models: Qwen 3.8 27B (vision variant)
- Mode: off, cpu, gpu
- Measure: Tokens/sec, VRAM usage

---

## Documentation Template

For each hardware profile, document:

```markdown
# [Hardware Name] - Local AI Setup

## Specifications
- GPU: [model]
- VRAM: [size]
- RAM: [size]
- Architecture: [arch]
- OS: [os]

## Compatible Models
| Model | Quant | Size | Tokens/sec | Status |
|-------|-------|------|------------|--------|

## Recommended Configuration
- Model: [best model]
- Quant: [quantization]
- Context: [size]
- Engine: [engine]
- Threads: [count]

## Test Results
| Test | Value | Notes |
|------|-------|-------|

## Known Issues
- [issue 1]
- [issue 2]

## Setup Commands
```bash
# Installation
# Model download
# Run command
```
```

---

## Quick Start Commands

### AMD 7900 XT (24GB VRAM)
```bash
# Install Strata
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh | bash

# Launch Qwen 3.8B Flash Next (91 tok/s)
strata launch --model iq3_xxs --family qwen --context 16384

# Launch Qwen 3.8 27B (45-60 tok/s)
strata launch --model ud-q4_k_xl --family unsloth --context 16384
```

### Steam Deck (14GB RAM)
```bash
# Install Strata
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh | bash

# Launch Inkling-2-Mini (5-10 tok/s)
strata launch --model sq-10 --family inkling-2-mini --context 8192

# Launch Phi-3.5-mini via llama.cpp CPU
./llama-server --model phi-3.5-mini-Q4_K.gguf --ctx-size 4096 --threads 4 -ngl 0
```

### General CPU Mode
```bash
# Install llama.cpp
wget https://github.com/ggerganov/llama.cpp/releases/download/b12757/llama-linux-x64-avx2 -O llama
chmod +x llama

# Run Gemma 4 12B
./llama --model gemma-4-12b-Q4_K.gguf --ctx-size 8192 --threads 4 -ngl 0
```
