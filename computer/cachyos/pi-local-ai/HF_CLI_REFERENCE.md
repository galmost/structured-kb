# HF CLI Reference: Complete Guide

**Tool**: `hf` - Hugging Face Hub CLI (system package, `/usr/bin/hf`)
**Version**: hf_hub/2.4.0
**Status**: ✅ Authenticated (user: Galmost90, OAuth token in `~/.cache/huggingface/token`)

---

## How We Use It (Actual Workflow)

### 1. Check Auth
```bash
hf auth whoami        # -> user=Galmost90
hf auth token         # -> hf_oauth_...
```

### 2. Discover Models
```bash
# List files in a repo
hf models list unsloth/Qwen3.5-4B-GGUF -R

# Search via API
curl -s "https://huggingface.co/api/models?author=unsloth&search=qwen3.5" \
  | python3 -c "import sys,json; print([m['id'] for m in json.load(sys.stdin)])"
```

### 3. Download (Working Command Pattern)
```bash
hf download REPO_ID FILENAME --local-dir DIR --max-workers 4

# Examples used:
hf download unsloth/Inkling-2-Mini-GGUF Inkling-2-Mini-UD-IQ3_XXS.gguf --local-dir ~/.pi/research/models/inkling-2-mini --max-workers 8
hf download unsloth/gemma-4-E4B-it-GGUF gemma-4-E4B-it-UD-IQ3_XXS.gguf --local-dir ~/.pi/research/models/gemma-4-e4b --max-workers 4
hf download unsloth/Qwen3.5-4B-GGUF Qwen3.5-4B-UD-IQ2_XXS.gguf --local-dir ~/.pi/research/models/qwen3.5-4b --max-workers 4
hf download unsloth/Qwen3.5-9B-GGUF Qwen3.5-9B-Q4_K_S.gguf --local-dir ~/.pi/research/models/qwen3.5-9b --max-workers 4
hf download unsloth/Qwen2.5-Coder-7B-Instruct-GGUF Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf --local-dir ~/.pi/research/models/qwen2.5-coder-7b --max-workers 4
```

**Key flags**:
- `--local-dir`: save to specific folder (creates if missing)
- `--max-workers N`: parallel downloads (4-8 works well)
- `-R` on `models list`: recursive file listing

### 4. Download Script
```bash
~/.pi/research/scripts/hf_download_steamdeck.sh   # downloads all Steam Deck models
```

---

## Installed Models (via hf CLI)

| Model | Repo | File | Size | Downloaded |
|-------|------|------|------|------------|
| Inkling-2-Mini | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-IQ3_XXS.gguf | 11GB | ✅ |
| Gemma-4-E4B | unsloth/gemma-4-E4B-it-GGUF | gemma-4-E4B-it-UD-IQ3_XXS.gguf | 3.5GB | ✅ |
| Gemma-4-12B | unsloth/gemma-4-12b-it-GGUF | gemma-4-12b-it-UD-IQ3_XXS.gguf | 4.4GB | ✅ |
| Qwen3.8-27B | unsloth/Qwen3.8-27B-GGUF | Qwen3.8-27B-UD-IQ3_XXS.gguf | 11GB | ✅ |
| Qwen3.5-4B | unsloth/Qwen3.5-4B-GGUF | Qwen3.5-4B-UD-IQ2_XXS.gguf | 1.5GB | ✅ |
| Qwen3.5-9B | unsloth/Qwen3.5-9B-GGUF | Qwen3.5-9B-Q4_K_S.gguf | 5.1GB | ✅ |
| Qwen2.5-Coder-7B | unsloth/Qwen2.5-Coder-7B-Instruct-GGUF | Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf | 4.4GB | ✅ |

---

## 1. Authentication Commands

### Login
```bash
# Interactive browser login
hf auth login

# Login with token
hf auth login --token hf_YourTokenHere
```

### Logout
```bash
# Logout from current token
hf auth logout

# Logout from specific token
hf auth logout --token hf_YourTokenHere
```

