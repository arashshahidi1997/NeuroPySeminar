**Prompt for Codex: Plan + Instructions (do NOT write code here)**

You are to generate a **small collection of Python scripts** that serve as a didactic toolkit for ICA, whitening (PCA & ZCA), and FastICA.

The goal is to gradually introduce:

* Non-Gaussian 1D distributions and joint distributions (independent vs dependent)
* Linear mixing vs probabilistic mixtures
* Whitening (PCA whitening and ZCA whitening)
* FastICA: algorithm, non-Gaussianity, and practical demos

Each `.py` file must be:

* **Formatted in Jupytext “percent” style**, so it can be converted to a notebook later
* Use **matplotlib** for plotting, with all figures saved under `figures/<topic>/<figurename>.png`
* Always call `plt.show()` after saving figures (so later Jupyter conversion is smooth)

Below is the plan, **by script**, with content and structure. Do not write the code in this step; use this as guidance for later code generation.

---

## Global style & tooling rules (apply to ALL scripts)

1. **Jupytext format**

   * Use the `py:percent` format:

     * Markdown cells as:

       ```python
       # %% [markdown]
       """
       Markdown text...
       """
       ```
     * Code cells as:

       ```python
       # %%
       # Python code here
       ```
   * At the very top of each file, include a standard Jupytext YAML header in comments, for example:

     ```python
     # ---
     # jupyter:
     #   jupytext:
     #     formats: py:percent,ipynb
     #     text_representation:
     #       extension: .py
     #       format_name: percent
     #       format_version: '1.3'
     #       jupytext_version: '1.16.0'
     # ---

     # %% [markdown]
     """
     Title, short description...
     """
     ```

2. **Figure saving conventions**

   * For each script, define a topic name (e.g. `intro_distributions`, `whitening`, `fastica`).
   * All figures must be saved as:

     ```python
     import os
     os.makedirs("figures/<topic>", exist_ok=True)
     plt.savefig("figures/<topic>/<figure_name>.png", dpi=300, bbox_inches="tight")
     plt.show()
     ```
   * Always call `plt.show()` after saving.

3. **Imports**

   * Use standard imports (`numpy`, `matplotlib.pyplot`, `sklearn.decomposition.FastICA` where needed).
   * Keep things reproducible by using `np.random.default_rng(seed)`.

4. **Narrative structure**

   * Each script must begin with a **markdown “Overview” cell** describing its purpose and connection to ICA.
   * Use markdown cells to explain concepts between code blocks.

---

## Script 1: `intro_distributions_and_joints.py`

**Topic name for figures**: `intro_distributions`

### Purpose

Introduce various **1D non-Gaussian distributions** and show how to construct:

* Independent joint distributions (product of marginals)
* Dependent joint distributions via:

  * **Linear mixing** (ICA-style)
  * **Probabilistic mixtures** (mixture of 2D Gaussians)

### Structure

1. **Markdown cell – Overview**

   * Briefly explain:

     * Goal: show that sources can be independent without “non-overlapping limbs”.
     * Difference between 1D distributions, independent joints, and dependent joints.
     * Distinguish **linear mixing** vs **probabilistic mixtures**.

2. **Code cell – Imports & random seed setup**

   * Import `numpy`, `matplotlib.pyplot`, and `os`.
   * Set a global RNG seed.

3. **Code + Markdown cells – 1D distributions**

   * Implement helper functions to sample from:

     * Laplace
     * Uniform
     * Bimodal Gaussian (mixture of two Gaussians)
     * Logistic
     * Sparse Laplace (spike + mostly zeros)
     * Beta (rescaled to [-1, 1])
     * Student-t
     * Lognormal (centered)
   * Plot histograms of each distribution in a grid (2x4 or similar).
   * Save figure as `figures/intro_distributions/1d_distributions.png`.

4. **Code + Markdown cells – Independent joints**

   * Define a function to generate independent pairs `(s1, s2)` from two chosen 1D distributions.
   * Example A: Laplace × Uniform
   * Example B: Bimodal × Logistic
   * Scatter plots of these independent joints.
   * Save as `figures/intro_distributions/independent_pairs.png`.

