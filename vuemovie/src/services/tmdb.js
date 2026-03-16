import axios from 'axios'

// TMDB API 配置
// 注意：实际使用时需要替换为真实的 API Key
// 可以从 https://www.themoviedb.org/settings/api 获取
const API_KEY = 'YOUR_TMDB_API_KEY'
const BASE_URL = 'https://api.themoviedb.org/3'
const IMAGE_BASE_URL = 'https://image.tmdb.org/t/p'

// Mock 数据 - 当 API 不可用时使用
const mockMovies = [
  {
    id: 550,
    title: '搏击俱乐部',
    original_title: 'Fight Club',
    overview: '一个充满愤怒和暴力的故事，探讨了现代社会中个人的异化问题。',
    poster_path: '/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg',
    backdrop_path: '/hZkgoQYus5vegHoetLkCJzb17zJ.jpg',
    release_date: '1999-10-15',
    vote_average: 8.4,
    vote_count: 26000,
    popularity: 100,
    genre_ids: [18, 53, 35]
  },
  {
    id: 680,
    title: '黑客帝国',
    original_title: 'The Matrix',
    overview: '一名黑客发现了现实的真相，卷入了一场反抗机器的战争。',
    poster_path: '/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
    backdrop_path: '/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg',
    release_date: '1999-03-30',
    vote_average: 8.2,
    vote_count: 22000,
    popularity: 90,
    genre_ids: [28, 878, 12]
  },
  {
    id: 155,
    title: '黑暗骑士',
    original_title: 'The Dark Knight',
    overview: '蝙蝠侠与小丑之间的终极对决，探讨正义与混乱的边界。',
    poster_path: '/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
    backdrop_path: '/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg',
    release_date: '2008-07-14',
    vote_average: 8.5,
    vote_count: 28000,
    popularity: 95,
    genre_ids: [18, 28, 80]
  },
  {
    id: 13,
    title: '阿甘正传',
    original_title: 'Forrest Gump',
    overview: '一个智商低于常人的男子经历了美国历史上许多重大事件。',
    poster_path: '/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
    backdrop_path: '/7c9UVPPiTPltouxRVY6N9uugaVA.jpg',
    release_date: '1994-06-23',
    vote_average: 8.5,
    vote_count: 23000,
    popularity: 85,
    genre_ids: [35, 18, 10749]
  },
  {
    id: 278,
    title: '肖申克的救赎',
    original_title: 'The Shawshank Redemption',
    overview: '一位银行家被冤枉入狱，在监狱中度过余生并最终逃脱。',
    poster_path: '/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    backdrop_path: '/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg',
    release_date: '1994-09-23',
    vote_average: 8.7,
    vote_count: 22000,
    popularity: 80,
    genre_ids: [18, 80]
  },
  {
    id: 238,
    title: '教父',
    original_title: 'The Godfather',
    overview: '意大利黑手党家族的权利斗争和传承故事。',
    poster_path: '/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    backdrop_path: '/tmU7GeKVybMWFButWEGl2M4GeiP.jpg',
    release_date: '1972-03-14',
    vote_average: 8.7,
    vote_count: 17000,
    popularity: 75,
    genre_ids: [18, 80]
  },
  {
    id: 240,
    title: '泰坦尼克号',
    original_title: 'Titanic',
    overview: '穷画家和富家女在泰坦尼克号上的爱情故事。',
    poster_path: '/9xrGrkfqPpEE0XgCGtgVzXJLQcE.jpg',
    backdrop_path: '/6VmGqBz17OsXvZ9xE0eS2F0cJ7T.jpg',
    release_date: '1997-11-18',
    vote_average: 7.9,
    vote_count: 20000,
    popularity: 70,
    genre_ids: [18, 10749]
  },
  {
    id: 122,
    title: '指环王：王者归来',
    original_title: 'The Lord of the Rings: The Return of the King',
    overview: '霍比特人弗罗多销毁至尊戒的史诗旅程。',
    poster_path: '/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',
    backdrop_path: '/2u7zbn8EudG6kLlBzUYqP8RyFU4.jpg',
    release_date: '2003-12-01',
    vote_average: 8.5,
    vote_count: 20000,
    popularity: 88,
    genre_ids: [12, 14, 28]
  }
]

const api = axios.create({
  baseURL: BASE_URL,
  params: {
    api_key: API_KEY,
    language: 'zh-CN'
  }
})

