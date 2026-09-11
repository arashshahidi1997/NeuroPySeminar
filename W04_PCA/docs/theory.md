# PCA — Theory

*Week 04 · Dimensionality reduction · Tuesday theory session.*

> **Where this sits in the course.** Almost every method in the first block is a
> statement about **second-order (covariance) structure**. The power spectrum
> (W02) is the Fourier transform of the temporal autocovariance; an AR model
> (W03) is a generative model of that same autocovariance; **PCA (here) is the
> eigendecomposition of the spatial covariance matrix.** Keep that sentence in
> view and the block becomes one idea seen from several sides.

---

## 1. The problem

We observe data in $p$ dimensions (channels, pixels, genes, neurons) but suspect
the *interesting* variation lives in far fewer. Dimensionality reduction seeks a
low-dimensional representation that keeps what matters — for visualization,
denoising, compression, or as a first step before clustering/regression. In
systems neuroscience this is now routine: population activity of hundreds of
neurons is often well described by a handful of latent dimensions
[@cunningham_2014_DimensionalityReduction].

PCA is the canonical **linear** answer: find a small set of orthogonal directions
that capture as much of the data's variance as possible.

## 2. Setup: centering and the covariance matrix

Let $X \in \mathbb{R}^{n \times p}$ hold $n$ samples (rows) of $p$ features
(columns). Center each feature, $X_c = X - \mathbf{1}\bar{x}^\top$, and form the
**sample covariance matrix**

$$
C \;=\; \frac{1}{n-1}\, X_c^\top X_c \;\in\; \mathbb{R}^{p\times p},
\qquad C_{ij} = \operatorname{cov}(x_i, x_j).
$$

$C$ is symmetric and positive semi-definite, so (spectral theorem) it has an
orthonormal eigenbasis with real, non-negative eigenvalues. **That eigenbasis is
PCA.** Everything below follows from this one fact.

## 3. Two equivalent definitions

PCA was introduced twice, from two directions that turn out to coincide:

- **Maximum variance** [@hotelling_1933_AnalysisComplex]: find the direction along which the
  projected data vary most.
- **Best linear fit** [@pearson_1901_LiiiLines]: find the low-dimensional subspace that
  minimizes squared reconstruction (orthogonal) distance.

That these give the *same* answer is the content of the Eckart–Young theorem
(§6). We derive PCA from the variance view because it leads most directly to the
eigenproblem.

## 4. Derivation: why eigenvectors?

For a unit vector $w$, the projected data $X_c w$ have variance

$$
\operatorname{Var}(X_c w) \;=\; \frac{1}{n-1}\, w^\top X_c^\top X_c\, w \;=\; w^\top C\, w .
$$

The first principal component maximizes this subject to $\lVert w\rVert = 1$.
Introduce a Lagrange multiplier $\lambda$:

$$
\mathcal{L}(w,\lambda) = w^\top C w - \lambda\,(w^\top w - 1),
\qquad
\nabla_w \mathcal{L} = 2Cw - 2\lambda w = 0
\;\;\Longrightarrow\;\;
\boxed{\,C w = \lambda w\,}.
$$

So the optimal direction is an **eigenvector** of $C$, and the variance it
captures equals its **eigenvalue**: $w^\top C w = \lambda$. The maximum-variance
direction is therefore the *top* eigenvector. The quantity $w^\top C w / w^\top w$
is the **Rayleigh quotient**; its stationary points are exactly the eigenvectors,
and its maximum is $\lambda_{\max}$.

Subsequent components maximize variance *subject to orthogonality* with the
earlier ones; by the same argument they are the remaining eigenvectors, taken in
order of decreasing eigenvalue. Projecting the data onto the top $k$ eigenvectors
gives the **scores** (the reduced representation).

## 5. The SVD view (and why software uses it)

With the thin singular value decomposition $X_c = U\Sigma V^\top$,

$$
C = \frac{1}{n-1} V \Sigma^\top U^\top U \Sigma V^\top
  = V\,\frac{\Sigma^2}{n-1}\,V^\top .
$$

So the **right singular vectors $V$ are the principal directions**, and
$\lambda_i = \sigma_i^2 / (n-1)$. Numerically stable implementations take the SVD
of $X_c$ directly and never form $C$ (squaring the data worsens conditioning)
[@shlens_2014_TutorialPrincipal].

## 6. Optimal low-rank approximation (Eckart–Young)

Among all rank-$k$ approximations of $X_c$, the truncated SVD (equivalently, the
projection onto the top $k$ eigenvectors) minimizes the squared reconstruction
error, and that error equals the sum of the discarded eigenvalues,
$\sum_{i>k}\lambda_i$. Two consequences worth memorizing:

