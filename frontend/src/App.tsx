import React, { useRef, useState } from 'react'
import { Loader2, Search } from 'lucide-react'
import MovieCard from './components/MovieCard'
import { searchMovies, transcribeAudio } from './api'

const App: React.FC = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunks = useRef<Blob[]>([])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value)
  }

  const handleSearch = async (q?: string) => {
    setLoading(true)
    setError('')
    try {
      const movies = await searchMovies(q ?? query)
      setResults(movies)
    } catch (e) {
      setError('Could not fetch results')
    }
    setLoading(false)
  }

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) handleSearch()
  }

  const handleMicClick = async () => {
    if (isRecording) {
      mediaRecorderRef.current?.stop()
      setIsRecording(false)
      return
    }
    setError('')
    setIsRecording(true)
    audioChunks.current = []
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new window.MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.ondataavailable = (e) => {
        audioChunks.current.push(e.data)
      }
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' })
        const reader = new FileReader()
        reader.onloadend = async () => {
          const base64Audio = reader.result as string
          setLoading(true)
          try {
            const transcription = await transcribeAudio(base64Audio)
            setQuery(transcription)
            await handleSearch(transcription)
          } catch {
            setError('Could not transcribe audio')
          }
          setLoading(false)
        }
        reader.readAsDataURL(audioBlob)
      }
      mediaRecorder.start()
      setTimeout(() => {
        if (mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop()
          setIsRecording(false)
        }
      }, 5000)
    } catch {
      setError('Microphone access denied')
      setIsRecording(false)
    }
  }

  return (
    <div className="min-h-screen bg-black flex flex-col items-center px-4 py-8">
      <div className="text-4xl md:text-5xl font-extrabold text-red-600 mb-2 select-none">VoiceFlix</div>
      <div className="text-lg text-neutral-400 mb-8 select-none">Describe your mood, speak your desires, discover your next favorite movie</div>
      
      <form
        className="flex w-full max-w-xl gap-2 mb-8"
        onSubmit={handleFormSubmit}
        role="search"
        aria-label="Search for movies or shows"
      >
        <input
          className="flex-1 rounded-l-lg bg-neutral-800 text-white px-4 py-2 focus:ring-2 focus:ring-red-600 outline-none"
          type="text"
          value={query}
          onChange={handleInputChange}
          placeholder="What do you want to watch?"
          aria-label="Search input"
        />
        <button
          type="submit"
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-r-lg flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-red-600"
          tabIndex={0}
          aria-label="Search"
        >
          <Search className="w-5 h-5" />
        </button>
        <button
          type="button"
          onClick={handleMicClick}
          className={`ml-2 rounded-full p-3 ${isRecording ? 'bg-red-700' : 'bg-neutral-800 hover:bg-red-700'} text-white focus:outline-none focus:ring-2 focus:ring-red-600 flex items-center justify-center`}
          tabIndex={0}
          aria-label={isRecording ? 'Stop recording' : 'Start voice search'}
          onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleMicClick() }}
        >
          <div className="flex items-center space-x-1">
            <div className={`w-1 h-3 bg-white rounded ${isRecording ? 'animate-pulse' : ''}`} style={{ animationDelay: '0ms' }}></div>
            <div className={`w-1 h-5 bg-white rounded ${isRecording ? 'animate-pulse' : ''}`} style={{ animationDelay: '150ms' }}></div>
            <div className={`w-1 h-4 bg-white rounded ${isRecording ? 'animate-pulse' : ''}`} style={{ animationDelay: '300ms' }}></div>
            <div className={`w-1 h-6 bg-white rounded ${isRecording ? 'animate-pulse' : ''}`} style={{ animationDelay: '450ms' }}></div>
            <div className={`w-1 h-3 bg-white rounded ${isRecording ? 'animate-pulse' : ''}`} style={{ animationDelay: '600ms' }}></div>
          </div>
        </button>
      </form>
      
      {loading && <Loader2 className="animate-spin text-red-600 w-8 h-8 mb-8" aria-label="Loading" />}
      {error && <div className="text-red-500 mb-4" role="alert">{error}</div>}
      
      {results.length > 0 && (
        <div className="w-130 mx-auto grid grid-cols-1 gap-4">
          {results.map(movie => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  )
}

export default App
