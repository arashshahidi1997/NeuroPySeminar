# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# NeuroPySeminar

A teaching seminar repository — *Advances in Data Analysis: Python* (LMU, WiSe 2025/26).
Each week introduces a data analysis method (EMD, multitaper, AR, PCA, ICA, UMAP, CCA,
NNMF, GPFA, SINDy, networks, HMM) through tutorial + exercise Jupyter notebooks.

## Repository structure

The codebase is organized **by week**, not by language or component. Each `Wxx_<Method>/`
folder is self-contained and follows the same shape:

```
Wxx_<Method>/
  tutorial/         # walkthrough notebooks (often imported from upstream library docs)
  exercise/         # student-facing exercise + solution notebooks
  resources/        # papers, supplementary code, data references
  neuropy-<m>.yml   # week-specific conda env (when the method needs special deps)
```

Top-level non-week directories:
- `docs/` — mkdocs-material site source (schedule, announcements, tools, slides) — built to `site/`.
- `notes/` — course content fragments (Assessment, Prerequisites, Papers, etc.) included into `index.md` and the site.
- `bin/src/` — small installable Python package (`setup.py`) used across weeks.
- `scripts/factory/` — Snakemake pipeline (`Snakefile`) that generates teaching artifacts (notebooks, raw materials).
- `bib/`, `animate/`, `png/` — bibliography, animations, figures.
- `tutorials/`, `resources/` — cross-week shared material.

When adding new content for a week, place it inside the matching `Wxx_*/` directory rather than at the repo root.

## DataLad / git-annex

This repo is a **DataLad dataset**. Notebooks and large files are managed via git-annex (see `large-blobs.txt`, `large-paths.txt`). Practical implications:

- The `git status` at the start of a session may show many `D` (deleted) entries for `.ipynb` files — these are annex symlinks that aren't currently retrieved, not actual deletions. Don't "fix" them by recreating files.
- Save with `make save` (runs `datalad save`), push with `make push` (pushes to the github sibling). Don't use bare `git commit`/`git push` for content changes.
- To retrieve an annexed file before reading or editing it, use `datalad get <path>`.

## Projio workspace

This project uses **projio** — a project-centric research assistance ecosystem.
All project knowledge (papers, notes, code libraries, search indexes) is managed
through MCP tools. **Always use MCP tools instead of direct file manipulation**
for projio-managed resources.

At the start of a session, call `project_context()` to understand the workspace
and `runtime_conventions()` to see available Makefile targets.

## Agent tool routing

| Intent | MCP tool | Do NOT |
|--------|----------|--------|
| Understand the project | `project_context()` | Read config files directly |
| See available commands | `runtime_conventions()` | Parse the Makefile manually |
| Search project knowledge | `rag_query(query)` | Grep through docs manually |
| Multi-facet search | `rag_query_multi(queries)` | Run multiple greps |
| Check indexed sources | `corpus_list()` | Inspect Chroma store directly |
| Rebuild search index | `indexio_build()` | Run `indexio build` in terminal |
| Ingest papers by DOI | `biblio_ingest(dois)` | Write BibTeX by hand |
| Look up a paper | `citekey_resolve(citekeys)` | Read .bib files directly |
| Get full paper context | `paper_context(citekey)` | Read docling/GROBID outputs directly |
| Find unresolved refs | `paper_absent_refs(citekey)` | Parse references.json manually |
| Check paper status | `library_get(citekey)` | Read library.yml directly |
| Update paper status | `biblio_library_set(citekeys)` | Edit library.yml directly |
| Merge bibliography | `biblio_merge()` | Run `biblio merge` in terminal |
| Extract full text | `biblio_docling(citekey)` | Run `biblio docling` in terminal |
| Extract references | `biblio_grobid(citekey)` | Run `biblio grobid` in terminal |
| Check GROBID server | `biblio_grobid_check()` | Curl the GROBID API manually |
| Create a note/task/idea | `note_create(note_type)` | Create markdown files directly |
| List recent notes | `note_list()` | List files in notes/ directory |
| Read a note | `note_read(path)` | Read the file directly |
| Search notes | `note_search(query)` | Grep through notes/ |
| Update note metadata | `note_update(path, fields)` | Edit frontmatter directly |
| See note types | `note_types()` | Read notio.toml directly |
| Add a library | `codio_add_urls(urls)` | Edit YAML registry files |
| Find libraries by capability | `codio_discover(query)` | Grep catalog.yml |
| Inspect a library | `codio_get(name)` | Read catalog + profiles manually |
| List all libraries | `codio_list()` | Parse registry files directly |
| Check registry vocabulary | `codio_vocab()` | Read schema docs |
| Validate registry | `codio_validate()` | Run consistency checks manually |

## Workflow conventions

1. **Search first** — check existing knowledge (`rag_query`) before creating new content.
2. **Ingest pipeline** — after `biblio_ingest`, run `biblio_merge` → `biblio_docling` → `biblio_grobid` → `indexio_build`.
3. **Record decisions** — create notes (`note_create`) to capture analysis and decisions rather than scattered comments.
4. **Per-week scope** — when answering a question about a method, look inside that week's folder first; cross-week shared utilities live in `bin/src/` and `tutorials/`.

## Environment (pixi)

This project uses **pixi** for the Python environment. There is **one shared
environment** at the repo root (`pixi.toml` + `pixi.lock`) that covers every
week — including method-specific deps (`emd`, `scikit-learn`, etc.). Do not
add per-week conda `environment.yml` files; add new deps to the root
`pixi.toml` instead.

```bash
pixi install         # solve and create .pixi/envs/default
pixi shell           # enter the env
pixi run lab         # launch Jupyter Lab inside the env
pixi run kernel      # register an ipykernel named "neuropyseminar"
pixi run test        # pytest
pixi add <pkg>       # add a new shared dep (updates pixi.toml + pixi.lock)
```

The lockfile (`pixi.lock`) is committed and must be kept in sync with
`pixi.toml` — run `pixi install` after editing the manifest.

## Development

```bash
make            # see available targets (delegates to .projio/projio.mk)
make save       # datalad save -m "$MSG"
make push       # datalad push --to github
make site-build # mkdocs build via projio
make site-serve # local docs preview
make url        # show project URL
```

Projio targets (`projio-status`, `projio-auth`, `mcp-config`, …) and a Snakemake-based
artifact factory (`scripts/factory/Snakefile`) are also available. The Makefile only
defines `PYTHON`/`DATALAD`/`MSG` and includes `.projio/projio.mk` for everything else,
so check that file when looking for more targets.
