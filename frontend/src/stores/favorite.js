import { defineStore } from 'pinia'
import {
  checkFavorite,
  addFavorite,
  removeFavorite,
  getFavoriteList,
  clearFavorite
} from '../api/favorite'

export const useFavoriteStore = defineStore('favorite', {
  state: () => ({
    // 收藏状态 key: newsId -> boolean
    cache: {},
    // 列表
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
    // =================================================
    // 单条收藏状态
    // =================================================
    async check(newsId) {
      try {
        const res = await checkFavorite({ newsId })
        const val = !!(res.data && res.data.isFavorite)
        this.cache[newsId] = val
        return val
      } catch (e) {
        return !!this.cache[newsId]
      }
    },

    // 只返回缓存（不发请求）
    getCached(newsId) {
      return !!this.cache[newsId]
    },

    async toggle(newsId, currentState) {
      this.actionLoading = true
      try {
        if (currentState) {
          await removeFavorite({ newsId })
          this.cache[newsId] = false
        } else {
          const res = await addFavorite({ newsId })
          this.cache[newsId] = true
          return res.data
        }
      } finally {
        this.actionLoading = false
      }
    },

    async add(newsId) {
      this.actionLoading = true
      try {
        const res = await addFavorite({ newsId })
        this.cache[newsId] = true
        return res.data
      } finally {
        this.actionLoading = false
      }
    },

    async remove(newsId) {
      this.actionLoading = true
      try {
        await removeFavorite({ newsId })
        this.cache[newsId] = false
        // 同步移除列表和数量
        const before = this.list.length
        this.list = this.list.filter((i) => (i.newsId || i.id) !== newsId)
        if (this.list.length !== before) {
          this.total = Math.max(0, this.total - (before - this.list.length))
        }
      } finally {
        this.actionLoading = false
      }
    },

    // =================================================
    // 收藏列表
    // =================================================
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
        const res = await getFavoriteList({
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

    async clearAll() {
      this.actionLoading = true
      try {
        const res = await clearFavorite()
        this.cache = {}
        this.resetList()
        return res
      } finally {
        this.actionLoading = false
      }
    }
  }
})
