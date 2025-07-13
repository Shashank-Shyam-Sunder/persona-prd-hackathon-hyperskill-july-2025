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
