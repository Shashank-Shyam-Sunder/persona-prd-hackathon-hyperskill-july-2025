# src/cluster_diagnostics_module.py

import numpy as np
import os
import pandas as pd
from sklearn.metrics import silhouette_score


def compute_intra_inter_cluster_distances(embeddings, labels):
    unique_labels = set(labels)
    if -1 in unique_labels:
        unique_labels.remove(-1)  # Exclude noise, if any

    intra_dists = []
    inter_dists = []

    centroids = {}

    for label in unique_labels:
        cluster_points = embeddings[labels == label]
        if len(cluster_points) < 2:
            continue
        centroid = cluster_points.mean(axis=0)
        centroids[label] = centroid

        # Intra-cluster distances: distance of each point to its cluster centroid
        dists = np.linalg.norm(cluster_points - centroid, axis=1)
        intra_dists.extend(dists)

    # Inter-cluster distances: distance between cluster centroids
    cluster_ids = list(centroids.keys())
    for i in range(len(cluster_ids)):
        for j in range(i + 1, len(cluster_ids)):
            dist = np.linalg.norm(centroids[cluster_ids[i]] - centroids[cluster_ids[j]])
            inter_dists.append(dist)

    return intra_dists, inter_dists


def run_cluster_diagnostics(embeddings, labels, output_folder):
    """
    Compute and save clustering diagnostics including:
    - Silhouette score
    - Intra/inter-cluster distances
    - Summary CSV of all metrics
    """
    print("\n📊 Running clustering diagnostics...")

    os.makedirs(output_folder, exist_ok=True)

    # Metrics
    silhouette = silhouette_score(embeddings, labels)
    intra, inter = compute_intra_inter_cluster_distances(embeddings, labels)
    intra_mean = np.mean(intra)
    inter_mean = np.mean(inter)
    intra_inter_ratio = intra_mean / inter_mean
    num_clusters = len(set(labels))

    print(f"📈 Silhouette Score: {silhouette:.4f}")
    print(f"📌 Avg. Intra-cluster distance: {intra_mean:.4f}")
    print(f"📍 Avg. Inter-cluster distance: {inter_mean:.4f}")
    print(f"📉 Intra/Inter Ratio (lower is better): {intra_inter_ratio:.4f}")

    # Save metrics CSV
    metrics_df = pd.DataFrame({
        "silhouette_score": [silhouette],
        "avg_intra_cluster_distance": [intra_mean],
        "avg_inter_cluster_distance": [inter_mean],
        "intra_inter_ratio": [intra_inter_ratio],
        "num_clusters": [num_clusters]
    })

    metrics_path = os.path.join(output_folder, "cluster_diagnostics_metrics.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"📁 Saved diagnostics CSV to: {metrics_path}")
