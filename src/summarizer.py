import streamlit as st
from transformers import pipeline


@st.cache_resource
def load_summarizer():
    """
    Loads a lightweight summarization model.
    Cached so it does not reload every time the app refreshes.
    """
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )


def summarize_text(chunks: list[str]) -> str:
    """
    Summarizes text chunks and combines them into one final summary.
    """
    summarizer = load_summarizer()
    summaries = []

    for chunk in chunks:
        if len(chunk.split()) < 40:
            summaries.append(chunk)
            continue

        result = summarizer(
            chunk,
            max_length=130,
            min_length=35,
            do_sample=False
        )

        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)