#!/usr/bin/env bash
set -euo pipefail

# Build all or selected decks.
#   scripts/build_reveal.sh
#   scripts/build_reveal.sh bootcamp emd

export LC_ALL=C.UTF-8

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SLIDES_ROOT="$REPO_ROOT/docs/slides"
SHARED_DIR="$SLIDES_ROOT/_shared"

command -v obsidian-export >/dev/null || { echo "ERROR: obsidian-export not found"; exit 1; }
command -v rsync >/dev/null || { echo "ERROR: rsync not found"; exit 1; }
command -v python3 >/dev/null || { echo "ERROR: python3 not found"; exit 1; }

# --- discover decks -----------------------------------------------------------
if (( $# > 0 )); then
  mapfile -t DECK_DIRS < <(for d in "$@"; do echo "$SLIDES_ROOT/$d"; done)
else
  mapfile -t DECK_DIRS < <(find "$SLIDES_ROOT" -mindepth 1 -maxdepth 1 -type d ! -name "_shared" | sort)
fi

# --- helpers -----------------------------------------------------------------
yqval() { # yqval key file   (extracts a simple scalar from YAML front matter)
  awk -v k="$1" '
    BEGIN{inY=0; dash=0}
    /^[[:space:]]*---[[:space:]]*$/ { dash++; if (dash==1) inY=1; else if (dash==2) exit; next }
    inY && $0 ~ "^[[:space:]]*"k":[[:space:]]" {
      sub("^[[:space:]]*"k":[[:space:]]*", "", $0); print; exit
    }' "$2" || true
}

first_h1() { # file -> first line starting with "# "
  awk '/^# /{sub(/^# /,""); print; exit}' "$1" || true
}

# --- build loop ---------------------------------------------------------------
built_any=false
for DIR in "${DECK_DIRS[@]}"; do
  slug="${DIR##*/}"
  TPL="$DIR/index.template.html"
  OUT="$DIR/index.html"

  if [[ ! -f "$TPL" ]]; then
    echo "WARN: [$slug] missing index.template.html — skipping"
    continue
  fi

  # Create a tiny per-deck "subset vault": {_shared, this deck}
  SUBSET="$(mktemp -d)"; EXPORT_DIR="$(mktemp -d)"
  cleanup() { rm -rf "$SUBSET" "$EXPORT_DIR"; }
  trap cleanup EXIT

  mkdir -p "$SUBSET"
  [[ -d "$SHARED_DIR" ]] && rsync -a "$SHARED_DIR" "$SUBSET/" >/dev/null
  rsync -a "$DIR" "$SUBSET/" >/dev/null

  # Export just this subset so embeds resolve but other decks can't break it
  if ! obsidian-export "$SUBSET" "$EXPORT_DIR" >/dev/null 2>&1; then
    echo "ERROR: [$slug] obsidian-export failed (likely non-UTF8 in this deck)."
    cleanup; trap - EXIT
    continue
  fi

  EXPORTED_MD="$EXPORT_DIR/$slug/slides.md"
  if [[ ! -f "$EXPORTED_MD" ]]; then
    echo "WARN: [$slug] exported slides.md not found — skipping"
    cleanup; trap - EXIT
    continue
  fi

  # ---- metadata: deck.env > YAML > first H1 ---------------------------------
  TITLE=""; THEME="black"; WIDTH="1280"; HEIGHT="720"
  [[ -f "$DIR/deck.env" ]] && source "$DIR/deck.env"

  # If YAML exists in exported file, it will be clean UTF-8 here
  if [[ -z "${TITLE:-}" ]]; then TITLE="$(yqval title  "$EXPORTED_MD" || true)"; fi
  if [[ -n "$(yqval theme  "$EXPORTED_MD" || true)" ]]; then THEME="$(yqval theme "$EXPORTED_MD")"; fi
  if [[ -n "$(yqval width  "$EXPORTED_MD" || true)" ]]; then WIDTH="$(yqval width "$EXPORTED_MD")"; fi
  if [[ -n "$(yqval height "$EXPORTED_MD" || true)" ]]; then HEIGHT="$(yqval height "$EXPORTED_MD")"; fi
  if [[ -z "${TITLE:-}" ]]; then TITLE="$(first_h1 "$EXPORTED_MD")"; fi

  # ---- inject exported markdown into template -------------------------------
  python3 - "$TPL" "$EXPORTED_MD" "$OUT" <<'PY'
import io, sys
tpl, md, out = sys.argv[1:4]
with io.open(tpl, 'r', encoding='utf-8', newline='') as f: html = f.read()
with io.open(md,  'r', encoding='utf-8', newline='') as f: body = f.read()
html = html.replace("{{SLIDES_MD}}", body)
with io.open(out, 'w', encoding='utf-8', newline='') as f: f.write(html)
PY

  # ---- apply metadata to HTML ----------------------------------------------
  # title
  if [[ -n "${TITLE:-}" ]]; then
    esc_title="${TITLE//\//\\/}"
    sed -E -i "s#<title>.*</title>#<title>${esc_title}</title>#g" "$OUT"
  fi
  # theme (id="theme" href=".../theme/<name>.css")
  if [[ -n "${THEME:-}" ]]; then
    esc_theme="${THEME//\//\\/}"
    sed -E -i 's#(href="[^"]*/theme/)[A-Za-z0-9_-]+(.css"[^>]*id="theme")#\1REPL\2#g' "$OUT"
    sed -E -i "s#REPL#${esc_theme}#g" "$OUT"
  fi
  # dimensions
  sed -E -i "s/(width:[[:space:]]*)[0-9]+/\1${WIDTH}/" "$OUT"
  sed -E -i "s/(height:[[:space:]]*)[0-9]+/\1${HEIGHT}/" "$OUT"

  # sanity: ensure placeholder is gone
  if grep -q "{{SLIDES_MD}}" "$OUT"; then
    echo "ERROR: [$slug] injection failed (placeholder still present)."
    cleanup; trap - EXIT
    continue
  fi

  echo "Built $slug: 
        $OUT"
  built_any=true
  cleanup; trap - EXIT
done

$built_any || { echo "Nothing built."; exit 0; }
