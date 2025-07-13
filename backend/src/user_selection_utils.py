# src/user_selection_utils.py

import os
from persona_config import DISPLAY_TO_PERSONA, PERSONA_TO_FOLDER

def get_available_personas():
    """
    Returns a list of display names for all available personas.
    Example: ["Vibe Coders (AI coding tool users)", "Self-Hosting Enthusiasts", "Data Professionals"]
    """
    return list(DISPLAY_TO_PERSONA.keys())

def get_subreddits_for_persona(display_name: str):
    """
    Returns a list of subreddit JSON filenames available for the given persona display name.

    Args:
        display_name (str): Display name chosen by the user, e.g. "Vibe Coders (AI coding tool users)"

    Returns:
        List[str]: Subreddit JSON filenames (e.g. ["reddit_datascience_hot_500.json", ...])
    """
    persona_key = DISPLAY_TO_PERSONA.get(display_name)
    if not persona_key:
        raise ValueError(f"Invalid persona display name: {display_name}")

    folder_name = PERSONA_TO_FOLDER.get(persona_key)
    if not folder_name:
        raise ValueError(f"No folder mapping found for persona key: {persona_key}")

    folder_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "raw", "starter_datasets", folder_name)
    )
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Subreddit folder not found: {folder_path}")

    return sorted([f for f in os.listdir(folder_path) if f.endswith(".json")])
