import numpy as np
from sentence_transformers import SentenceTransformer

# Loads the pre-trained SentenceTransformer model for generating text embeddings.
# Model: 'all-MiniLM-L6-v2'
# Input: None (model is loaded at import)
# Output: model object used by embedding functions
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(texts):
    """
    Generate normalized embeddings for a list of texts.
    Args:
        texts (list of str): List of input text strings.
    Returns:
        np.ndarray: 2D array of normalized embeddings (shape: [len(texts), embedding_dim]).
    """
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

def embed_query(text):
    """
    Generate a normalized embedding for a single query string.
    Args:
        text (str): Input query string.
    Returns:
        np.ndarray: 2D array of normalized embedding (shape: [1, embedding_dim]).
    """
    emb = model.encode([text])
    return emb / np.linalg.norm(emb, axis=1, keepdims=True)
