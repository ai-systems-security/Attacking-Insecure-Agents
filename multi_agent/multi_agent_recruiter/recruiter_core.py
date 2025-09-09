# recruiter_core.py
import os
import re
from pypdf import PdfReader
import chromadb
import ollama

# -------------------------
# Initialize ChromaDB (persistent)
# -------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("resume_collection")

# -------------------------
# Utility: Load resumes into ChromaDB
# -------------------------
def ingest_resumes(resume_dir="data/resumes", embedding_model="all-minilm"):
    for file in os.listdir(resume_dir):
        if file.endswith(".pdf"):
            name = file.replace("_resume.pdf", "").title()
            reader = PdfReader(os.path.join(resume_dir, file))
            text = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])

            emb = ollama.embeddings(model=embedding_model, prompt=text)["embedding"]
            collection.add(
                ids=[file],
                documents=[text],
                metadatas=[{"name": name}],
                embeddings=[emb]
            )
            print(f"✅ Ingested: {name}")

# -------------------------
# Step 1: Semantic Search Agent
# -------------------------
class SemanticSearchAgent:
    def __init__(self, collection, embedding_model="all-minilm"):
        self.collection = collection
        self.embedding_model = embedding_model

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return ollama.embeddings(model=self.embedding_model, prompt=text)["embedding"]

    def search_candidates(self, job_description, k=3):
        job_emb = self.get_embedding(job_description)
        results = self.collection.query(
            query_embeddings=[job_emb],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        candidates = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            candidates.append({
                "name": meta.get("name", "Unknown"),
                "text": doc,
                "distance": dist
            })
        return candidates

# -------------------------
# Step 2: Evaluation Agent
# -------------------------
class EvaluationAgent:
    def __init__(self, model="llama3.1:8b"):
        self.model = model

    def evaluate_candidate(self, job_desc, name, text):
        system_prompt = (
            "You are an experienced hiring manager. For each candidate, provide:\n"
            "1. Relevant skills\n2. Accomplishments\n3. Gaps\n4. Match Score (1–10)"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Job Description:\n{job_desc}\n\nCandidate: {name}\nRésumé:\n{text}"}
        ]
        resp = ollama.chat(model=self.model, messages=messages)
        return resp["message"]["content"]

    def evaluate_candidates(self, job_desc, candidates):
        evals, memory = [], []
        for c in candidates:
            e = self.evaluate_candidate(job_desc, c["name"], c["text"])
            score = self.extract_match_score(e) or 0
            evals.append({"name": c["name"], "evaluation": e, "distance": c["distance"]})
            memory.append({"name": c["name"], "score": score, "text": c["text"]})
        return evals, memory

    @staticmethod
    def extract_match_score(text):
        m = re.search(r"Match Score.*?(\d{1,2})/10", text)
        return int(m.group(1)) if m else None

# -------------------------
# Step 3: Decision Agent
# -------------------------
class DecisionAgent:
    def select_best_candidate(self, memory):
        if not memory:
            return "❌ No candidates found."
        best = sorted(memory, key=lambda x: x["score"], reverse=True)[0]
        return f"🏆 Best Candidate: {best['name']} (Score: {best['score']}/10)"