### Token Management
```bash
# List all stored tokens
hf auth list

# Show current token
hf auth token

# Switch between tokens
hf auth switch

# Check current user
hf auth whoami
```

**Output**: `user=Galmost90` (currently authenticated)

---

## 2. Download Commands

### Download Single File
```bash
hf download REPO_ID FILENAME --local-dir DIR

# Example: Download Inkling-2-Mini Q4_K_XL
hf download unsloth/Inkling-2-Mini-GGUF Inkling-2-Mini-UD-Q4_K_XL.gguf \
  --local-dir ~/.pi/research/models/inkling-2-mini
```

### Download Multiple Files
```bash
hf download REPO_ID FILE1 FILE2 FILE3 --local-dir DIR

# Example: Download all Q4_K files
hf download unsloth/Inkling-2-Mini-GGUF \
  Inkling-2-Mini-UD-Q4_K_M.gguf \
  Inkling-2-Mini-UD-Q4_K_S.gguf \
  Inkling-2-Mini-UD-Q4_K_XL.gguf \
  --local-dir ~/.pi/research/models/inkling-2-mini
```

### Download Entire Repo
```bash
# Download all files
hf download unsloth/Inkling-2-Mini-GGUF --local-dir ~/.pi/research/models/inkling-2-mini

# Download with pattern
hf download unsloth/Inkling-2-Mini-GGUF --include "*.gguf" \
  --local-dir ~/.pi/research/models/inkling-2-mini
```

### Download Options
```bash
# Force download (skip cache)
hf download REPO_ID FILE --force-download

# Resume interrupted download
hf download REPO_ID FILE --force-download

# Specific revision
hf download REPO_ID FILE --revision main

# Multiple workers (faster)
hf download REPO_ID FILE --max-workers 16
```

---

## 3. Model Discovery

### List Files in Repo
```bash
# List files (non-recursive)
hf models list REPO_ID

# List files recursively
hf models list REPO_ID -R

# Example
hf models list unsloth/Inkling-2-Mini-GGUF -R
```

### Get Model Info
```bash
hf models info REPO_ID

# Example
hf models info unsloth/Inkling-2-Mini-GGUF
```

### Get Model Card
```bash
hf models card REPO_ID

# Example
hf models card unsloth/Inkling-2-Mini-GGUF
```

---

## 4. Repository Management

### List Repos
```bash
# List all repos (models, datasets, spaces)
hf repos ls

# List with limit
hf repos ls --limit 10

# List by type
hf repos ls --type model
```

### Create Repo
```bash
hf repos create REPO_ID --type model --private

# Example
hf repos create my-model --type model
```

### Copy Files
```bash
# Copy from repo to local
hf repos cp REPO_ID/FILE LOCAL_PATH

# Example
hf repos cp unsloth/Inkling-2-Mini-GGUF/Inkling-2-Mini-UD-Q4_K_XL.gguf .
```

---

## 5. Steam Deck Compatible Models

### Verified Repos (Public, GGUF Available)

