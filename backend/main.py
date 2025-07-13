# backend/main.py

import sys
from pathlib import Path

# 👇 Ensure root directory is in Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

from src import persona_config
from src.prd_generator import generate_prd

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

@app.get("/")
def root():
    return {"message": "PersonaPRD backend is live 🚀"}

@app.get("/personas")
def get_personas():
    return list(persona_config.PERSONA_SUBREDDIT_MAP.keys())

@app.get("/subreddits/{persona}")
def get_subreddits(persona: str):
    try:
        return persona_config.PERSONA_SUBREDDIT_MAP[persona]
    except KeyError:
        raise HTTPException(status_code=404, detail="Persona not found")

@app.get("/painpoints/{persona}/{subreddit}")
def get_painpoints(persona: str, subreddit: str):
    folder_name = persona_config.folder_from_persona_and_subreddit(persona, subreddit)
    painpoint_file = DATA_DIR / folder_name / "pain_point_summaries.csv"

    if not painpoint_file.exists():
        raise HTTPException(status_code=404, detail="No pain point data available")

    df = pd.read_csv(painpoint_file)
    result = []
    for i, row in df.iterrows():
        result.append({
            "id": f"{folder_name}_pp_{i}",
            "summary": row["summary"],
            "postCount": int(row["post_count"]),
            "persona": persona,
            "exampleComments": eval(row["example_comments"]) if isinstance(row["example_comments"], str) else [],
        })
    return result

@app.get("/generate_prd/{persona}/{summary}")
def generate_prd_endpoint(persona: str, summary: str):
    try:
        prd = generate_prd([summary], persona_config.PERSONA_DISPLAY_NAMES[persona])
        return {"prd_text": prd}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
