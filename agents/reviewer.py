from transformers import pipeline
import os

def review_chapter(spun_text: str) -> str:
    """
    Provides a multi-faceted review of the spun chapter using multiple pipelines.
    
    Args:
        spun_text (str): The spun chapter content.
    
    Returns:
        str: Consolidated review feedback.
    """
    # Sentiment analysis for tone
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    sentiment = sentiment_analyzer(spun_text[:512])[0]  # API limit

    # Summarization for readability / length compliance
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(spun_text[:1024], max_length=100, min_length=30, do_sample=False)[0]['summary_text']

    # Zero-shot classification for style (optional, comment if slow)
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    labels = ["formal", "casual", "engaging", "neutral"]
    classification = classifier(spun_text[:512], candidate_labels=labels)
    top_style = classification['labels'][0]
    top_score = classification['scores'][0]

    # Consolidated review text
    review_summary = (
        "=== AI Reviewer Feedback ===\n"
        f"Sentiment: {sentiment['label']} (confidence {sentiment['score']:.2f})\n"
        f"Top Style: {top_style} (confidence {top_score:.2f})\n\n"
        "Summary of Spun Text:\n"
        f"{summary}\n"
    )
    return review_summary

def save_review(content: str, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    spun_path = "../data/preprocessed/chapter_spun.txt"
    output_path = "../data/preprocessed/chapter_review.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(spun_path, "r", encoding="utf-8") as file:
        spun_text = file.read()

    review = review_chapter(spun_text)
    save_review(review, output_path)
    print("Review saved.")
