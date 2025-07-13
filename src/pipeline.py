# src/pipeline.py

import os
import argparse
from data_loader import load_data_for_persona_subreddit
from preprocessing import preprocess_texts
from embedding import load_or_generate_embeddings
from clustering_KMeans_UMAP import cluster_embeddings_kmeans_umap, save_cluster_labels_kmeans_umap
from cluster_diagnostics_module import run_cluster_diagnostics
from summarization import summarise_all_clusters
from persona_config import PERSONA_TO_FOLDER


def run_pipeline(persona: str, subreddit_file: str):
    # NOTE: No duplicate print here — already handled in CLI
    # If you need logging, prefer using a logging framework later

    # ───────────────────────────────────────────────────────────────
    # STEP 1: Load Reddit data for the selected persona/subreddit
    # ───────────────────────────────────────────────────────────────
    df = load_data_for_persona_subreddit(persona, subreddit_file)
    print(f"📥 Loaded {len(df)} posts.")

    # ───────────────────────────────────────────────────────────────
    # STEP 2: Clean and normalize the text
    # ───────────────────────────────────────────────────────────────
    df["cleaned_text"] = preprocess_texts(df["combined_text"])
    print("🧼 Text cleaning and preprocessing complete.")

    # ───────────────────────────────────────────────────────────────
    # STEP 3: Generate or load cached sentence embeddings
    # ───────────────────────────────────────────────────────────────
    embeddings = load_or_generate_embeddings(df["cleaned_text"].tolist(), persona, subreddit_file)
    print(f"🔑 Embeddings ready. Shape: {embeddings.shape}")

    # ───────────────────────────────────────────────────────────────
    # STEP 4: Apply UMAP + KMeans for clustering
    # ───────────────────────────────────────────────────────────────
    labels = cluster_embeddings_kmeans_umap(embeddings, n_clusters=10, n_components=10)
    df["cluster"] = labels
    print(f"🔗 Clustering done. Total clusters: {len(set(labels))}")

    # ───────────────────────────────────────────────────────────────
    # STEP 5: Save cluster labels
    # ───────────────────────────────────────────────────────────────
    save_cluster_labels_kmeans_umap(labels, persona, subreddit_file)

    # ───────────────────────────────────────────────────────────────
    # STEP 6: Run cluster diagnostics
    # ───────────────────────────────────────────────────────────────
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    subreddit_folder = subreddit_file.replace(".json", "")
    output_folder = os.path.join("data", "processed", persona_folder, subreddit_folder)
    os.makedirs(output_folder, exist_ok=True)
    run_cluster_diagnostics(embeddings, labels, output_folder)

    # ───────────────────────────────────────────────────────────────
    # STEP 7: Summarise each cluster
    # ───────────────────────────────────────────────────────────────
    print("🧠 Summarising clusters using Gemini LLM (with caching)...")
    summarise_all_clusters(df, n_clusters=10, persona=persona, subreddit_filename=subreddit_file)
    print("📝 Cluster summaries generated.\n")

    # ───────────────────────────────────────────────────────────────
    # DONE
    # ───────────────────────────────────────────────────────────────
    print(f"✅ Pipeline completed successfully for {persona} / {subreddit_file}")
    print(f"📁 Results saved to: {output_folder}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run clustering pipeline for a given persona and subreddit")
    parser.add_argument("--persona", type=str, required=True, help="Persona key (e.g. 'vibecoding')")
    parser.add_argument("--subreddit", type=str, required=True,
                        help="Subreddit JSON file (e.g. 'reddit_cursor_hot_500.json')")

    args = parser.parse_args()
    run_pipeline(args.persona, args.subreddit)
