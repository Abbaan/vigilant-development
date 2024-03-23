from abc import ABC, abstractmethod
from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA
import torch
import pandas as pd
from typing import List
from sklearn.cluster import KMeans



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

    def cluster(self, data, n_clusters) -> List[int]:
        """Cluster the data using KMeans."""
        kmeans = KMeans(n_clusters)
        kmeans.fit(data)
        labels = kmeans.labels_
        return labels