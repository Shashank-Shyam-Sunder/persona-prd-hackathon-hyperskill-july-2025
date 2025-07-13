# backend/main.py

import sys
import os
import signal
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# 👇 Ensure root directory is in Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from pydantic import BaseModel

from src import persona_config
from src.prd_generator import generate_prd
from src.pipeline import run_pipeline
from src.run_generate_prd import run_generate_prd_api

# Load environment variables
load_dotenv()
PORT = int(os.getenv("PORT", 8000))

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models for request validation
class PipelineRequest(BaseModel):
    persona: str
    subreddit: str

class GeneratePRDRequest(BaseModel):
    persona: str
    subreddit: str
    cluster_ids: List[int]

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

@app.get("/")
def root():
    return {"message": "PersonaPRD backend is live 🚀"}

def shutdown_server():
    """Shutdown the server by sending SIGTERM to the current process"""
    pid = os.getpid()
    print(f"\n⛔ Shutting down server (PID: {pid})...")
    os.kill(pid, signal.SIGTERM)

@app.post("/shutdown")
async def shutdown_endpoint(background_tasks: BackgroundTasks):
    """Endpoint to shutdown the server gracefully"""
    background_tasks.add_task(shutdown_server)
    return {"message": "Server shutting down..."}

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

@app.post("/run-pipeline")
def api_run_pipeline(request: PipelineRequest):
    """Run the clustering pipeline for a selected persona and subreddit"""
    try:
        # Convert display name to persona key if needed
        persona_key = request.persona

        # Run the pipeline
        result = run_pipeline(persona_key, request.subreddit)
        return {"message": "Pipeline completed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-prd")
def api_generate_prd(request: GeneratePRDRequest):
    """Generate PRD for selected clusters"""
    try:
        # Generate PRD
        prd_text, docx_path = run_generate_prd_api(
            request.persona, 
            request.subreddit, 
            request.cluster_ids
        )
        return {
            "message": "PRD generated successfully",
            "prd_text": prd_text,
            "docx_path": str(docx_path)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n🚀 Starting PersonaPRD API server on port", PORT)
    print("\n📌 Ways to stop the server:")
    print("   1. Press CTRL+C in this terminal")
    print("   2. Make a POST request to the shutdown endpoint: curl -X POST http://localhost:" + str(PORT) + "/shutdown")
    print("   3. Find and kill the process:")
    print("      - Find the process ID: ps aux | grep uvicorn")
    print("      - Kill the process: kill <PID> (replace <PID> with the process ID number)")
    print("\n🔗 API documentation available at: http://localhost:" + str(PORT) + "/docs\n")
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n⛔ Server stopped by user (CTRL+C)")
        print("✅ Uvicorn process terminated successfully")
