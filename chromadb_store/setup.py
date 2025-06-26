# chromadb_store/setup.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from datetime import datetime

# Initialize ChromaDB client and collection
client = chromadb.Client(Settings())
collection = client.get_or_create_collection(name="chapter_versions")

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def add_version(text: str, metadata: dict):
    """
    Adds a new chapter version to ChromaDB with embeddings and metadata.
    """
    embedding = embedder.encode(text).tolist()
    doc_id = f"{metadata['chapter']}_{metadata['version_type']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[doc_id]
    )
    print(f"Added version to ChromaDB: {doc_id}")

def query_versions(query_text: str, top_k=3):
    """
    Queries ChromaDB for the most similar stored versions to the query text.
    """
    query_embedding = embedder.encode(query_text).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return results

if __name__ == "__main__":
    # Example usage
    example_text = "This is a sample chapter version text for testing."
    example_metadata = {"chapter": "1", "version_type": "approved", "editor": "human"}
    add_version(example_text, example_metadata)
    
    query = "sample text for testing"
    res = query_versions(query)
    print(res)
