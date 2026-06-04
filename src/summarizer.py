import re


def split_into_sentences(text: str) -> list[str]:
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip().split()) >= 5]


def summarize_text(text, max_sentences: int = 5) -> str:
    """
    Lightweight summary without transformers.
    Accepts either a string or a list of text chunks.
    """

    if isinstance(text, list):
        text = " ".join(str(chunk) for chunk in text)

    if not text or not str(text).strip():
        return "No text provided."

    text = str(text)

    sentences = split_into_sentences(text)

    if not sentences:
        return "No summary could be generated from the provided text."

    return " ".join(sentences[:max_sentences])