| Model | Repo | Recommended File | Size | Tokens/sec (CPU) | Memory |
|-------|------|-----------------|------|------------------|---------|
| **Inkling-2-Mini** | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-Q4_K_XL.gguf | 17.6GB | 5-10 | ~18GB |
| **Inkling-2-Mini** | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-Q4_K_M.gguf | 16.6GB | 5-10 | ~17GB |
| **Inkling-2-Mini** | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-Q4_K_S.gguf | 15.3GB | 5-10 | ~16GB |
| **Inkling-2-Mini** | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-IQ4_XS.gguf | 11.6GB | 5-10 | ~12GB |
| **Inkling-2-Mini** | unsloth/Inkling-2-Mini-GGUF | Inkling-2-Mini-UD-IQ3_XXS.gguf | 10.9GB | 5-10 | ~11GB |
| **Gemma-4-E4B** | unsloth/gemma-4-E4B-it-GGUF | gemma-4-E4B-it-Q4_K_S.gguf | 4.8GB | 15-20 | ~5GB |
| **Gemma-4-E4B** | unsloth/gemma-4-E4B-it-GGUF | gemma-4-E4B-it-UD-IQ3_XXS.gguf | 3.7GB | 10-15 | ~4GB |
| **Gemma-4-12B** | unsloth/gemma-4-12b-it-GGUF | gemma-4-12b-it-Q4_K_S.gguf | 6.8GB | 8-12 | ~7GB |
| **Gemma-4-12B** | unsloth/gemma-4-12b-it-GGUF | gemma-4-12b-it-UD-IQ3_XXS.gguf | 4.6GB | 5-10 | ~5GB |
| **Qwen3.8-27B** | unsloth/Qwen3.8-27B-GGUF | Qwen3.8-27B-UD-Q4_K_S.gguf | 15.4GB | 3-5 | ~16GB |
| **Qwen3.8-27B** | unsloth/Qwen3.8-27B-GGUF | Qwen3.8-27B-UD-IQ3_XXS.gguf | 10.9GB | 3-5 | ~11GB |

### Download Commands for Steam Deck

```bash
# Inkling-2-Mini Q4_K_S (15.3GB)
hf download unsloth/Inkling-2-Mini-GGUF Inkling-2-Mini-UD-Q4_K_S.gguf \
  --local-dir ~/.pi/research/models/inkling-2-mini

# Gemma-4-E4B Q4_K_S (4.8GB)
hf download unsloth/gemma-4-E4B-it-GGUF gemma-4-E4B-it-Q4_K_S.gguf \
  --local-dir ~/.pi/research/models/gemma-4-e4b

# Gemma-4-12B Q4_K_S (6.8GB)
hf download unsloth/gemma-4-12b-it-GGUF gemma-4-12b-it-Q4_K_S.gguf \
  --local-dir ~/.pi/research/models/gemma-4-12b

# Qwen3.8-27B Q4_K_S (15.4GB)
hf download unsloth/Qwen3.8-27B-GGUF Qwen3.8-27B-UD-Q4_K_S.gguf \
  --local-dir ~/.pi/research/models/qwen-3.8-27b
```

---

## 6. AMD 7900 XT Compatible Models

| Model | Repo | Recommended File | Size | Tokens/sec | VRAM |
|-------|------|-----------------|------|------------|------|
| **Qwen 3.8 27B** | unsloth/Qwen3.8-27B-GGUF | Qwen3.8-27B-UD-Q4_K_S.gguf | 15.4GB | 45-60 | 16.8GB |
| **Qwen 3.8 27B** | unsloth/Qwen3.8-27B-GGUF | Qwen3.8-27B-UD-IQ3_XXS.gguf | 10.9GB | 40-55 | 12.3GB |
| **Gemma-4-12B** | unsloth/gemma-4-12b-it-GGUF | gemma-4-12b-it-Q4_K_S.gguf | 6.8GB | 50-70 | 7.4GB |
| **Gemma-4-31B** | unsloth/gemma-4-31B-it-GGUF | gemma-4-31B-it-Q4_K_S.gguf | 19.5GB | 45-60 | 18.7GB |

---

## 7. Scripts

