import re
import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_text_generator():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )


def clean_model_output(text: str) -> str:
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
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if len(s.strip().split()) >= 6]


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

    text = text.replace("•", "-")

    # Add line breaks before bullet-like patterns if model returns one long line
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
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Extract exactly 5 key study points from the text.

Use this exact format:
- key point 1
- key point 2
- key point 3
- key point 4
- key point 5

Rules:
- Use only bullet points.
- Each point must start with "- ".
- Each point must be short and clear.
- Use only information from the text.

Text:
{text[:2500]}
"""

    try:
        result = generator(
            prompt,
            max_new_tokens=250,
            do_sample=False,
            num_beams=4
        )

        output = clean_model_output(result[0]["generated_text"])

        if not output:
            return fallback_key_points(text)

        formatted = format_as_bullets(output)

        if "No key points generated" in formatted:
            return fallback_key_points(text)

        return formatted

    except Exception:
        return fallback_key_points(text)


def generate_flashcards(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Create exactly 5 flashcards from the text.

Use this exact format:
Q1: question
A1: answer

Q2: question
A2: answer

Q3: question
A3: answer

Q4: question
A4: answer

Q5: question
A5: answer

Rules:
- Questions must be useful for studying.
- Answers must be based only on the text.
- Do not write random symbols.

Text:
{summary[:2500]}
"""

    try:
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

    except Exception:
        return fallback_flashcards(summary)


def generate_quiz(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
You are a study assistant.

Create exactly 5 multiple-choice quiz questions from the text.

Use this exact format:
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
{summary[:2500]}
"""

    try:
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

    except Exception:
        return fallback_quiz(summary)