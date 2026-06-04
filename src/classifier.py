import re


def normalize_text(text) -> str:
    """
    Converts input into a safe string.
    Accepts normal text or a list of chunks.
    """
    if isinstance(text, list):
        return " ".join(str(chunk) for chunk in text)

    if text is None:
        return ""

    return str(text)


def clean_words(text) -> list[str]:
    text = normalize_text(text)

    if not text:
        return []

    return re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())


def classify_topic(text) -> str:
    """
    Lightweight topic classifier without AI model.
    Uses simple keyword matching.
    """

    words = clean_words(text)
    joined_text = " ".join(words)

    topic_keywords = {
        "Computer Science / Programming": [
            "python", "java", "code", "programming", "function", "class",
            "object", "algorithm", "database", "sql", "html", "css",
            "javascript", "software", "application", "streamlit"
        ],
        "Artificial Intelligence / Machine Learning": [
            "machine", "learning", "model", "training", "dataset",
            "neural", "network", "classification", "regression",
            "clustering", "prediction", "transformer", "encoder",
            "decoder", "attention"
        ],
        "Business / Management": [
            "business", "management", "strategy", "company", "market",
            "customer", "finance", "bank", "performance", "organization"
        ],
        "Biology / Medicine": [
            "cell", "body", "health", "disease", "blood", "virus",
            "bacteria", "medicine", "treatment", "organ", "protein"
        ],
        "History / Society": [
            "history", "war", "political", "society", "government",
            "culture", "people", "country", "rights", "law"
        ],
        "Mathematics": [
            "number", "equation", "formula", "variable", "function",
            "matrix", "probability", "statistics", "calculation"
        ],
        "Networking / Cybersecurity": [
            "network", "server", "client", "packet", "protocol",
            "ip", "tcp", "udp", "http", "security", "encryption"
        ],
    }

    scores = {}

    for topic, keywords in topic_keywords.items():
        score = 0

        for keyword in keywords:
            if keyword in joined_text:
                score += 1

        scores[topic] = score

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return "General Study Topic"

    return best_topic


def classify_difficulty(text) -> str:
    """
    Lightweight difficulty classifier without AI model.
    Uses sentence length and technical word count.
    """

    text = normalize_text(text)

    if not text or not text.strip():
        return "Unknown"

    words = clean_words(text)

    if not words:
        return "Easy"

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s for s in sentences if s.strip()]

    average_sentence_length = len(words) / max(len(sentences), 1)

    technical_words = [
        "algorithm", "architecture", "implementation", "classification",
        "regression", "optimization", "normalization", "standardization",
        "infrastructure", "encapsulation", "inheritance", "polymorphism",
        "database", "encryption", "authentication", "probability",
        "statistical", "transformer", "attention", "neural"
    ]

    technical_count = 0

    for word in words:
        if word in technical_words:
            technical_count += 1

    if average_sentence_length > 22 or technical_count >= 8:
        return "Hard"

    if average_sentence_length > 14 or technical_count >= 3:
        return "Medium"

    return "Easy"