5. **Code + Markdown cells – Dependent joints via linear mixing**

   * Introduce linear mixing: `x = A @ s`, with `A` a random full-rank 2×2 matrix.
   * Mix the independent pairs from above.
   * Show that the resulting `(x1, x2)` are dependent.
   * Scatter plots of linearly mixed examples.
   * Save as `figures/intro_distributions/dependent_linear_mixing.png`.

6. **Code + Markdown cells – Dependent joints via probabilistic mixture**

   * Implement a small 2D Gaussian mixture model: 2–3 components with different means/covariances.
   * Sample from the mixture to illustrate a **GMM-style joint**.
   * Scatter plot of GMM samples.
   * Save as `figures/intro_distributions/dependent_gmm.png`.

7. **Markdown cell – Summary**

   * Recap:

     * Independent vs dependent joints.
     * Linear mixing vs mixture distributions.
     * All of these produce point clouds that may look quite different.

---

## Script 2: `ica_pointclouds_nonlimb.py`

**Topic name for figures**: `ica_pointclouds`

### Purpose

Demonstrate that **ICA works on non-limb point clouds**: sources can be continuously “on,” overlapping in activation, yet independent and ICA-separable.

### Structure

1. **Markdown – Overview**

   * Explain:

     * The myth: ICA needs limb / cross-shaped sources.
     * Reality: ICA only needs independent, non-Gaussian sources; continuous overlapping is fine.
     * Outline what examples will be shown.

2. **Code – Imports & RNG**

3. **Code + Markdown – Define source generators**

   * Reuse or re-implement:

     * Laplace
     * Logistic
     * Uniform
     * Bimodal, etc. (keep it minimal but reusable).

4. **Example 1: Laplace + Logistic (overlapping sources)**

   * Generate independent sources `s1 ~ Laplace`, `s2 ~ Logistic`.
   * Show their joint scatter: **no limbs, just a fuzzy blob**.
   * Save as `figures/ica_pointclouds/sources_laplace_logistic.png`.

5. **Example 1: Linear mixing + scatter**

   * Choose a non-orthogonal mixing matrix `A`.
   * Compute `X = A @ S`.
   * Scatter plot of mixtures (still no limbs, just skewed blobs).
   * Save as `figures/ica_pointclouds/mixed_laplace_logistic.png`.

6. **Example 1: Run FastICA + recovered components**

   * Use `sklearn.decomposition.FastICA` to recover sources from `X`.
   * Scatter plot of recovered components (showing that they line up with the original sources up to sign/perm).
   * Save as `figures/ica_pointclouds/recovered_laplace_logistic.png`.
   * Optionally compute and print correlation matrix between true and recovered sources.

7. **Example 2 (optional): Bimodal + Logistic or Uniform + Laplace**

   * Repeat steps for another non-limb combination to reinforce the point.
   * Save corresponding figures under `figures/ica_pointclouds/…`.

8. **Markdown – Summary**

   * Emphasize:

     * Independence ≠ non-overlapping support.
     * ICA does not rely on limb structure.
     * What matters is non-Gaussianity + linear mixing + independence.

---

## Script 3: `whitening_pca_zca.py`

**Topic name for figures**: `whitening`

### Purpose

Explain and visualize **whitening**, comparing **z-scoring**, **PCA whitening**, and **ZCA whitening**. Show:

* That z-scoring is not whitening
* PCA whitening rotates into eigenbasis
* ZCA whitening decorrelates but preserves orientation “as much as possible”

### Structure

1. **Markdown – Overview**

   * Define:

     * Centering
     * Z-scoring
     * Whitening
   * Explain motivation: for ICA we want `Cov(z) = I`, not just unit variances.

2. **Code – Imports & RNG**

3. **Code + Markdown – Generate a correlated Gaussian cloud**

   * Create 2D Gaussian with nontrivial covariance (e.g. correlation 0.8).
   * Scatter plot as “Original data (correlated Gaussian)”.
   * Save as `figures/whitening/original_correlated_gaussian.png`.

4. **Code + Markdown – Z-scoring vs whitening**

   * Apply per-component z-scoring.
   * Compute and print covariance / correlation matrix.
   * Scatter plot z-scored data.
   * Save as `figures/whitening/zscored_data.png`.
   * Highlight in markdown that correlations remain.

5. **Code + Markdown – PCA whitening**

   * Implement PCA eigendecomposition `Sigma = U Λ U^T`.
   * Define PCA whitening matrix `V_pca = Λ^{-1/2} U^T`.
   * Apply: `z_pca = V_pca @ x`.
   * Confirm `Cov(z_pca) ≈ I`.
   * Scatter plot PCA-whitened data.
   * Save as `figures/whitening/pca_whitened.png`.