### Script: Download Steam Deck Models
```bash
cat > ~/.pi/research/scripts/hf_download_steamdeck.sh << 'SCRIPT'
#!/bin/bash
set -e

MODELS_DIR="$HOME/research/models"
mkdir -p "$MODELS_DIR"

echo "=== Downloading Steam Deck Models ==="

# Inkling-2-Mini Q4_K_S (15.3GB, fits in 14GB RAM with room)
echo "[1/4] Inkling-2-Mini Q4_K_S..."
hf download unsloth/Inkling-2-Mini-GGUF Inkling-2-Mini-UD-Q4_K_S.gguf \
  --local-dir "$MODELS_DIR/inkling-2-mini" \
  --max-workers 8

# Gemma-4-E4B Q4_K_S (4.8GB, fast)
echo "[2/4] Gemma-4-E4B Q4_K_S..."
hf download unsloth/gemma-4-E4B-it-GGUF gemma-4-E4B-it-Q4_K_S.gguf \
  --local-dir "$MODELS_DIR/gemma-4-e4b" \
  --max-workers 8

# Gemma-4-12B Q4_K_S (6.8GB, good balance)
echo "[3/4] Gemma-4-12B Q4_K_S..."
hf download unsloth/gemma-4-12b-it-GGUF gemma-4-12b-it-Q4_K_S.gguf \
  --local-dir "$MODELS_DIR/gemma-4-12b" \
  --max-workers 8

# Qwen3.8-27B Q4_K_S (15.4GB, best reasoning)
echo "[4/4] Qwen3.8-27B Q4_K_S..."
hf download unsloth/Qwen3.8-27B-GGUF Qwen3.8-27B-UD-Q4_K_S.gguf \
  --local-dir "$MODELS_DIR/qwen-3.8-27b" \
  --max-workers 8

echo ""
echo "=== All models downloaded ==="
echo "Verify: du -sh $MODELS_DIR/*"
SCRIPT

chmod +x ~/.pi/research/scripts/hf_download_steamdeck.sh
```

### Script: List Available Models
```bash
cat > ~/.pi/research/scripts/hf_list_models.sh << 'SCRIPT'
#!/bin/bash

echo "=== Steam Deck Compatible Models ==="
echo ""

for repo in \
  unsloth/Inkling-2-Mini-GGUF \
  unsloth/gemma-4-E4B-it-GGUF \
  unsloth/gemma-4-12b-it-GGUF \
  unsloth/Qwen3.8-27B-GGUF
do
  echo "--- $repo ---"
  hf models list $repo -R | grep ".gguf$" | head -5
  echo ""
done
SCRIPT

chmod +x ~/.pi/research/scripts/hf_list_models.sh
```

---

## 8. Useful Commands

### Check Authentication
```bash
hf auth whoami
hf auth token
```

### List All Files
```bash
hf models list REPO_ID -R
```

### Download with Pattern
```bash
hf download REPO_ID --include "*.gguf" --local-dir DIR
```

### Download with Exclude
```bash
hf download REPO_ID --exclude "*.md" --exclude "*.txt" --local-dir DIR
```

### Multiple Workers (Faster)
```bash
hf download REPO_ID FILE --max-workers 16 --local-dir DIR
```

---

## 9. Troubleshooting

### 401 Authentication Error
```bash
# Re-login
hf auth login

# Verify token
hf auth whoami

# Check token permissions
# Visit: https://huggingface.co/settings/tokens
```

### Model Not Found
```bash
# List available models
hf models list ORG_NAME

# Check exact repo name
curl -s "https://huggingface.co/api/models?author=ORG_NAME" | python3 -m json.tool
```

### Download Stalls
```bash
# Use more workers
hf download REPO_ID FILE --max-workers 16

# Or use aria2c
aria2c -x 16 -s 16 -c URL
```

### Out of Disk Space
```bash
# Check space
df -h

# Clean cache
hf cache clean
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Login | `hf auth login` |
| Logout | `hf auth logout` |
| Who am I | `hf auth whoami` |
| List tokens | `hf auth list` |
| Download | `hf download REPO FILE --local-dir DIR` |
| List files | `hf models list REPO -R` |
| Model info | `hf models info REPO` |
| Model card | `hf models card REPO` |
| List repos | `hf repos ls` |
| Copy file | `hf repos cp REPO/FILE LOCAL` |

---

## Links

- [HF CLI Docs](https://huggingface.co/docs/huggingface_hub/en/guides/cli)
- [HF Hub Python Library](https://huggingface.co/docs/huggingface_hub)
- [Unsloth GGUF Models](https://huggingface.co/unsloth)
- [Steam Deck Models](https://huggingface.co/models?search=GGUF)
