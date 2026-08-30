import { defineStore } from 'pinia'
import { login, register, getUserInfo, updateUser, changePassword } from '../api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null')
  }),

  actions: {
    // 登录
    async doLogin(data) {
      const res = await login(data)
      this.token = res.data.token
      this.userInfo = res.data.userInfo
      localStorage.setItem('token', this.token)
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      return res
    },

    // 注册
    async doRegister(data) {
      const res = await register(data)
      this.token = res.data.token
      this.userInfo = res.data.userInfo
      localStorage.setItem('token', this.token)
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      return res
    },

    // 拉取最新用户信息
    async fetchUserInfo() {
      const res = await getUserInfo()
      this.userInfo = res.data
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      return res
    },

    // 更新用户信息（简介等）
    async updateUserInfo(data) {
      const res = await updateUser(data)
      // 合并更新，保留未变字段
      this.userInfo = { ...this.userInfo, ...res.data }
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      return res
    },

    // 修改密码
    async changePassword(data) {
      const res = await changePassword(data)
      return res
    },

    // 退出登录
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }
})
