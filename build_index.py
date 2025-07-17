from utils.preprocess import preprocess_netflix_data
from utils.faiss_io import build_faiss_index, save_faiss_index, save_id_map

df = preprocess_netflix_data("./data/netflix_titles.csv")
index, id_map = build_faiss_index(df)

save_faiss_index(index, "./models/netflix_faiss.index")
save_id_map(id_map, "./models/id_map.pkl")

print("FAISS index and ID map saved to /models.")
