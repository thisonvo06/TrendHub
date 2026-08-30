import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Categories',
    component: () => import('../views/Categories.vue'),
    meta: { title: '全部分类' }
  },
  {
    path: '/news/list/:categoryId',
    name: 'NewsList',
    component: () => import('../views/NewsList.vue'),
    meta: { title: '新闻列表' }
  },
  {
    path: '/news/detail/:id',
    name: 'NewsDetail',
    component: () => import('../views/NewsDetail.vue'),
    meta: { title: '新闻详情' }
  },
  {
    path: '/my',
    name: 'My',
    component: () => import('../views/My.vue'),
    meta: { title: '我的' }
  },
  {
    path: '/user/info',
    name: 'UserInfo',
    component: () => import('../views/UserInfo.vue'),
    meta: { title: '用户信息' }
  },
  {
    path: '/favorite/list',
    name: 'FavoriteList',
    component: () => import('../views/FavoriteList.vue'),
    meta: { title: '我的收藏', requireAuth: true }
  },
  {
    path: '/history/list',
    name: 'HistoryList',
    component: () => import('../views/HistoryList.vue'),
    meta: { title: '浏览历史', requireAuth: true }
  },
  {
    path: '/message/list',
    name: 'MessageList',
    component: () => import('../views/MessageList.vue'),
    meta: { title: '消息通知', requireAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { title: '设置' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：设置页面标题 + 简单鉴权（requireAuth）
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  const token = localStorage.getItem('token')
  if (to.meta.requireAuth && !token) {
    // 未登录：回到我的页，My.vue 会弹登录框
    next({ path: '/my' })
    return
  }
  next()
})

export default router
