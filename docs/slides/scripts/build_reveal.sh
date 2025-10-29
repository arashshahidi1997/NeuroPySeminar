#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/build_reveal.sh            # build all decks
#   scripts/build_reveal.sh bootcamp   # build only these slugs
#   scripts/build_reveal.sh bootcamp emd

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
VAULT="$REPO_ROOT"                      # treat repo as the vault
SLIDES_ROOT="$REPO_ROOT/docs/slides"

command -v obsidian-export >/dev/null || { echo "ERROR: obsidian-export not found"; exit 1; }

# If deck slugs passed, limit build set; else build all deck dirs with a template
if (( $# > 0 )); then
  mapfile -t DECK_DIRS < <(for d in "$@"; do echo "$SLIDES_ROOT/$d"; done)
else
  mapfile -t DECK_DIRS < <(find "$SLIDES_ROOT" -mindepth 1 -maxdepth 1 -type d ! -name "_shared")
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Export vault once so all embeds resolve
obsidian-export "$VAULT" "$TMP" >/dev/null

# tiny function: extract YAML front matter key from exported slides.md
yqval() { # yqval key file
  awk -v k="$1" '
    BEGIN{inY=0}
    /^---[ \t]*$/ { c++; inY=(c==1); next }
    (inY && $0 ~ "^"k":[ ]") {
      sub("^"k":[ ]*", "", $0); print; exit
    }' "$2"
}

for DIR in "${DECK_DIRS[@]}"; do
  TPL="$DIR/index.template.html"
  [ -f "$TPL" ] || { echo "WARN: no index.template.html in $(basename "$DIR")"; continue; }

  REL="${DIR#$SLIDES_ROOT/}"                   # slug
  EXPORTED_MD="$TMP/docs/slides/$REL/slides.md"
  [ -f "$EXPORTED_MD" ] || { echo "WARN: no exported slides.md for $REL"; continue; }

  OUT="$DIR/index.html"

  # Read metadata from exported MD (front matter preserved by obsidian-export)
  TITLE="$(yqval title "$EXPORTED_MD" || true)"
  THEME="$(yqval theme "$EXPORTED_MD" || true)"
  WIDTH="$(yqval width "$EXPORTED_MD" || true)"
  HEIGHT="$(yqval height "$EXPORTED_MD" || true)"

  # Prepare replacements
  MD_ESCAPED=$(sed -e 's/[\/&]/\\&/g' -e 's/$/\\n/' "$EXPORTED_MD" | tr -d '\n')

  # Clone template into a buffer and do safe replacements:
  HTML="$(cat "$TPL")"
  # Inject slides
  HTML="${HTML//\{\{SLIDES_MD\}\}/$MD_ESCAPED}"

  # Optional: adjust <title> if front matter provided
  if [[ -n "${TITLE:-}" ]]; then
    HTML="$(printf "%s" "$HTML" | sed -E "s#<title>.*</title>#<title>${TITLE//\//\\/}</title>#")"
  fi
  # Optional: swap theme link id=theme if THEME set
  if [[ -n "${THEME:-}" ]]; then
    HTML="$(printf "%s" "$HTML" | sed -E "s#(theme/)[a-zA-Z0-9_-]+(.css\" id=\"theme\")#\1${THEME}\2#")"
  fi
  # Optional: adjust Reveal size if provided
  if [[ -n "${WIDTH:-}" || -n "${HEIGHT:-}" ]]; then
    HTML="$(printf "%s" "$HTML" \
      | sed -E "s/(width:\s*)[0-9]+/\1${WIDTH:-1280}/" \
      | sed -E "s/(height:\s*)[0-9]+/\1${HEIGHT:-720}/")"
  fi

  printf "%s" "$HTML" > "$OUT"
  echo "Built $OUT"
done
