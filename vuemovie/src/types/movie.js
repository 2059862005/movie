// TMDB API Types

export interface Movie {
  id: number
  title: string
  original_title: string
  overview: string
  poster_path: string | null
  backdrop_path: string | null
  release_date: string
  vote_average: number
  vote_count: number
  popularity: number
  adult: boolean
  genre_ids: number[]
  original_language: string
  video: boolean
}

export interface MovieDetail extends Movie {
  runtime: number | null
  budget: number
  revenue: number
  status: string
  tagline: string | null
  genres: Genre[]
  production_companies: ProductionCompany[]
  credits: Credits
  videos: Videos
  similar: MovieResponse
  recommendations: MovieResponse
}

export interface Genre {
  id: number
  name: string
}

export interface ProductionCompany {
  id: number
  name: string
  logo_path: string | null
  origin_country: string
}

export interface Credits {
  cast: CastMember[]
  crew: CrewMember[]
}

export interface CastMember {
  id: number
  name: string
  character: string
  profile_path: string | null
  order: number
}

export interface CrewMember {
  id: number
  name: string
  job: string
  department: string
  profile_path: string | null
}

export interface Videos {
  results: Video[]
}

export interface Video {
  id: string
  key: string
  name: string
  site: string
  type: string
  official: boolean
}

export interface MovieResponse {
  page: number
  results: Movie[]
  total_pages: number
  total_results: number
}

export interface GenreResponse {
  genres: Genre[]
}

export interface SearchParams {
  query: string
  page?: number
}

export interface DiscoverParams {
  with_genres?: number
  primary_release_year?: number
  page?: number
  sort_by?: string
}
