import streamlit as st

from src.preprocessing import clean_text, split_text
from src.summarizer import summarize_text
from src.generator import generate_key_points, generate_flashcards, generate_quiz
from src.classifier import classify_topic, classify_difficulty
from src.utils import create_download_text


st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI Study Notes Generator")
st.write(
    "Paste long text and generate a summary, key points, flashcards, and quiz questions using transformer-based NLP models."
)


with st.sidebar:
    st.header("Project Info")
    st.write("Method: Seq2Seq Transformers")
    st.write("Models: DistilBART + FLAN-T5")
    st.write("Framework: Hugging Face + Streamlit")

    st.markdown("---")
    st.write("Tip: Use at least 150 words for better results.")


sample_text = """
Natural Language Processing is a field of artificial intelligence that focuses on enabling computers to understand, interpret, and generate human language. It combines linguistics, computer science, and machine learning. Traditional NLP systems used rule-based methods and statistical models, while modern NLP uses deep learning and transformer architectures. Transformers rely on attention mechanisms to understand relationships between words in a sequence. These models are used in tasks such as sentiment analysis, named entity recognition, machine translation, summarization, question answering, and text generation.
"""


text_input = st.text_area(
    "Paste your text here:",
    value=sample_text,
    height=300
)


col1, col2 = st.columns([1, 1])

with col1:
    generate_button = st.button("Generate Study Notes", type="primary")

with col2:
    clear_button = st.button("Clear")


if clear_button:
    st.rerun()


if generate_button:
    cleaned_text = clean_text(text_input)

    if len(cleaned_text.split()) < 50:
        st.warning("Please enter at least 50 words for better results.")
    else:
        with st.spinner("Processing text..."):
            chunks = split_text(cleaned_text)
            summary = summarize_text(chunks)

        st.subheader("1. Summary")
        st.write(summary)

        with st.spinner("Generating key points..."):
            key_points = generate_key_points(summary)

        st.subheader("2. Key Points")
        st.write(key_points)

        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(summary)

        st.subheader("3. Flashcards")
        st.write(flashcards)

        with st.spinner("Generating quiz questions..."):
            quiz = generate_quiz(summary)

        st.subheader("4. Quiz Questions")
        st.write(quiz)

        with st.spinner("Classifying topic and difficulty..."):
            try:
                topic = classify_topic(summary)
                difficulty = classify_difficulty(summary)
            except Exception:
                topic = "Not available"
                difficulty = "Not available"

        st.subheader("5. Classification")
        st.write(f"**Topic:** {topic}")
        st.write(f"**Difficulty:** {difficulty}")

        final_output = create_download_text(
            summary,
            key_points,
            flashcards,
            quiz,
            topic,
            difficulty
        )

        st.download_button(
            label="Download Study Notes",
            data=final_output,
            file_name="study_notes.txt",
            mime="text/plain"
        )