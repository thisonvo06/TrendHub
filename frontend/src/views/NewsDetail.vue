<template>
  <div class="news-detail-page">
    <van-nav-bar title="新闻详情" left-arrow @click-left="onClickLeft" safe-area-inset-bottom="false">
      <!-- 右上角收藏按钮 -->
      <template #right>
        <van-icon
          :name="isFavorited ? 'star' : 'star-o'"
          :color="isFavorited ? '#07c160' : undefined"
          size="20"
          @click="onToggleFavorite"
        />
      </template>
    </van-nav-bar>

    <van-loading v-if="loading" class="page-loading" />

    <div v-else-if="detail" class="detail">
      <h1 class="title">{{ detail.title }}</h1>
      <div class="meta">
        <span>{{ detail.author || '匿名' }}</span>
        <span>{{ formatTime(detail.publishTime || detail.publish_time) }}</span>
        <span>浏览 {{ detail.views || 0 }}</span>
      </div>
      <img v-if="detail.image" :src="detail.image" class="cover" />
      <div class="content" v-html="detail.content"></div>

      <!-- 相关推荐 -->
      <div v-if="detail.relatedNews && detail.relatedNews.length > 0" class="related">
        <h3>相关推荐</h3>
        <van-cell
          v-for="news in detail.relatedNews"
          :key="news.id"
          clickable
          @click="goDetail(news)"
        >
          <template #title>{{ news.title }}</template>
          <template #right-icon>
            <span class="views">{{ news.views || 0 }} 浏览</span>
          </template>
        </van-cell>
      </div>
    </div>

    <van-empty v-else description="新闻不存在" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useNewsStore } from '../stores/news'
import { useFavoriteStore } from '../stores/favorite'
import { useHistoryStore } from '../stores/history'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const favoriteStore = useFavoriteStore()
const historyStore = useHistoryStore()
const userStore = useUserStore()

const newsId = computed(() => Number(route.params.id))

const detail = computed(() => newsStore.detail)
const loading = computed(() => newsStore.detailLoading)
const isFavorited = ref(false)

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

async function refreshFavorite() {
  if (!userStore.token) {
    isFavorited.value = false
    return
  }
  try {
    isFavorited.value = await favoriteStore.check(newsId.value)
  } catch (e) {}
}

async function onToggleFavorite() {
  if (!userStore.token) {
    showToast('请先登录')
    return
  }
  const current = isFavorited.value
  try {
    await favoriteStore.toggle(newsId.value, current)
    isFavorited.value = !current
    showToast(current ? '已取消收藏' : '收藏成功')
  } catch (e) {
    // 拦截器已提示
  }
}

async function addHistory() {
  if (!userStore.token) return
  try {
    await historyStore.add(newsId.value)
  } catch (e) {
    // 失败不影响阅读
  }
}

function onClickLeft() {
  router.back()
}

function goDetail(news) {
  router.push({ name: 'NewsDetail', params: { id: news.id } })
}

watch(
  newsId,
  (newId) => {
    if (!newId) return
    loadDetail()
  }
)

async function loadDetail() {
  try {
    await newsStore.fetchNewsDetail(newsId.value)
    // 同时拉收藏状态 + 写浏览历史
    await Promise.all([refreshFavorite(), addHistory()])
  } catch (e) {}
}

onMounted(loadDetail)
</script>

<style scoped>
.news-detail-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 60px;
}

.page-loading {
  display: block;
  margin: 80px auto 0;
}

.detail {
  padding: 16px;
  background: #fff;
}

.title {
  font-size: 20px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 12px;
}

.meta {
  font-size: 13px;
  color: #969799;
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebedf0;
}

.cover {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.content {
  font-size: 15px;
  line-height: 1.7;
  color: #333;
  word-break: break-all;
}

.content :deep(p) {
  margin-bottom: 12px;
}

.related {
  margin-top: 30px;
  padding-top: 16px;
  border-top: 1px solid #ebedf0;
  background: #fff;
}

.related h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.views {
  font-size: 12px;
  color: #969799;
}
</style>
