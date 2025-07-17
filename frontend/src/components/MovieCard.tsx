import React from 'react'

type Movie = {
  id: string
  title: string
  type: string
  director: string
  cast: string
  country: string
  release_year: number | null
  rating: string
  duration: string
  listed_in: string
  description: string
}

type Props = {
  movie: Movie
}

const MovieCard: React.FC<Props> = ({ movie }) => (
  <div
    className="bg-neutral-900 rounded-lg shadow-lg p-4 flex flex-col gap-2 h-full focus:outline-none focus:ring-2 focus:ring-red-600"
    tabIndex={0}
    aria-label={movie.title}
  >
    <div className="text-lg font-bold text-white truncate" title={movie.title}>{movie.title}</div>
    <div className="text-xs text-red-500 font-semibold">{movie.type} {movie.release_year ? `• ${movie.release_year}` : ''}</div>
    <div className="text-xs text-neutral-400 truncate" title={movie.cast}>{movie.cast}</div>
    <div className="text-xs text-neutral-400 truncate" title={movie.listed_in}>{movie.listed_in}</div>
    <div className="text-xs text-neutral-300 line-clamp-3">{movie.description}</div>
    <div className="flex flex-wrap gap-2 mt-auto">
      {movie.rating && <span className="text-xs bg-red-700 text-white rounded px-2 py-0.5">{movie.rating}</span>}
      {movie.duration && <span className="text-xs bg-neutral-800 text-white rounded px-2 py-0.5">{movie.duration}</span>}
      {movie.country && <span className="text-xs bg-neutral-700 text-white rounded px-2 py-0.5">{movie.country}</span>}
    </div>
  </div>
)

export default MovieCard 