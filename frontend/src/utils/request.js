import axios from 'axios'
import { showToast } from 'vant'

const request = axios.create({
  baseURL: '/',
  timeout: 10000
})

// 请求拦截：自动加 Authorization
request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => Promise.reject(error))

// 响应拦截：统一处理错误 + 提取后端 data
request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 后端 success_response 返回 { code:200, message, data }
    if (res.code === 200) {
      return res
    }
    showToast(res.message || '请求失败')
    return Promise.reject(res)
  },
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail
    if (status === 401) {
      showToast(detail || '登录已过期')
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    } else {
      showToast(detail || error.message || '网络错误')
    }
    return Promise.reject(error)
  }
)

export default request
