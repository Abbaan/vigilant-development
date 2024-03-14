import numpy as np
from sklearn.cluster import KMeans
from .model import text_to_vector


def normalize_ratings(ratings):
    min_rating = min(ratings)
    max_rating = max(ratings)
    return [(r - min_rating) / (max_rating - min_rating) for r in ratings]


def calculate_cluster_centroids(labels, vectors):
    cluster_centers = {}
    for label, vector in zip(labels, vectors):
        cluster_centers.setdefault(label, []).append(vector)
    return {label: np.mean(points, axis=0) for label, points in cluster_centers.items()}

def perform_clustering(data, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    labels = kmeans.labels_
    return labels


