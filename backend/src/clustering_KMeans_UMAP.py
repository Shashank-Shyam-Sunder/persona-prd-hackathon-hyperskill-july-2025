# src/clustering_kMeans_UMAP.py

import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import umap
import warnings
from persona_config import PERSONA_TO_FOLDER

warnings.filterwarnings("ignore", message="n_jobs value 1 overridden to 1 by setting random_state")


def cluster_embeddings_kmeans_umap(embeddings: np.ndarray, n_clusters: int = 10, n_components: int = 10, random_state: int = 42) -> np.ndarray:
    """
    Reduce dimensionality with UMAP and cluster using KMeans.
    """
    print(f"Reducing dimensionality with UMAP to {n_components} components...")
    reducer = umap.UMAP(n_components=n_components, random_state=random_state)
    scaled_embeddings = StandardScaler().fit_transform(embeddings)
    reduced_embeddings = reducer.fit_transform(scaled_embeddings)

    print(f"Clustering reduced embeddings into {n_clusters} clusters using KMeans...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans.fit_predict(reduced_embeddings)
    print("Clustering completed.")
    return labels


def save_cluster_labels_kmeans_umap(labels: np.ndarray, persona: str, subreddit_filename: str):
    """
    Save cluster labels to a structured folder path:
    data/processed/<persona_folder>/<subreddit_folder>/clusters_KMeans_UMAP.csv
    """
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    if not persona_folder:
        raise ValueError(f"Unknown persona '{persona}'")

    subreddit_folder = subreddit_filename.replace('.json', '')
    output_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "processed", persona_folder, subreddit_folder)
    )
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "clusters_KMeans_UMAP.csv")
    pd.DataFrame({"cluster": labels}).to_csv(output_path, index=False)
    print(f"Saved cluster labels to {output_path}")


# Optional test
if __name__ == "__main__":
    dummy_embeddings = np.random.rand(100, 384)
    dummy_labels = cluster_embeddings_kmeans_umap(dummy_embeddings, n_clusters=10)
    save_cluster_labels_kmeans_umap(dummy_labels, "vibecoding", "reddit_PromptEngineering_hot_500.json")
