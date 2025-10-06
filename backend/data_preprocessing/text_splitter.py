import re
from typing import List, Dict

def split_text_into_chunks(
    text: str,
    chunk_size: int = 400,
    overlap: int = 0,
    source: str = "unknown"
) -> List[Dict]:
    """
    Splits text into chunks of approximately `chunk_size` characters, 
    preserving sentence boundaries when possible. Adds optional overlap.
    Returns: [{"id": ..., "text": ..., "source": ...}, ...]
    """
    sentences = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    chunks, current, chunk_id = [], "", 0

    for sent in sentences:
        if len(current) + len(sent) + 1 <= chunk_size or not current:
            current = (current + " " + sent).strip()
        else:
            chunks.append({
                "id": f"{source}__chunk_{chunk_id}",
                "text": current,
                "source": source
            })
            chunk_id += 1
            tail = current[-overlap:] if overlap > 0 else ""
            current = (tail + " " + sent).strip()

    if current:
        chunks.append({
            "id": f"{source}__chunk_{chunk_id}",
            "text": current,
            "source": source
        })

    return chunks
