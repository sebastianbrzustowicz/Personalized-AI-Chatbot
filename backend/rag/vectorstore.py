import chromadb
from chromadb.config import Settings
from typing import List, Dict

class VectorStore:
    def __init__(self, persist_dir: str = None):
        settings = (
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
            if persist_dir
            else Settings()
        )
        self.client = chromadb.Client(settings=settings)
        try:
            self.collection = self.client.get_collection("docs")
        except Exception:
            self.collection = self.client.create_collection("docs")

    def rebuild(self, docs: List[Dict], embeddings):
        """Recreates collection with new embeddings."""
        if not docs:
            raise ValueError("No documents provided.")

        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        metadatas = [{"source": d["source"]} for d in docs]

        emb_list = [e.tolist() for e in embeddings]

        try:
            self.client.delete_collection("docs")
        except Exception:
            pass

        self.collection = self.client.create_collection("docs")
        self.collection.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=emb_list)

    def query(self, query_embedding, k: int = 3) -> List[Dict]:
        res = self.collection.query(query_embeddings=[query_embedding], n_results=k, include=["documents", "metadatas"])
        documents = res.get("documents", [[]])[0]
        metadatas = res.get("metadatas", [[]])[0]
        ids = res.get("ids", [[]])[0]

        return [{"id": _id, "text": doc, "metadata": meta} for _id, doc, meta in zip(ids, documents, metadatas)]
