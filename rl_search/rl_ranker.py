# rl_search/rl_ranker.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chromadb_store import setup as chromadb_setup

def rl_rank_results(query_text: str, top_k=3):
    """
    Queries ChromaDB and applies a simple RL-style ranking policy.
    
    Args:
        query_text (str): User query to match against stored versions.
        top_k (int): Number of top results to return.
    
    Returns:
        list: Ranked list of documents with scores.
    """
    results = chromadb_setup.query_versions(query_text, top_k=top_k)
    ranked = []
    
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        # RL reward: prefer approved versions, prefer closer distance
        reward = 1.0 / (dist + 1e-5)  # the closer the distance, the higher the reward
        if meta.get('version_type') == 'approved':
            reward *= 1.2  # boost for approved versions
        if meta.get('editor') == 'human':
            reward *= 1.1  # small bonus for human-approved
        ranked.append((doc, meta, reward))
    
    # Sort by reward descending
    ranked.sort(key=lambda x: x[2], reverse=True)
    return ranked

if __name__ == "__main__":
    query = "sample text for testing"
    ranked_results = rl_rank_results(query)
    for i, (doc, meta, reward) in enumerate(ranked_results, 1):
        print(f"Rank {i}: Reward {reward:.4f}")
        print(f"Metadata: {meta}")
        print(f"Document: {doc[:100]}...")
        print("---")
