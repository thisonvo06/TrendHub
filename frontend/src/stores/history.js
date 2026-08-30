import { defineStore } from 'pinia'
import {
  addHistory,
  getHistoryList,
  deleteHistory,
  clearHistory
} from '../api/history'

export const useHistoryStore = defineStore('history', {
  state: () => ({
    list: [],
    page: 1,
    pageSize: 10,
    total: 0,
    hasMore: true,
    listLoading: false,
    listRefreshing: false,
    actionLoading: false
  }),

  actions: {
    // 打开新闻详情时添加一条历史
    async add(newsId) {
      this.actionLoading = true
      try {
        const res = await addHistory({ newsId })
        return res.data
      } finally {
        this.actionLoading = false
      }
    },

    resetList() {
      this.list = []
      this.page = 1
      this.total = 0
      this.hasMore = true
    },

    async fetchList({ reset = false } = {}) {
      if (reset) this.resetList()
      if (this.listLoading) return
      if (!this.hasMore && !reset) return

      this.listLoading = true
      try {
        const res = await getHistoryList({
          page: this.page,
          pageSize: this.pageSize
        })
        const { list = [], total = 0, hasMore = false } = res.data || {}
        if (reset) {
          this.list = list
        } else {
          this.list = [...this.list, ...list]
        }
        this.total = total
        this.hasMore = hasMore
        if (!reset && list.length > 0) this.page += 1
        return { list, total, hasMore }
      } finally {
        this.listLoading = false
      }
    },

    async refreshList() {
      this.listRefreshing = true
      try {
        return await this.fetchList({ reset: true })
      } finally {
        this.listRefreshing = false
      }
    },

    async remove(historyId) {
      this.actionLoading = true
      try {
        const res = await deleteHistory(historyId)
        // 从列表移除（兼容 history_id 和 id 两种字段）
        const before = this.list.length
        this.list = this.list.filter((i) => (i.history_id || i.id) !== historyId)
        if (this.list.length !== before) {
          this.total = Math.max(0, this.total - (before - this.list.length))
        }
        return res
      } finally {
        this.actionLoading = false
      }
    },

    async clearAll() {
      this.actionLoading = true
      try {
        const res = await clearHistory()
        this.resetList()
        return res
      } finally {
        this.actionLoading = false
      }
    }
  }
})
