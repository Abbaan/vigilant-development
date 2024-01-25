import pandas as pd
from .data_processing import process_data
from .model import text_to_vector
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def process_courses(file_path):
    # Step 1: Read the data
    df = pd.read_csv(file_path)
    df['cleaned_description'] = df['description'].apply(process_data)

    # Step 2: Vectorize descriptions and maintain a mapping
    vectors = df['cleaned_description'].apply(text_to_vector)
    df['vector'] = vectors

    # Step 3: Create a mapping (vector to course information)
    mapping = df.set_index('vector')[['rating', 'link']]

    # Step 4: Reduce the dimensionality of the vectors
    vectors = df['vector'].tolist()
    pca = PCA(n_components=3)
    reduced_vectors = pca.fit_transform(vectors)
    df['reduced_vectors'] = reduced_vectors.tolist()
    
    return df, mapping


def perform_clustering(data, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    labels = kmeans.labels_
    return labels




# Example Usage
# df, mapping = process_courses('path_to_your_file.csv')
