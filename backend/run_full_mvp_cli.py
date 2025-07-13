# run_full_mvp_cli.py (in project root)

import os
import sys

# ✅ Add src/ to Python path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from user_selection_utils import get_available_personas, get_subreddits_for_persona
from persona_config import DISPLAY_TO_PERSONA, PERSONA_DISPLAY_NAMES
from pipeline import run_pipeline
from run_generate_prd import run_generate_prd


def prompt_user_selection(options, prompt_text):
    print(prompt_text)
    for idx, option in enumerate(options):
        print(f"[{idx}] {option}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and int(choice) in range(len(options)):
            return options[int(choice)]
        else:
            print("❌ Invalid selection. Try again.")


def main():
    print("\n🧠 PersonaPRD CLI MVP Runner\n")

    # Step 1: Choose persona (display name)
    persona_display_names = get_available_personas()
    selected_display_name = prompt_user_selection(persona_display_names, "👉 Choose a persona:")
    persona_key = DISPLAY_TO_PERSONA[selected_display_name]
    print(f"✅ Selected persona: {selected_display_name}\n")

    # Step 2: Choose subreddit file for selected persona
    subreddits = get_subreddits_for_persona(selected_display_name)
    selected_subreddit = prompt_user_selection(subreddits, f"👉 Choose a subreddit for {selected_display_name}:")
    print(f"✅ Selected subreddit: {selected_subreddit}\n")

    # Step 3: Run clustering pipeline
    print(f"\n🚀 Starting full clustering pipeline for:")
    print(f"   👤 Persona  : {selected_display_name}")
    print(f"   📄 Subreddit: {selected_subreddit}\n")
    run_pipeline(persona_key, selected_subreddit)

    # Step 4: Generate PRD using full display name
    run_generate_prd(persona=persona_key, subreddit_file=selected_subreddit)

    print("\n🎉 MVP End-to-End Complete!\n")


if __name__ == "__main__":
    main()