6. **Code + Markdown – ZCA whitening**

   * Define ZCA whitening matrix `V_zca = U Λ^{-1/2} U^T`.
   * Apply: `z_zca = V_zca @ x`.
   * Confirm `Cov(z_zca) ≈ I`.
   * Scatter plot ZCA-whitened data.
   * Save as `figures/whitening/zca_whitened.png`.
   * Optionally overlay orientation vs original.

7. **Markdown – Comparison and ICA context**

   * Summarize:

     * Z-scoring ≠ whitening.
     * PCA vs ZCA whitening: both yield identity covariance; differ by rotation.
     * For ICA: whitening reduces mixing to **orthogonal** transformations, making FastICA’s job easier.

---

## Script 4: `fastica_algorithm_demo.py`

**Topic name for figures**: `fastica`

### Purpose

Explain and demonstrate the **FastICA algorithm**:

* Its objective: maximize non-Gaussianity
* Its fixed-point iteration update
* Practical behavior on synthetic mixtures

### Structure

1. **Markdown – Overview**

   * Explain:

     * ICA goal: find `W` such that `y = W x` are independent.
     * Role of whitening (reminder, refer to previous script).
     * FastICA idea: fixed-point algorithm maximizing a contrast (e.g. negentropy / kurtosis).

2. **Code – Imports & RNG**

   * Import `numpy`, `matplotlib.pyplot`.
   * Import `FastICA` from `sklearn.decomposition` for reference / comparison.

3. **Markdown – FastICA math**

   * In markdown, write the main update equation for a single component after whitening:
     [
     w_{\text{new}} = \mathbb{E}[z, g(w^\top z)] - \mathbb{E}[g'(w^\top z)], w
     ]
   * Mention typical choices of `g(u)` (e.g. `tanh`, `u^3`, etc.).
   * Mention normalization + orthogonalization steps.

4. **Code + Markdown – Generate non-Gaussian sources and mixtures**

   * Use something like Laplace + Logistic or Bimodal + Logistic.
   * Mix via a non-orthogonal matrix to form `X`.
   * Scatter plot sources and mixtures.
   * Save as:

     * `figures/fastica/sources_example.png`
     * `figures/fastica/mixtures_example.png`

5. **Code + Markdown – Run sklearn FastICA**

   * Apply `FastICA` to `X`.
   * Scatter plot recovered components.
   * Save as `figures/fastica/recovered_fastica_sklearn.png`.
   * Compute correlation matrix between true sources and recovered components; print it.

6. **Code + Markdown – (Optional) Manual FastICA step**

   * Optionally implement **one or a few iterations** of the FastICA fixed-point update manually on whitened data, to illustrate:

     * Centering and whitening
     * Iterative update of `w`
     * Normalization & decorrelation
   * Plot the evolution of `w` or the change in contrast value over iterations.
   * Save any relevant figure as `figures/fastica/fastica_convergence.png`.

7. **Markdown – Summary**

   * Summarize:

     * How FastICA leverages whitening + non-Gaussianity.
     * Why fixed-point iteration is fast (no learning rates).
     * The relationship between contrast functions and independence.

---

## Script 5 (optional): `ica_vs_pca_geometry.py`

**Topic name for figures**: `ica_vs_pca`

### Purpose

Visually compare **PCA vs ICA** for a non-Gaussian dataset:

* Show PCA finds orthogonal directions based on covariance
* Show ICA finds directions based on non-Gaussianity
* Use a non-elliptical cloud (e.g. cross, star, or sparse sources) to highlight the difference.

### Structure (brief)

1. **Markdown – Overview:** PCA vs ICA, geometry vs statistics.
2. **Code – Generate non-Gaussian sources, mix, and visualize.**
3. **Code – Apply PCA to mixed data; plot principal components & transformed data.**
4. **Code – Apply FastICA; plot independent components & transformed data.**
5. **Save figures** under `figures/ica_vs_pca/…`.

---

This is the complete plan.

When you (Codex) are later asked to implement each `.py` file, follow this structure, adhere to the **figure-saving rules** and **Jupytext percent style**, and include clear markdown explanations between code cells.
