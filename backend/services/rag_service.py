from backend.rag.pipeline import RAGPipeline
from backend.data_preprocessing.file_loader import load_text_files
from backend.core.logger import logger
from backend.core.config import DATA_DIR

logger.info("🔧 Initializing RAG pipeline (loading model and embeddings)...")
rag = RAGPipeline()

logger.info(f"📚 Loading documents from {DATA_DIR}...")
docs = load_text_files(DATA_DIR)
logger.info(f"➡️ Found {len(docs)} chunks. Building vector store...")
rag.build_vectorstore(docs)
logger.info("✅ Vector store ready!")
