import request from '../utils/request'

// ============================================
// 收藏模块
// 参考 docs/API接口规范文档.md
// ============================================

/**
 * 1. 检查新闻收藏状态
 * GET /api/favorite/check?newsId=
 */
export const checkFavorite = (params) => {
  return request.get('/api/favorite/check', { params })
}

/**
 * 2. 添加收藏
 * POST /api/favorite/add
 * body: { newsId }
 */
export const addFavorite = (data) => {
  return request.post('/api/favorite/add', data)
}

/**
 * 3. 取消收藏
 * DELETE /api/favorite/remove?newsId=
 */
export const removeFavorite = (params) => {
  return request.delete('/api/favorite/remove', { params })
}

/**
 * 4. 获取收藏列表
 * GET /api/favorite/list?page=&pageSize=
 */
export const getFavoriteList = (params) => {
  return request.get('/api/favorite/list', { params })
}

/**
 * 5. 清空所有收藏
 * DELETE /api/favorite/clear
 */
export const clearFavorite = () => {
  return request.delete('/api/favorite/clear')
}
