# Setup Guide: Local AI on Current Hardware

**Current Hardware**: AMD Custom APU 0932 / 0405 (Sephiroth), 8 cores (4C/8T), 14GB RAM, AMD Custom GPU 0405 (Sephiroth)
**OS**: CachyOS Linux (Arch-based)
**Architecture**: Zen 2 CPU + RDNA 2 GPU (shared memory)

---

## Software Installed

| Tool | Version | Location | Status |
|------|---------|----------|--------|
| **Strata** | 0.2.22 | ~/.local/bin/strata | ✅ Installed |
| **llama.cpp** | b12757 | ~/.local/bin/llama.cpp/ | ✅ Installed |
| **pipx** | 1.19.1 | ~/.local/bin/pipx | ✅ Installed |
| **pip** | 26.3 | ~/.local/bin/pip | ✅ Installed |
| **huggingface-hub** | latest | Python package | ✅ Installed |

---

## Installation Commands

### 1. pipx (Python CLI tool installer)
```bash
# Install pipx in user space (no sudo, no system breakage)
python3 -m pip install --user --break-system-packages pipx

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify
pipx --version
```

### 2. Strata (Inference Engine)
```bash
# Download and run install script
curl -L https://github.com/Niko1221/Strata/releases/latest/download/install.sh -o install.sh
chmod +x install.sh
./install.sh

# Verify
strata --version
```

**Note**: Strata does NOT support AMD Custom GPU 0405 (Steam Deck) yet. Use CPU mode or llama.cpp.

### 3. llama.cpp (CPU/GPU Inference)
```bash
# Download pre-built Ubuntu binary
curl -L -o llama.tar.gz https://github.com/ggml-org/llama.cpp/releases/download/b12757/llama-b12757-bin-ubuntu-x64.tar.gz
tar -xzf llama.tar.gz
mv llama-b12757 ~/.local/bin/llama.cpp

# Add to PATH
export PATH="$HOME/.local/bin/llama.cpp:$PATH"

# Verify
llama --version
```

---

## Model Setup

### Model Sources

| Source | Models | Format | Notes |
|--------|--------|--------|-------|
| **Unsloth** | Gemma 4, Llama 3, Phi-3, Qwen | GGUF | Recommended |
| **ISTA-DASLab** | Qwen 3.8B Flash Next | GGUF | MoE models |
| **Hugging Face** | All models | GGUF, Safetensors | Direct download |
| **Strata** | Qwen, Inkling, Hy4-Flash | Strata format | Engine-specific |

### Recommended Models for 14GB RAM

| Model | Params | Quant | Size | Engine | Tokens/sec (CPU) | Memory Used | Notes |
|-------|--------|-------|------|--------|------------------|-------------|-------|
| **Inkling-2-Mini** | 12B | SQ-10 | 11GB | Strata | 5-10 | ~11GB | Strata format, vision |
| **Phi-3.5-mini** | 3.8B | Q4_K | 4.5GB | llama.cpp | 10-15 | ~5GB | Fast, good quality |
| **Gemma 4 9B** | 9B | Q4_K | 5.5GB | llama.cpp | 5-10 | ~6GB | Balanced |
| **Gemma 4 9B** | 9B | UD-IQ1_M | 8.02GB | llama.cpp | 3-8 | ~8GB | 90.2% accuracy, 0.0867 KLD |
| **Gemma 4 12B** | 12B | Q4_K | 7.4GB | llama.cpp | 3-7 | ~8GB | Tight fit |
| **Llama 3.3 8B** | 8B | Q4_K | 4.7GB | llama.cpp | 8-12 | ~5GB | Good alternative |

**Previous Context**: Inkling-2-Mini-GGUF options assessed. UD-IQ1_M selected: 8.02GB, 90.2% top-1 accuracy, 0.0867 KLD. UD-IQ1_M fits in 14GB RAM for CPU inference.

### Model Download Commands

#### Using Strata (for Strata-format models)
```bash
# List available models
strata models list --all

# Set up model (Strata will download)
strata launch --model sq-10 --family inkling-2-mini --context 8192 --vision off
```

#### Using huggingface-hub (Python)
```bash
# Install if not already
python3 -m pip install --user --break-system-packages huggingface-hub

# Download single file
python3 - <<'EOF'
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id='unsloth/Phi-3.5-mini-instruct-4k-GGUF',
    filename='phi-3.5-mini-instruct-4k-Q4_K.gguf',
    local_dir='~/.pi/research/models/phi-3.5-mini'
)
print(f"Downloaded: {path}")
EOF
```

#### Manual Download (curl/wget)
```bash
# Phi-3.5-mini Q4_K (4.5GB)
mkdir -p ~/.pi/research/models/phi-3.5-mini
cd ~/.pi/research/models/phi-3.5-mini
wget https://huggingface.co/unsloth/Phi-3.5-mini-instruct-4k-GGUF/resolve/main/phi-3.5-mini-instruct-4k-Q4_K.gguf

# Gemma 4 9B Q4_K (5.5GB)
mkdir -p ~/.pi/research/models/gemma-4-9b
cd ~/.pi/research/models/gemma-4-9b
wget https://huggingface.co/unsloth/gemma-4-9b-GGUF/resolve/main/gemma-4-9b-Q4_K.gguf

# Gemma 4 9B UD-IQ1_M (8.02GB)
wget https://huggingface.co/unsloth/gemma-4-9b-GGUF/resolve/main/gemma-4-9b-UD-IQ1_M.gguf
```

