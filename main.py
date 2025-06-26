# main.py
import os
from scraper import playwright_scraper
from agents import writer, reviewer
from chromadb_store import setup as chromadb_setup
from rl_search import rl_ranker
from datetime import datetime

def main():
    print("=== Automated Book Publication Workflow ===")
    
    # 1️⃣ Scrape chapter
    chapter_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
    data_dir = "./data"
    raw_path = playwright_scraper.scrape_chapter(chapter_url, data_dir)
    print(f"Scraped chapter saved at: {raw_path}")

    # 2️⃣ Spin chapter
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    spun_text = writer.spin_chapter(raw_text)
    spun_path = os.path.join(data_dir, "preprocessed", "chapter_spun.txt")
    os.makedirs(os.path.dirname(spun_path), exist_ok=True)
    writer.save_spun_version(spun_text, spun_path)
    print(f"Spun version saved at: {spun_path}")

    # 3️⃣ Review chapter
    review_text = reviewer.review_chapter(spun_text)
    review_path = os.path.join(data_dir, "preprocessed", "chapter_review.txt")
    reviewer.save_review(review_text, review_path)
    print(f"Review saved at: {review_path}")

    # 4️⃣ Store in ChromaDB
    chromadb_setup.add_version(
        spun_text,
        {"chapter": "1", "version_type": "spun", "editor": "AI", "timestamp": datetime.now().isoformat()}
    )

    chromadb_setup.add_version(
        review_text,
        {"chapter": "1", "version_type": "review", "editor": "AI", "timestamp": datetime.now().isoformat()}
    )

    # 5️⃣ RL rank query
    query = input("Enter search query for RL ranker: ")
    ranked = rl_ranker.rl_rank_results(query)
    print("=== RL Ranked Results ===")
    for i, (doc, meta, reward) in enumerate(ranked, 1):
        print(f"Rank {i}: Reward {reward:.4f}")
        print(f"Metadata: {meta}")
        print(f"Document preview: {doc[:100]}...")
        print("---")

if __name__ == "__main__":
    main()
