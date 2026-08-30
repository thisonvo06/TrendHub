import request from '../utils/request'

// ============================================
// 新闻模块
// 参考 docs/API接口规范文档.md
// ============================================

/**
 * 1. 获取新闻分类列表
 * GET /api/news/categories?skip=&limit=
 */
export const getCategories = (params) => {
  return request.get('/api/news/categories', { params })
}

/**
 * 2. 获取新闻列表（按分类分页）
 * GET /api/news/list?categoryId=&page=&pageSize=
 */
export const getNewsList = (params) => {
  return request.get('/api/news/list', { params })
}

/**
 * 3. 获取新闻详情
 * GET /api/news/detail?id=
 */
export const getNewsDetail = (params) => {
  return request.get('/api/news/detail', { params })
}