- **Total variance is basis-independent:** $\sum_i \operatorname{Var}(x_i) = \operatorname{tr}(C) = \sum_i \lambda_i.$
- **Explained-variance ratio:** the top $k$ components capture
  $\big(\sum_{i\le k}\lambda_i\big) / \big(\sum_i\lambda_i\big)$ of the total variance —
  the quantity plotted in a **scree plot**.

## 7. Geometry

PCA is a **rotation** of the coordinate axes onto the directions of the data
cloud, ordered by spread. In the principal basis the covariance is diagonal
($V^\top C V = \Lambda$): PCA *removes linear correlations*. Rescaling each score
by $1/\sqrt{\lambda_i}$ makes the covariance the identity — **whitening** — which
is the standard preprocessing step before ICA (W05) [@jolliffe_2016_PrincipalComponent].

## 8. Using PCA in practice

- **Center** always (PCA is about variation *around the mean*).
- **Scale** when features are incommensurable: variance is not unit-free, so a
  feature in large units will dominate purely by its scale. Standardizing
  (z-scoring) is PCA on the *correlation* matrix rather than the covariance
  matrix.
- **Choosing $k$:** look for an elbow in the scree plot, a cumulative-variance
  threshold (e.g. 90%), or use parallel analysis / cross-validation. There is no
  universal rule; the right $k$ depends on the question [@jolliffe_2016_PrincipalComponent].

## 9. Assumptions and failure modes

PCA is powerful precisely because it assumes so little — but those assumptions
bite:

1. **Linearity.** PCA can only rotate and project. Curved structure (rings,
   manifolds) is not untangled by any linear projection → kernel PCA / UMAP (W06).
2. **Variance = importance.** PCA is *unsupervised*: the direction that separates
   your classes can be a *low-variance* one that PCA discards. If you have labels
   and care about discrimination, use LDA.
3. **Second-order only.** PCA uses only means and covariances. Uncorrelated is not
   independent: for non-Gaussian sources you need higher-order structure → ICA (W05).
4. **Scale/outlier sensitivity.** Because it maximizes variance, PCA is sensitive
   to feature scaling and to outliers.
5. **Sign/rotation ambiguity.** Components are defined only up to sign; within a
   degenerate (equal-eigenvalue) subspace, only the subspace — not individual
   axes — is identified.

## 10. Connections

- **Covariance spine.** PCA diagonalizes the *spatial* covariance; the power
  spectrum (W02) is the Fourier transform of the *temporal* autocovariance, and
  an AR model (W03) is a parametric model of the same autocovariance.
- **Whitening → ICA (W05).** PCA decorrelates; ICA goes further to statistical
  independence using higher-order statistics.
- **Nonlinear → UMAP (W06).** When the data lie on a curved manifold, linear PCA
  is insufficient.
- **Probabilistic cousins.** Probabilistic PCA and factor analysis place PCA in a
  latent-variable / generative framework [@tipping_1999_ProbabilisticPrincipal], the same framework that
  underlies GPFA (W09).

---

## References

- Pearson, K. (1901). On lines and planes of closest fit to systems of points in
  space. *Philosophical Magazine* 2(11), 559–572. `[@pearson_1901_LiiiLines]`
- Hotelling, H. (1933). Analysis of a complex of statistical variables into
  principal components. *Journal of Educational Psychology* 24(6), 417–441.
  `[@hotelling_1933_AnalysisComplex]`
- Tipping, M.E. & Bishop, C.M. (1999). Probabilistic principal component analysis.
  *J. R. Stat. Soc. B* 61(3), 611–622. `[@tipping_1999_ProbabilisticPrincipal]`
- Shlens, J. (2014). A tutorial on principal component analysis.
  *arXiv:1404.1100*. `[@shlens_2014_TutorialPrincipal]`
- Cunningham, J.P. & Yu, B.M. (2014). Dimensionality reduction for large-scale
  neural recordings. *Nature Neuroscience* 17, 1500–1509. `[@cunningham_2014_DimensionalityReduction]`
- Jolliffe, I.T. & Cadima, J. (2016). Principal component analysis: a review and
  recent developments. *Phil. Trans. R. Soc. A* 374, 20150202. `[@jolliffe_2016_PrincipalComponent]`
- Durstewitz, D. (2017). *Advanced Data Analysis in Neuroscience.* Springer.
  (course textbook) `[@durstewitz_2017_AdvancedData]`

> **Companion exercise:** [`../exercise/pca_from_covariance.ipynb`](../exercise/pca_from_covariance.ipynb)
> works through the derivation numerically (from-scratch PCA vs. `sklearn`),
> recovers a hidden subspace, and demonstrates each failure mode above.
>
> *Citations use pandoc `[@citekey]` keys; run `biblio_ingest` on the DOIs to
> populate `bib/` so they resolve at render time (see the session notes).*
