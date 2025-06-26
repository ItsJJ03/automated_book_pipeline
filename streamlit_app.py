# streamlit_app.py
import streamlit as st
import os
from datetime import datetime
from scraper import playwright_scraper
from agents import writer, reviewer
from chromadb_store import setup as chromadb_setup
from rl_search import rl_ranker
import subprocess
def run_scraper():
    """
    Runs the Playwright scraper script as a subprocess.
    Returns the expected saved path of the raw text file.
    """
    result = subprocess.run(
        ["python", "./scraper/playwright_scraper.py"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        st.success("Scraper ran successfully!")
        st.text(result.stdout)
    else:
        st.error("Scraper failed to run.")
        st.text(result.stderr)

    # Assuming scraper saves to latest_chapter.txt consistently
    return "./data/raw/latest_chapter.txt"

def run_writer(raw_path):
    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    spun_text = writer.spin_chapter(raw_text)
    spun_path = os.path.join("./data/preprocessed", "chapter_spun.txt")
    os.makedirs(os.path.dirname(spun_path), exist_ok=True)
    writer.save_spun_version(spun_text, spun_path)
    st.success(f"Spun version saved at {spun_path}")
    return spun_text, spun_path

def run_reviewer(spun_text):
    review = reviewer.review_chapter(spun_text)
    review_path = os.path.join("./data/preprocessed", "chapter_review.txt")
    reviewer.save_review(review, review_path)
    st.success(f"Review saved at {review_path}")
    return review, review_path

def run_storage(spun_text, review):
    chromadb_setup.add_version(
        spun_text,
        {"chapter": "1", "version_type": "spun", "editor": "AI", "timestamp": datetime.now().isoformat()}
    )
    chromadb_setup.add_version(
        review,
        {"chapter": "1", "version_type": "review", "editor": "AI", "timestamp": datetime.now().isoformat()}
    )
    st.success("Versions stored in ChromaDB.")

def run_ranker(query):
    ranked = rl_ranker.rl_rank_results(query)
    
    if not ranked:
        st.warning("No results found for your query.")
        return
    
    output = ""
    for i, (doc, meta, reward) in enumerate(ranked, 1):
        output += f"Rank {i}: Reward {reward:.4f}\n"
        output += f"Metadata: {meta}\n"
        output += f"Document preview: {doc[:100]}...\n"
        output += "---\n"
    
    st.markdown(f"```\n{output}\n```")




def main():
    st.set_page_config(page_title="Automated Book Publication Dashboard", layout="wide")
    st.title("📘 Automated Book Publication Workflow")

    if st.button("🚀 Run Scraper"):
        st.session_state["raw_path"] = run_scraper()

    if "raw_path" in st.session_state and st.button("✏️ Run Writer"):
        spun_text, _ = run_writer(st.session_state["raw_path"])
        st.session_state["spun_text"] = spun_text

    if "spun_text" in st.session_state and st.button("🔎 Run Reviewer"):
        review, _ = run_reviewer(st.session_state["spun_text"])
        st.session_state["review_text"] = review

    if "spun_text" in st.session_state and "review_text" in st.session_state and st.button("💾 Store Versions"):
        run_storage(st.session_state["spun_text"], st.session_state["review_text"])

    query = st.text_input("Enter query for RL ranker")
    if st.button("🏁 Run RL Ranker") and query.strip():
        run_ranker(query)

if __name__ == "__main__":
    main()
