#!/usr/bin/env bash
set -euo pipefail

DURATION=11.4
TRANSITION=0.5
FPS=30
WIDTH=1920
HEIGHT=1080
OUTPUT="pastebin_evolution.mp4"
PADDED_DIR="padded"

# Input image list
images=(pastebin_evolution{01..22}.png)

# Ensure ffmpeg is available
command -v ffmpeg >/dev/null || {
  echo "ffmpeg not found"
  exit 1
}

# Preprocess images to uniform padded size
mkdir -p "$PADDED_DIR"
for img in "${images[@]}"; do
  ffmpeg -y -i "$img" -vf "scale=w=${WIDTH}:h=${HEIGHT}:force_original_aspect_ratio=decrease,pad=${WIDTH}:${HEIGHT}:(ow-iw)/2:(oh-ih)/2" "$PADDED_DIR/$img"
done

# Build input args
inputs=()
for img in "${images[@]}"; do
  inputs+=("-loop" "1" "-t" "$DURATION" "-i" "$PADDED_DIR/$img")
done

# Build filter chain with format/setsar
filter=""
for i in "${!images[@]}"; do
  filter+="[$i:v]format=rgba,setsar=1[v$i];"
done

# Build chained xfades without trailing semicolon
xfade_chain=""
for ((i = 1; i < ${#images[@]}; i++)); do
  offset=$(awk "BEGIN {print $i * ($DURATION - $TRANSITION)}")
  in1=$([[ $i -eq 1 ]] && echo "v0" || echo "x$((i - 1))")
  in2="v$i"
  out="x$i"
  xfade="[${in1}][${in2}]xfade=transition=fade:duration=$TRANSITION:offset=$offset[$out]"
  xfade_chain+="$xfade"
  [[ $i -lt $((${#images[@]} - 1)) ]] && xfade_chain+=";"
done

# Merge format and xfade filter chains
filter+="$xfade_chain"

# Final output label
last="x$((${#images[@]} - 1))"

echo "------ FILTER COMPLEX ------"
echo "$filter"
echo "----------------------------"

echo "------ LAST ------"
echo "$last"
echo "----------------------------"

# Generate video

ffmpeg "${inputs[@]}" \
  -filter_complex "$filter" \
  -map "[$last]" \
  -r "$FPS" -c:v libx264 -pix_fmt yuv420p -movflags +faststart "$OUTPUT"

echo "✅ Done: $OUTPUT"
