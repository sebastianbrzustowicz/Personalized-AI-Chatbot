from typing import List, Dict
from backend.rag.embedder import Embedder
from backend.rag.vectorstore import VectorStore
from backend.rag.llm_model import LocalLLM

class RAGPipeline:
    def __init__(self, model_path=None, sbert_model="all-MiniLM-L6-v2", chroma_persist=None):
        self.embedder = Embedder(sbert_model)
        self.vectorstore = VectorStore(chroma_persist)
        self.llm = LocalLLM(model_path or "./llm_models/llama-2-7b-chat.Q4_K_M/llama-2-7b-chat.Q4_K_M.gguf")

    def build_vectorstore(self, docs: List[Dict]):
        embeddings = self.embedder.encode([d["text"] for d in docs])
        self.vectorstore.rebuild(docs, embeddings)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        query_emb = self.embedder.encode([query])[0]
        return self.vectorstore.query(query_emb, k)

    def answer(self, question: str, k: int = 3) -> Dict:
        retrieved = self.retrieve(question, k=k)
        context = ""
        max_context_tokens = 1200

        for d in retrieved:
            chunk_text = f"Source: {d['metadata'].get('source', '')}\n{d['text']}\n"
            if len(context) + len(chunk_text) > max_context_tokens * 4:
                break
            context += chunk_text

        prompt = f"""
        You are a helpful assistant. Answer **only** based on the provided context.
        Use bullet points when possible. Avoid adding extra information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        answer = self.llm.generate(prompt)
        return {"answer": answer, "retrieved": retrieved, "prompt": prompt}
