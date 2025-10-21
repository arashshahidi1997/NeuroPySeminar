#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

build_one() {
  local deckdir="$1"
  local tpl="$deckdir/index.template.html"
  local md="$deckdir/slides.md"
  local out="$deckdir/index.html"

  if [[ ! -f "$tpl" || ! -f "$md" ]]; then
    echo "[skip] $deckdir (missing template or slides.md)"
    return 0
  fi

  # Stream the markdown at the placeholder line, no huge awk variables.
  awk -v mdfile="$md" '
    # When we hit the placeholder (either spelling), delete it and insert the file
    /\{\{SLIDES_MD\}\}|\{\{SLIDE_MD\}\}/ {
      # remove the token(s) from the current line (so nothing literal remains)
      gsub(/\{\{SLIDES_MD\}\}|\{\{SLIDE_MD\}\}/, "");
      print;
      # inject the markdown exactly here
      system("cat \"" mdfile "\"");
      next
    }
    { print }
  ' "$tpl" > "$out"

  echo "[ok] built $out"
}

# Build all decks with a template
while IFS= read -r -d '' tpl; do
  build_one "$(dirname "$tpl")"
done < <(find "$ROOT/docs/slides" -type f -name 'index.template.html' -print0)

# Stage updated HTML (best effort)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git add docs/slides/**/index.html 2>/dev/null || true
fi
