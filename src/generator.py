import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_text_generator():
    """
    Loads FLAN-T5 for text-to-text generation.
    """
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )


def generate_key_points(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
    Extract 5 clear study key points from this text:

    {summary}
    """

    result = generator(
        prompt,
        max_new_tokens=180,
        do_sample=False
    )

    return result[0]["generated_text"]


def generate_flashcards(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
    Create 5 simple flashcards from this text.
    Format each flashcard like:
    Q: question
    A: answer

    Text:
    {summary}
    """

    result = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False
    )

    return result[0]["generated_text"]


def generate_quiz(summary: str) -> str:
    generator = load_text_generator()

    prompt = f"""
    Create 5 multiple choice quiz questions from this text.
    Each question should have 4 options and mark the correct answer.

    Text:
    {summary}
    """

    result = generator(
        prompt,
        max_new_tokens=350,
        do_sample=False
    )

    return result[0]["generated_text"]