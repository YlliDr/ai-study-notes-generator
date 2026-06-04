import re
import streamlit as st
from transformers import pipeline


MODEL_NAME = "google/flan-t5-small"
# If your laptop is too slow, change back to:
# MODEL_NAME = "google/flan-t5-small"


@st.cache_resource
def load_text_generator():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )


def clean_model_output(text: str) -> str:
    """
    Cleans weak model outputs.
    """
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    bad_outputs = ["iii .", "iii.", ".", "-", "none", "n/a"]

    if text.lower() in bad_outputs or len(text.split()) < 5:
        return ""

    return text


def split_into_sentences(text: str) -> list[str]:
    """
    Simple sentence splitter.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip().split()) >= 6]


def fallback_key_points(text: str) -> str:
    """
    Rule-based fallback if model output is bad.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return "- The text contains important study information."

    selected = sentences[:5]

    return "\n".join([f"- {sentence}" for sentence in selected])


def fallback_flashcards(text: str) -> str:
    """
    Rule-based flashcard fallback.
    """
    sentences = split_into_sentences(text)

    if not sentences:
        return "Q: What is the main idea of the text?\nA: The text explains an important topic for study."

    flashcards = []

    for i, sentence in enumerate(sentences[:5], start=1):
        flashcards.append(
            f"Q{i}: What is one important idea from the text?\nA{i}: {sentence}"
        )

    return "\n\n".join(flashcards)


def fallback_quiz(text: str) -> str:
    """
    Rule-based quiz fallback.
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


def generate_key_points(text: str) -> str:
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Task:
Extract exactly 5 key study points from the text.

Format:
- key point 1
- key point 2
- key point 3
- key point 4
- key point 5

Rules:
- Use only bullet points.
- Start every point with "- ".
- Do not write a paragraph.
- Do not repeat the summary.
- Each point must be short and clear.
- Use only information from the text.

Text:
{text[:2500]}
"""

    result = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False,
        num_beams=4
    )

    output = clean_model_output(result[0]["generated_text"])

    if not output:
        return fallback_key_points(text)

    return format_as_bullets(output)

def format_as_bullets(text: str) -> str:
    """
    Converts model output into clean markdown bullet points.
    """
    if not text:
        return "- No key points generated."

    lines = text.replace("•", "-").split("\n")
    bullets = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove numbering like 1. or 1)
        line = re.sub(r"^\d+[\.\)]\s*", "", line)

        # Remove existing messy dash spacing
        line = line.lstrip("-").strip()

        if line:
            bullets.append(f"- {line}")

    # If model returned everything in one line, split by semicolon or periods
    if len(bullets) <= 1:
        parts = re.split(r";|\.\s+", text)
        bullets = []

        for part in parts:
            part = part.strip()
            part = re.sub(r"^\d+[\.\)]\s*", "", part)
            part = part.lstrip("-").strip()

            if len(part.split()) >= 4:
                bullets.append(f"- {part}")

    return "\n".join(bullets[:5])


def generate_flashcards(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Task:
Create exactly 5 flashcards from the text.

Format:
Q1: ...
A1: ...

Q2: ...
A2: ...

Q3: ...
A3: ...

Q4: ...
A4: ...

Q5: ...
A5: ...

Rules:
- Questions must be useful for studying.
- Answers must be based only on the text.
- Do not write random symbols.
- Do not answer with only roman numerals.

Text:
{summary}
"""

    result = generator(
        prompt,
        max_new_tokens=350,
        do_sample=False,
        num_beams=4
    )

    output = clean_model_output(result[0]["generated_text"])

    if not output or "Q" not in output or "A" not in output:
        return fallback_flashcards(summary)

    return output


def generate_quiz(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Task:
Create exactly 5 multiple-choice quiz questions from the text.

Format:
1. Question?
A) Option
B) Option
C) Option
D) Option
Correct answer: A

Rules:
- Each question must have 4 options.
- Mark the correct answer.
- Use only information from the text.
- Do not write random symbols.

Text:
{summary}
"""

    result = generator(
        prompt,
        max_new_tokens=500,
        do_sample=False,
        num_beams=4
    )

    output = clean_model_output(result[0]["generated_text"])

    if not output or "Correct answer" not in output:
        return fallback_quiz(summary)

    return output