#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE >&2
Usage:
  scripts/new_deck.sh <deck-slug> [Title]
  scripts/new_deck.sh --deploy <deck-slug> [Title]
Options:
  -d, --deploy   Also register deck in mkdocs.yml and docs/slides/index.md
USAGE
  exit 1
}

DEPLOY=false
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--deploy) DEPLOY=true; shift ;;
    -h|--help) usage ;;
    *) ARGS+=("$1"); shift ;;
  esac
done
set -- "${ARGS[@]}"

[[ $# -ge 1 ]] || usage

SLUG="$1"
TITLE="${2:-$(echo "$SLUG" | tr '-' ' ' | sed 's/\b./\u&/g')}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DECK_DIR="$REPO_ROOT/docs/slides/$SLUG"
BOOTCAMP_DIR="$REPO_ROOT/docs/slides/bootcamp"

if [[ -d "$DECK_DIR" ]]; then
  echo "Deck '$SLUG' already exists at $DECK_DIR" >&2
  exit 1
fi

mkdir -p "$DECK_DIR/css"

# Use bootcamp template as a base; fall back to a fresh template if missing
TPL_SRC="$BOOTCAMP_DIR/index.template.html"
if [[ -f "$TPL_SRC" ]]; then
  cp "$TPL_SRC" "$DECK_DIR/index.template.html"
else
  cat > "$DECK_DIR/index.template.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Deck</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/black.css" id="theme" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/monokai.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-copycode@1.3.2/plugin/copycode/copycode.css" />
  <link rel="stylesheet" href="../_shared/css/theme.css" />
  <link rel="stylesheet" href="./css/local.css" />
</head>
<body>
  <div class="reveal"><div class="slides">
    <section data-markdown
             data-separator="^\n---\n$"
             data-separator-vertical="^\n--\n$"
             data-separator-notes="^Note:"
             data-charset="utf-8">
      <textarea data-template>
{{SLIDES_MD}}
      </textarea>
    </section>
  </div></div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/markdown/markdown.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-copycode@1.3.2/plugin/copycode/copycode.js"></script>
  <script>
    Reveal.initialize({
      hash: true,
      slideNumber: true,
      navigationMode: 'linear',
      width: 1280, height: 720, margin: 0.04,
      pdfSeparateFragments: false, pdfMaxPagesPerSlide: 1,
      transition: 'slide', backgroundTransition: 'fade',
      copycode: { button: "hover", display: "icons", timeout: 1200 },
      plugins: [ RevealMarkdown, RevealNotes, RevealHighlight, CopyCode ]
    });
  </script>
</body>
</html>
HTML
fi

# Copy local.css seed if present
if [[ -f "$BOOTCAMP_DIR/css/local.css" ]]; then
  cp "$BOOTCAMP_DIR/css/local.css" "$DECK_DIR/css/local.css"
else
  : > "$DECK_DIR/css/local.css"
fi

# slides.md scaffold
cat > "$DECK_DIR/slides.md" <<MD
---
title: "$TITLE"
author: "Sirota Lab"
theme: "black"
width: 1280
height: 720
---

# $TITLE

Welcome! Replace this content with your slides.

---

## Example Fragment Embed

![[../_shared/fragments/terminal-setup/section-heading.md]]

---

## Outro

Thank you!
MD

echo "✅ Created new deck: $DECK_DIR"

if ! $DEPLOY; then
  echo "Run: scripts/build_reveal.sh $SLUG"
  exit 0
fi

###############################################
# --deploy: register in mkdocs.yml and slides index
###############################################

MKDOCS="$REPO_ROOT/mkdocs.yml"
SLIDES_INDEX="$REPO_ROOT/docs/slides/index.md"
DECK_URL="slides/$SLUG/index.html"
# 1) Append to mkdocs.yml under the Slides nav group with correct indent
if [[ -f "$MKDOCS" ]]; then
  tmpfile="$(mktemp)"
  awk -v title="$TITLE" -v url="$DECK_URL" '
    function insert_line() {
      printf("%s- %s: %s\n", item_indent, title, url)
      inserted=1
    }
    BEGIN {
      in_slides=0
      inserted=0
      item_indent="      "   # sensible default: 6 spaces under "  - Slides:"
      base_indent=0
    }
    {
      print $0

      # Detect the start of the Slides group: capture its indent
      if ($0 ~ /^[[:space:]]*-[[:space:]]+Slides:/) {
        in_slides=1
        match($0, /^([[:space:]]*)-[[:space:]]Slides:/, m)
        base_indent = length(m[1])
        next
      }

      if (in_slides) {
        # Any list item line: figure out its indent
        if ($0 ~ /^[[:space:]]*-[[:space:]]/) {
          match($0, /^([[:space:]]*)-[[:space:]]/, m)
          cur_indent = length(m[1])

          if (cur_indent <= base_indent) {
            # We hit the next top-level/sibling group -> insert before leaving
            if (!inserted) insert_line()
            in_slides=0
          } else {
            # This is an item inside Slides: remember its indent (e.g., 6 spaces)
            item_indent = substr($0, 1, cur_indent)
          }
        }
      }
    }
    END {
      # If file ended while still in Slides, insert now
      if (in_slides && !inserted) insert_line()
    }
  ' "$MKDOCS" > "$tmpfile"
  mv "$tmpfile" "$MKDOCS"
  echo "✅ Registered in mkdocs.yml → Slides → $TITLE"
else
  echo "WARN: $MKDOCS not found; skipping mkdocs.yml registration" >&2
fi

# 2) Append to docs/slides/index.md bullets before any placeholder line, else at end
if [[ -f "$SLIDES_INDEX" ]]; then
  # Choose an icon based on slug (very simple heuristic)
  ICON="🧠"
  case "$SLUG" in
    emd) ICON="📊" ;;
    *bootcamp*) ICON="🧠" ;;
  esac

  # Build the bullet line
  BULLET="- [$ICON $TITLE]($SLUG/index.html)"

  if grep -qE '^\s*>\s*to be added' "$SLIDES_INDEX"; then
    # Insert before the placeholder line
    tmpfile="$(mktemp)"
    awk -v bullet="$BULLET" '
      BEGIN{done=0}
      {
        if (!done && $0 ~ /^[[:space:]]*>\s*to be added/) {
          print bullet
          done=1
        }
        print $0
      }
      END{
        if (!done) print bullet
      }
    ' "$SLIDES_INDEX" > "$tmpfile"
    mv "$tmpfile" "$SLIDES_INDEX"
  else
    # Append at end
    echo "$BULLET" >> "$SLIDES_INDEX"
  fi
  echo "✅ Added to docs/slides/index.md"
else
  echo "WARN: $SLIDES_INDEX not found; skipping slides index registration" >&2
fi

echo "Now build and serve:"
echo "  scripts/build_reveal.sh $SLUG"
echo "  mkdocs serve   # or: mkdocs gh-deploy"
