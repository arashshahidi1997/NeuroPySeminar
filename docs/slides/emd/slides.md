set -euo pipefail

# create slides.md ONLY if it's missing (bootcamp + bootcamp-ii preserved)
for d in emd; do
  if [[ ! -f "/slides.md" ]]; then
    cat > "/slides.md" <<'MD'
# EMD — Intro

Welcome! Replace this with your EMD deck content.

---

## What is EMD?

- Short definition…
- Why it matters…

---

## Example

