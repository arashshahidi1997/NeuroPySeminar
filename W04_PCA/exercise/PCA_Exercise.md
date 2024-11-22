
# Exercise 1: PCA plots 
Apply PCA on a dataset of your choice and plot the following:
- scree plot (eigenvalues)
- eigenvectors (loadings)
- seaborn PairGrid, first 5 PCs
- 3d plot of first 3 PCs

# Exercise 2: Reverse Engineering
- PC: create multivariate (3 dimensions) well separated Gaussian bumps with 100 points per cluster. (300, 3) matrix
- Unembedding: pad with zeros to get a (300, 10) matrix, Z, such that the last 7 columns are all zero
- Mixing Matrix: create a (10x10) mixing matrix, R - matrix of eigenvectors: use the random_son to generate an arbitrary rotation matrix in 10 dimensions
- Apply the mixing matrix to the unembedded datapoints to get the (300, 10) design matrix: X = R @ Z
- apply PCA and reduce dimensionality to 3
- apply KMeans clustering to label the gaussian bumps