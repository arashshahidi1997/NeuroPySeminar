#!/usr/bin/env python3
"""
Synthetic ICA datasets beyond the classic "limb" model.

Generates:
1. Classic limb model (Laplace + Laplace)
2. Uniform + Laplace
3. Bimodal + Logistic
4. Sparse + Sub-Gaussian (Beta)
5. Heavy-tailed (Student-t) + Skewed (Lognormal)

Each example:
- Generates independent sources S (2 x N)
- Applies a non-orthogonal mixing matrix A
- Plots sources vs mixtures
- Optionally runs FastICA and plots recovered components
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import FastICA


# --------------------
# Utility functions
# --------------------

def mix_sources(S, A=None, seed=None):
    """
    S: array shape (2, N) of independent sources
    A: mixing matrix shape (2, 2), if None choose random full-rank
    Returns:
        X: mixed signals (2, N)
        A: mixing matrix used
    """
    rng = np.random.default_rng(seed)
    if A is None:
        # Random full-rank 2x2 matrix
        A = rng.normal(size=(2, 2))
        # Ensure it's not too close to singular
        while abs(np.linalg.det(A)) < 0.2:
            A = rng.normal(size=(2, 2))

    X = A @ S
    return X, A


def run_fastica(X, n_components=2, seed=None):
    """
    Run FastICA on 2xN mixture.
    Returns:
        S_est: estimated sources (2, N)
        W: unmixing matrix
        A_est: mixing matrix estimate
    """
    ica = FastICA(
        n_components=n_components,
        random_state=seed,
        whiten="unit-variance",
    )
    # scikit-learn expects shape (N, 2)
    X_T = X.T
    S_est = ica.fit_transform(X_T).T  # shape (2, N)
    A_est = ica.mixing_.T             # (2, 2)
    W = ica.components_               # (2, 2)
    return S_est, W, A_est


def plot_example(S, X, S_est=None, title_prefix="", show=False, save=True):
    """
    Plot sources, mixtures, and optionally recovered ICA sources.
    S: (2, N) sources
    X: (2, N) mixed signals
    S_est: (2, N) recovered sources (optional)
    """
    fig_cols = 3 if S_est is not None else 2
    fig, axes = plt.subplots(1, fig_cols, figsize=(5 * fig_cols, 4))

    # Sources
    ax = axes[0]
    ax.scatter(S[0, :], S[1, :], s=2, alpha=0.5)
    ax.set_title(f"{title_prefix}Sources")
    ax.set_xlabel("s1")
    ax.set_ylabel("s2")
    ax.axhline(0, linewidth=0.5)
    ax.axvline(0, linewidth=0.5)

    # Mixtures
    ax = axes[1]
    ax.scatter(X[0, :], X[1, :], s=2, alpha=0.5)
    ax.set_title(f"{title_prefix}Mixtures")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.axhline(0, linewidth=0.5)
    ax.axvline(0, linewidth=0.5)

    # Recovered ICA components
    if S_est is not None:
        ax = axes[2]
        ax.scatter(S_est[0, :], S_est[1, :], s=2, alpha=0.5)
        ax.set_title(f"{title_prefix}Recovered (FastICA)")
        ax.set_xlabel("y1")
        ax.set_ylabel("y2")
        ax.axhline(0, linewidth=0.5)
        ax.axvline(0, linewidth=0.5)

    plt.tight_layout()
    if show:
        plt.show()

    save_dir = "figures/mixing/"
    os.makedirs(save_dir, exist_ok=True)
    if save:
        filename = title_prefix.strip().replace(" ", "_").replace("+", "plus").replace(",", "") + ".png"
        plt.savefig(save_dir + filename)
    plt.close()

# --------------------
# Source generators
# --------------------

def generate_limb_sources(N, seed=None):
    """
    Classic 'limb' model: two super-Gaussian sources (e.g. Laplace).
    """
    rng = np.random.default_rng(seed)
    s1 = rng.laplace(loc=0.0, scale=1.0, size=N)
    s2 = rng.laplace(loc=0.0, scale=1.0, size=N)
    return np.vstack([s1, s2])


def generate_uniform_laplace_sources(N, seed=None):
    """
    One uniform, one Laplace.
    """
    rng = np.random.default_rng(seed)
    s1 = rng.uniform(-1, 1, size=N)
    s2 = rng.laplace(0.0, 1.0, size=N)
    return np.vstack([s1, s2])


def generate_bimodal_logistic_sources(N, seed=None):
    """
    Bimodal Gaussian mixture + Logistic.
    """
    rng = np.random.default_rng(seed)
    # Bimodal: mixture of two Gaussians
    comp = rng.integers(0, 2, size=N)
    means = np.array([-3.0, 3.0])
    s1 = means[comp] + rng.normal(scale=1.0, size=N)
    # Logistic source
    s2 = rng.logistic(loc=0.0, scale=1.0, size=N)
    return np.vstack([s1, s2])


def generate_sparse_beta_sources(N, sparsity=0.95, seed=None):
    """
    Sparse + sub-Gaussian (Beta).
    s1: mostly zeros with occasional Laplace spikes
    s2: Beta(2,2) scaled to [-1,1]
    """
    rng = np.random.default_rng(seed)
    mask = rng.uniform(size=N) > sparsity  # True for spikes
    s1 = np.zeros(N)
    s1[mask] = rng.laplace(0.0, 1.0, size=mask.sum())
    # Beta distributed between 0 and 1, then scaled to [-1,1]
    s2_raw = rng.beta(a=2.0, b=2.0, size=N)
    s2 = 2 * s2_raw - 1.0
    return np.vstack([s1, s2])


def generate_student_lognormal_sources(N, df=3.0, seed=None):
    """
    Heavy-tailed Student-t + skewed Lognormal.
    """
    rng = np.random.default_rng(seed)
    # Student-t heavy-tailed source
    s1 = rng.standard_t(df=df, size=N)
    # Lognormal skewed source, centered roughly
    s2 = rng.lognormal(mean=0.0, sigma=1.0, size=N) - np.exp(0.0 + 0.5 * 1.0**2)
    return np.vstack([s1, s2])


# --------------------
# Main: generate and plot all examples
# --------------------

def main():
    N = 10000
    seed = 42

    examples = [
        ("Classic limb (Laplace + Laplace)", generate_limb_sources),
        ("Uniform + Laplace", generate_uniform_laplace_sources),
        ("Bimodal + Logistic", generate_bimodal_logistic_sources),
        ("Sparse + Beta", generate_sparse_beta_sources),
        ("Student-t + Lognormal", generate_student_lognormal_sources),
    ]

    for title, gen_func in examples:
        print(f"Generating example: {title}")
        S = gen_func(N, seed=seed)
        X, A = mix_sources(S, A=None, seed=seed)

        # Run FastICA
        S_est, W, A_est = run_fastica(X, n_components=2, seed=seed)

        # Plot sources, mixtures, and recovered components
        plot_example(S, X, S_est=S_est, title_prefix=f"{title}\n")

        print(f"  Mixing matrix A:\n{A}")
        print(f"  Estimated mixing A_est (up to scale/perm):\n{A_est}\n")

    print("Done.")


if __name__ == "__main__":
    main()