**Note**: Hugging Face requires authentication for some models. Use `huggingface-cli login` or HF_TOKEN environment variable.

---

## Run Commands

### Strata (for Strata-format models)
```bash
# CPU mode (no GPU)
strata launch --model sq-10 --family inkling-2-mini --context 8192 --vision off --backend auto

# With specific settings
strata launch --model sq-10 --family inkling-2-mini --context 8192 --vision off --threads 4 --kv 8
```

### llama.cpp (for GGUF models)
```bash
# CPU mode, no GPU
./llama -m ~/.pi/research/models/phi-3.5-mini/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --ctx-size 4096 \
  --threads 4 \
  -ngl 0

# With 8-bit KV cache
./llama -m ~/.pi/research/models/phi-3.5-mini/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --ctx-size 8192 \
  --threads 4 \
  -ngl 0 \
  --kv-cache-8bit

# Server mode
./llama-server -m ~/.pi/research/models/phi-3.5-mini/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --ctx-size 4096 \
  --threads 4 \
  -ngl 0 \
  --port 8080
```

---

## Configuration Files

### ~/.bashrc or ~/.zshrc Additions
```bash
# Add user binaries to PATH
export PATH="$HOME/.local/bin:$HOME/.local/bin/llama.cpp:$PATH"

# Strata
export STRATA_DATA_DIR="$HOME/research/models"

# For Hugging Face authentication
export HF_TOKEN="your_token_here"
```

---

## Testing Workflow

### 1. Verify Installation
```bash
# Check versions
strata --version
llama --version
pipx --version
```

### 2. Download Test Model
```bash
# Download Phi-3.5-mini (small, fast)
mkdir -p ~/.pi/research/models/phi-3.5-mini
cd ~/.pi/research/models/phi-3.5-mini
# Use Strata or manual download
```

### 3. Run Benchmark
```bash
# llama.cpp benchmark
./llama -m phi-3.5-mini-instruct-4k-Q4_K.gguf --bench 100 --threads 4 -ngl 0

# Strata benchmark (if model is Strata format)
strata launch --model sq-10 --family inkling-2-mini --context 8192 --yes --no-tui
```

### 4. Test Different Settings
```bash
# Context sizes
for ctx in 1024 2048 4096 8192; do
  echo "Testing context: $ctx"
  ./llama -m model.gguf --ctx-size $ctx --threads 4 -ngl 0 --bench 50
  echo "---"
done

# Thread counts
for threads in 1 2 4 8; do
  echo "Testing threads: $threads"
  ./llama -m model.gguf --threads $threads -ngl 0 --bench 50
  echo "---"
done
```

---

## Troubleshooting

### Strata: GPU Not Supported
**Error**: "Strata couldn't find an engine for this computer"
**Fix**: Use CPU mode or llama.cpp
```bash
# Force CPU mode
strata launch --backend auto  # May still try GPU
# Use llama.cpp instead
./llama -m model.gguf -ngl 0
```

### Hugging Face: 401/403 Authentication Error
**Error**: "Repository Not Found" or "401 Client Error"
**Fix**: Add HF_TOKEN
```bash
export HF_TOKEN="your_huggingface_token"
# Or use huggingface-cli login
```

### Out of Memory
**Error**: "alloc failed" or "bad_alloc"
**Fix**: Use smaller model or lower context
```bash
# Use smaller model
./llama -m smaller-model.gguf --ctx-size 2048

# Use 8-bit KV cache
./llama -m model.gguf --kv-cache-8bit --ctx-size 4096
```

### Slow Performance
**Issue**: Low tokens/sec
**Fix**: Try different settings
```bash
# Increase threads
./llama -m model.gguf --threads 8 -ngl 0

# Use different quantization
./llama -m model-Q3_K.gguf --threads 4 -ngl 0
```

---

## Performance Expectations

| Model | Quant | Context | Tokens/sec (CPU) | Memory Used | Use Case |
|-------|-------|---------|------------------|-------------|----------|
| Phi-3.5-mini | Q4_K | 4096 | 10-15 | ~5GB | Chat, coding |
| Phi-3.5-mini | Q4_K | 8192 | 8-12 | ~6GB | Longer context |
| Gemma 4 9B | Q4_K | 4096 | 5-10 | ~6GB | General |
| Gemma 4 9B | UD-IQ1_M | 4096 | 3-8 | ~8GB | Better quality |
| Inkling-2-Mini | SQ-10 | 8192 | 5-10 | ~11GB | Vision capable |

---

## Next Steps

1. **Download models** - Use Strata or manual download
2. **Run benchmarks** - Test different settings
3. **Document results** - Fill in performance tables
4. **Create hardware-specific docs** - For Steam Deck and 7900 XT

---

## Links

- [Strata GitHub](https://github.com/Niko1221/Strata)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [Unsloth GGUF Models](https://huggingface.co/unsloth)
- [Hugging Face Hub](https://huggingface.co)
