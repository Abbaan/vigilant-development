from abc import ABC, abstractmethod
from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA
import torch
import pandas as pd
from typing import List
from sklearn.cluster import KMeans
import numpy as np



class EmbeddingModel(ABC):
    """Abstract base class for an embedding model."""

    @abstractmethod
    def embed(self):
        """Embed a text."""
        pass


class SciBert(EmbeddingModel):
    """Concrete implementation of a SciBERT model."""

    def __init__(self):
        """Load the SciBERT model."""
        self.model_name = 'allenai/scibert_scivocab_uncased'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
    
    def embed(self, text):
        """Embed a text using SciBERT."""
        inputs = self.tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
        return embeddings


class DimensionReductionStrategy(ABC):
    """Abstract base class for a dimension reduction strategy."""

    def reduce_dimensionality(self): 
        """Reduce the dimensionality of the embeddings."""
        pass


class PCAReduction(DimensionReductionStrategy):
    """Concrete implementation of a PCA dimension reduction strategy."""

    def __init__(self, n_components=2):
        """Initialize the PCA dimension reduction strategy."""
        self.n_components = n_components
        self.pca = PCA(n_components=self.n_components)

    def reduce_dimensionality(self, vectors: List[torch.Tensor]) -> List[torch.Tensor]:
        """Reduce the dimensionality of the embeddings using PCA."""
        reduced_vectors = self.pca.fit_transform(vectors)
        return reduced_vectors.tolist()
    
class ClusterStrategy(ABC):
    """Abstract base class for a clustering strategy."""

    @abstractmethod
    def cluster(self):
        """Cluster the data."""
        pass

class KMeansClustering(ClusterStrategy):
    """Concrete implementation of a KMeans clustering strategy."""

    def __init__(self):
        """Initialize the KMeans clustering strategy."""
        self.state = 'initialized'

    def cluster(self, vectors, n_clusters) -> List[int]:
        """Cluster the vectors into n clusters using KMeans."""
        kmeans = KMeans(n_clusters)
        kmeans.fit(vectors)
        self.cluster_labels = kmeans.labels_
        self.vectors = vectors
        self.state = 'clustered'
        return self.cluster_labels
    
    def calculate_cluster_centroids(self):
        if self.state != 'clustered':
            raise ValueError("Data has not been clustered yet.")
        cluster_centers = {}
        for label, vector in zip(self.cluster_labels, self.vectors):
            cluster_centers.setdefault(label, []).append(vector)
        return {label: np.mean(points, axis=0) for label, points in cluster_centers.items()}
    
    def convert_label_to_color(self, label):
        if self.state != 'clustered':
            raise ValueError("Data has not been clustered yet.")
        # Define a list of colors in RGBA format (with full opacity by default)
        colors = [
            'rgba(255, 0, 0, 1)',   # Red
            'rgba(0, 255, 0, 1)',   # Green
            'rgba(0, 0, 255, 1)',   # Blue
            'rgba(128, 0, 128, 1)', # Purple
            'rgba(255, 165, 0, 1)', # Orange
            # ... add more colors as needed ...
        ]
        return colors[label % len(colors)]