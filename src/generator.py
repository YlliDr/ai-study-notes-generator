import re
import streamlit as st


def clean_model_output(text: str) -> str:
    """
    Cleans generated text output.
    Kept for compatibility, even though this version does not use an AI model.
    """
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    bad_outputs = ["iii .", "iii.", ".", "-", "none", "n/a", "null"]

    if text.lower().strip() in bad_outputs or len(text.split()) < 5:
        return ""

    return text


def split_into_sentences(text: str) -> list[str]:
    """
    Splits text into usable sentences.
    Very short sentences are ignored.
    """
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip().split()) >= 6]


def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """
    Extracts simple keywords from the text without using AI.
    """
    if not text:
        return []

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
    """
    Creates simple key points from the first useful sentences.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return "- The text contains important study information."

    return "\n".join(f"- {sentence}" for sentence in sentences[:5])


def fallback_flashcards(text: str) -> str:
    """
    Creates basic flashcards from useful sentences.
    """
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
    """
    Creates simple multiple-choice questions from useful sentences.
    """
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
    """
    Formats any text as bullet points.
    """
    if not text:
        return "- No key points generated."

    text = text.replace("•", "-")

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
    """
    Generates 5 key study points without AI model.
    This is memory-safe for Streamlit Cloud.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return fallback_key_points(text)

    key_points = []

    for sentence in sentences[:5]:
        key_points.append(f"- {sentence}")

    return "\n".join(key_points)


def generate_flashcards(summary: str) -> str:
    """
    Generates 5 flashcards without AI model.
    """
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
    """
    Generates 5 multiple-choice questions without AI model.
    """
    sentences = split_into_sentences(summary)

    if not sentences:
        return fallback_quiz(summary)

    quiz_items = []

    for i, sentence in enumerate(sentences[:5], start=1):
        quiz_items.append(
            f"{i}. Which statement is supported by the text?\n"
            f"A) {sentence}\n"
            f"B) The text says the opposite of this idea.\n"
            f"C) The text does not provide any useful information.\n"
            f"D) The text is only about unrelated details.\n"
            f"Correct answer: A"
        )

    return "\n\n".join(quiz_items)


def generate_summary(text: str, max_sentences: int = 5) -> str:
    """
    Optional helper function for summary generation.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return "No summary could be generated from the provided text."

    return " ".join(sentences[:max_sentences])


# Streamlit UI
st.title("AI Study Notes Generator")

text = st.text_area("Paste your lesson text here:", height=250)

if st.button("Generate Study Notes"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        summary = generate_summary(text)

        st.subheader("Summary")
        st.write(summary)

        st.subheader("Key Points")
        st.markdown(generate_key_points(text))

        st.subheader("Flashcards")
        st.text(generate_flashcards(summary))

        st.subheader("Quiz")
        st.text(generate_quiz(summary))