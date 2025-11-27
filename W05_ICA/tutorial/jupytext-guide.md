# Jupytext Sync Guide

This short guide captures the exact commands we used (and you can re-run) for keeping our Python scripts and notebooks paired via [Jupytext](https://github.com/mwouts/jupytext). All commands below assume you are inside the repository root (`/storage2/arash/teaching/NeuroPySeminar/W05_ICA/tutorial`) and you invoke Jupytext through the shared environment:

```bash
/storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext ...
```

or simply activate the `neuropy-env` beforehand and run:

```bash
jupytext ...
```

---

## 1. Single-file sync

Use these commands when you want to pair or refresh a single script/notebook:

1. **Create or update the notebook from a script**

   ```bash
   /storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext --to ipynb scripts/<name>.py
   ```

   This writes `<name>.ipynb` next to the script. Add `--output notebooks/<name>.ipynb` to store it elsewhere.

2. **Set pairing metadata (one-time per file)**

   ```bash
   /storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext --set-formats "notebooks//ipynb,scripts//py:percent" scripts/<name>.py
   ```

   This embeds the pairing info into the script/notebook metadata so future syncs know where each counterpart lives.

3. **Subsequent round trips**

   ```bash
   /storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext --sync scripts/<name>.py
   ```

   Jupytext compares timestamps between the `.py` and `.ipynb` versions and updates whichever side is older.

---

## 2. Folder-to-folder sync

When you want every script in `scripts/` to stay paired with a notebook in `notebooks/`, use a repository-level config plus bulk commands.

1. **Configuration file**

   Ensure `.jupytext.toml` contains:

   ```toml
   formats = "notebooks//ipynb,scripts//py:percent"
   ```

   This tells Jupytext that anything under `scripts/` should sync with `notebooks/` using the percent format.

2. **One-time metadata injection for existing scripts**

   ```bash
   for f in scripts/*.py; do
       /storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext --set-formats "notebooks//ipynb,scripts//py:percent" "$f"
   done
   ```

   Now every script knows it is paired with the notebook located in `notebooks/` with the same basename.

3. **Bulk synchronization**

   ```bash
   /storage/share/python/environments/Anaconda3/envs/neuropy-env/bin/python -m jupytext --sync scripts/*.py
   ```

   This command walks through all scripts, compares them with their corresponding notebooks under `notebooks/`, and updates whichever representation is older. Because the `.toml` defines the pairing, no extra flags are required.

4. **Cleanup tip**

   If you previously had `.ipynb` files sitting next to your scripts, remove them after creating the paired versions in `notebooks/` to avoid confusion:

   ```bash
   rm scripts/*.ipynb
   ```

---

With this workflow, you can edit either the `.py` or `.ipynb` files and use `--sync` to propagate changes. Commit both the scripts and notebooks (plus `.jupytext.toml`) so collaborators can choose their preferred environment.***
