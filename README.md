# PersonaPRD – AI Hackathon July 2025 🚀

**PersonaPRD** is an AI-powered system developed during the **AI Hackathon July 2025**. It transforms unstructured Reddit feedback into structured, persona-specific **Product Requirements Documents (PRDs)** using semantic embeddings, clustering, and Gemini-based summarization.

> 🎯 The goal: Accelerate early-stage product discovery and prioritization by extracting pain points directly from community conversations.

---

## 🔍 What It Does

1. **Loads persona-aligned Reddit data** from curated datasets.
2. **Cleans and embeds posts** using SBERT (`all-MiniLM-L6-v2`).
3. **Clusters posts** with UMAP + KMeans for topic grouping.
4. **Computes diagnostics** like silhouette and intra/inter-cluster distance ratios.
5. **Summarizes each cluster** into user pain points using Gemini (LangChain).
6. **Lets you select clusters** to auto-generate a structured PRD (.docx).

---

## 🗂️ Project Structure

```bash
persona-prd-hackathon-hyperskill-july-2025/
│
├── .venv/                                 # Python virtual environment (optional)
├── .env                                   # API credentials (GOOGLE_API_KEY)
├── requirements.txt                       # Python dependencies
├── README.md                              # You're reading it
│
├── run_full_mvp_cli.py                    # 🧠 Run full pipeline via CLI (embedding → PRD)
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

---

## 🚀 Quickstart

### 1. 🔧 Install requirements

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. 🔑 Set your `.env`

Create a file named `.env` in the root and add your Google API key:

```bash
GOOGLE_API_KEY=your-real-key-here
```

### 3. 🧠 Run the full MVP pipeline

```bash
python run_full_mvp_cli.py
```

You'll be prompted to:
- Select a **persona**
- Select a **subreddit dataset**
- Review pain point summaries
- Select which clusters to include in the PRD

---

## 📄 Output Examples

After running the pipeline, you’ll get:

- ✅ `clusters_KMeans_UMAP.csv`: Cluster labels for each post
- ✅ `cluster_diagnostics_metrics.csv`: Silhouette and distance metrics
- ✅ `pain_point_summaries.csv`: Gemini-based summaries per cluster
- ✅ `PRD_DRAFT.docx`: A fully structured PRD

---

## 💡 Ideal Use Cases

- Product Managers and Designers doing early-stage **user discovery**
- AI teams building **semantic feedback clustering** tools
- Startups validating ideas using community pain points

---

## 🧠 Credits

Built by [Team PersonaPRD](https://github.com/Shashank-Shyam-Sunder) as part of the **Hyperskill AI Engineer Bootcamp + Hackathon (July 2025)**.

---

## 📜 License

MIT License — feel free to fork, use, and build on top of this.
