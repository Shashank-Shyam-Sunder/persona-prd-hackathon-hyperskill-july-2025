# src/summarization.py

import os
from typing import List, Dict
from dotenv import load_dotenv
import pandas as pd

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .persona_config import PERSONA_TO_FOLDER

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# LLM model setup
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Fast and cost-efficient
    google_api_key=GOOGLE_API_KEY
)

# Summarization prompt
SUMMARY_PROMPT_TEMPLATE = """
You are an expert Product Manager AI assistant. Summarise the following Reddit posts into a concise pain point summary.

Posts:
{cluster_posts}

Instructions:
- Identify the core pain point(s) expressed in these posts.
- Summarise clearly in 2-3 sentences.
- Do NOT mention Reddit or posts. Only output the pain point summary.

Summary:
"""

prompt = PromptTemplate(
    input_variables=["cluster_posts"],
    template=SUMMARY_PROMPT_TEMPLATE,
)

# Chain setup
summarisation_chain = prompt | model

def summarise_cluster(posts: List[str]) -> str:
    combined_posts = "\n".join(posts)
    response = summarisation_chain.invoke({"cluster_posts": combined_posts})
    return response.content.strip()


def summarise_all_clusters(df: pd.DataFrame, n_clusters: int, persona: str, subreddit_filename: str) -> Dict[int, str]:
    """
    Summarise each cluster using Gemini LLM and cache results in CSV.
    """
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    if not persona_folder:
        raise ValueError(f"Unknown persona '{persona}'")

    subreddit_folder = subreddit_filename.replace(".json", "")
    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", persona_folder, subreddit_folder))
    os.makedirs(output_folder, exist_ok=True)

    output_filepath = os.path.join(output_folder, "pain_point_summaries.csv")

    if os.path.exists(output_filepath):
        print(f"✅ Loading cached summaries from {output_filepath}")
        summary_df = pd.read_csv(output_filepath)
        return dict(zip(summary_df["cluster_id"], summary_df["pain_point_summary"]))

    summaries = {}
    for cluster_id in range(n_clusters):
        cluster_posts = df[df["cluster"] == cluster_id]["cleaned_text"].tolist()
        if cluster_posts:
            print(f"✍️  Summarising cluster {cluster_id} with {len(cluster_posts)} posts...")
            summary = summarise_cluster(cluster_posts)
            summaries[cluster_id] = summary
            print(f"📌 Cluster {cluster_id} summary: {summary}\n")
        else:
            summaries[cluster_id] = "No posts in this cluster."

    summary_df = pd.DataFrame(list(summaries.items()), columns=["cluster_id", "pain_point_summary"])
    summary_df.to_csv(output_filepath, index=False)
    print(f"📄 Saved pain point summaries to {output_filepath}")

    return summaries
