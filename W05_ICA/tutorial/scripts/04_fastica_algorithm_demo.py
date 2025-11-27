# ---
# jupyter:
#   jupytext:
#     formats: notebooks//ipynb,scripts//py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
# ---

# %% [markdown]
"""
# FastICA Algorithm Demo

We connect FastICA's theory to practice: generate non-Gaussian sources, mix
them, recall the fixed-point update, and compare sklearn's implementation to a
minimal manual routine.
"""

# %%
import os
from typing import Callable, Tuple

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import FastICA

TOPIC = "fastica"
FIG_DIR = os.path.join("figures", TOPIC)
os.makedirs(FIG_DIR, exist_ok=True)

rng = np.random.default_rng(99)


# %% [markdown]
r"""
## FastICA at a glance

For whitened data `z`, one fixed-point update for a component `w` is:

\\[
w_{\\text{new}} = \\mathbb{E}[z\\,g(w^\\top z)] - \\mathbb{E}[g'(w^\\top z)]\\,w
\\]

After each update we re-normalize and (for multiple components) orthogonalize
the rows of `W`. Popular nonlinearities include:

* `g(u) = tanh(u)` (robust, logistic-ish model)
* `g(u) = u^3` (kurtosis-based)
* `g(u) = u * exp(-u^2 / 2)` (gauss)
"""

# %% [markdown]
"""
## Generate sources and mixtures
"""

# %%
def laplace(size: int) -> np.ndarray:
    return rng.laplace(0.0, 1 / np.sqrt(2), size)


def logistic(size: int) -> np.ndarray:
    return rng.logistic(0.0, 1.0, size)


n_samples = 6000
S = np.column_stack([laplace(n_samples), logistic(n_samples)])
A = np.array([[1.0, 2.0], [-1.5, 1.0]])
X = (A @ S.T).T

plt.figure(figsize=(6, 6))
plt.scatter(S[:, 0], S[:, 1], s=5, alpha=0.35, color="#4477aa")
plt.title("True sources")
plt.xlabel("$s_1$")
plt.ylabel("$s_2$")
plt.axis("equal")
plt.savefig(
    os.path.join(FIG_DIR, "sources_example.png"), dpi=300, bbox_inches="tight"
)
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(X[:, 0], X[:, 1], s=5, alpha=0.35, color="#cc6677")
plt.title("Observed mixtures")
plt.xlabel("$x_1$")
plt.ylabel("$x_2$")
plt.axis("equal")
plt.savefig(
    os.path.join(FIG_DIR, "mixtures_example.png"), dpi=300, bbox_inches="tight"
)
plt.show()


# %% [markdown]
"""
## sklearn FastICA
"""

# %%
ica = FastICA(random_state=0, whiten="unit-variance")
S_hat = ica.fit_transform(X)

plt.figure(figsize=(6, 6))
plt.scatter(S_hat[:, 0], S_hat[:, 1], s=5, alpha=0.35, color="#228833")
plt.title("Recovered components (sklearn)")
plt.xlabel("$\\hat{s}_1$")
plt.ylabel("$\\hat{s}_2$")
plt.axis("equal")
plt.savefig(
    os.path.join(FIG_DIR, "recovered_fastica_sklearn.png"),
    dpi=300,
    bbox_inches="tight",
)
plt.show()


def corr_matrix(true_sources: np.ndarray, estimates: np.ndarray) -> np.ndarray:
    true_centered = true_sources - true_sources.mean(axis=0, keepdims=True)
    est_centered = estimates - estimates.mean(axis=0, keepdims=True)
    true_std = true_centered.std(axis=0, keepdims=True)
    est_std = est_centered.std(axis=0, keepdims=True)
    corr = np.dot(true_centered / true_std, (est_centered / est_std)) / (
        true_sources.shape[0] - 1
    )
    return corr


print("Correlation (sklearn):\n", np.round(corr_matrix(S, S_hat), 3))


# %% [markdown]
"""
## Manual FastICA iteration

We whiten `X`, then run a handful of fixed-point steps with `g(u) = tanh(u)`
to visualize convergence.
"""

# %%
def whiten(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = data.mean(axis=0, keepdims=True)
    centered = data - mean
    cov = np.cov(centered, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    eps = 1e-6
    D_inv_sqrt = np.diag(1.0 / np.sqrt(eigvals + eps))
    whitening = D_inv_sqrt @ eigvecs.T
    dewhitening = eigvecs @ np.diag(np.sqrt(eigvals + eps))
    Z = (whitening @ centered.T).T
    return Z, whitening, dewhitening


def symmetric_decorrelation(W: np.ndarray) -> np.ndarray:
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    return (U @ np.diag(1.0 / s) @ Vt) @ W


def manual_fastica(Z: np.ndarray, max_iter: int = 200, tol: float = 1e-6):
    n_components = Z.shape[1]
    W = rng.normal(size=(n_components, n_components))
    W = symmetric_decorrelation(W)
    contrasts = []

    for _ in range(max_iter):
        WX = Z @ W.T
        G = np.tanh(WX)
        G_prime = 1.0 - np.tanh(WX) ** 2
        W_new = (G.T @ Z) / Z.shape[0] - np.diag(G_prime.mean(axis=0)) @ W
        W_new = symmetric_decorrelation(W_new)
        delta = np.max(np.abs(np.abs(np.diag(W_new @ W.T)) - 1))
        W = W_new
        contrasts.append(np.mean(np.log(np.cosh(WX))))
        if delta < tol:
            break
    return W, contrasts


Z, whitening, dewhitening = whiten(X)
W_manual, contrast_history = manual_fastica(Z)
S_manual = Z @ W_manual.T

plt.figure(figsize=(6, 6))
plt.scatter(S_manual[:, 0], S_manual[:, 1], s=5, alpha=0.35, color="#aa7744")
plt.title("Recovered components (manual FastICA)")
plt.xlabel("$\\tilde{s}_1$")
plt.ylabel("$\\tilde{s}_2$")
plt.axis("equal")
plt.savefig(
    os.path.join(FIG_DIR, "recovered_fastica_manual.png"),
    dpi=300,
    bbox_inches="tight",
)
plt.show()

print("Correlation (manual):\n", np.round(corr_matrix(S, S_manual), 3))

plt.figure(figsize=(6, 4))
plt.plot(contrast_history, marker="o")
plt.xlabel("Iteration")
plt.ylabel("Mean log cosh (contrast)")
plt.title("FastICA convergence")
plt.grid(True, alpha=0.3)
plt.savefig(
    os.path.join(FIG_DIR, "fastica_convergence.png"),
    dpi=300,
    bbox_inches="tight",
)
plt.show()


# %% [markdown]
"""
## Summary

* Whitening simplifies ICA to an orthogonal search.
* FastICA uses fixed-point updates that do not require learning rates.
* Both sklearn and our tiny implementation recover the original non-Gaussian
  sources up to permutation/sign.
"""
