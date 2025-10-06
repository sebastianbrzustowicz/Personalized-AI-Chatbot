from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

DATA_DIR = os.getenv("DATA_DIR", "data/docs")

ALLOWED_ORIGINS = ["*"]

def setup_cors(app: FastAPI) -> None:
    """Attach CORS middleware to FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
