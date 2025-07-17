from utils.faiss_io import load_faiss_index, load_id_map
from utils.search import search_with_intent
from voice.capture_and_transcribe import capture_and_transcribe

index = load_faiss_index("models/netflix_faiss.index")
id_map = load_id_map("models/id_map.pkl")

# query = "I'm curious about the psychology behind murderers. Got anything like that?"
# Is there a documentary on cults or strange communities?
query = capture_and_transcribe()
print("You said:", query)

results = search_with_intent(query, index, id_map)
print(results[['title', 'listed_in', 'duration_cleaned', 'description']])
