from utils.openai_intent import extract_structured_intent
from utils.embeddings import embed_query
import faiss
import numpy as np

def filter_catalog_by_intent(df, intent):
    """
    Filters the catalog DataFrame based on the intent.
    Args:
        df (pd.DataFrame): Input DataFrame.
        intent (dict): Intent dictionary.
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    filtered = df.copy()

    if intent.get("genre"):
        for g in intent['genre']:
            filtered = filtered[filtered['listed_in'].str.lower().str.contains(g.lower())]

    if intent.get("type"):
        for t in intent['type']:
            filtered = filtered[filtered['type'].str.lower() == t.lower()]
    
    if intent.get("actors"):
        for actor in intent['actors']:
            filtered = filtered[filtered['cast'].str.lower().str.contains(actor.lower())]

    if intent.get("country"):
        for c in intent['country']:
            filtered = filtered[filtered['country'].str.lower().str.contains(c.lower())]

    if intent.get("rating"):
        filtered = filtered[filtered['rating'].str.lower() == intent['rating'].lower()]

    if intent.get("release_year"):
        filtered = filtered[filtered['release_year'] == int(intent['release_year'])]

    if intent.get("duration_minutes"):
        try:
            dur = intent["duration_minutes"]
            if '<' in dur:
                threshold = int(dur.split('<')[-1].strip())
                filtered = filtered[filtered['duration_cleaned'] < threshold]
            elif '>' in dur:
                threshold = int(dur.split('>')[-1].strip())
                filtered = filtered[filtered['duration_cleaned'] > threshold]
        except:
            pass
    
    return filtered

def search_fallback(query, index, id_map, top_k=5):
    """
    Fallback search function when intent-based filtering fails.
    Args:
        query (str): User's natural language query.
        index (faiss.Index): FAISS index.
        id_map (pd.DataFrame): ID map DataFrame.
        top_k (int): Number of top results to return.
    Returns:
        pd.DataFrame: Filtered DataFrame with top results.
    """
    query_embedding = embed_query(query)
    D, I = index.search(query_embedding, top_k)
    return id_map.iloc[I[0]]

def search_with_intent(query, index, id_map, top_k=5):
    """
    Searches the catalog DataFrame with a user query and intent.
    Args:
        query (str): User's natural language query.
        index (faiss.Index): FAISS index.
        id_map (pd.DataFrame): ID map DataFrame.
        top_k (int): Number of top results to return.
    Returns:
        pd.DataFrame: Filtered DataFrame with top results.
    """
    intent = extract_structured_intent(query)
    filtered_df = filter_catalog_by_intent(id_map, intent)

    if len(filtered_df) == 0:
        print("No shows match intent filters. Returning top results for raw query.")
        return search_fallback(query, index, id_map, top_k)

    # Build enriched query
    enriched_parts = [query]
    for key, value in intent.items():
        if isinstance(value, str) and value.strip():
            enriched_parts.append(value.strip())
        elif isinstance(value, list) and value:
            enriched_parts.extend([v.strip() for v in value if v.strip()])
    enriched_query = ". ".join(enriched_parts)

    # Get embeddings for the filtered subset
    filtered_embeddings = np.vstack(filtered_df['embedding'].to_numpy())
    filtered_ids = filtered_df.index.tolist()

    query_embedding = embed_query(enriched_query)
    scores = np.dot(filtered_embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(-scores)[:top_k]

    # Map top indices back to original IDs
    matched_ids = [filtered_ids[i] for i in top_indices]
    
    return id_map.loc[matched_ids]