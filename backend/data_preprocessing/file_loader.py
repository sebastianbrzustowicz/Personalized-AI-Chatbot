from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
from backend.data_preprocessing.text_cleaning import clean_text
from backend.data_preprocessing.text_splitter import split_text_into_chunks

def read_pdf(path: str) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(path)
    texts = [page.extract_text() for page in reader.pages if page.extract_text()]
    return "\n".join(texts)

def read_docx(path: str) -> str:
    """Extracts all text from a DOCX file."""
    doc = Document(path)
    texts = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(texts)

def read_html(path: str) -> str:
    """Extracts visible text from an HTML file, ignoring tags."""
    html_content = Path(path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    return text

def load_text_files(data_dir: str = "data/docs") -> List[Dict]:
    """
    Loads .txt, .pdf, .docx, and .html files from `data/docs` and returns
    a list of document chunks:
    [
        {"id": "file_1_chunk_0", "text": "...", "source": "file.pdf"},
        ...
    ]
    """
    p = Path(data_dir)
    if not p.exists():
        raise FileNotFoundError(f"Folder {data_dir} does not exist. Add .pdf/.txt/.docx/.html files there.")

    docs = []
    for file in sorted(p.iterdir()):
        suffix = file.suffix.lower()
        if suffix == ".txt":
            text = file.read_text(encoding="utf-8")
        elif suffix == ".pdf":
            text = read_pdf(str(file))
        elif suffix == ".docx":
            text = read_docx(str(file))
        elif suffix == ".html":
            text = read_html(str(file))
        else:
            continue

        text = clean_text(text)
        docs.extend(split_text_into_chunks(text, source=file.name))

    return docs
