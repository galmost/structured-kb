# Steam Deck Hardware: Local AI Setup

**Real benchmarks**: [STEAM_DECK_BENCHMARKS.md](STEAM_DECK_BENCHMARKS.md) — 7 models tested.

**Hardware**: AMD Custom APU 0932 / 0405 (Sephiroth), 8 cores (4C/8T), 14GB RAM, AMD Custom GPU 0405 (Sephiroth)
**Architecture**: Zen 2 CPU + RDNA 2 GPU (shared memory)
**VRAM**: ~1-4GB dedicated, rest shared with system RAM

**Previous Context**: Inkling-2-Mini-GGUF options assessed. UD-IQ1_M selected: 8.02GB, 90.2% top-1 accuracy, 0.0867 KLD. UD-IQ1_M fits in 14GB RAM for CPU inference.

---

## Model Compatibility Table

### Dense Models

| Model | Params | Quant | File Size | VRAM Needed | RAM Needed | Tokens/sec | Engine | Status |
|-------|--------|-------|-----------|-------------|------------|------------|--------|--------|
| Gemma 4 9B | 9B | Q4 | 5.5GB | 1-2GB | 5-6GB | 15-20 | Strata | ✅ Works |
| Gemma 4 12B | 12B | Q4 | 7.4GB | 2-3GB | 7-8GB | 10-15 | Strata | ✅ Works |
| Phi-3.5-mini | 3.8B | Q4 | 4.5GB | 1GB | 4-5GB | 15-20 | Strata | ✅ Works |
| Qwen 3.8 27B | 27B | Q3 | 12.3GB | 3-4GB | 12-13GB | 3-5 | Strata | ⚠️ Tight |
| Llama 3.3 8B | 8B | Q4 | 4.7GB | 1GB | 4-5GB | 10-15 | Strata | ✅ Works |

### MoE Models (Expert Models)

| Model | Total Params | Active Params | Quant | File Size | VRAM Needed | RAM Needed | Tokens/sec | Engine | Status |
|-------|--------------|---------------|-------|-----------|-------------|------------|------------|--------|--------|
| Qwen 3.8B Flash Next | 177B | 125B | IQ3 | 89GB | 3-4GB | 8-10GB | 2-5 | Strata | ⚠️ Needs SSD |
| GLM 5.3 Flash | 320B | 18B | 4-bit | 111GB | 2-3GB | 10-12GB | 3-8 | Strata | ⚠️ Needs SSD |

**Note**: MoE models stream expert weights from SSD. Requires fast NVMe.

---

## Engine Performance

| Engine | Version | Installation | Status | Notes |
|--------|---------|--------------|--------|-------|
| **Strata** | 0.2.22 | install.sh | ✅ Installed | CLI + GUI |
| llama.cpp | latest | Manual build | ❌ Not installed | CPU mode possible |
| Avalon | latest | Manual build | ❌ Not installed | AMD RDNA 3 optimized |

---

## Tweaks to Test

### 1. Context Length
```bash
# Strata: default varies by model
strata launch --model gemma-4-12b-q4 --ctx-size 8192

# Test different sizes
--ctx-size 4096   # Conservative
--ctx-size 8192   # Default for 12B
--ctx-size 16384  # Push limits
```

### 2. CPU Offloading
```bash
# Force CPU mode (no GPU)
strata launch --model gemma-4-12b-q4 --device cpu

# Auto (uses GPU if available)
strata launch --model gemma-4-12b-q4 --device auto
```

### 3. Quantization Levels
```bash
# Try different quantizations
strata launch --model gemma-4-12b-q4      # 4-bit
strata launch --model gemma-4-12b-q3      # 3-bit (smaller, slower)
strata launch --model gemma-4-12b-iq2_xs  # 2-bit (smallest)
```

### 4. Thread Count
```bash
# Limit CPU threads
strata launch --model gemma-4-12b-q4 --threads 4

# Use all threads
strata launch --model gemma-4-12b-q4 --threads auto
```

### 5. Speculative Decoding
```bash
# Enable draft model (if available)
strata launch --model gemma-4-12b-q4 --draft-model phi-3-mini
```

### 6. KV Cache
```bash
# 8-bit KV cache (saves memory)
strata launch --model gemma-4-12b-q4 --kv-cache-8bit
```

---

## Setup Commands

### Strata Installation
```bash
# Install via install.sh (user space, no sudo)
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh -o install.sh
chmod +x install.sh
./install.sh

# Verify
strata --version
```

### pipx Installation (for Python CLI tools)
```bash
# Install pipx in user space
python3 -m pip install --user --break-system-packages pipx

# Ensure in PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify
pipx --version
```

---

## Model Download Commands

### Gemma 4 9B
```bash
# Using Strata CLI
strata download gemma-4-9b-q4

# Manual download (Unsloth)
wget https://huggingface.co/unsloth/gemma-4-9b-GGUF/resolve/main/gemma-4-9b-Q4_K.gguf
```

### Gemma 4 12B
```bash
# Using Strata CLI
strata download gemma-4-12b-q4

# Manual download (Unsloth)
wget https://huggingface.co/unsloth/gemma-4-12b-GGUF/resolve/main/gemma-4-12b-Q4_K.gguf
```

### Phi-3.5-mini
```bash
strata download phi-3.5-mini-instruct-4k-fp16
```

---

## Benchmark Results

*To be filled after testing*

| Model | Quant | Context | Tokens/sec | Memory Used | Latency | Notes |
|-------|-------|---------|------------|-------------|---------|-------|
| Gemma 4 9B | Q4 | 4096 | | | | |
| Gemma 4 9B | Q4 | 8192 | | | | |
| Gemma 4 12B | Q4 | 4096 | | | | |
| Gemma 4 12B | Q4 | 8192 | | | | |
| Phi-3.5-mini | Q4 | 4096 | | | | |

---

## Known Issues

1. **Memory constraints**: 14GB RAM limits model size
2. **Shared memory**: GPU uses system RAM, reducing available memory
3. **No dedicated VRAM**: Performance depends on memory bandwidth
4. **Strata auto-detection**: May default to CPU mode on unknown GPU

---

## Recommended Configuration

### For 14GB RAM:
- **Model**: Gemma 4 9B Q4 (5.5GB)
- **Context**: 4096-8192
- **Engine**: Strata
- **Device**: auto (CPU+GPU)
- **Threads**: 4-8

### For Coding:
- **Model**: Phi-3.5-mini Q4 (4.5GB)
- **Context**: 8192
- **Engine**: Strata
- **Device**: auto

---

## Links

- [Strata GitHub](https://github.com/Niko1221/Strata)
- [Strata Models](https://github.com/Niko1221/Strata/blob/main/docs/MODELS.md)
- [Unsloth GGUF](https://huggingface.co/unsloth)
