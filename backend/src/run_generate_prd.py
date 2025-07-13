# src/run_generate_prd.py

import os
import argparse
import pandas as pd
from .prd_generator import generate_prd, save_prd_to_docx
from .persona_config import PERSONA_TO_FOLDER, PERSONA_DISPLAY_NAMES
from typing import List, Tuple


def run_generate_prd(persona: str, subreddit_file: str):
    display_name = PERSONA_DISPLAY_NAMES.get(persona, persona)
    print(f"\n📝 Generating PRD for Persona: {display_name} / Subreddit: {subreddit_file}")

    # Construct paths
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    subreddit_folder = subreddit_file.replace(".json", "")
    if not persona_folder:
        raise ValueError(f"Invalid persona key: {persona}")

    summary_path = os.path.join("data", "processed", persona_folder, subreddit_folder, "pain_point_summaries.csv")
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Pain point summaries not found at: {summary_path}")

    # Load summaries
    df = pd.read_csv(summary_path)
    print(f"\n📌 Found {len(df)} pain point summaries. Here they are:\n")
    for idx, row in df.iterrows():
        print(f"[{row['cluster_id']}] {row['pain_point_summary']}\n")

    # Prompt user to select cluster IDs
    raw_input = input("👉 Enter comma-separated cluster IDs to include in PRD (e.g. 0,1,4): ").strip()
    selected_ids = [int(cid.strip()) for cid in raw_input.split(",") if cid.strip().isdigit()]
    selected_summaries = df[df['cluster_id'].isin(selected_ids)]['pain_point_summary'].tolist()

    if not selected_summaries:
        print("⚠️ No valid summaries selected. Exiting.")
        return

    # Generate PRD text
    prd_text = generate_prd(selected_summaries, display_name)

    print("\n=== Generated PRD Draft ===\n")
    print(prd_text)

    # Save to DOCX
    output_dir = os.path.join("data", "processed", persona_folder, subreddit_folder)
    os.makedirs(output_dir, exist_ok=True)
    docx_path = os.path.join(output_dir, "PRD_DRAFT.docx")
    save_prd_to_docx(prd_text, docx_path)


def run_generate_prd_api(persona: str, subreddit_file: str, cluster_ids: List[int]) -> Tuple[str, str]:
    """API version of run_generate_prd that accepts cluster IDs directly

    Args:
        persona: The persona key
        subreddit_file: The subreddit JSON filename
        cluster_ids: List of cluster IDs to include in the PRD

    Returns:
        Tuple containing the PRD text and the path to the saved DOCX file
    """
    display_name = PERSONA_DISPLAY_NAMES.get(persona, persona)

    # Construct paths
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    subreddit_folder = subreddit_file.replace(".json", "")
    if not persona_folder:
        raise ValueError(f"Invalid persona key: {persona}")

    summary_path = os.path.join("data", "processed", persona_folder, subreddit_folder, "pain_point_summaries.csv")
    if not os.path.exists(summary_path):
        raise FileNotFoundError(f"Pain point summaries not found at: {summary_path}")

    # Load summaries
    df = pd.read_csv(summary_path)
    selected_summaries = df[df['cluster_id'].isin(cluster_ids)]['pain_point_summary'].tolist()

    if not selected_summaries:
        raise ValueError("No valid summaries selected")

    # Generate PRD text
    prd_text = generate_prd(selected_summaries, display_name)

    # Save to DOCX
    output_dir = os.path.join("data", "processed", persona_folder, subreddit_folder)
    os.makedirs(output_dir, exist_ok=True)
    docx_path = os.path.join(output_dir, "PRD_DRAFT.docx")
    save_prd_to_docx(prd_text, docx_path)

    return prd_text, docx_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PRD from pain point summaries")
    parser.add_argument("--persona", type=str, required=True, help="Persona key (e.g. 'vibecoding')")
    parser.add_argument("--subreddit", type=str, required=True, help="Subreddit JSON filename")
    args = parser.parse_args()
    run_generate_prd(args.persona, args.subreddit)
