from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from typing import List, Dict
from ctransformers import AutoModelForCausalLM, AutoConfig

# Change the path to the model if it is different
#DEFAULT_MODEL_PATH = "./llm_models/llama-2-7b-chat.Q4_K_M/llama-2-7b-chat.Q4_K_M.gguf"
DEFAULT_MODEL_PATH = "./llm_models/bielik_Q6/bielik-7b-instruct-v0.1.Q6_K.gguf"

class RAGPipeline:
    def __init__(self,
                 model_path: str = DEFAULT_MODEL_PATH,
                 sbert_model: str = "all-MiniLM-L6-v2",
                 chroma_persist: str = None):
        # 1) embedding model
        self.embedder = SentenceTransformer(sbert_model)

        # 2) chroma client (in-memory by default; persist if passed)
        if chroma_persist:
            settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=chroma_persist)
        else:
            settings = Settings()
        self.client = chromadb.Client(settings=settings)
        # create or get collection
        try:
            self.collection = self.client.get_collection("docs")
        except Exception:
            self.collection = self.client.create_collection("docs")

        # 3) configuration and load of local LLM
        config = AutoConfig.from_pretrained(model_path)
        config.config.context_length = 1200   # context length setting
        config.config.max_new_tokens = 300   # max new tokens setting

        # adjust gpu_layers according to your hardware
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="llama",
            gpu_layers=50,
            config=config
        )
        # generation settings
        self.max_new_tokens = 300

    def build_vectorstore(self, docs: List[Dict]):
        """
        docs: list of {"id":.., "text":.., "source":..}
        """
        if len(docs) == 0:
            raise ValueError("No documents to load into vectorstore.")

        texts = [d["text"] for d in docs]
        ids = [d["id"] for d in docs]
        metadatas = [{"source": d["source"]} for d in docs]

        # compute embeddings (returns numpy arrays)
        emb = self.embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

        # Chroma expects a list of embedding lists
        emb_list = [e.tolist() for e in emb]

        # If collection has existing docs, remove or re-create (for prototype: we recreate)
        try:
            # remove any existing collection and recreate to ensure fresh state
            self.client.delete_collection("docs")
        except Exception:
            pass
        self.collection = self.client.create_collection("docs")
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=emb_list
        )

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        q_emb = self.embedder.encode([query], convert_to_numpy=True)[0].tolist()
        res = self.collection.query(query_embeddings=[q_emb], n_results=k, include=["documents", "metadatas"])
        docs = []
        # res has 'documents' as list of lists because we queried 1 item
        documents = res.get("documents", [[]])[0]
        metadatas = res.get("metadatas", [[]])[0]
        ids = res.get("ids", [[]])[0]
        for _id, doc_text, meta in zip(ids, documents, metadatas):
            docs.append({"id": _id, "text": doc_text, "metadata": meta})
        return docs

    def generate(self, prompt: str) -> str:
        # model behaves as callable and returns text (ctranformers)
        resp = self.model(prompt, max_new_tokens=self.max_new_tokens)
        # ensure string
        if isinstance(resp, str):
            return resp.strip()
        # some wrapper return list/dict — be defensive
        try:
            # if resp is list of dicts
            if isinstance(resp, list) and len(resp) > 0:
                return str(resp[0]).strip()
        except Exception:
            pass
        return str(resp).strip()

    def answer(self, question: str, k: int = 3) -> Dict:
        # 1) retrieve
        retrieved = self.retrieve(question, k=k)
        
        # 2) limit the number of context tokens
        context = ""
        max_context_tokens = 1200  # leave 100 tokens for the prompt and response
        for d in retrieved:
            chunk_text = f"Source: {d['metadata'].get('source', '')}\n{d['text']}\n"
            # simple token estimation: ~1 token ≈ 4 characters
            if len(context) + len(chunk_text) > max_context_tokens*4:
                break
            context += chunk_text

        # 3) prompt
        prompt = f"""
        You are a helpful assistant. Answer **only** based on the provided context. Do not add any additional information. The answer should be short and in bullet points, if possible.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        # 4) generate
        answer = self.generate(prompt)
        return {
            "answer": answer,
            "retrieved": retrieved,
            "prompt": prompt
        }
