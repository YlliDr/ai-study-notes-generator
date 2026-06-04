from transformers import pipeline

def load_summarizer():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

def summarize_text(chunks):
    summarizer = load_summarizer()
    summaries = []

    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=130,
            min_length=30,
            do_sample=False
        )
        summaries.append(result[0]["summary_text"])

    combined_summary = " ".join(summaries)

    if len(summaries) > 1:
        final_result = summarizer(
            combined_summary,
            max_length=180,
            min_length=50,
            do_sample=False
        )
        return final_result[0]["summary_text"]

    return combined_summary