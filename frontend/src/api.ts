import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export const searchMovies = async (query: string) => {
  const res = await axios.post(`${API_BASE}/search`, { query })
  return res.data.movies
}

export const transcribeAudio = async (audio: string) => {
  const res = await axios.post(`${API_BASE}/transcribe`, { audio })
  return res.data.transcription
} 