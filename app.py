import streamlit as st

from src.preprocessing import clean_text, split_text
from src.summarizer import summarize_text
from src.generator import generate_key_points, generate_flashcards, generate_quiz
from src.classifier import classify_topic, classify_difficulty
from src.utils import create_download_text


# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------
sample_text = """
Genpact is a global professional services company that helps businesses transform the way they operate by using digital technology, data, artificial intelligence, and process optimization. The company works with organizations from different industries, including banking, finance, insurance, healthcare, manufacturing, and retail. Its main goal is to help clients improve efficiency, reduce operational costs, and make better decisions through intelligent business solutions.

One of Genpact’s strongest areas is digital transformation. This means helping companies move from traditional manual processes to smarter, automated systems. For example, a bank may use Genpact’s solutions to improve customer service, analyze financial data, detect fraud, or automate repetitive back-office tasks. By combining human expertise with modern technologies, Genpact supports companies in becoming faster, more accurate, and more competitive.

Genpact also focuses heavily on artificial intelligence and data analytics. These tools allow businesses to understand customer behavior, predict future trends, and solve complex problems. In today’s digital economy, companies need reliable data-driven insights, and Genpact helps turn raw data into useful business knowledge."""

if "text_input" not in st.session_state:
    st.session_state.text_input = sample_text

if "results" not in st.session_state:
    st.session_state.results = None

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark"


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    theme_mode = st.radio(
        "Choose theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme_mode == "Dark" else 1
    )

    st.session_state.theme_mode = theme_mode

    st.markdown("---")

    st.subheader("Project Info")
    st.write("**Method:** Seq2Seq Transformers")
    st.write("**Models:** DistilBART + FLAN-T5")
    st.write("**Framework:** Hugging Face + Streamlit")

    st.markdown("---")

    st.subheader("Features")
    st.write("✅ Text preprocessing")
    st.write("✅ Summarization")
    st.write("✅ Key points")
    st.write("✅ Flashcards")
    st.write("✅ Quiz questions")
    st.write("✅ Classification")
    st.write("✅ Download output")

    st.markdown("---")
    st.info("Use at least 150 words for better results.")


# --------------------------------------------------
# Theme Colors
# --------------------------------------------------
if st.session_state.theme_mode == "Dark":
    BG = "#0E1117"
    CARD = "#161B22"
    CARD_2 = "#1F2630"
    TEXT = "#F2F4F8"
    MUTED = "#A7B0BE"
    BORDER = "#30363D"
    INPUT_BG = "#FFFFFF"
    INPUT_TEXT = "#111827"
    ACCENT = "#4F8EF7"
    SUCCESS_BG = "#123524"
    WARNING_BG = "#3A2E12"
    ERROR_BG = "#3A1616"
else:
    BG = "#F6F8FB"
    CARD = "#FFFFFF"
    CARD_2 = "#F1F5F9"
    TEXT = "#111827"
    MUTED = "#4B5563"
    BORDER = "#E5E7EB"
    INPUT_BG = "#FFFFFF"
    INPUT_TEXT = "#111827"
    ACCENT = "#2563EB"
    SUCCESS_BG = "#DCFCE7"
    WARNING_BG = "#FEF3C7"
    ERROR_BG = "#FEE2E2"


# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown(
    f"""
    <style>
        /* Whole app */
        .stApp {{
            background-color: {BG};
            color: {TEXT};
        }}

        /* Main text */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: {TEXT};
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {CARD};
            border-right: 1px solid {BORDER};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT};
        }}

        /* Title */
        .main-title {{
            font-size: 44px;
            font-weight: 900;
            color: {TEXT};
            margin-bottom: 0px;
            line-height: 1.1;
        }}

        .subtitle {{
            font-size: 18px;
            color: {MUTED};
            margin-top: 8px;
            margin-bottom: 28px;
        }}

        /* Cards */
        .custom-card {{
            background-color: {CARD};
            color: {TEXT};
            padding: 22px;
            border-radius: 18px;
            border: 1px solid {BORDER};
            box-shadow: 0 8px 22px rgba(0,0,0,0.15);
            margin-bottom: 18px;
            line-height: 1.7;
            font-size: 16px;
        }}

        .custom-card * {{
            color: {TEXT};
        }}

        .mini-card {{
            background-color: {CARD_2};
            color: {TEXT};
            padding: 18px;
            border-radius: 16px;
            border: 1px solid {BORDER};
            margin-bottom: 14px;
        }}

        .mini-card * {{
            color: {TEXT};
        }}

        .muted {{
            color: {MUTED};
            font-size: 14px;
        }}

        /* Text area fix */
        textarea {{
            background-color: {INPUT_BG} !important;
            color: {INPUT_TEXT} !important;
            border-radius: 16px !important;
            border: 1px solid {BORDER} !important;
            font-size: 16px !important;
            line-height: 1.6 !important;
        }}

        textarea::placeholder {{
            color: #6B7280 !important;
        }}

        /* Input labels */
        div[data-testid="stTextArea"] label {{
            color: {TEXT} !important;
            font-weight: 600;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 12px;
            height: 46px;
            font-weight: 700;
            border: 1px solid {BORDER};
        }}

        .stDownloadButton > button {{
            border-radius: 12px;
            height: 46px;
            font-weight: 700;
            border: 1px solid {BORDER};
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            color: {TEXT} !important;
            font-weight: 700;
        }}

        div[data-baseweb="tab-panel"] {{
            background-color: transparent;
        }}

        /* Metrics */
        div[data-testid="metric-container"] {{
            background-color: {CARD};
            border: 1px solid {BORDER};
            padding: 16px;
            border-radius: 16px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        }}

        div[data-testid="metric-container"] * {{
            color: {TEXT} !important;
        }}

        /* Alerts */
        div[data-testid="stAlert"] {{
            border-radius: 14px;
        }}

        /* Footer */
        .footer {{
            color: {MUTED};
            text-align: center;
            font-size: 14px;
            padding-top: 24px;
            margin-top: 40px;
            border-top: 1px solid {BORDER};
        }}

        /* Expander */
        details {{
            background-color: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 8px;
        }}

        details * {{
            color: {TEXT};
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    <h1 class="main-title">📚 AI Study Notes Generator</h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="subtitle">
        Turn long text into summaries, key points, flashcards, and quiz questions using transformer-based NLP models.
    </p>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Input Section
# --------------------------------------------------
left_col, right_col = st.columns([2.2, 1])

with left_col:
    st.markdown("### Paste your text")

    text_input = st.text_area(
        "Text input",
        value=st.session_state.text_input,
        height=340,
        label_visibility="collapsed",
        placeholder="Paste lecture notes, articles, textbook sections, or any long text here..."
    )

    st.session_state.text_input = text_input

with right_col:
    cleaned_preview = clean_text(text_input)
    word_count = len(cleaned_preview.split())
    char_count = len(cleaned_preview)

    st.markdown("### Text Overview")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric("Words", word_count)

    with metric_col2:
        st.metric("Characters", char_count)

    if word_count < 50:
        st.error("Text is too short. Add at least 50 words.")
    elif word_count < 150:
        st.warning("Good enough, but 150+ words gives better results.")
    else:
        st.success("Text length looks good.")

    st.markdown(
        f"""
        <div class="mini-card">
            <b>Best input types:</b><br><br>
            <span class="muted">
            Lecture notes, course material, Wikipedia articles, textbook paragraphs, research summaries, and blog posts.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <b>Current theme:</b><br><br>
            <span class="muted">{st.session_state.theme_mode} mode</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Action Buttons
