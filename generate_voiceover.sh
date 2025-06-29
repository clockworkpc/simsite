#!/usr/bin/env bash

set -e

# Ensure Python and pip are available
command -v python3 >/dev/null || {
  echo "Python3 is required"
  exit 1
}
command -v pip >/dev/null || {
  echo "pip is required"
  exit 1
}

# Install TTS if not already installed
if ! command -v tts >/dev/null; then
  echo "Installing Coqui TTS..."
  pip install TTS
fi

# Model choice (LJSpeech Tacotron2 with vocoder)
MODEL_NAME="tts_models/en/ljspeech/tacotron2-DDC"

# Output file
OUT_WAV="pastebin_evolution.wav"

# Script file
SCRIPT_FILE="pastebin_script.txt"

# Check if script file exists
if [[ ! -f "$SCRIPT_FILE" ]]; then
  echo "Missing voiceover script: $SCRIPT_FILE"
  exit 1
fi

# Run TTS
echo "Generating voiceover..."

# tts --text "$(cat "$SCRIPT_FILE")" \
#   --model_name "tts_models/en/vctk/vits" \
#   --out_path "$OUT_WAV"

tts \
  --text "Hello world" \
  --model_name "tts_models/en/vctk/vits" \
  --speaker_idx 1 \
  --out_path test.wav

echo "✅ Voiceover saved to $OUT_WAV"
