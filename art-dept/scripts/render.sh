#!/usr/bin/env bash
# render.sh <name> <width_in> <height_in> [--pdf-only|--png-only]
# Renders <name>.html -> <name>.pdf (print) and <name>.png (preview) via headless Chrome.
set -euo pipefail
NAME="${1:?usage: render.sh <name> <width_in> <height_in>}"
W_IN="${2:?width in inches}"
H_IN="${3:?height in inches}"
MODE="${4:-both}"

CHROME="${CHROME:-}"
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "$(command -v google-chrome || true)" \
         "$(command -v chromium || true)"; do
  [ -n "$CHROME" ] && break
  [ -x "$c" ] && CHROME="$c"
done
[ -n "$CHROME" ] || { echo "no Chrome/Chromium found; set CHROME=" >&2; exit 1; }

HTML="$(cd "$(dirname "$NAME")" && pwd)/$(basename "$NAME").html"
[ -f "$HTML" ] || { echo "missing $HTML" >&2; exit 1; }
BASE="${HTML%.html}"

# 192dpi preview keeps QR/fiducial probes meaningful
PX_W=$(python3 -c "print(int($W_IN*192))")
PX_H=$(python3 -c "print(int($H_IN*192))")

if [ "$MODE" != "--png-only" ]; then
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$BASE.pdf" "file://$HTML" 2>/dev/null
  echo "wrote $BASE.pdf"
fi
if [ "$MODE" != "--pdf-only" ]; then
  "$CHROME" --headless --disable-gpu --window-size="$PX_W,$PX_H" \
    --screenshot="$BASE.png" "file://$HTML" 2>/dev/null
  echo "wrote $BASE.png (${PX_W}x${PX_H})"
fi
