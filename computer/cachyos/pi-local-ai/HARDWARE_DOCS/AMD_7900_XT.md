# AMD Radeon RX 7900 XT 24G: Local AI Setup

**Hardware**: AMD Radeon RX 7900 XT
**VRAM**: 24GB GDDR6
**Memory Bandwidth**: 800 GB/s
**Architecture**: RDNA 3
**Compute Units**: 84
**OS Support**: Linux (best), Windows (limited)

---

## Model Compatibility Table

### Dense Models (Standard Transformers)

| Model | Params | Quant | Size | VRAM Used | RAM Used | Tokens/sec | Engine | Quality Score | Notes |
|-------|--------|-------|------|-----------|----------|------------|--------|----------------|-------|
| **Qwen 3.8 27B** | 27B | Q4 | 16.8GB | 16.8GB | 1-2GB | 45-60 | Strata/llama.cpp | 20.1 | Orca Router build |
| **Qwen 3.8 27B** | 27B | Q5 | 19.5GB | 19.5GB | 1-2GB | 40-55 | Strata/llama.cpp | 20.1 | Higher quality |
| **Gemma 4 31B** | 31B | Q4 | 18.7GB | 18.7GB | 1-2GB | 50-70 | Strata/llama.cpp | ~19.5 | Shorter thinking |
| **Llama 3.3 70B** | 70B | Q4 | 21.5GB | 21.5GB | 1-2GB | 35-50 | llama.cpp | ~21.0 | Tight fit |
| **Gemma 4 12B** | 12B | Q4 | 7.4GB | 7.4GB | 1GB | 80-100 | Strata/llama.cpp | ~18.5 | Fast, low VRAM |
| **Gemma 4 9B** | 9B | Q4 | 5.5GB | 5.5GB | 1GB | 90-110 | Strata/llama.cpp | ~18.0 | Very fast |

### Mixture of Experts (MoE) Models

| Model | Total Params | Active Params | Quant | Size | VRAM Used | RAM Used | Tokens/sec | Engine | Notes |
|-------|--------------|---------------|-------|------|-----------|----------|------------|--------|-------|
| **Qwen 3.8B Flash Next** | 177B | 125B | IQ3 | 89GB | 3-4GB | 8-10GB | **91** | Avalon | Expert cache optimized |
| **Qwen 3.8B Flash Next** | 177B | 125B | IQ3 | 89GB | 3-4GB | 8-10GB | ~60 | Strata | Baseline |
| **Qwen 3.8B Flash Next** | 177B | 125B | IQ2_XS | 39.2GB | 3-4GB | 4-5GB | 85-90 | Strata | Faster, lower quality |
| **Qwen 3.8B Flash Next** | 177B | 125B | IQ3_XXS | 47.0GB | 3-4GB | 6-8GB | 70-80 | Strata | Better quality |
| **GLM 5.3 Flash** | 320B | 18B | 4-bit | 111GB | 2-3GB | 10-12GB | 47-54 | Strata | 320B total, 18B active |

---

## Engine Performance

| Engine | Version | Qwen 3.8B Flash Next | Qwen 3.8 27B | Status | Notes |
|--------|---------|----------------------|--------------|--------|-------|
| **Avalon** | latest | **91 tok/s** | ~45-60 tok/s | Active | 47% faster than Strata for MoE |
| **Strata** | 0.2.22 | ~60 tok/s | ~45-60 tok/s | Active | Mature, multi-model |
| **Radiance** | 2.x | N/A | N/A | Active | RDNA 4 only (R9 700+) |
| **llama.cpp** | b12757 | ~30 tok/s | ~45 tok/s | Stable | Baseline, no MoE optimizations |

### Benchmark Results (Solcer Vienna Test)

| Engine | Model | Prompt Size | Prefill Tokens/sec | Decode Tokens/sec | Notes |
|--------|-------|-------------|---------------------|-------------------|-------|
| Radiance | Qwen 3.8 27B Q4 | 1,000 | 3,002 | N/A | 4.2x vs llama.cpp |
| Radiance | Qwen 3.8 27B Q4 | 16,000 | 2,868 | N/A | 3.2x vs llama.cpp |
| Radiance | Qwen 3.8 27B Q4 | 100,000 | 2,045 | N/A | 3x vs llama.cpp |
| llama.cpp | Qwen 3.8 27B Q4 | 1,000 | 720 | N/A | Baseline |
| llama.cpp | Qwen 3.8 27B Q4 | 16,000 | 888 | N/A | Baseline |
| llama.cpp | Qwen 3.8 27B Q4 | 100,000 | 691 | N/A | Baseline |

**Real-world**: 32,000 token prompt: 36.5s → 11.6s (3.2x faster)

### Speculative Decoding Performance (Solcer Test)

| Content Type | Tokens/sec (No Draft) | Tokens/sec (With Draft) | Speed Gain |
|---------------|------------------------|--------------------------|------------|
| JSON | 46.6 | 135.7 | 2.9x |
| Code | 44.3 | 124.6 | 2.8x |
| Math | ~45 | ~90 | 2.0x |
| Translation | ~45 | ~81 | 1.8x |
| Prose | 33.0 | 44.6 | 1.4x |

