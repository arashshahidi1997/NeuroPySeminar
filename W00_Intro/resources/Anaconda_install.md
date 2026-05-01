# Installing the course environment with **pixi**

> The course used to ship per-week conda envs (`neuropy-*.yml`). It is now a single
> **pixi** workspace defined in the repository's `pixi.toml` — one shared env
> covering every week.

## 1. Install pixi

Pixi is a single-binary, no-dependencies package manager. It builds isolated
conda+PyPI environments per project from a lockfile.

**macOS / Linux** (one-liner):

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

**Windows** (PowerShell):

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

Restart your shell, then verify:

```bash
pixi --version
```

Other install options (Homebrew, scoop, manual) are listed at
<https://pixi.sh/latest/installation/>.

## 2. Clone the course repo

```bash
git clone https://github.com/arashshahidi1997/NeuroPySeminar.git
cd NeuroPySeminar
```

## 3. Solve and create the environment

From the repo root:

```bash
pixi install
```

This reads `pixi.toml` + `pixi.lock` and materializes the environment in
`./.pixi/envs/default/`. It does **not** modify your global Python install.

## 4. Use it

```bash
pixi shell             # enter the env (like `conda activate`)
pixi run lab           # launch Jupyter Lab inside the env
pixi run kernel        # register an ipykernel named "neuropyseminar"
                       # (so VS Code / classic Jupyter can pick it up)
pixi run test          # run the smoke test
```

To exit `pixi shell`, just type `exit`.

## 5. Adding a package

```bash
pixi add some-package          # conda-forge package
pixi add --pypi some-package   # pip package
```

Both update `pixi.toml` and `pixi.lock` together. Commit both files.

---

### Why pixi instead of conda / Anaconda?

- **Reproducible** — `pixi.lock` pins exact versions across linux / macOS /
  windows. `conda env create -f env.yml` does not.
- **Self-contained** — environment lives in the repo (`./.pixi/`), not in
  `~/anaconda3/envs/`. No collisions between courses.
- **Fast** — Rust-based solver. `pixi install` on a fresh clone takes ~30 s.
- **No Anaconda licensing concerns** — pixi uses conda-forge only.

If you already have Anaconda or Miniconda installed, that's fine — pixi runs
alongside it without conflict.