# --------------------------------------------------
button_col1, button_col2, button_col3 = st.columns([1, 1, 2])

with button_col1:
    generate_button = st.button(
        "🚀 Generate Notes",
        type="primary",
        use_container_width=True
    )

with button_col2:
    clear_button = st.button(
        "🧹 Clear",
        use_container_width=True
    )

with button_col3:
    st.write("")


if clear_button:
    st.session_state.text_input = ""
    st.session_state.results = None
    st.rerun()


# --------------------------------------------------
# Generate Logic
# --------------------------------------------------
if generate_button:
    cleaned_text = clean_text(text_input)

    if len(cleaned_text.split()) < 50:
        st.error("Please enter at least 50 words before generating study notes.")
    else:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.write("Cleaning and splitting text...")
            chunks = split_text(cleaned_text)
            progress_bar.progress(15)

            status_text.write("Generating summary...")
            summary = summarize_text(chunks)
            progress_bar.progress(40)

            status_text.write("Generating key points...")
            key_points = generate_key_points(cleaned_text)
            progress_bar.progress(60)

            status_text.write("Generating flashcards...")
            flashcards = generate_flashcards(summary)
            progress_bar.progress(75)

            status_text.write("Generating quiz questions...")
            quiz = generate_quiz(summary)
            progress_bar.progress(90)

            status_text.write("Classifying topic and difficulty...")

            try:
                topic = classify_topic(summary)
                difficulty = classify_difficulty(summary)
            except Exception:
                topic = "Educational Text"
                difficulty = "Intermediate"

            progress_bar.progress(100)
            status_text.success("Study notes generated successfully.")

            st.session_state.results = {
                "summary": summary,
                "key_points": key_points,
                "flashcards": flashcards,
                "quiz": quiz,
                "topic": topic,
                "difficulty": difficulty,
                "word_count": word_count,
                "char_count": char_count,
                "chunks": len(chunks)
            }

        except Exception as e:
            st.error("Something went wrong while generating the study notes.")
            st.exception(e)


# --------------------------------------------------
# Results Section
# --------------------------------------------------
if st.session_state.results:
    results = st.session_state.results

    st.markdown("---")
    st.markdown("## Generated Study Notes")

    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)

    with overview_col1:
        st.metric("Input Words", results["word_count"])

    with overview_col2:
        st.metric("Text Chunks", results["chunks"])

    with overview_col3:
        st.metric("Topic", results["topic"])

    with overview_col4:
        st.metric("Difficulty", results["difficulty"])

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📝 Summary",
            "📌 Key Points",
            "🧠 Flashcards",
            "❓ Quiz",
            "⬇️ Download"
        ]
    )

    with tab1:
        st.markdown(
            f"""
            <div class="custom-card">
                {results["summary"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(results["key_points"])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown(
            f"""
            <div class="custom-card">
                {results["flashcards"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab4:
        st.markdown(
            f"""
            <div class="custom-card">
                {results["quiz"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab5:
        final_output = create_download_text(
            results["summary"],
            results["key_points"],
            results["flashcards"],
            results["quiz"],
            results["topic"],
            results["difficulty"]
        )

        st.markdown("### Download your generated study notes")

        st.download_button(
            label="📥 Download Study Notes",
            data=final_output,
            file_name="study_notes.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.text_area(
            "Preview",
            value=final_output,
            height=320
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Built with Python, Streamlit, Hugging Face Transformers, DistilBART, and FLAN-T5.
    </div>
    """,
    unsafe_allow_html=True
)