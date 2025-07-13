import json
import os
import pandas as pd

# ===== Friendly Persona Names for Frontend Display =====
FRIENDLY_PERSONA_NAMES = {
    "vibecoding": "Vibe Coders: Users of AI coding tools",
    "selfhost": "Self-Hosting Enthusiasts: Privacy + Infrastructure",
    "data": "Data Professionals: BI + Engineering + Science",
}

# ===== Mapping to internal folder structure =====
PERSONA_TO_FOLDER = {
    "vibecoding": "vibecoding_neighbourhood",
    "selfhost": "selfhost_neighbourhood",
    "data": "data_neighbourhood"
}

def get_json_filepath(persona: str, subreddit_filename: str) -> str:
    base_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "starter_datasets"))
    persona_folder = PERSONA_TO_FOLDER.get(persona)
    if not persona_folder:
        raise ValueError(f"Unknown persona '{persona}'. Valid options: {list(PERSONA_TO_FOLDER.keys())}")

    full_path = os.path.join(base_folder, persona_folder, subreddit_filename)
    print(f"Looking for file at: {full_path}")
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"File not found: {full_path}")

    return full_path

def load_reddit_data(json_filepath: str) -> pd.DataFrame:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    data = []
    for post in posts:
        post_id = post.get('id') or post.get('post_id') or ""
        title = post.get('title') or ""
        selftext = post.get('selftext') or ""
        combined_text = f"{title.strip()}\n{selftext.strip()}".strip()
        data.append({
            'post_id': post_id,
            'title': title,
            'selftext': selftext,
            'combined_text': combined_text
        })

    return pd.DataFrame(data)

def load_data_for_persona_subreddit(persona: str, subreddit_filename: str) -> pd.DataFrame:
    filepath = get_json_filepath(persona, subreddit_filename)
    return load_reddit_data(filepath)

def list_available_subreddits(persona: str):
    folder_name = PERSONA_TO_FOLDER.get(persona)
    if not folder_name:
        raise ValueError(f"Unknown persona key: {persona}")
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "starter_datasets", folder_name))
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Persona folder not found: {folder_path}")

    files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
    return files

def get_readable_subreddit_name(filename: str) -> str:
    if filename.startswith("reddit_") and filename.endswith(".json"):
        middle = filename[len("reddit_"):-len("_hot_500.json")]
        return f"r/{middle} (top 500)"
    return filename

if __name__ == "__main__":
    persona = "vibecoding"
    subreddit_file = "reddit_PromptEngineering_hot_500.json"
    df = load_data_for_persona_subreddit(persona, subreddit_file)
    print(f"Loaded {len(df)} posts from persona '{persona}' and subreddit file '{subreddit_file}'")
    print(df.head(3))

    print("\nAvailable subreddits for 'selfhost':")
    print(list_available_subreddits("selfhost"))