---

## Recommended Configurations

### Coding Agent (Best Performance)
- **Model**: Qwen 3.8B Flash Next
- **Quant**: IQ3
- **Engine**: Avalon
- **Context**: 8192-16384
- **Tokens/sec**: 91
- **VRAM**: ~20GB
- **RAM**: 64GB recommended, 32GB minimum
- **Notes**: Expert cache optimized for RDNA 3

### General Reasoning (Best Quality)
- **Model**: Qwen 3.8 27B
- **Quant**: Q4 or Q5
- **Engine**: Strata or llama.cpp
- **Context**: 16384-32768
- **Tokens/sec**: 45-60
- **VRAM**: 16.8-19.5GB
- **Notes**: Strong reasoning, proven performance

### Fast General Use
- **Model**: Gemma 4 31B
- **Quant**: Q4
- **Engine**: Strata or llama.cpp
- **Context**: 8192-16384
- **Tokens/sec**: 50-70
- **VRAM**: 18.7GB
- **Notes**: Shorter thinking drafts (3k chars vs 12k for Qwen)

### Lightweight
- **Model**: Gemma 4 12B or 9B
- **Quant**: Q4
- **Engine**: Strata or llama.cpp
- **Context**: 16384-32768
- **Tokens/sec**: 80-110
- **VRAM**: 5.5-7.4GB
- **Notes**: Fast, low VRAM usage

---

## Setup Commands

### 1. Install Avalon (for Qwen 3.8B Flash Next on 7900 XT)
```bash
# Clone repository
git clone https://github.com/frieren-duck/avalon
cd avalon

# Build
make

# Run server
./avalon-server --model /path/to/qwen3-8b-flash-next-iq3
```

### 2. Install Strata (General Use)
```bash
# Download and run install script
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh -o install.sh
chmod +x install.sh
./install.sh

# Verify
strata --version
```

### 3. Install llama.cpp (Baseline)
```bash
# Download pre-built
curl -L -o llama.tar.gz https://github.com/ggml-org/llama.cpp/releases/download/b12757/llama-b12757-bin-ubuntu-x64.tar.gz
tar -xzf llama.tar.gz
mv llama-b12757 ~/.local/bin/llama.cpp

export PATH="$HOME/.local/bin/llama.cpp:$PATH"
```

---

## Model Download

### Qwen 3.8B Flash Next (ISTA-DASLab)
```bash
# IQ3 (47GB, recommended for 7900 XT)
strata launch --model iq3_xxs --family qwen --context 16384

# Or manual download
wget https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/qwen3-8b-flash-next-iq3_xxs.gguf
```

### Qwen 3.8 27B (Orca Router)
```bash
# Q4 (16.8GB)
wget https://huggingface.co/OrcaRouter/Qwen3.8-27B-GGUF/resolve/main/qwen3.8-27b-Q4_K.gguf

# Q5 (19.5GB)
wget https://huggingface.co/OrcaRouter/Qwen3.8-27B-GGUF/resolve/main/qwen3.8-27b-Q5_K.gguf
```

### Gemma 4 31B
```bash
wget https://huggingface.co/unsloth/gemma-4-31b-GGUF/resolve/main/gemma-4-31b-Q4_K.gguf
```

---

## Run Commands

### Avalon
```bash
# Qwen 3.8B Flash Next
./avalon-server --model /path/to/qwen3-8b-flash-next-iq3 --ctx-size 16384

# With speculative decoding
./avalon-server --model /path/to/model --ctx-size 16384 --draft-model b-flash-2
```

### Strata
```bash
# Qwen 3.8B Flash Next
strata launch --model iq3_xxs --family qwen --context 16384

# Qwen 3.8 27B
strata launch --model ud-q4_k_xl --family unsloth --context 16384

# With 8-bit KV cache
strata launch --model iq3_xxs --family qwen --context 16384 --kv 8
```

### llama.cpp
```bash
# Qwen 3.8 27B
./llama -m qwen3.8-27b-Q4_K.gguf --ctx-size 16384 --threads 8 --kv-cache-8bit

# Server mode
./llama-server -m qwen3.8-27b-Q4_K.gguf --ctx-size 16384 --threads 8 --port 8080
```

---

## Tweaks to Test

### 1. Context Length
```bash
# Test different context sizes
for ctx in 4096 8192 16384 32768; do
  strata launch --model iq3_xxs --family qwen --context $ctx --yes --no-tui
  # Measure tokens/sec
done
```

### 2. KV Cache Compression
```bash
# 8-bit KV cache (doubles context capacity)
strata launch --model iq3_xxs --family qwen --kv 8 --context 32768

# 4-bit KV cache (quadruples context capacity)
strata launch --model iq3_xxs --family qwen --kv 4 --context 65536
```

