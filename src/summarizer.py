import re


def split_into_sentences(text: str) -> list[str]:
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip().split()) >= 5]


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """
    Lightweight summary without transformers.
    Takes the first useful sentences from the text.
    Safe for Streamlit Cloud memory limits.
    """
    if not text or not text.strip():
        return "No text provided."

    sentences = split_into_sentences(text)

    if not sentences:
        return "No summary could be generated from the provided text."

    return " ".join(sentences[:max_sentences])