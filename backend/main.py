from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import load_text_files
from backend.rag_pipeline import RAGPipeline
import uvicorn

app = FastAPI(title="Local RAG Chatbot")

# Enable CORS for all origins (useful for local React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # zezwalaj na wszystkie domeny
    allow_credentials=True,
    allow_methods=["*"],        # wszystkie metody HTTP
    allow_headers=["*"],        # wszystkie nagłówki
)

# Pipeline initialization (heavy) — performed when the server starts up
print("➡️ Initializing the RAG pipeline. This may take a moment (loading the model & embedding model).")
rag = RAGPipeline()

# Load docs and build vectorstore
print("➡️ Loading documents from data/docs ...")
docs = load_text_files("data/docs")
print(f"➡️ Found {len(docs)} chunks. Building the vector store (embeddings)...")
rag.build_vectorstore(docs)
print("✅ Vector store ready. API server is available.")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(request: Request, k: int = Query(2, ge=1, le=10)):
    body = await request.json()
    question = body.get("question", "")
    print(f"Question: {question}")
    resp = rag.answer(question, k=k)
    retrieved_summary = [
        {
            "id": d["id"],
            "source": d["metadata"].get("source", ""),
            "text_snippet": d["text"][:300]
        }
        for d in resp["retrieved"]
    ]
    return {
        "answer": resp["answer"],
        "retrieved": retrieved_summary
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
