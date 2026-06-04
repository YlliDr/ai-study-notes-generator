import re


def clean_model_output(text: str) -> str:
    if not text:
        return ""

    text = str(text).strip()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    bad_outputs = ["iii .", "iii.", ".", "-", "none", "n/a", "null"]

    if text.lower().strip() in bad_outputs or len(text.split()) < 5:
        return ""

    return text


def split_into_sentences(text: str) -> list[str]:
    if not text:
        return []

    text = str(text)

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip().split()) >= 5]


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    if not text:
        return []

    text = str(text)

    words = re.findall(r"\b[a-zA-Z]{5,}\b", text.lower())

    stop_words = {
        "which", "there", "their", "about", "would", "could", "should",
        "because", "these", "those", "where", "when", "while", "using",
        "therefore", "however", "between", "important", "information",
        "example", "examples", "study", "topic", "text", "based",
        "answer", "question", "questions", "correct", "option"
    }

    keywords = []

    for word in words:
        if word not in stop_words and word not in keywords:
            keywords.append(word)

        if len(keywords) >= max_keywords:
            break

    return keywords


def fallback_key_points(text: str) -> str:
    sentences = split_into_sentences(text)

    if not sentences:
        return "- The text contains important study information."

    return "\n".join(f"- {sentence}" for sentence in sentences[:5])


def fallback_flashcards(text: str) -> str:
    sentences = split_into_sentences(text)

    if not sentences:
        return (
            "Q1: What is the main idea of the text?\n"
            "A1: The text explains an important topic for study."
        )

    flashcards = []

    for i, sentence in enumerate(sentences[:5], start=1):
        flashcards.append(
            f"Q{i}: What is one important idea from the text?\n"
            f"A{i}: {sentence}"
        )

    return "\n\n".join(flashcards)


def fallback_quiz(text: str) -> str:
    sentences = split_into_sentences(text)

    if not sentences:
        return (
            "1. What is the main purpose of the text?\n"
            "A) To explain a topic\n"
            "B) To advertise a product\n"
            "C) To tell a fictional story\n"
            "D) To list random facts\n"
            "Correct answer: A"
        )

    quiz_items = []

    for i, sentence in enumerate(sentences[:5], start=1):
        quiz_items.append(
            f"{i}. Which statement is supported by the text?\n"
            f"A) {sentence}\n"
            f"B) The text is unrelated to the topic.\n"
            f"C) The text gives no useful information.\n"
            f"D) The text only contains opinions.\n"
            f"Correct answer: A"
        )

    return "\n\n".join(quiz_items)


def format_as_bullets(text: str) -> str:
    if not text:
        return "- No key points generated."

    text = str(text).replace("•", "-")

    text = re.sub(r"\s*-\s+", "\n- ", text)
    text = re.sub(r"\s*(\d+[\.\)])\s+", r"\n\1 ", text)

    lines = text.splitlines()
    bullets = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^\d+[\.\)]\s*", "", line)
        line = line.lstrip("-").strip()

        if len(line.split()) >= 3:
            bullets.append(f"- {line}")

    if len(bullets) < 3:
        parts = re.split(r";|\.\s+", text)
        bullets = []

        for part in parts:
            part = part.strip()
            part = re.sub(r"^\d+[\.\)]\s*", "", part)
            part = part.lstrip("-").strip()

            if len(part.split()) >= 4:
                bullets.append(f"- {part}")

    if not bullets:
        return "- No key points generated."

    return "\n".join(bullets[:5])


def generate_key_points(text: str) -> str:
    sentences = split_into_sentences(text)

    if not sentences:
        return fallback_key_points(text)

    return "\n".join(f"- {sentence}" for sentence in sentences[:5])


def generate_flashcards(summary: str) -> str:
    sentences = split_into_sentences(summary)
    keywords = extract_keywords(summary, max_keywords=5)

    if not sentences:
        return fallback_flashcards(summary)

    flashcards = []

    for i in range(min(5, len(sentences))):
        keyword = keywords[i] if i < len(keywords) else "this concept"

        flashcards.append(
            f"Q{i + 1}: What should you remember about {keyword}?\n"
            f"A{i + 1}: {sentences[i]}"
        )

    return "\n\n".join(flashcards)


def generate_quiz(summary: str) -> str:
    sentences = split_into_sentences(summary)

    if not sentences:
        return fallback_quiz(summary)

    quiz_items = []

    for i, sentence in enumerate(sentences[:5], start=1):
        quiz_items.append(
            f"{i}. Which statement is supported by the text?\n"
            f"A) {sentence}\n"
            f"B) The text says the opposite of this idea.\n"
            f"C) The text does not provide useful information.\n"
            f"D) The text is only about unrelated details.\n"
            f"Correct answer: A"
        )

    return "\n\n".join(quiz_items)