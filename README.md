# 🎙️ Voice Search System

A voice-powered search application for content recommendation that combines natural language processing, semantic search, and voice recognition to help users find their perfect movie or TV show.

---

## ✨ Features

- **Voice Interface**: Converts natural language voice queries to text using browser-based input
- **Intent Extraction**: Extracts mood, genre, actor, length preferences, etc. using OpenAI. Parses free-form queries like "I want something about sibling rivalry or complicated families."
- **Semantic Search**: Embedding-based search using Sentence Transformers and FAISS. Finds contextually similar titles based on user query
- **Interactive UI**: React based UI includes voice input, and dynamic search results

---

## 📸 Demo

<video width="100%" controls>
  <source src="demo/demo_video.mov" type="video/quicktime">
  Your browser does not support the video tag.
</video>

---

## 📁 Dataset

This project uses the publicly available on [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows). It has been included here for educational and portfolio purposes only.

The dataset contains metadata about Netflix content as of 2021, including both movies and TV shows across various genres and countries. Each row represents a unique title available on Netflix.

Key columns include:

```
| Column       | Description                                |
|--------------|--------------------------------------------|
| show_id      | Unique identifier for the show/movie       |
| type         | Content type – either "Movie" or "TV Show" |
| title        | Title of the content                       |
| director     | Director(s) of the content                 |
| cast         | Actors                                     |
| country      | Country where the movie/show was produced  |
| date_added   | Date the content was added to Netflix      |
| release_year | Year the title was released                |
| rating       | Age rating (e.g., PG, TV-MA, etc.)         |
| duration     | Length in minutes or number of seasons     |
| listed_in    | Genre(s)                                   |
| description  | Short description/summary                  |
```
---

## 🏗️ Architecture

The project consists of two main components:
- **Python Backend**: Flask API with voice processing and semantic search
- **React Frontend**: Modern web interface with voice recording capabilities

---

## 🔧 Technologies Used

* **Google SpeechRecognition API** 
* **OpenAI GPT-3.5-turbo**
* **Sentence Transformers (all-mpnet-base-v2)** 
* **FAISS (Facebook AI Similarity Search)** 
* **React + TypeScript + Tailwind CSS** 
* **Flask** 
* **NumPy, pandas, scikit-learn** 

---

## ⚙️ Python Backend

### How It Works

The Python backend is built with Flask and implements a sophisticated search system:

1. **Data Processing**: Content titles are preprocessed and embedded using sentence transformers
2. **FAISS Index**: High-performance vector similarity search using FAISS
3. **Intent Extraction**: OpenAI GPT-3.5-turbo extracts structured intent from natural language queries
4. **Semantic Search**: Combines intent-based filtering with vector similarity search
5. **Voice Processing**: Speech recognition using Google's Speech Recognition API

### Key Components

- **`api.py`**: Main Flask API with search and transcription endpoints
- **`utils/search.py`**: Core search logic with intent-based filtering
- **`utils/openai_intent.py`**: AI-powered intent extraction
- **`utils/embeddings.py`**: Text embedding generation
- **`utils/faiss_io.py`**: FAISS index management
- **`utils/preprocess.py`**: Data preprocessing utilities

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Build Search Index**:
   ```bash
   python build_index.py
   ```

4. **Run the API Server**:
   ```bash
   python api.py
   ```
   The API will be available at `http://localhost:5000`

### API Endpoints

- `POST /api/search`: Search for movies/shows
- `POST /api/transcribe`: Transcribe audio to text
- `GET /api/health`: Health check endpoint

---

## ⚛️ React Frontend

### How It Works

The React frontend provides an intuitive voice search interface:

1. **Voice Recording**: Uses Web Audio API for real-time voice capture
2. **Audio Processing**: Converts audio to base64 and sends to backend
3. **Search Interface**: Text input with voice button for dual input methods
4. **Results Display**: Movie cards with detailed information
5. **Responsive Design**: Works seamlessly on desktop and mobile devices

### Key Components

- **`App.tsx`**: Main application with voice recording and search logic
- **`MovieCard.tsx`**: Individual movie/show display component
- **`api.ts`**: API communication functions for search and transcription

### Setup Instructions

1. **Navigate to Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Start Development Server**:
   ```bash
   npm start
   ```
   The app will open at `http://localhost:3000`

4. **Build for Production**:
   ```bash
   npm run build
   ```

---

## 🚀 Quick Start

### Complete Setup

1. **Clone and Setup Backend**:
   ```bash
   git clone <repository-url>
   cd voice-to-search
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_actual_api_key_here
   ```
3Build Search Index**:
   ```bash
   python build_index.py
   ```

4 **Start Backend**:
   ```bash
   python api.py
   ```5. **Setup Frontend** (in new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

6. **Open Application**:
   Navigate to `http://localhost:3000 in your browser

### Environment Variables

Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

**⚠️ Security Note:** Never commit your actual API keys to version control. The `.env` file is already in `.gitignore` to prevent accidental commits.

### Usage

1. **Voice Search**: Click the microphone button and speak your preferences
2. **Text Search**: Type your query in the search box
3. **Examples**:
   - "I want something funny and short"
   - "Show me dark thrillers from the 90s"
   - "Anything with doctors set in Seattle"
   - "I need a feel-good movie for the family"

---

## 📁 Project Structure

voice-to-search/
├── api.py                   # Main Flask API
├── app.py                   # Streamlit alternative UI
├── requirements.txt         # Python dependencies
├── build_index.py          # Index building script
├── data/
│   └── netflix_titles.csv  # Netflix dataset
├── models/
│   ├── netflix_faiss.index # FAISS search index
│   └── id_map.pkl         # ID mapping
├── utils/
│   ├── search.py          # Search logic
│   ├── embeddings.py      # Text embeddings
│   ├── openai_intent.py   # Intent extraction
│   ├── faiss_io.py        # FAISS utilities
│   └── preprocess.py      # Data preprocessing
├── voice/
│   └── capture_and_transcribe.py
├── evaluation/             # Evaluation scripts
└── frontend/              # React application
    ├── package.json
    ├── src/
    │   ├── App.tsx
    │   ├── api.ts
    │   └── components/
    └── public/

---

## 👩‍💻 Author

**Shraddha Gupte**
*Data Scientist | Machine Learning | NLP | LLM | Product Strategy*
🔗 [LinkedIn](https://www.linkedin.com/in/shraddha-gupte/) | 🌐 [GitHub](https://github.com/shraddhagupte)
