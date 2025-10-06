import re

def clean_text(text: str) -> str:
    """
    Cleans text by removing sequences like '\X' (backslash + any character),
    merging multiple spaces, and trimming whitespace.
    This helps avoid issues when embedding or passing to LLMs.
    """
    cleaned = re.sub(r'\\.', ' ', text)        # remove \X sequences
    cleaned = re.sub(r'\s+', ' ', cleaned)     # merge multiple spaces
    return cleaned.strip()
