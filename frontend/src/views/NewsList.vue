<template>
  <div class="news-list-page">
    <van-nav-bar :title="title" left-arrow @click-left="onClickLeft" />

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="listLoading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <van-card
          v-for="item in list"
          :key="item.id"
          class="news-card"
          :thumb="item.image"
          :title="item.title"
          :desc="item.description"
          @click="goDetail(item)"
        >
          <template #footer>
            <div class="news-meta">
              <span>{{ item.author || '匿名' }}</span>
              <span>{{ formatTime(item.publish_time || item.publishTime) }}</span>
              <span>浏览 {{ item.views || 0 }}</span>
            </div>
          </template>
        </van-card>
      </van-list>
    </van-pull-refresh>

    <van-empty v-if="!listLoading && list.length === 0" description="暂无新闻" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../stores/news'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()

const categoryId = computed(() => Number(route.params.categoryId))

const title = computed(() => {
  if (newsStore.currentCategoryName) return newsStore.currentCategoryName
  // 尝试从 categories 中找
  const hit = newsStore.categories.find((c) => c.id === categoryId.value)
  return hit ? hit.name : '新闻列表'
})

const list = computed(() => newsStore.list)
const listLoading = computed(() => newsStore.listLoading)
const refreshing = computed({
  get: () => newsStore.listRefreshing,
  set: (v) => (newsStore.listRefreshing = v)
})
const finished = computed(() => !newsStore.hasMore && list.value.length > 0)

function formatTime(time) {
  if (!time) return ''
  const date = new Date(time)
  if (isNaN(date.getTime())) return ''
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const mm = String(date.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${d} ${hh}:${mm}`
}

async function onLoad() {
  await newsStore.fetchNewsList()
}

async function onRefresh() {
  await newsStore.refreshNewsList()
}

function onClickLeft() {
  router.back()
}

function goDetail(item) {
  router.push({ name: 'NewsDetail', params: { id: item.id } })
}

// categoryId 变化（比如从分类页切到另一个分类）时重新拉
watch(
  categoryId,
  (newId) => {
    if (!newId) return
    newsStore.setCurrentCategory(newId)
    newsStore.refreshNewsList()
  },
  { flush: 'post' }
)

onMounted(async () => {
  // 设置当前分类 id / name
  if (newsStore.currentCategoryId !== categoryId.value) {
    // 从 categories 里找对应 name
    const name = newsStore.categories.find((c) => c.id === categoryId.value)?.name || ''
    newsStore.setCurrentCategory(categoryId.value, name)
  }
  // 如果分类列表还没拉，先拉一次（为了标题）
  if (newsStore.categories.length === 0) {
    try {
      await newsStore.fetchCategories()
    } catch (e) {}
  }
  // 第一页
  await newsStore.refreshNewsList()
})
</script>

<style scoped>
.news-list-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 60px;
}

.news-card {
  margin: 12px;
}

.news-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #969799;
  align-items: center;
}
</style>
