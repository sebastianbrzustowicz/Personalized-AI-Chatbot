from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from backend.data_preprocessing.text_cleaning import clean_text
from backend.data_preprocessing.text_splitter import split_text_into_chunks

def read_pdf(path: str) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(path)
    texts = [page.extract_text() for page in reader.pages if page.extract_text()]
    return "\n".join(texts)

def load_text_files(data_dir: str = "data/docs") -> List[Dict]:
    """
    Loads .txt and .pdf files from `data/docs` and returns
    a list of document chunks:
    [
        {"id": "file_1_chunk_0", "text": "...", "source": "file.pdf"},
        ...
    ]
    """
    p = Path(data_dir)
    if not p.exists():
        raise FileNotFoundError(f"Folder {data_dir} does not exist. Add .pdf/.txt files there.")

    docs = []
    for file in sorted(p.iterdir()):
        if file.suffix.lower() == ".txt":
            text = file.read_text(encoding="utf-8")
        elif file.suffix.lower() == ".pdf":
            text = read_pdf(str(file))
        else:
            continue

        text = clean_text(text)
        docs.extend(split_text_into_chunks(text, source=file.name))

    return docs
