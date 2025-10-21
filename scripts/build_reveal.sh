#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

build_one() {
  local deckdir="$1"
  local tpl="$deckdir/index.template.html"
  local md="$deckdir/slides.md"
  local out="$deckdir/index.html"

  [[ -f "$tpl" && -f "$md" ]] || { echo "[skip] $deckdir missing template or slides.md"; return; }

  # Replace placeholder with the literal contents of slides.md
  awk -v RS='\\Z' -v mdfile="$md" '
    BEGIN {
      while ((getline line < mdfile) > 0) { md = md line "\n" }
      close(mdfile)
    }
    { gsub(/\\{\\{SLIDES_MD\\}\\}/, md); print }
  ' "$tpl" > "$out"

  echo "[ok] built $out"
}

# Build all decks under docs/slides/**/ that have index.template.html
while IFS= read -r -d '' tpl; do
  build_one "$(dirname "$tpl")"
done < <(find "$ROOT/docs/slides" -type f -name 'index.template.html' -print0)
