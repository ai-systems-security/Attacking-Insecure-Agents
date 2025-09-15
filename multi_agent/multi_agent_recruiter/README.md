# 🤖 Multi Agentic Recruiter

This project demonstrates a simple AI-powered resume screening system built with **Ollama LLM**, **Chroma vector database**, and **PDF resume parsing**.  

---

## 📂 Project Structure

### `recruiter_core.py`
Implements the **core recruiter logic**:

- **PDF Ingestion**
  - Extracts text from resume PDFs with `pypdf`.
  - Generates embeddings using `ollama.embeddings`.
  - Stores embeddings in a persistent Chroma collection.

- **Agents**
  - **Semantic Search Agent**
    - Queries Chroma for resumes most relevant to a given job description.
    - Returns top-k candidates with similarity distances.
  - **Evaluation Agent**
    - Uses `ollama.chat` to analyze each resume against the job description.
    - Produces natural language output with a “Match Score (1–10)”.
    - Relies on **regex parsing** to extract the score.
  - **Decision Agent**
    - Selects the best candidate by comparing match scores.
    - Ignores retrieval distance, relying only on LLM scores.

### `multi_agent_runner.py`
Coordinates the recruiter pipeline:

1. Ingest PDFs from `data/resumes/`.
2. Define a **job description**.
3. Run the **Semantic Search Agent** to retrieve top-k candidates.
4. Use the **Evaluation Agent** to score each resume.
5. Apply the **Decision Agent** to pick the highest-scoring candidate.

---

## ⚙️ Requirements

- **Python 3.10+**
- Dependencies:
  ```bash
  pip install ollama chromadb pypdf

---

## ▶️ Usage
- **How to Run:**
```bash
C:\...\attacking_insecure_agents\multi_agent\multi_agent_recruiter> python multi_agent_runner.py "We are seeking a Software Engineer with strong Python and Machine Learning skill.Experience with data pipelines and cloud deployment is a plus."
```
- **How to Attack:**
```bash
cd C:\...\attacking_insecure_agents\multi_agent
python -m multi_agent_recruiter.attack.test_redteam
```





