from transformers import pipeline
import os
def spin_chapter(raw_text: str) -> str:
    """
    Uses a Hugging Face model to rewrite the chapter content.

    Args:
        raw_text (str): Original chapter content.

    Returns:
        str: Rewritten chapter content.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # BART works well on chunks up to 1024 tokens
    # For simplicity, take first 1024 characters for demo
    chunk = raw_text[:1024]
    
    summary = summarizer(chunk, max_length=300, min_length=100, do_sample=False)
    rewritten = summary[0]['summary_text']
    
    return rewritten

def save_spun_version(content: str, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    raw_path = "../data/raw/latest_chapter.txt"
    output_path = "../data/preprocessed/chapter_spun.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(raw_path, "r", encoding="utf-8") as file:
        raw_text = file.read()

    spun = spin_chapter(raw_text)
    save_spun_version(spun, output_path)
    print("Spun version saved.")
