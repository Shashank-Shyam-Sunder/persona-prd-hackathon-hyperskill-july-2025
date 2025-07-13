# src/embedding.py

import os
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

# Lightweight SBERT model
model_name = "all-MiniLM-L6-v2"
sbert_model = SentenceTransformer(model_name)

# Folder mapping (same as used in data_loader)
PERSONA_TO_FOLDER = {
    "vibecoding": "vibecoding_neighbourhood",
    "selfhost": "selfhost_neighbourhood",
    "data": "data_neighbourhood"
}

def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of texts using Sentence Transformers.
    """
    return sbert_model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

def get_embedding_cache_path(persona: str, subreddit_filename: str) -> str:
    """
    Return structured path to cache embeddings in a dedicated folder per subreddit.
    Example: data/processed/data_neighbourhood/reddit_BusinessIntelligence_hot_500/embeddings.npy
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    if not persona_folder:
        raise ValueError(f"Unknown persona '{persona}'. Valid options: {list(PERSONA_TO_FOLDER.keys())}")

    subreddit_folder = subreddit_filename.replace(".json", "")
    full_dir = os.path.join(base_path, persona_folder, subreddit_folder)
    os.makedirs(full_dir, exist_ok=True)

    return os.path.join(full_dir, "embeddings.npy")

def load_or_generate_embeddings(texts: List[str], persona: str, subreddit_filename: str) -> np.ndarray:
    """
    Load cached embeddings if available, else generate and save to disk.
    """
    embedding_path = get_embedding_cache_path(persona, subreddit_filename)

    if os.path.exists(embedding_path):
        print(f"Loading cached embeddings from {embedding_path}")
        return np.load(embedding_path)
    else:
        print(f"No cached embeddings found. Generating embeddings for {persona} - {subreddit_filename}...")
        embeddings = generate_embeddings(texts)
        np.save(embedding_path, embeddings)
        print(f"Saved embeddings to {embedding_path}")
        return embeddings

# Optional test case
if __name__ == "__main__":
    texts = [
        "LLMs are reshaping how we write code.",
        "Best tools for self-hosting AI models?",
        "How to choose a vector database?"
    ]
    embs = load_or_generate_embeddings(texts, "vibecoding", "reddit_PromptEngineering_hot_500.json")
    print(f"Embeddings shape: {embs.shape}")
