# src/persona_config.py

# Maps the display name (used in UI) to the internal persona key
DISPLAY_TO_PERSONA = {
    "Vibe Coders (AI coding tool users)": "vibecoding",
    "Self-Hosting Enthusiasts": "selfhost",
    "Data Professionals": "data"
}

# Maps internal persona key to the folder name in data/raw/starter_datasets/
PERSONA_TO_FOLDER = {
    "vibecoding": "vibecoding_neighbourhood",
    "selfhost": "selfhost_neighbourhood",
    "data": "data_neighbourhood"
}

# Reverse mapping: internal persona key to display name
PERSONA_DISPLAY_NAMES = {v: k for k, v in DISPLAY_TO_PERSONA.items()}

# Maps persona keys to available subreddits
PERSONA_SUBREDDIT_MAP = {
    "vibecoding": [
        "reddit_ChatGPTCoding_hot_500.json",
        "reddit_ClaudeAI_hot_500.json",
        "reddit_PromptEngineering_hot_500.json",
        "reddit_Windsurf_hot_500.json",
        "reddit_cursor_hot_500.json",
        "reddit_replit_hot_500.json"
    ],
    "selfhost": ["reddit_LocalLLM_hot_500.json"],
    "data": ["reddit_BusinessIntelligence_hot_500.json"]
}

def folder_from_persona_and_subreddit(persona: str, subreddit: str) -> str:
    """
    Constructs a folder path from persona and subreddit.

    Args:
        persona (str): The persona key (e.g., 'vibecoding')
        subreddit (str): The subreddit filename (e.g., 'reddit_ChatGPTCoding_hot_500.json')

    Returns:
        str: The folder path (e.g., 'vibecoding_neighbourhood/reddit_ChatGPTCoding_hot_500')
    """
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    if not persona_folder:
        raise ValueError(f"Invalid persona key: {persona}")

    subreddit_folder = subreddit.replace(".json", "")
    return f"{persona_folder}/{subreddit_folder}"
