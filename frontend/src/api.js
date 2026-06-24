import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(err)
  }
)

export const authAPI = {
  login: (email, password) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

export const documentsAPI = {
  list: () => api.get('/documents/'),
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  delete: (id) => api.delete(`/documents/${id}`),
}

export const chatAPI = {
  send: (message, sessionId) => api.post('/chat/message', { message, session_id: sessionId }),
  sessions: () => api.get('/chat/sessions'),
}

export const graphAPI = {
  get: () => api.get('/knowledge-graph/'),
}

export const complianceAPI = {
  list: () => api.get('/compliance/'),
  summary: () => api.get('/compliance/summary'),
}

export const maintenanceAPI = {
  list: () => api.get('/maintenance/'),
  summary: () => api.get('/maintenance/summary'),
}

export const rootCauseAPI = {
  analyze: (data) => api.post('/root-cause/analyze', data),
}

export const analyticsAPI = {
  dashboard: () => api.get('/analytics/dashboard'),
}

export default api
