from transformers import pipeline

summarizer = pipeline(
    "text-generation",
    model="google/flan-t5-small"
)

def summarize_issue(text):

    prompt = f"Summarize this bug report in one sentence: {text}"

    result = summarizer(
        prompt,
        max_new_tokens=40
    )

    return result[0]["generated_text"]