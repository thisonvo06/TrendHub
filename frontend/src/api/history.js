import request from '../utils/request'

// ============================================
// 浏览历史模块
// 参考 docs/API接口规范文档.md
// ============================================

/**
 * 1. 添加浏览记录（打开新闻详情时调用）
 * POST /api/history/add
 * body: { newsId }
 */
export const addHistory = (data) => {
  return request.post('/api/history/add', data)
}

/**
 * 2. 获取浏览历史列表
 * GET /api/history/list?page=&pageSize=
 */
export const getHistoryList = (params) => {
  return request.get('/api/history/list', { params })
}

/**
 * 3. 删除单条浏览记录
 * DELETE /api/history/delete/{history_id}
 */
export const deleteHistory = (historyId) => {
  return request.delete(`/api/history/delete/${historyId}`)
}

/**
 * 4. 清空浏览历史
 * DELETE /api/history/clear
 */
export const clearHistory = () => {
  return request.delete('/api/history/clear')
}
