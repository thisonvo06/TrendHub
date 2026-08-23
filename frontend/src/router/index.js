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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：设置页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

export default router
