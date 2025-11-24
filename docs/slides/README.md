# 🪄 Slide Deck Workflow Guide

This project uses **Reveal.js** slides built via helper scripts.
Use these commands to create, update, and deploy decks quickly.

---

## 🆕 Create a New Deck

```bash
scripts/new_deck.sh my-new-deck "My New Deck Title"
```

**What it does:**

* Creates `docs/slides/my-new-deck/`
* Copies the template `index.template.html`
* Adds `slides.md` scaffold with metadata and starter slides
* Creates a local stylesheet `css/local.css`

You can then edit `slides.md` to add your content.

---

## 🚀 Deploy (Register in Docs)

```bash
scripts/new_deck.sh --deploy my-new-deck "My New Deck Title"
```

**This will:**

* Create the deck (as above)
* Add it under the “Slides” section in `mkdocs.yml`
* Add a bullet link in `docs/slides/index.md`

Then rebuild your site:

```bash
scripts/build_reveal.sh my-new-deck
mkdocs serve
```

---

## ♻️ Update an Existing Deck

```bash
scripts/new_deck.sh --update my-existing-deck "New Title (optional)"
```

**This will:**

* Backup your current `slides.md` → `slides.md.bk`
* Refresh `index.template.html`, `css/local.css`, and scaffold
* Leave any existing registration intact

---

## 🧰 Tips

* All decks live in: `docs/slides/<deck-slug>/`
* Shared assets go in: `docs/slides/_shared/`
* To change global slide look & feel, edit:
  `docs/slides/_shared/css/theme.css`
* You can embed Markdown fragments like:

  ```markdown
  ![[_shared/fragments/example.md]]
  ```

---

## 🧩 Quick Reference

| Action | Command                                     | Notes                 |
| ------ | ------------------------------------------- | --------------------- |
| Create | `scripts/new_deck.sh slug "Title"`          | Fresh deck            |
| Deploy | `scripts/new_deck.sh --deploy slug "Title"` | Registers in MkDocs   |
| Update | `scripts/new_deck.sh --update slug`         | Backs up slides.md    |
| Serve  | `mkdocs serve`                              | Local preview         |
| Build  | `scripts/build_reveal.sh slug`              | Generates reveal deck |

