#!/usr/bin/env python3
"""
Intro script: 1D non-Gaussian distributions + independent vs dependent joints.

- Defines a set of 1D distributions used in ICA toy examples
  (Laplace, Uniform, Bimodal, Logistic, Sparse, Beta, Student-t, Lognormal)

- Shows how to:
  * Generate independent joint distributions (product of marginals)
  * Generate dependent joint distributions by:
      (a) Linear mixing:  x = A s       (ICA-style mixing)
      (b) Probabilistic mixture: mixture of 2D Gaussians (GMM-style)

Run:
    python intro_distributions_and_mixtures.py
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# 1D distributions
# ---------------------------------------------------------

def laplace_1d(N, loc=0.0, scale=1.0, rng=None):
    rng = np.random.default_rng(rng)
    return rng.laplace(loc=loc, scale=scale, size=N)


def uniform_1d(N, low=-1.0, high=1.0, rng=None):
    rng = np.random.default_rng(rng)
    return rng.uniform(low=low, high=high, size=N)


def bimodal_gaussian_1d(N, means=(-3.0, 3.0), sigma=1.0, rng=None):
    rng = np.random.default_rng(rng)
    comp = rng.integers(0, 2, size=N)
    means = np.array(means)
    return means[comp] + rng.normal(scale=sigma, size=N)


def logistic_1d(N, loc=0.0, scale=1.0, rng=None):
    rng = np.random.default_rng(rng)
    return rng.logistic(loc=loc, scale=scale, size=N)


def sparse_laplace_1d(N, sparsity=0.95, loc=0.0, scale=1.0, rng=None):
    """
    Mostly zeros with occasional Laplace spikes.
    """
    rng = np.random.default_rng(rng)
    mask = rng.uniform(size=N) > sparsity
    out = np.zeros(N)
    out[mask] = rng.laplace(loc=loc, scale=scale, size=mask.sum())
    return out


def beta_1d(N, a=2.0, b=2.0, rng=None):
    """
    Beta(a,b) in [0,1], then rescaled to [-1,1].
    """
    rng = np.random.default_rng(rng)
    x = rng.beta(a=a, b=b, size=N)
    return 2.0 * x - 1.0


def student_t_1d(N, df=3.0, rng=None):
    rng = np.random.default_rng(rng)
    return rng.standard_t(df=df, size=N)


def lognormal_centered_1d(N, mean=0.0, sigma=1.0, rng=None):
    """
    Lognormal shifted so mean is roughly zero (for nicer visuals).
    """
    rng = np.random.default_rng(rng)
    x = rng.lognormal(mean=mean, sigma=sigma, size=N)
    # subtract theoretical mean of lognormal
    shift = np.exp(mean + 0.5 * sigma**2)
    return x - shift


# ---------------------------------------------------------
# Joint distributions: independent vs dependent
# ---------------------------------------------------------

def make_independent_pair(N, dist1, dist2, rng=None):
    """
    Create (s1, s2) where s1 and s2 are independent draws from dist1, dist2.

    dist1, dist2: callables of form dist(N, rng=seed)
    Returns S with shape (2, N).
    """
    s1 = dist1(N, rng=rng)
    s2 = dist2(N, rng=rng)
    return np.vstack([s1, s2])


def linear_mix(S, A=None, rng=None):
    """
    Linear mixing: X = A S, ICA-style (S shape: (2,N), A shape: (2,2)).
    If A is None, random full-rank matrix is chosen.
    """
    rng = np.random.default_rng(rng)
    if A is None:
        A = rng.normal(size=(2, 2))
        # ensure not too close to singular
        while abs(np.linalg.det(A)) < 0.2:
            A = rng.normal(size=(2, 2))
    X = A @ S
    return X, A


def gaussian_mixture_2d(N, pis, mus, covs, rng=None):
    """
    Mixture of 2D Gaussians to illustrate probabilistic mixtures.

    N   : total samples
    pis : list of mixture weights summing to 1
    mus : list of mean vectors, each shape (2,)
    covs: list of covariance matrices, each shape (2,2)
    Returns X shape (2, N).
    """
    rng = np.random.default_rng(rng)
    K = len(pis)
    pis = np.array(pis)
    assert np.isclose(pis.sum(), 1.0), "Mixture weights must sum to 1"

    # Choose component labels
    zs = rng.choice(K, size=N, p=pis)
    X = np.zeros((2, N))

    for k in range(K):
        idx = (zs == k)
        nk = idx.sum()
        if nk == 0:
            continue
        X[:, idx] = rng.multivariate_normal(mean=mus[k], cov=covs[k], size=nk).T

    return X


# ---------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------

def plot_1d_hist(samples, title, ax=None, bins=100):
    if ax is None:
        fig, ax = plt.subplots()
    ax.hist(samples, bins=bins, density=True, alpha=0.7)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    return ax


def plot_2d_scatter(X, title, ax=None, s=5):
    """
    X shape (2, N)
    """
    if ax is None:
        fig, ax = plt.subplots()
    ax.scatter(X[0, :], X[1, :], s=s, alpha=0.4)
    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.axhline(0, linewidth=0.5)
    ax.axvline(0, linewidth=0.5)
    ax.grid(True, alpha=0.3)
    return ax


# ---------------------------------------------------------
# Main demo
# ---------------------------------------------------------

def main():
    N = 20000
    seed = 42

    rng = np.random.default_rng(seed)

    # -------------------------------------------
    # 1. Show 1D distributions
    # -------------------------------------------
    dists = [
        ("Laplace", laplace_1d),
        ("Uniform", uniform_1d),
        ("Bimodal Gaussian", bimodal_gaussian_1d),
        ("Logistic", logistic_1d),
        ("Sparse Laplace", sparse_laplace_1d),
        ("Beta(2,2) rescaled", beta_1d),
        ("Student-t(df=3)", student_t_1d),
        ("Lognormal (centered)", lognormal_centered_1d),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.ravel()

    for ax, (name, dist) in zip(axes, dists):
        x = dist(N, rng=rng)
        plot_1d_hist(x, name, ax=ax)

    fig.suptitle("1D Distributions for ICA-style examples", fontsize=16)
    plt.tight_layout()
    plt.show()

    # -------------------------------------------
    # 2. Independent joint distributions
    # -------------------------------------------
    # Example A: independent (Laplace, Uniform)
    S_ind1 = make_independent_pair(
        N,
        dist1=lambda n, rng=None: laplace_1d(n, rng=rng),
        dist2=lambda n, rng=None: uniform_1d(n, rng=rng),
        rng=seed,
    )

    # Example B: independent (Bimodal, Logistic)
    S_ind2 = make_independent_pair(
        N,
        dist1=lambda n, rng=None: bimodal_gaussian_1d(n, rng=rng),
        dist2=lambda n, rng=None: logistic_1d(n, rng=rng),
        rng=seed + 1,
    )

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    plot_2d_scatter(S_ind1, "Independent: Laplace ⨉ Uniform", ax=axes[0])
    plot_2d_scatter(S_ind2, "Independent: Bimodal ⨉ Logistic", ax=axes[1])
    fig.suptitle("Independent joints (product of marginals)", fontsize=14)
    plt.tight_layout()
    plt.show()

    # -------------------------------------------
    # 3. Dependent joints via linear mixing (ICA model)
    # -------------------------------------------
    X_dep1, A1 = linear_mix(S_ind1, rng=seed)
    X_dep2, A2 = linear_mix(S_ind2, rng=seed + 1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    plot_2d_scatter(X_dep1, "Linear mixture of Laplace + Uniform", ax=axes[0])
    plot_2d_scatter(X_dep2, "Linear mixture of Bimodal + Logistic", ax=axes[1])
    fig.suptitle("Dependent joints via linear mixing (ICA-style)", fontsize=14)
    plt.tight_layout()
    plt.show()

    print("Example linear mixing matrices:")
    print("A1 =\n", A1)
    print("A2 =\n", A2)

    # -------------------------------------------
    # 4. Dependent joints via probabilistic mixture (GMM-style)
    # -------------------------------------------
    pis = [0.4, 0.35, 0.25]
    mus = [
        np.array([-3.0, -3.0]),
        np.array([3.0, 0.0]),
        np.array([0.0, 3.0]),
    ]
    covs = [
        np.array([[1.0, 0.3], [0.3, 1.0]]),
        np.array([[0.5, -0.2], [-0.2, 0.5]]),
        np.array([[0.8, 0.0], [0.0, 0.2]]),
    ]

    X_mix = gaussian_mixture_2d(N, pis, mus, covs, rng=seed)

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    plot_2d_scatter(X_mix, "Probabilistic mixture of 3 Gaussians (GMM-style)", ax=ax)
    fig.suptitle("Dependent joint via mixture distribution", fontsize=14)
    plt.tight_layout()
    plt.show()

    print("Done. You now have:")
    print("  - 1D distributions useful for ICA examples")
    print("  - Independent 2D joints (product of marginals)")
    print("  - Dependent 2D joints via linear mixing (ICA model)")
    print("  - Dependent 2D joint via probabilistic mixture (GMM model)")


if __name__ == "__main__":
    main()
