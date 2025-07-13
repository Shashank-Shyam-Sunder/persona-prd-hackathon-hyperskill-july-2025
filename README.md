
# PersonaPRD – AI Hackathon July 2025 🚀

PersonaPRD is an AI-powered system developed during the AI Hackathon July 2025. 
It transforms unstructured Reddit feedback into structured, persona-specific 
Product Requirements Documents (PRDs) using semantic embeddings, clustering, 
and Gemini-based summarization.

🎯 **The goal**: Accelerate early-stage product discovery and prioritization 
by extracting pain points directly from community conversations.

## 🔍 What It Does

- Loads persona-aligned Reddit data from curated datasets.
- Cleans and embeds posts using SBERT (`all-MiniLM-L6-v2`).
- Clusters posts with UMAP + KMeans for topic grouping.
- Computes diagnostics like silhouette and intra/inter-cluster distance ratios.
- Summarizes each cluster into user pain points using Gemini (LangChain).
- Lets you select clusters to auto-generate a structured PRD (`.docx`).

## 🗂️ Project Structure

```
persona-prd-hackathon-hyperskill-july-2025/
│
├── .venv/                                 # Python virtual environment (optional)
├── .env                                   # API credentials (GOOGLE_API_KEY, PORT)
├── .env.example                           # Example environment variables
├── requirements.txt                       # Python dependencies
├── README.md                              # You're reading it
│
├── run_full_mvp_cli.py                    # 🧠 Run full pipeline via CLI (embedding → PRD)
├── backend/main.py                        # 🌐 API server implementation
│
├── data/
│   ├── raw/
│   │   └── starter_datasets/
│   │       ├── data_neighbourhood/
│   │       │   ├── reddit_BusinessIntelligence_hot_500.json
│   │       ├── vibecoding_neighbourhood/
│   │       ├── selfhost_neighbourhood/
│   │       └── ...
│   │
│   └── processed/
│       ├── data_neighbourhood/
│       │   └── reddit_BusinessIntelligence_hot_500/
│       │       ├── clusters_KMeans_UMAP.csv
│       │       ├── cluster_diagnostics_metrics.csv
│       │       ├── pain_point_summaries.csv
│       │       └── PRD_DRAFT.docx
│       ├── vibecoding_neighbourhood/
│       └── ...
│
├── src/
│   ├── __init__.py
│   ├── pipeline.py                        # Core pipeline logic
│   ├── run_generate_prd.py               # CLI for generating PRD only
│   ├── data_loader.py                    # Load Reddit JSON
│   ├── preprocessing.py                  # Clean + normalize post text
│   ├── embedding.py                      # Generate + cache embeddings
│   ├── clustering_KMeans_UMAP.py         # UMAP + KMeans clustering
│   ├── cluster_diagnostics_module.py     # Diagnostics: silhouette, intra/inter
│   ├── summarization.py                  # Summarize each cluster with Gemini
│   ├── prd_generator.py                  # Convert pain points to structured PRD
│   ├── persona_config.py                 # Mapping between keys, display names
│   ├── user_selection_utils.py           # CLI user prompts
│   └── utils.py                          # Save PRD as .docx
```

## 🚀 Quickstart

1. 🔧 **Install requirements**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. 🔑 **Set your .env**

Create a file named `.env` in the root and add your Google API key:

```env
GOOGLE_API_KEY=your-real-key-here
```
To generate Google API key,
open
https://aistudio.google.com/app/u/1/apikey?pli=1
Click on "Create API key" and follow instructions.

3. 🧠 **Run the full MVP pipeline**

```bash
python run_full_mvp_cli.py
```

You'll be prompted to:

- Select a persona
- Select a subreddit dataset
- Review pain point summaries
- Select which clusters to include in the PRD

## 🌐 API Version

In addition to the CLI version, PersonaPRD also provides a REST API that allows 
you to access the same functionality via HTTP requests.

### Setting Up the API

1. 🔑 **Update your .env file**

Make sure your `.env` file includes both the Google API key and the PORT:

```env
GOOGLE_API_KEY=your-real-key-here
PORT=8000
```

2. 🚀 **Run the API server**

```bash
cd backend
python main.py
```

The server will start on port 8000 
(or the port specified in your .env file).

### API Endpoints

The API provides the following endpoints:

- `GET /personas`: Get all available personas
- `GET /subreddits/{persona}`: Get subreddits for a specific persona
- `POST /run-pipeline`: Run the clustering pipeline for a selected persona 
  and subreddit
- `POST /generate-prd`: Generate a PRD for selected clusters

### API Documentation

FastAPI provides automatic interactive API documentation.
Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

These interfaces allow you to explore and test all available endpoints 
directly from your browser.

### API Usage Examples

#### Run Pipeline
```
POST /run-pipeline
Content-Type: application/json

{
  "persona": "vibecoding",
  "subreddit": "reddit_cursor_hot_500.json"
}
```

#### Generate PRD
```
POST /generate-prd
Content-Type: application/json

{
  "persona": "vibecoding",
  "subreddit": "reddit_cursor_hot_500.json",
  "cluster_ids": [0, 1, 4]
}
```

For more details on the API implementation, see the 
`There_is_a_console_application_performs.md` file, which describes 
the process of converting the CLI application to an API.

## 📄 Output Examples

After running the pipeline, you’ll get:

- ✅ `clusters_KMeans_UMAP.csv`: Cluster labels for each post
- ✅ `cluster_diagnostics_metrics.csv`: Silhouette and distance metrics
- ✅ `pain_point_summaries.csv`: Gemini-based summaries per cluster
- ✅ `PRD_DRAFT.docx`: A fully structured PRD

## 🧾 Data Format

Each dataset is a `.json` file containing an array of Reddit posts, where each post includes:

- **Post metadata**: `id`, `title`, `selftext`, `url`, `score`, `upvote_ratio`, 
  `num_comments`, `created_utc`, `author`, `subreddit`
- **Post flags**: e.g., `is_self`, `stickied`, `locked`, `spoiler`, etc.
- **Comment threads** (up to 100): Nested objects with `id`, `body`, `score`, 
  `created_utc`, `author`, and parent relationships
- **Engagement metrics**: Vote scores, comment counts, interaction ratios

**📌 Current Scope in MVP:**  
We currently use only the **post title** and **selftext** for our semantic analysis. 
These are combined into a single string (`combined_text`) per post to generate embeddings.

> 💡 Developers can experiment with incorporating other metadata 
> (e.g., comment threads, engagement) for more nuanced clustering and insights.

## 🔬 Embedding & Model Configuration

- **Embeddings**: We use `sentence-transformers/all-MiniLM-L6-v2`, producing 384-dimensional embeddings.
  - ✅ Lightweight, fast, suitable for hackathon constraints
  - 💡 You can swap this out with higher-dimensional models like `OpenAI`'s 
    `text-embedding-3-large` for potentially better clustering and semantic results

- **LLM Summarization**: We currently use `Gemini 1.5 Flash` via LangChain 
  to summarize clusters and generate PRDs.
  - 💡 Swap in your preferred model (e.g., GPT-4, Claude) for improved quality 
    or domain-specific tuning.

## 💡 Ideal Use Cases

- Product Managers and Designers doing early-stage user discovery
- AI teams building semantic feedback clustering tools
- Startups validating ideas using community pain points

## 🧠 Credits

Built by Team PersonaPRD as part of the Hyperskill AI Engineer Bootcamp + 
Hackathon (July 2025).

## 📜 License

MIT License — feel free to fork, use, and build on top of this.
