from fastapi import FastAPI
from backend.routers import chat, health
from backend.core.logger import logger
from backend.core.config import setup_cors

app = FastAPI(title="Local RAG Chatbot")

setup_cors(app)

app.include_router(chat.router)
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI app...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