### 3. Speculative Decoding
```bash
# Enable drafting
strata launch --model iq3_xxs --family qwen --drafting auto

# Specific draft model
strata launch --model iq3_xxs --family qwen --drafting dflash2
```

### 4. Parallel Requests
```bash
# 2 parallel requests
strata launch --model iq3_xxs --family qwen --parallel 2

# 4 parallel requests
strata launch --model iq3_xxs --family qwen --parallel 4
```

### 5. Thread Count
```bash
# Test different thread counts
for threads in 1 2 4 8 16; do
  strata launch --model iq3_xxs --family qwen --threads $threads --yes --no-tui
  # Measure tokens/sec
done
```

### 6. Expert Cache (MoE Models)
```bash
# Monitor expert cache hit rate
# Avalon: built-in expert cache
# Strata: auto-manages based on available memory
```

---

## Performance Optimization

### Critical Settings

1. **Context Length**: Set to 16,000+ minimum
   ```bash
   strata launch --context 16384
   ```

2. **KV Cache**: Enable 8-bit for more context
   ```bash
   strata launch --kv 8
   ```

3. **Speculative Decoding**: Enable for 2-3x speedup
   ```bash
   strata launch --drafting auto
   ```

4. **RAM**: 64GB recommended for MoE models

5. **SSD**: Fast NVMe (7GB/s+) for expert streaming

### Memory Breakdown (Qwen 3.8 27B Q4)

```
Total VRAM:        24,000 MB
Model weights:    16,810 MB (Q4)
KV Cache (16k, 16-bit): 1,000 MB
KV Cache (16k, 8-bit):    500 MB
Overhead:             200 MB
----------------------------------
Remaining (16-bit KV):   5,990 MB (~90k tokens)
Remaining (8-bit KV):    11,490 MB (~180k tokens)
```

---

## Known Issues

1. **Strata GPU Support**: Strata supports RDNA 4 (R9 700+), but 7900 XT is RDNA 3. Use Avalon for best performance.

2. **Avalon Model-Specific**: Avalon is optimized for Qwen 3.8B Flash Next. Other models use default llama.cpp behavior.

3. **Radiance RDNA 4 Only**: Radiance targets RDNA 4 cards (R9 700, R9 790). Not compatible with 7900 XT (RDNA 3).

4. **Multi-GPU**: Two 7900 XT cards: ~130 tok/s single request, ~596 tok/s total for 8 concurrent requests (~75 tok/s each).

---

## Benchmark References

| Source | Test | Hardware | Result |
|--------|------|----------|--------|
| Avalon README | Qwen 3.8B Flash Next | RX 7900 XT | 91 tok/s |
| Solcer Vienna | Qwen 3.8 27B prefill | R9 700 | 3,002 tok/s (4.2x) |
| BizFlow AI | 12 business tasks | R9 700 | 125.5min → 61.7min (2x) |

---

## Hardware-Specific Notes

### What Works Well
✅ Dense models up to 21-22GB (70B params at Q4)
✅ MoE models with expert caching (Qwen 3.8B Flash Next)
✅ Coding agents with structured output (JSON/code = 2.5-2.9x speedup)
✅ Linux (primary support for Avalon/Strata)
✅ Speculative decoding (2.5-2.9x on code/JSON)

### What Doesn't
❌ Windows (Avalon: no Vulkan backend. Strata: limited support)
❌ Qwen 3.8 Flash Next at full precision (needs expert caching)
❌ Multi-user without second card (single user: ~130 tok/s max)
❌ Prose-heavy workloads (only 1.4x speedup from speculative decoding)
❌ RDNA 4 optimizations (Radiance targets R9 700+, not 7900 XT)

---

## Recommended Setup

### For 7900 XT Owner

1. **OS**: Linux (Ubuntu 22.04+ or Debian 13)
2. **Engine**: Avalon for Qwen 3.8B Flash Next, Strata for other models
3. **RAM**: 64GB minimum (32GB works with slowdowns)
4. **Storage**: NVMe SSD (7GB/s+ for expert caching)
5. **Context**: 16,000-32,000
6. **KV Cache**: 8-bit enabled

### Installation
```bash
# Avalon (for Qwen 3.8B Flash Next)
git clone https://github.com/frieren-duck/avalon
cd avalon
make
./avalon-server --model /path/to/qwen3-8b-flash-next-iq3 --ctx-size 32000

# Strata (for other models)
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh | bash
strata launch --model iq3_xxs --family qwen --context 32000 --kv 8

# llama.cpp (for dense models)
./llama -m qwen3.8-27b-Q4_K.gguf --ctx-size 32000 --threads 8 --kv-cache-8bit
```

---

## Links

- [Avalon GitHub](https://github.com/frieren-duck/avalon)
- [Strata GitHub](https://github.com/Niko1221/Strata)
- [Radiance GitHub](https://codeberg.org/still-dead-code/Radiance)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [ISTA-DASLab Models](https://huggingface.co/ISTA-DASLab)
- [OrcaRouter Models](https://huggingface.co/OrcaRouter)
- [Unsloth Models](https://huggingface.co/unsloth)
