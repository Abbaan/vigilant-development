import pandas as pd
from .data_processing import process_data, markdown_files_to_df
from .model import text_to_vector
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def process_courses(folder_path):
    # Step 1: Read the data
    df = markdown_files_to_df(folder_path)
    df['cleaned_description'] = df['description'].apply(process_data)

    # Step 2: Vectorize descriptions and maintain a mapping
    vectors = df['cleaned_description'].apply(text_to_vector)
    df['vector'] = vectors

    # Step 3: Reduce the dimensionality of the vectors
    vectors = df['vector'].tolist()
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(vectors)
    df['reduced_vectors'] = reduced_vectors.tolist()

    return df
