from abc import ABC, abstractmethod
from .data_loader import LearningResourceLoader, DataExtractionStrategy
from .utils.text_utils import clean_text
from .model import SciBert, PCAReduction, ClusterStrategy


class Pipeline(ABC):
    """Abstract base class for a data science pipeline."""

    @abstractmethod
    def load_data(self):
        """Load the data."""
        pass

    @abstractmethod
    def clean_data(self):
        """Clean the data."""
        pass

    @abstractmethod
    def transform_data(self):
        """Transform the data."""
        pass

    @abstractmethod
    def run_cluster_algorithm(self):
        """Run the algorithm."""
        pass
        
    @abstractmethod
    def run(self):
        """Run the pipeline."""
        pass


class ClusteringPipeline(Pipeline):
    """Concrete implementation of a clustering pipeline."""

    def __init__(self, data_folder_path: str, extraction_strategy: DataExtractionStrategy, cluster_strategy: ClusterStrategy):
        self.data_folder_path = data_folder_path
        self.extraction_strategy = extraction_strategy
        self.cluster_strategy = cluster_strategy

    def load_data(self):
        """Load the data."""
        loader = LearningResourceLoader(self.data_folder_path, self.extraction_strategy)
        self.learning_resources = loader.load_learning_resources()

    def clean_data(self):
        """Clean the data."""
        for resource in self.learning_resources:
            resource.description = clean_text(resource.description)
        
    def transform_data(self):
        """Transform the data."""
        scibert_model = SciBert()
        self.transformed_data = self.learning_resources.to_dataframe()
        vectors = self.transformed_data['description'].apply(scibert_model.embed)

        pca_reduction = PCAReduction()
        reduced_vectors_list = pca_reduction.reduce_dimensionality(self.transformed_data, vectors.tolist())
        self.transformed_data['reduced_vectors'] = reduced_vectors_list


    def run_cluster_algorithm(self, n_clusters):
        """Run the algorithm."""
        labels = self.cluster_strategy.cluster(self.df['reduced_vectors'], n_clusters)
        return labels
        

    def run(self):
        """Run the pipeline."""
        self.load_data()
        self.clean_data()
        self.transform_data()
        self.run_cluster_algorithm()