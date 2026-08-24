import request from '../utils/request'

// 注册
export const register = (data) => {
  return request.post('/api/user/register', data)
}

// 登录
export const login = (data) => {
  return request.post('/api/user/login', data)
}

// 获取用户信息（需带 Authorization）
export const getUserInfo = () => {
  return request.get('/api/user/info')
}

// 更新用户信息（PUT /api/user/update）
export const updateUser = (data) => {
  return request.put('/api/user/update', data)
}
