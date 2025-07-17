from evaluation.evaluate import evaluate_model
from evaluation.test_queries import test_queries
from utils.faiss_io import load_faiss_index, load_id_map
import pandas as pd

if __name__ == "__main__":
    # Step 1: Load the index and id_map
    index = load_faiss_index("./models/netflix_faiss.index")
    id_map = load_id_map("./models/id_map.pkl")

    # Step 2: Run evaluation on test queries
    eval_df = evaluate_model(test_queries, index, id_map, top_k=5)

    # Step 3: Save and display results
    eval_df.to_csv("./evaluation/intent_based_query_results.csv", index=False)
    print("\nSample Evaluation Results:")
    print(eval_df[['query', 'hit_rate', 'hit_count']].head())