// 检查是否使用 mock 数据
const isMockMode = API_KEY === 'YOUR_TMDB_API_KEY' || !API_KEY

// 图片路径处理
export const getImageUrl = (path, size = 'original') => {
  if (!path) return ''
  return `${IMAGE_BASE_URL}/${size}${path}`
}

// 获取热门电影
export const getPopularMovies = async (page = 1) => {
  if (isMockMode) {
    return {
      page: 1,
      results: mockMovies,
      total_pages: 1,
      total_results: mockMovies.length
    }
  }
  const response = await api.get('/movie/popular', { params: { page } })
  return response.data
}

// 获取正在上映电影
export const getNowPlayingMovies = async (page = 1) => {
  if (isMockMode) {
    return {
      page: 1,
      results: mockMovies.slice(0, 4),
      total_pages: 1,
      total_results: 4
    }
  }
  const response = await api.get('/movie/now_playing', { params: { page } })
  return response.data
}

// 获取电影详情
export const getMovieDetail = async (movieId) => {
  if (isMockMode) {
    const movie = mockMovies.find(m => m.id === parseInt(movieId)) || mockMovies[0]
    return {
      ...movie,
      runtime: 120,
      budget: 10000000,
      revenue: 100000000,
      status: 'Released',
      tagline: '一部经典电影',
      genres: [{ id: 18, name: '剧情' }],
      production_companies: [],
      credits: {
        cast: [
          { id: 1, name: '布拉德·皮特', character: '泰勒·德顿', profile_path: null, order: 0 },
          { id: 2, name: '爱德华·诺顿', character: '无名氏', profile_path: null, order: 1 },
          { id: 3, name: '海伦娜·伯翰·卡特', character: '玛拉·辛格', profile_path: null, order: 2 }
        ],
        crew: []
      },
      videos: {
        results: []
      },
      similar: { results: mockMovies.slice(0, 4), page: 1, total_pages: 1, total_results: 4 },
      recommendations: { results: mockMovies.slice(0, 4), page: 1, total_pages: 1, total_results: 4 }
    }
  }
  const response = await api.get(`/movie/${movieId}`, {
    params: { append_to_response: 'credits,videos,similar,recommendations' }
  })
  return response.data
}

// 搜索电影
export const searchMovies = async (params) => {
  if (isMockMode) {
    const results = mockMovies.filter(m => 
      m.title.toLowerCase().includes(params.query.toLowerCase())
    )
    return {
      page: 1,
      results,
      total_pages: 1,
      total_results: results.length
    }
  }
  const response = await api.get('/search/movie', { 
    params: { 
      query: params.query, 
      page: params.page || 1 
    } 
  })
  return response.data
}

// 获取电影分类列表
export const getMovieGenres = async () => {
  if (isMockMode) {
    return {
      genres: [
        { id: 28, name: '动作' },
        { id: 12, name: '冒险' },
        { id: 16, name: '动画' },
        { id: 35, name: '喜剧' },
        { id: 80, name: '犯罪' },
        { id: 99, name: '纪录片' },
        { id: 18, name: '剧情' },
        { id: 10751, name: '家庭' },
        { id: 14, name: '奇幻' },
        { id: 36, name: '历史' },
        { id: 27, name: '恐怖' },
        { id: 10402, name: '音乐' },
        { id: 9648, name: '悬疑' },
        { id: 10749, name: '爱情' },
        { id: 878, name: '科幻' },
        { id: 10770, name: '电视电影' },
        { id: 53, name: '惊悚' },
        { id: 10752, name: '战争' },
        { id: 37, name: '西部' }
      ]
    }
  }
  const response = await api.get('/genre/movie/list')
  return response.data
}

// 按分类获取电影
export const discoverMovies = async (params) => {
  if (isMockMode) {
    let results = [...mockMovies]
    if (params.with_genres) {
      results = results.filter(m => m.genre_ids.includes(params.with_genres))
    }
    return {
      page: 1,
      results,
      total_pages: 1,
      total_results: results.length
    }
  }
  const response = await api.get('/discover/movie', { params })
  return response.data
}

// 获取电影视频（预告片）
export const getMovieVideos = async (movieId) => {
  if (isMockMode) {
    return { results: [] }
  }
  const response = await api.get(`/movie/${movieId}/videos`)
  return response.data
}

export default api
