import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  register: (data) => api.post('/auth/users/', data),
  login: (data) => api.post('/jwt/create/', data),
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
  getCurrentUser: () => api.get('/auth/users/me/'),
  setPassword: (data) => api.post('/auth/users/set_password/', data),
  resetPassword: (data) => api.post('/auth/users/reset_password/', data)
}

export const movieApi = {
  getMovies: (params) => api.get('/movies/', { params }),
  getMovie: (id) => api.get(`/movies/${id}/`),
  getCategories: () => api.get('/movies/categories/'),
  getMoviePlay: (id) => api.get(`/movies/${id}/play/`),
  collectMovie: (id) => api.post(`/movies/${id}/collect/`),
  wishMovie: (id) => api.post(`/movies/${id}/wish/`),
  watchingMovie: (id) => api.post(`/movies/${id}/watching/`),
  watchedMovie: (id) => api.post(`/movies/${id}/watched/`),
  getMyCollections: () => api.get('/movies/my_collections/'),
  getMyWishes: () => api.get('/movies/my_wishes/'),
  getMyWatching: () => api.get('/movies/my_watching/'),
  getMyWatched: () => api.get('/movies/my_watched/')
}

export const vipApi = {
  getVipCards: () => api.get('/vip/cards/'),
  getMyVip: () => api.get('/vip/my-vip/'),
  buyVip: (cardId) => api.post(`/vip/buy-vip/${cardId}/`)
}

export const paymentApi = {
  createOrder: (vipCardId) => api.post('/payment/create_order/', { vip_card_id: vipCardId }),
  getMyOrders: () => api.get('/payment/my_orders/'),
  checkOrder: (outTradeNo) => api.get('/payment/check_order/', { params: { out_trade_no: outTradeNo } })
}

export const getImageUrl = (path) => {
  if (!path) return '/placeholder.jpg'
  if (path.startsWith('http')) return path
  return `/media/${path}`
}

export default api
