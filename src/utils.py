def create_download_text(summary, key_points, flashcards, quiz, topic, difficulty):
    """
    Creates final downloadable text.
    """
    return f"""
AI STUDY NOTES GENERATOR OUTPUT

TOPIC:
{topic}

DIFFICULTY:
{difficulty}

SUMMARY:
{summary}

KEY POINTS:
{key_points}

FLASHCARDS:
{flashcards}

QUIZ QUESTIONS:
{quiz}
"""