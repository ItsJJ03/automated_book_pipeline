import streamlit as st
import os
from datetime import datetime

def load_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_approved_version(content: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def apply_custom_css():
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            min-height: 300px;
            font-size: 16px;
            font-family: 'Courier New', monospace;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .reportview-container .main .block-container{
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(page_title="Automated Book Editor", layout="wide")
    apply_custom_css()
    st.title("📖 Automated Book Publication Editor")
    st.markdown("Refine AI-generated chapters with ease. Edit, review, approve!")

    spun_text = load_file("../data/preprocessed/chapter_spun.txt")
    review_text = load_file("../data/preprocessed/chapter_review.txt")

    with st.expander("👁 View AI Review Feedback"):
        st.text_area("AI Review", review_text, height=200, disabled=True)

    with st.expander("📜 View AI Spun Chapter"):
        st.text_area("Spun Chapter", spun_text, height=300, disabled=True)

    st.subheader("✏️ Your Edited Chapter")
    user_edit = st.text_area("Make edits below:", spun_text, height=400)

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("✅ Save Final Approved Version"):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = f"../data/preprocessed/chapter_approved_{timestamp}.txt"
            save_approved_version(user_edit, output_path)
            st.success(f"Approved version saved at: {output_path}")

    with col2:
        st.caption("Tip: Make sure your edits preserve the story's meaning while improving readability and tone.")

if __name__ == "__main__":
    main()
