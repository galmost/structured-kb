#!/bin/bash
set -e

MODELS_DIR="$HOME/research/models"
mkdir -p "$MODELS_DIR"

echo "=== Steam Deck Model Download Script ==="
echo "Models: Phi-3.5-mini, Gemma 4 9B, Llama 3.3 8B"
echo "Target: $MODELS_DIR"
echo ""

# Phi-3.5-mini (4.5GB)
echo "[1/4] Downloading Phi-3.5-mini..."
huggingface-cli download \
  unsloth/Phi-3.5-mini-instruct-4k-GGUF \
  phi-3.5-mini-instruct-4k-Q4_K.gguf \
  --local-dir "$MODELS_DIR/phi-3.5-mini" \
  --local-dir-use-symlinks False

# Gemma 4 9B Q4_K (5.5GB)
echo "[2/4] Downloading Gemma 4 9B Q4_K..."
huggingface-cli download \
  unsloth/Gemma-4-9B-GGUF \
  gemma-4-9b-Q4_K.gguf \
  --local-dir "$MODELS_DIR/gemma-4-9b" \
  --local-dir-use-symlinks False

# Gemma 4 9B UD-IQ1_M (8.02GB) - 90.2% accuracy, 0.0867 KLD
echo "[3/4] Downloading Gemma 4 9B UD-IQ1_M..."
huggingface-cli download \
  unsloth/Gemma-4-9B-GGUF \
  gemma-4-9b-UD-IQ1_M.gguf \
  --local-dir "$MODELS_DIR/gemma-4-9b" \
  --local-dir-use-symlinks False

# Llama 3.3 8B (4.7GB)
echo "[4/4] Downloading Llama 3.3 8B..."
huggingface-cli download \
  unsloth/Llama-3.3-8B-Instruct-GGUF \
  llama-3.3-8b-instruct-Q4_K.gguf \
  --local-dir "$MODELS_DIR/llama-3.3-8b" \
  --local-dir-use-symlinks False

echo ""
echo "=== All models downloaded to $MODELS_DIR ==="
echo ""
echo "Verify with: du -sh $MODELS_DIR/*"
