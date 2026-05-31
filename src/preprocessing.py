import re


def clean_text(text: str) -> str:
    """
    Cleans raw input text by removing extra spaces and unnecessary line breaks.
    """
    if not text:
        return ""

    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_text(text: str, max_words: int = 450) -> list[str]:
    """
    Splits long text into smaller chunks so transformer models can process it.
    """
    words = text.split()

    if len(words) <= max_words:
        return [text]

    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks