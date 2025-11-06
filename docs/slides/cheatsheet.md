# 🎨 **Slide Deck Cheat Sheet**

A quick reference for creating, updating, and deploying Reveal.js decks in this repo.

---

## 🚀 **Create a New Deck**

```bash
scripts/new_deck.sh my-new-deck "My New Deck Title"
```

✨ **What happens:**

* Creates: `docs/slides/my-new-deck/`
* Adds:

  * `index.template.html` (Reveal.js base)
  * `slides.md` (editable content)
  * `css/local.css` (local overrides)
* Ready to edit immediately!

🧱 **Edit your slides** in `slides.md` using Markdown.

---

## 🌐 **Deploy the Deck (Register in Docs)**

```bash
scripts/new_deck.sh --deploy my-new-deck "My New Deck Title"
```

📋 **Adds your deck to:**

* `mkdocs.yml` under the “Slides” nav group
* `docs/slides/index.md` list (adds an icon + link)

Then build & preview your site:

```bash
scripts/build_reveal.sh my-new-deck
mkdocs serve
```

💡 **Tip:** Run `mkdocs gh-deploy` to publish to GitHub Pages.

---

## ♻️ **Update an Existing Deck**

```bash
scripts/new_deck.sh --update my-existing-deck "Optional New Title"
```

🗄️ **What it does:**

* Backs up current `slides.md` → `slides.md.bk`
* Replaces templates and local CSS
* Keeps your existing registration

✅ Great for syncing new base styles or layout changes without losing your content.

---

## 🧰 **Folder Structure Overview**

```
docs/slides/
├── _shared/             # Shared fragments, themes, and assets
├── bootcamp/            # Template deck (source of new deck scaffolds)
├── my-new-deck/
│   ├── index.template.html
│   ├── slides.md
│   └── css/local.css
└── index.md             # Slide list (auto-updated on --deploy)
```

---

## 🧩 **Embedding Shared Fragments**

You can include reusable snippets:

```markdown
![[_shared/fragments/terminal-setup/section-heading.md]]
```

🔁 Keeps slides DRY (Don’t Repeat Yourself).

---

## ⚙️ **Quick Reference Table**

| 🏷️ Action     | 💻 Command                                  | 📝 Description               |
| -------------- | ------------------------------------------- | ---------------------------- |
| ➕ **Create**   | `scripts/new_deck.sh slug "Title"`          | Make a new deck              |
| 🚀 **Deploy**  | `scripts/new_deck.sh --deploy slug "Title"` | Register deck in site        |
| ♻️ **Update**  | `scripts/new_deck.sh --update slug`         | Backup + refresh scaffold    |
| 🧱 **Build**   | `scripts/build_reveal.sh slug`              | Generate the Reveal.js build |
| 👀 **Preview** | `mkdocs serve`                              | Live local preview           |
| 🌍 **Publish** | `mkdocs gh-deploy`                          | Push to GitHub Pages         |

---

## 🎨 **Customization Tips**

* Global theme → `docs/slides/_shared/css/theme.css`
* Deck-specific tweaks → `docs/slides/<deck>/css/local.css`
* Update template → `docs/slides/bootcamp/index.template.html`

---

> 💡 **Pro Tip:**
> Keep your decks modular — use `_shared/fragments` for any repeated intros, section headings, or code examples.

