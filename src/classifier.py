import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_classifier():
    """
    Loads zero-shot classifier for topic/difficulty prediction.
    """
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )


def classify_topic(text: str) -> str:
    classifier = load_classifier()

    labels = [
        "Artificial Intelligence",
        "Computer Science",
        "Business",
        "Health",
        "Education",
        "History",
        "Science",
        "Technology"
    ]

    result = classifier(text[:1000], labels)
    return result["labels"][0]


def classify_difficulty(text: str) -> str:
    classifier = load_classifier()

    labels = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    result = classifier(text[:1000], labels)
    return result["labels"][0]