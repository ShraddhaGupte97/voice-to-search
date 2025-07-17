from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import faiss
import numpy as np
from utils.search import search_with_intent
from utils.embeddings import embed_query
import speech_recognition as sr
import base64
import io
import wave
import os
import tempfile
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

df = None
index = None
id_map = None

def load_data():
    global df, index, id_map
    df = pd.read_csv('data/netflix_titles.csv')
    
    with open('models/id_map.pkl', 'rb') as f:
        id_map = pickle.load(f)
    
    index = faiss.read_index('models/netflix_faiss.index')

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        results = search_with_intent(query, index, id_map, top_k=5)
        
        movies = []
        for _, row in results.iterrows():
            movie = {
                'id': row['show_id'],
                'title': row['title'],
                'type': row['type'],
                'director': row['director'] if pd.notna(row['director']) else '',
                'cast': row['cast'] if pd.notna(row['cast']) else '',
                'country': row['country'] if pd.notna(row['country']) else '',
                'release_year': int(row['release_year']) if pd.notna(row['release_year']) else None,
                'rating': row['rating'] if pd.notna(row['rating']) else '',
                'duration': str(row['duration_cleaned']) + ' min' if pd.notna(row['duration_cleaned']) else '',
                'listed_in': row['listed_in'] if pd.notna(row['listed_in']) else '',
                'description': row['description'] if pd.notna(row['description']) else ''
            }
            movies.append(movie)
        
        return jsonify({'movies': movies})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        data = request.get_json()
        audio_data = data.get('audio')
        
        if not audio_data:
            return jsonify({'error': 'Audio data is required'}), 400
        
        audio_bytes = base64.b64decode(audio_data.split(',')[1])
        
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_input:
            temp_input.write(audio_bytes)
            temp_input_path = temp_input.name
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        try:
            audio = AudioSegment.from_file(temp_input_path, format="webm")
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(temp_output_path, format="wav")
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_output_path) as source:
                audio_data = recognizer.record(source)
            
            text = recognizer.recognize_google(audio_data)
            return jsonify({'transcription': text})
        
        finally:
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    load_data()
    app.run(debug=True, port=5000) 