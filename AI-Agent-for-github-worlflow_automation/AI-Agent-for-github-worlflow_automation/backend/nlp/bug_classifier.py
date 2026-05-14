from transformers import pipeline

# Load zero-shot classification model
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "bug",
    "feature request",
    "documentation",
    "performance issue",
    "security issue"
]

def classify_issue(text):
    result = classifier(text, labels)

    # Return top prediction with its confidence score
    return {
        "category": result["labels"][0],
        "confidence": result["scores"][0]
    }
