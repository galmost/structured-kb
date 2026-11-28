# Hugging Face CLI: Login and Download Guide

**Purpose**: Download GGUF models from Hugging Face without browser. Required for Steam Deck and headless setups.

**Note**: `huggingface-cli` may not be available as standalone package. Use `huggingface_hub` Python package or `hf-transfer` for fast downloads.

---

## 1. Install Hugging Face Hub Package

```bash
# pip install (user space, no sudo)
python3 -m pip install --user --break-system-packages huggingface-hub hf-transfer

# Verify
python3 -c "from huggingface_hub import hf_hub_download; print('OK')"
```

---

## 2. Login

### Method A: CLI Login (Interactive)
```bash
huggingface-cli login
```
- Opens browser for authentication
- Stores token in `~/.huggingface/token`

### Method B: Token File
```bash
# Create token file
mkdir -p ~/.huggingface
echo "hf_YourTokenHere" > ~/.huggingface/token
chmod 600 ~/.huggingface/token
```

### Method C: Environment Variable
```bash
export HF_TOKEN="hf_YourTokenHere"
```

### Method D: Config File
```bash
# ~/.config/huggingface/hub.yml
hf_token: hf_YourTokenHere
```

**Token Location**: Get from [Hugging Face Settings](https://huggingface.co/settings/tokens)

---

## 3. Download Models

### Single File Download
```bash
# Download single GGUF file
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --local-dir ~/.pi/research/models/phi-3.5-mini \
  --local-dir-use-symlinks False
```

### Download All Files in Repo
```bash
# Download entire repo
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  --local-dir ~/.pi/research/models/phi-3.5-mini \
  --local-dir-use-symlinks False
```

### Download with Pattern
```bash
# Download all Q4_K files
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  --local-dir ~/.pi/research/models/phi-3.5-mini \
  --local-dir-use-symlinks False \
  --ignore-patterns "*.md" \
  --ignore-patterns "*.txt" \
  --ignore-patterns "*.json"
```

### Resume Interrupted Download
```bash
# Continue partial download
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --local-dir ~/.pi/research/models/phi-3.5-mini \
  --resume-download
```

---

## 4. Alternative: hf_hub_download (Python)

```python
from huggingface_hub import hf_hub_download

# Download single file
path = hf_hub_download(
    repo_id='unsloth/Phi-3.5-mini-instruct-4k-GGUF',
    filename='phi-3.5-mini-instruct-4k-Q4_K.gguf',
    local_dir='~/.pi/research/models/phi-3.5-mini'
)
print(f"Downloaded: {path}")
```

**Save as script**:
```bash
cat > ~/.pi/research/scripts/download_model.py << 'EOF'
from huggingface_hub import hf_hub_download
import sys

repo_id = sys.argv[1]
filename = sys.argv[2]
local_dir = sys.argv[3] if len(sys.argv) > 3 else '.'

path = hf_hub_download(
    repo_id=repo_id,
    filename=filename,
    local_dir=local_dir
)
print(f"Downloaded: {path}")
EOF

chmod +x ~/.pi/research/scripts/download_model.py
python3 ~/.pi/research/scripts/download_model.py unsloth/Phi-3.5-mini-instruct-4k-GGUF phi-3.5-mini-instruct-4k-Q4_K.gguf ~/.pi/research/models/phi-3.5-mini
```

---

## 5. Fast Download: aria2c

Hugging Face caps per-connection speed. aria2c uses multiple connections.

### Install aria2c
```bash
# Debian/Ubuntu
pkexec apt install -y aria2

# Arch/CachyOS
paru -S aria2
```

### Download with aria2c
```bash
# Single file, 16 connections
aria2c -x 16 -s 16 -c \
  https://huggingface.co/unsloth/Phi-3.5-mini-instruct-4k-GGUF/resolve/main/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  -d ~/.pi/research/models/phi-3.5-mini \
  -o phi-3.5-mini-instruct-4k-Q4_K.gguf
```

### Download Multiple Files
```bash
# Create URL list
cat > /tmp/download_list.txt << 'EOF'
https://huggingface.co/unsloth/Phi-3.5-mini-instruct-4k-GGUF/resolve/main/phi-3.5-mini-instruct-4k-Q4_K.gguf
https://huggingface.co/unsloth/Gemma-4-9B-GGUF/resolve/main/gemma-4-9b-Q4_K.gguf
https://huggingface.co/unsloth/Gemma-4-9B-GGUF/resolve/main/gemma-4-9b-UD-IQ1_M.gguf
EOF

# Download all with 16 connections each
aria2c -i /tmp/download_list.txt -j 3 -x 16 -s 16 -c \
  --dir=/home/galmost/.pi/research/models \
  --summary-interval=60
```

**Flags**:
- `-x 16`: 16 connections per file
- `-s 16`: 16 segments per file
- `-c`: resume
- `-j 3`: 3 files at once
- `--summary-interval=60`: progress every 60s

### Generate URL List from HF API
```bash
# Get all files from repo
curl -s "https://huggingface.co/api/models/unsloth/Phi-3.5-mini-instruct-4k-GGUF" \
  | python3 -c 'import json,sys; [print(f"https://huggingface.co/unsloth/Phi-3.5-mini-instruct-4k-GGUF/resolve/main/{s['rfilename']}") for s in json.load(sys.stdin)["siblings"] if s["rfilename"].endswith(".gguf")]' \
  > /tmp/gguf_urls.txt

# Download all GGUF files
aria2c -i /tmp/gguf_urls.txt -j 3 -x 16 -s 16 -c \
  --dir=/home/galmost/.pi/research/models/phi-3.5-mini
```

---

## 6. Steam Deck Compatible Models

### Recommended Models (14GB RAM)

| Model | Repo | File | Size | Download Command |
|-------|------|------|------|-----------------|
| **Phi-3.5-mini** | unsloth/Phi-3.5-mini-instruct-4k-GGUF | phi-3.5-mini-instruct-4k-Q4_K.gguf | 4.5GB | `huggingface-cli download unsloth/Phi-3.5-mini-instruct-4k-GGUF phi-3.5-mini-instruct-4k-Q4_K.gguf` |
| **Gemma 4 9B** | unsloth/Gemma-4-9B-GGUF | gemma-4-9b-Q4_K.gguf | 5.5GB | `huggingface-cli download unsloth/Gemma-4-9B-GGUF gemma-4-9b-Q4_K.gguf` |
| **Gemma 4 9B** | unsloth/Gemma-4-9B-GGUF | gemma-4-9b-UD-IQ1_M.gguf | 8.02GB | `huggingface-cli download unsloth/Gemma-4-9B-GGUF gemma-4-9b-UD-IQ1_M.gguf` |
| **Llama 3.3 8B** | unsloth/Llama-3.3-8B-Instruct-GGUF | llama-3.3-8b-instruct-Q4_K.gguf | 4.7GB | `huggingface-cli download unsloth/Llama-3.3-8B-Instruct-GGUF llama-3.3-8b-instruct-Q4_K.gguf` |
| **Mistral 7B** | TheBloke/Mistral-7B-Instruct-v0.2-GGUF | mistral-7b-instruct-v0.2.Q4_K.gguf | 4.1GB | `huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K.gguf` |

### Alternative Repos (Public)

| Model | Repo | Notes |
|-------|------|-------|
| Phi-3-mini | TheBloke/Phi-3-mini-4k-instruct-GGUF | 1.7GB |
| TinyLlama | TheBloke/TinyLlama-1.1B-GGUF | 1.1GB |
| MiniLM | TheBloke/MiniLM-L12-HF-GGUF | 0.5GB |

---

## 7. Download Scripts

### Script: Download Steam Deck Models
```bash
cat > ~/.pi/research/scripts/download_steamdeck_models.sh << 'SCRIPT'
#!/bin/bash
set -e

MODELS_DIR="$HOME/research/models"
mkdir -p "$MODELS_DIR"

# Phi-3.5-mini (4.5GB)
echo "Downloading Phi-3.5-mini..."
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --local-dir "$MODELS_DIR/phi-3.5-mini" \
  --local-dir-use-symlinks False

# Gemma 4 9B (5.5GB)
echo "Downloading Gemma 4 9B..."
huggingface-cli download \
  unsloth/Gemma-4-9B-GGUF \
  gemma-4-9b-Q4_K.gguf \
  --local-dir "$MODELS_DIR/gemma-4-9b" \
  --local-dir-use-symlinks False

# Gemma 4 9B UD-IQ1_M (8.02GB)
echo "Downloading Gemma 4 9B UD-IQ1_M..."
huggingface-cli download \
  unsloth/Gemma-4-9B-GGUF \
  gemma-4-9b-UD-IQ1_M.gguf \
  --local-dir "$MODELS_DIR/gemma-4-9b" \
  --local-dir-use-symlinks False

# Llama 3.3 8B (4.7GB)
echo "Downloading Llama 3.3 8B..."
huggingface-cli download \
  unsloth/Llama-3.3-8B-Instruct-GGUF \
  llama-3.3-8b-instruct-Q4_K.gguf \
  --local-dir "$MODELS_DIR/llama-3.3-8b" \
  --local-dir-use-symlinks False

echo "All models downloaded to $MODELS_DIR"
SCRIPT

chmod +x ~/.pi/research/scripts/download_steamdeck_models.sh
```

### Script: aria2c Fast Download
```bash
cat > ~/.pi/research/scripts/download_aria2c.sh << 'SCRIPT'
#!/bin/bash
set -e

MODELS_DIR="$HOME/research/models"
mkdir -p "$MODELS_DIR"

# Create URL list
cat > /tmp/model_urls.txt << 'EOF'
https://huggingface.co/unsloth/Phi-3.5-mini-instruct-4k-GGUF/resolve/main/phi-3.5-mini-instruct-4k-Q4_K.gguf
https://huggingface.co/unsloth/Gemma-4-9B-GGUF/resolve/main/gemma-4-9b-Q4_K.gguf
https://huggingface.co/unsloth/Gemma-4-9B-GGUF/resolve/main/gemma-4-9b-UD-IQ1_M.gguf
https://huggingface.co/unsloth/Llama-3.3-8B-Instruct-GGUF/resolve/main/llama-3.3-8b-instruct-Q4_K.gguf
EOF

# Download with aria2c
aria2c -i /tmp/model_urls.txt -j 3 -x 16 -s 16 -c \
  --dir="$MODELS_DIR" \
  --summary-interval=60 \
  --auto-file-renaming=false

# Clean up
rm -f /tmp/model_urls.txt

echo "Download complete. Files in $MODELS_DIR"
SCRIPT

chmod +x ~/.pi/research/scripts/download_aria2c.sh
```

---

## 8. Verify Downloads

```bash
# Check file sizes
du -sh ~/.pi/research/models/*

# Verify GGUF files
file ~/.pi/research/models/*/*.gguf

# Count downloaded files
find ~/.pi/research/models -name "*.gguf" | wc -l
```

---

## 9. Run Models with llama.cpp

### Phi-3.5-mini
```bash
./llama \
  -m ~/.pi/research/models/phi-3.5-mini/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --ctx-size 4096 \
  --threads 4 \
  -ngl 0 \
  --color
```

### Gemma 4 9B
```bash
./llama \
  -m ~/.pi/research/models/gemma-4-9b/gemma-4-9b-Q4_K.gguf \
  --ctx-size 4096 \
  --threads 4 \
  -ngl 0 \
  --color
```

### Server Mode
```bash
./llama-server \
  -m ~/.pi/research/models/phi-3.5-mini/phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --ctx-size 4096 \
  --threads 4 \
  -ngl 0 \
  --port 8080
```

---

## 10. Troubleshooting

### 401/403 Authentication Error
```bash
# Verify token
huggingface-cli whoami

# Re-login
huggingface-cli login

# Check token file
cat ~/.huggingface/token
```

### Download Stalls
```bash
# Use aria2c instead
aria2c -x 16 -s 16 -c <url>

# Lower connections
aria2c -x 4 -s 4 -c <url>
```

### Out of Disk Space
```bash
# Check available space
df -h

# Clean up old files
rm -rf ~/.pi/research/models/old_model
```

### File Not Found
```bash
# List repo files
huggingface-cli repo list unsloth/Phi-3.5-mini-instruct-4k-GGUF

# Check exact filename
huggingface-cli ls unsloth/Phi-3.5-mini-instruct-4k-GGUF
```

---

## 11. Token Management

### Show Token
```bash
huggingface-cli whoami
```

### Logout
```bash
huggingface-cli logout
```

### Check Token Permissions
```bash
# List accessible repos
huggingface-cli repo list --full
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install | `python3 -m pip install --user --break-system-packages huggingface-hub` |
| Login | `huggingface-cli login` |
| Download | `huggingface-cli download repo file --local-dir dir` |
| List files | `huggingface-cli ls repo` |
| Who am I | `huggingface-cli whoami` |
| Logout | `huggingface-cli logout` |

---

## Links

- [Hugging Face Hub CLI Docs](https://huggingface.co/docs/huggingface_hub/en/guides/cli)
- [Hugging Face Tokens](https://huggingface.co/settings/tokens)
- [aria2c Manual](https://aria2.github.io/manual/en/html/aria2c.html)
- [Unsloth GGUF Models](https://huggingface.co/unsloth)
