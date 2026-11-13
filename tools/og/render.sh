#!/usr/bin/env bash
# Sosyal medya / OG görsellerini tools/og/template.html'den üretir.
# Kullanım: tools/og/render.sh            (tümü)
#           tools/og/render.sh main tr    (tek konu, tek dil)
# Gereken: Google Chrome (macOS) ve sips. Yeni paket gerekmez.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
TPL="file://$ROOT/tools/og/template.html"
OUT="$ROOT/assets/og"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

VARIANTS=(${1:-main craving plan recovery insights widget})
LANGS=(${2:-tr en})
FORMATS=("landscape:1200,630" "square:1080,1080" "story:1080,1920")

for lang in "${LANGS[@]}"; do
  mkdir -p "$OUT/$lang"
  for v in "${VARIANTS[@]}"; do
    for fmt in "${FORMATS[@]}"; do
      name="${fmt%%:*}"; size="${fmt##*:}"
      png="$TMP/$lang-$v-$name.png"
      "$CHROME" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files \
        --force-device-scale-factor=1 --virtual-time-budget=3000 \
        --window-size="$size" --screenshot="$png" \
        "$TPL?v=$v&f=$name&lang=$lang" >/dev/null 2>&1
      sips -s format jpeg -s formatOptions 86 "$png" --out "$OUT/$lang/$v-$name.jpg" >/dev/null
      echo "✓ assets/og/$lang/$v-$name.jpg"
    done
  done
done
