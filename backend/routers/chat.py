from fastapi import APIRouter, Request, Query
from backend.services.rag_service import rag, logger

router = APIRouter()

@router.post("/ask")
async def ask(request: Request, k: int = Query(2, ge=1, le=10)):
    """Main chatbot endpoint"""
    body = await request.json()
    question = body.get("question", "")
    logger.info(f"User question: {question}")

    resp = rag.answer(question, k=k)
    retrieved_summary = [
        {
            "id": d["id"],
            "source": d["metadata"].get("source", ""),
            "text_snippet": d["text"][:300],
        }
        for d in resp["retrieved"]
    ]

    return {"answer": resp["answer"], "retrieved": retrieved_summary}
