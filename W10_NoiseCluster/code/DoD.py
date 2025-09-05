import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score

def compute_DoD_distance_matrix(X, K, metric='euclidean'):
    """
    Compute the Distance-of-Distances (DoD) matrix.
    
    Parameters:
    - X: ndarray of shape (N, D), input data points.
    - K: int, number of nearest neighbors to consider.
    - metric: str, distance metric to use ('euclidean' or 'manhattan').ou

    Returns:
    - F: ndarray of shape (N, N), the transformed distance matrix.
    """
    N = X.shape[0]
    D = pairwise_distances(X, metric=metric)
    F = np.zeros_like(D)
    
    for i in range(N):
        neighbors_i = np.argsort(D[i])[:K+1][1:]  # Exclude self
        for j in range(N):
            neighbors_j = np.argsort(D[j])[:K+1][1:]
            joint_neighbors = np.unique(np.concatenate((neighbors_i, neighbors_j)))
            
            diff_i = np.abs(D[joint_neighbors, i] - D[joint_neighbors, j])
            diff_j = np.abs(D[joint_neighbors, j] - D[joint_neighbors, i])
            
            F[i, j] = np.mean(np.concatenate((diff_i, diff_j)))
    
    return F

# Simulation of high-dimensional cluster and noise points
np.random.seed(42)
num_clusters = 5
points_per_cluster = 50
num_noise = 200
dimensions = 50

clusters = [np.random.multivariate_normal(np.random.rand(dimensions), np.eye(dimensions) * 0.1, points_per_cluster) for _ in range(num_clusters)]
noise = np.random.uniform(low=-5, high=5, size=(num_noise, dimensions))

X = np.vstack(clusters + [noise])
labels = np.concatenate([np.full(points_per_cluster, i) for i in range(num_clusters)] + [np.full(num_noise, num_clusters)])

# Compute the original and DoD-transformed distance matrices
K = 10
D_original = pairwise_distances(X, metric='euclidean')
D_DoD = compute_DoD_distance_matrix(X, K)

# Apply t-SNE visualization to compare original vs DoD-transformed distances
pca_preprocessed = PCA(n_components=30).fit_transform(X)
embedding_original = TSNE(perplexity=30, random_state=42, init='random', metric='precomputed').fit_transform(D_original)
embedding_DoD = TSNE(perplexity=30, random_state=42, init='random', metric='precomputed').fit_transform(D_DoD)

# Plot the results
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].scatter(embedding_original[:, 0], embedding_original[:, 1], c=labels, cmap='viridis', alpha=0.7)
ax[0].set_title('t-SNE with Original Distances')
ax[1].scatter(embedding_DoD[:, 0], embedding_DoD[:, 1], c=labels, cmap='viridis', alpha=0.7)
ax[1].set_title('t-SNE with DoD Transformed Distances')
plt.show()

# Compute clustering performance using Adjusted Rand Index (ARI)
ari_original = adjusted_rand_score(labels, np.round(embedding_original[:, 0]))
ari_DoD = adjusted_rand_score(labels, np.round(embedding_DoD[:, 0]))

print("Adjusted Rand Index (Original):", ari_original)
print("Adjusted Rand Index (DoD):", ari_DoD)

# Measuring shrinkage
cluster_indices = np.arange(num_clusters * points_per_cluster)
noise_indices = np.arange(num_clusters * points_per_cluster, X.shape[0])

cluster_to_cluster_dist = np.mean(D_original[np.ix_(cluster_indices, cluster_indices)])
cluster_to_noise_dist = np.mean(D_original[np.ix_(cluster_indices, noise_indices)])
noise_to_noise_dist = np.mean(D_original[np.ix_(noise_indices, noise_indices)])

cluster_to_cluster_DoD = np.mean(D_DoD[np.ix_(cluster_indices, cluster_indices)])
cluster_to_noise_DoD = np.mean(D_DoD[np.ix_(cluster_indices, noise_indices)])
noise_to_noise_DoD = np.mean(D_DoD[np.ix_(noise_indices, noise_indices)])

print("Distance shrinkage (absolute):")
print("Cluster-to-cluster:", cluster_to_cluster_dist - cluster_to_cluster_DoD)
print("Cluster-to-noise:", cluster_to_noise_dist - cluster_to_noise_DoD)
print("Noise-to-noise:", noise_to_noise_dist - noise_to_noise_DoD)

print("Distance shrinkage (fraction):")
print("Cluster-to-cluster:", cluster_to_cluster_DoD / cluster_to_cluster_dist)
print("Cluster-to-noise:", cluster_to_noise_DoD / cluster_to_noise_dist)
print("Noise-to-noise:", noise_to_noise_DoD / noise_to_noise_dist)