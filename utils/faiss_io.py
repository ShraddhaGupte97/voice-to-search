import faiss
import pandas as pd
from utils.embeddings import generate_embeddings

def build_faiss_index(df):
    """
    Builds a FAISS index from the embeddings of the DataFrame.
    Args:
        df (pd.DataFrame): Input DataFrame with 'embedding_input' column.
    Returns:
        tuple: Tuple containing the FAISS index and the DataFrame with reset index.
    """
    embeddings = generate_embeddings(df['embedding_input'].tolist())
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    df['embedding'] = list(embeddings)
    return index, df.reset_index()

def save_faiss_index(index, path):
    """
    Saves the FAISS index to a file.
    Args:
        index (faiss.Index): The FAISS index to save.
        path (str): The path to save the index.
    """
    faiss.write_index(index, path)

def save_id_map(df, path):
    """
    Saves the DataFrame to a pickle file.
    Args:
        df (pd.DataFrame): The DataFrame to save.
        path (str): The path to save the DataFrame.
    """
    df.to_pickle(path)

def load_faiss_index(path):
    """
    Loads the FAISS index from a file.
    Args:
        path (str): The path to load the index from.
    Returns:
        faiss.Index: The loaded FAISS index.
    """
    return faiss.read_index(path)

def load_id_map(path):
    """
    Loads the DataFrame from a pickle file.
    Args:
        path (str): The path to load the DataFrame from.
    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_pickle(path)