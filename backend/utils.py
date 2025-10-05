from pathlib import Path
from pypdf import PdfReader
import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Removes all sequences of the form \X (backslash + any character)
    and replaces them with a space to avoid confusing the model.
    Additionally, it merges multiple spaces into a single one.
    """

    # replaces \X with a space
    cleaned = re.sub(r'\\.', ' ', text)
    # removes multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def load_text_files(data_dir: str = "data/docs") -> List[Dict]:
    """
    Loads .txt and .pdf files from the data/docs folder and returns a list of documents:
    [{"id": "file_1_chunk_0", "text": "...", "source": "file.pdf"}, ...]
    """
    p = Path(data_dir)
    docs = []

    if not p.exists():
        raise FileNotFoundError(f"The folder {data_dir} does not exist. Please add .pdf/.txt files there.")

    for file in sorted(p.iterdir()):
        if file.suffix.lower() == ".txt":
            text = file.read_text(encoding="utf-8")
            text = clean_text(text)
            docs.extend(split_text_into_chunks(text, source=file.name))
        elif file.suffix.lower() == ".pdf":
            text = read_pdf(str(file))
            text = clean_text(text)
            docs.extend(split_text_into_chunks(text, source=file.name))
        else:
            continue

    return docs

def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            texts.append(txt)
    return "\n".join(texts)

def split_text_into_chunks(text: str, chunk_size: int = 400, overlap: int = 0, source: str = "unknown") -> List[Dict]:
    """
    Simple splitting into chunks of approximately chunk_size characters, with overlap.
    Returns a list of dictionaries containing 'id', 'text', and 'source'.
    """
    # simplified sentence division so as not to cut words in half
    sentences = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    chunks = []
    current = ""
    chunk_id = 0

    for sent in sentences:
        if len(current) + len(sent) + 1 <= chunk_size or current == "":
            current = (current + " " + sent).strip()
        else:
            # save chunk
            chunks.append({
                "id": f"{source}__chunk_{chunk_id}",
                "text": current,
                "source": source
            })
            chunk_id += 1
            # start next with overlap: take last `overlap` chars from current
            tail = current[-overlap:] if overlap > 0 else ""
            current = (tail + " " + sent).strip()

    if current:
        chunks.append({
            "id": f"{source}__chunk_{chunk_id}",
            "text": current,
            "source": source
        })

    return chunks
