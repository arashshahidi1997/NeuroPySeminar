#!/usr/bin/env bash
set -euo pipefail

# Build all or a subset of decks
#   scripts/build_reveal.sh
#   scripts/build_reveal.sh bootcamp emd

export LC_ALL=C.UTF-8
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLIDES_ROOT="$REPO_ROOT/docs/slides"
VAULT="$SLIDES_ROOT"

command -v obsidian-export >/dev/null || { echo "ERROR: obsidian-export not found"; exit 1; }

# Determine which deck directories to build
if (( $# > 0 )); then
  mapfile -t DECK_DIRS < <(for d in "$@"; do echo "$SLIDES_ROOT/$d"; done)
else
  mapfile -t DECK_DIRS < <(find "$SLIDES_ROOT" -mindepth 1 -maxdepth 1 -type d ! -name "_shared")
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Export once so all embeds are resolved and front matter is normalized
obsidian-export "$VAULT" "$TMP" >/dev/null

# Extract a single scalar from YAML front matter in exported MD
yqval() { # yqval key file
  awk -v k="$1" '
    BEGIN { inY=0; dash=0 }
    /^[[:space:]]*---[[:space:]]*$/ { dash++; if (dash==1) inY=1; else if (dash==2) exit; next }
    inY && $0 ~ "^[[:space:]]*"k":[[:space:]]" {
      sub("^[[:space:]]*"k":[[:space:]]*", "", $0)
      print
      exit
    }
  ' "$2"
}

for DIR in "${DECK_DIRS[@]}"; do
  TPL="$DIR/index.template.html"
  [ -f "$TPL" ] || { echo "WARN: no index.template.html in $(basename "$DIR")"; continue; }

  REL="${DIR#$SLIDES_ROOT/}"              # slug, used to find export path
  EXPORTED_MD="$TMP/$REL/slides.md"
  [ -f "$EXPORTED_MD" ] || { echo "WARN: no exported slides.md for $REL"; continue; }

  OUT="$DIR/index.html"

  # Front matter from exported MD (obsidian-export preserves it)
  TITLE="$(yqval title  "$EXPORTED_MD" || true)"
  THEME="$(yqval theme  "$EXPORTED_MD" || true)"
  WIDTH="$(yqval width  "$EXPORTED_MD" || true)"
  HEIGHT="$(yqval height "$EXPORTED_MD" || true)"

  # ---------- Injection option A: sed (placeholder must be on its own line) ----------
  # This replaces any line that is exactly the placeholder with the file content,
  # preserving real newlines.
  #
  # sed "/{{SLIDES_MD}}/ {
  #   r $EXPORTED_MD
  #   d
  # }" "$TPL" > "$OUT"

  # ---------- Injection option B: Python (works mid-line as well) ----------
  python3 - "$TPL" "$EXPORTED_MD" "$OUT" <<'PY'
import io, sys, re

tpl_path, md_path, out_path = sys.argv[1:4]
with io.open(tpl_path, 'r', encoding='utf-8', newline='') as f:
    html = f.read()
with io.open(md_path, 'r', encoding='utf-8', newline='') as f:
    md = f.read()

# Replace all occurrences of the placeholder with the raw markdown (real newlines preserved)
html = html.replace("{{SLIDES_MD}}", md)

with io.open(out_path, 'w', encoding='utf-8', newline='') as f:
    f.write(html)
PY

  # Optional tweaks on the generated HTML -------------------------------

  # Update <title>…</title> safely if TITLE provided
  if [[ -n "${TITLE:-}" ]]; then
    # escape forward slashes for sed
    esc_title="${TITLE//\//\\/}"
    sed -E -i "s#<title>.*</title>#<title>${esc_title}</title>#g" "$OUT"
  fi

  # Swap theme href ending in theme/*.css if THEME provided (expects id="theme")
  if [[ -n "${THEME:-}" ]]; then
    esc_theme="${THEME//\//\\/}"
    sed -E -i "s#(href=\".*?/theme/)[A-Za-z0-9_-]+(.css\"[^>]*id=\"theme\")#\1${esc_theme}\2#g" "$OUT"
  fi

  # Adjust Reveal size if provided (fallbacks keep existing value if unset)
  if [[ -n "${WIDTH:-}" || -n "${HEIGHT:-}" ]]; then
    [[ -n "${WIDTH:-}"  ]] && sed -E -i "s/(width:[[:space:]]*)[0-9]+/\1${WIDTH}/" "$OUT"
    [[ -n "${HEIGHT:-}" ]] && sed -E -i "s/(height:[[:space:]]*)[0-9]+/\1${HEIGHT}/" "$OUT"
  fi

  echo "Built $OUT"
done
