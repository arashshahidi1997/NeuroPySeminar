# Cloning the course and running notebooks

> The course migrated from per-week conda envs to a single **pixi** workspace.
> See `Anaconda_install.md` for installing pixi itself.

## 1. Clone the repository

```bash
git clone https://github.com/arashshahidi1997/NeuroPySeminar.git
cd NeuroPySeminar
```

## 2. Create the environment (one-time)

```bash
pixi install
```

## 3. Open a week's notebook

```bash
pixi run lab           # opens Jupyter Lab in the repo root
```

Then in the file browser, navigate to e.g. `W01_EMD/tutorial/` and open a
notebook. Make sure the kernel is set to **Python 3 (pixi)** — pixi auto-uses
the project env.

If you'd rather use VS Code:

```bash
pixi run kernel        # registers a named ipykernel
```

then in VS Code pick the **Python (NeuroPySeminar)** kernel from the top-right
dropdown.

## 4. Pull updates over the term

```bash
git pull
pixi install           # only re-solves if pixi.lock changed
```

## Tip — VS Code shortcut for opening a terminal

`Ctrl + Shift + P` → "Terminal: Create New Terminal".
