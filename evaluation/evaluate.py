from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
from utils.openai_intent import extract_structured_intent
from utils.search import search_with_intent
from utils.faiss_io import load_faiss_index, load_id_map

# Download wordnet resource
import nltk
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Preprocesses text by lemmatizing words and removing non-alphanumeric characters.
    Args:
        text (str): Input text string.
    Returns:
        set: Set of lemmatized words.
    """
    words = re.findall(r'\w+', text.lower())
    return set(lemmatizer.lemmatize(word) for word in words)

def keyword_match_score(results, expected_keywords):
    """
    Calculates the match score between expected keywords and results.
    Args:
        results (pd.DataFrame): Results DataFrame.
        expected_keywords (list): List of expected keywords.
    Returns:
        list: List of boolean values indicating keyword matches.
    """
    expected_lemmas = preprocess_text(" ".join(expected_keywords))
    hits = []

    for _, row in results.iterrows():
        text_lemmas = preprocess_text(row['embedding_input'])
        match = not expected_lemmas.isdisjoint(text_lemmas)
        hits.append(match)

    return hits

def evaluate_model(test_queries, index, id_map, top_k=5):
    """
    Evaluates the model's performance on a set of test queries.
    Args:
        test_queries (list): List of test queries with expected keywords.
        index (faiss.Index): FAISS index for searching.
        id_map (pd.DataFrame): ID map DataFrame for mapping search results.
        top_k (int): Number of top results to consider for evaluation.
    Returns:
        pd.DataFrame: DataFrame containing evaluation summary for each test query.
    """
    summary = []

    for test in test_queries:
        query = test["query"]
        expected = test["expected_keywords"]

        # Pass index and id_map into search
        results = search_with_intent(query, index, id_map, top_k=top_k)
        hits = keyword_match_score(results, expected)
        hit_count = sum(hits)
        hit_rate = hit_count / top_k

        result_lines = []
        for idx, (title, hit) in enumerate(zip(results['title'], hits)):
            check = "R" if hit else "W"
            result_lines.append(f"{check} {idx+1}. {title}")

        summary.append({
            "query": query,
            "hit_rate": hit_rate,
            "hit_count": hit_count,
            "top_results": "\n".join(result_lines)
        })

    return pd.DataFrame(summary)