from fastapi import FastAPI, Query
from app.utils import load_text_files
from app.rag_pipeline import RAGPipeline
import uvicorn

app = FastAPI(title="Local RAG Chatbot")

# Path to the model
#MODEL_PATH = os.environ.get("LLM_MODEL_PATH", "./llm_models/llama-2-7b-chat.Q4_K_M/llama-2-7b-chat.Q4_K_M.gguf")

# Pipeline initialization (heavy) — performed when the server starts up
print("➡️  Initializing the RAG pipeline. This may take a moment (loading the model & embedding model).")
#rag = RAGPipeline(model_path=MODEL_PATH)
rag = RAGPipeline()

# Load docs and build vectorstore
print("➡️  Loading documents from data/docs ...")
docs = load_text_files("data/docs")
print(f"➡️  Found {len(docs)} chunks. Building the vector store (embeddings)...")
rag.build_vectorstore(docs)
print("✅ Vector store ready. API server is available.")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ask")
def ask(question: str = Query(..., description="Question to chatbot"), k: int = Query(3, ge=1, le=10)):
    """
    Returns the generated response and a list of retrieved chunks (id + source).
    """
    print(f"Question: {question}")
    resp = rag.answer(question, k=k)
    retrieved_summary = [{"id": d["id"], "source": d["metadata"].get("source", ""), "text_snippet": d["text"][:300]} for d in resp["retrieved"]]
    return {
        "answer": resp["answer"],
        "retrieved": retrieved_summary
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
