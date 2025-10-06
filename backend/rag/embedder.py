from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str], show_progress_bar: bool = True) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=show_progress_bar, convert_to_numpy=True)
