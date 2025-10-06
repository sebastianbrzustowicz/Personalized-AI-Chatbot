from backend.rag.pipeline import RAGPipeline
from backend.data_preprocessing.file_loader import load_text_files
from backend.core.logger import logger

logger.info("🔧 Initializing RAG pipeline (loading model and embeddings)...")
rag = RAGPipeline()

logger.info("📚 Loading documents from data/docs...")
docs = load_text_files("data/docs")
logger.info(f"➡️ Found {len(docs)} chunks. Building vector store...")
rag.build_vectorstore(docs)
logger.info("✅ Vector store ready!")
