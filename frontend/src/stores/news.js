import { defineStore } from 'pinia'
import { getCategories, getNewsList, getNewsDetail } from '../api/news'

export const useNewsStore = defineStore('news', {
  state: () => ({
    // 分类列表
    categories: [],
    // 当前选中分类（news list 页）
    currentCategoryId: null,
    currentCategoryName: '',

    // 新闻列表分页数据
    list: [],
    page: 1,
    pageSize: 10,
    total: 0,
    hasMore: true,
    listLoading: false,
    listRefreshing: false,

    // 新闻详情
    detail: null,
    detailLoading: false
  }),

  actions: {
    // =================================================
    // 分类
    // =================================================
    async fetchCategories(params = { skip: 0, limit: 100 }) {
      const res = await getCategories(params)
      this.categories = res.data || []
      return res.data
    },

    setCurrentCategory(id, name = '') {
      this.currentCategoryId = id
      this.currentCategoryName = name
    },

    // =================================================
    // 新闻列表（按分类分页 + 下拉刷新 + 加载更多）
    // =================================================
    resetListParams() {
      this.list = []
      this.page = 1
      this.total = 0
      this.hasMore = true
    },

    async fetchNewsList(params = {}, { reset = false } = {}) {
      if (reset) this.resetListParams()
      if (this.listLoading) return
      if (!this.hasMore && !reset) return

      this.listLoading = true
      try {
        const payload = {
          categoryId: this.currentCategoryId,
          page: this.page,
          pageSize: this.pageSize,
          ...params
        }
        const res = await getNewsList(payload)
        // data: { list, total, hasMore }
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

    async refreshNewsList(params = {}) {
      this.listRefreshing = true
      try {
        return await this.fetchNewsList(params, { reset: true })
      } finally {
        this.listRefreshing = false
      }
    },

    // =================================================
    // 新闻详情
    // =================================================
    async fetchNewsDetail(id) {
      this.detailLoading = true
      this.detail = null
      try {
        const res = await getNewsDetail({ id })
        this.detail = res.data
        return res.data
      } finally {
        this.detailLoading = false
      }
    },

    clearDetail() {
      this.detail = null
    }
  }
})
