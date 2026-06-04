from transformers import pipeline

def load_summarizer():
    return pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(chunks: list[str]) -> str:
    summarizer = load_summarizer()
    summaries = []

    for chunk in chunks:
        if len(chunk.split()) < 40:
            summaries.append(chunk)
            continue

        result = summarizer(
            "summarize: " + chunk,
            max_new_tokens=130,
            do_sample=False
        )
        summaries.append(result[0]["generated_text"])

    return " ".join(summaries)