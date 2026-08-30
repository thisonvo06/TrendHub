<template>
  <div class="favorite-page">
    <van-nav-bar title="我的收藏" left-arrow @click-left="onBack" />

    <!-- 顶部：数量 + 清空按钮 -->
    <div class="top-bar" v-if="total > 0 || list.length > 0">
      <div class="total-tip">共 {{ total }} 条收藏</div>
      <van-button size="small" type="danger" plain @click="onClearAll" :loading="actionLoading">
        清空全部
      </van-button>
    </div>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="listLoading"
        :finished="finished"
        finished-text="— 没有更多了 —"
        @load="onLoad"
      >
        <van-card
          v-for="item in list"
          :key="item.id"
          class="news-card"
          :thumb="item.image"
          :title="item.title"
          :desc="item.description || item.favoriteTime"
          @click="goDetail(item)"
        >
          <template #footer>
            <div class="card-meta">
              <span>{{ item.author || '匿名' }}</span>
              <span>
                {{ formatTime(item.publishTime || item.publish_time || item.favoriteTime) }}
              </span>
              <span>浏览 {{ item.views || 0 }}</span>
              <van-button size="mini" type="default" plain @click.stop="onRemove(item)">
                取消收藏
              </van-button>
            </div>
          </template>
        </van-card>
      </van-list>
    </van-pull-refresh>

    <van-empty v-if="!listLoading && list.length === 0" description="还没有收藏任何内容" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import { useFavoriteStore } from '../stores/favorite'

const router = useRouter()
const favoriteStore = useFavoriteStore()

const list = computed(() => favoriteStore.list)
const total = computed(() => favoriteStore.total)
const listLoading = computed(() => favoriteStore.listLoading)
const actionLoading = computed(() => favoriteStore.actionLoading)
const refreshing = computed({
  get: () => favoriteStore.listRefreshing,
  set: (v) => (favoriteStore.listRefreshing = v)
})
const finished = computed(() => !favoriteStore.hasMore && list.value.length > 0)

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

function onBack() {
  if (window.history.length > 1) router.back()
  else router.replace('/my')
}

function goDetail(item) {
  router.push({ name: 'NewsDetail', params: { id: item.newsId || item.id } })
}

async function onRemove(item) {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定要取消收藏这条新闻吗？'
    })
    // 后端接口 favorite/remove 需要 newsId；如果列表里没有 newsId 字段，就用 id 兜底
    const newsId = item.newsId || item.id
    await favoriteStore.remove(newsId)
    showToast('已取消收藏')
  } catch (e) {
    // 用户取消 confirm 或 API 出错都不继续
  }
}

async function onClearAll() {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定要清空所有收藏吗？此操作不可撤销。'
    })
    await favoriteStore.clearAll()
    showToast('已清空收藏')
  } catch (e) {}
}

async function onLoad() {
  await favoriteStore.fetchList()
}

async function onRefresh() {
  await favoriteStore.refreshList()
}

onMounted(() => {
  return favoriteStore.refreshList()
})
</script>

<style scoped>
.favorite-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 60px;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
}

.total-tip {
  font-size: 13px;
  color: #969799;
}

.news-card {
  margin: 12px;
}

.card-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: #969799;
}
</style>
