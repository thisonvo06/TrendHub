<template>
  <div class="history-page">
    <van-nav-bar title="浏览历史" left-arrow @click-left="onBack" />

    <div class="top-bar" v-if="total > 0 || list.length > 0">
      <div class="total-tip">共 {{ total }} 条记录</div>
      <van-button size="small" type="danger" plain @click="onClearAll" :loading="actionLoading">
        清空
      </van-button>
    </div>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="listLoading"
        :finished="finished"
        finished-text="— 没有更多了 —"
        @load="onLoad"
      >
        <van-swipe-cell
          v-for="item in list"
          :key="item.history_id || item.id"
        >
          <template #left>
            <van-button
              square
              type="danger"
              @click="onDelete(item)"
            >
              删除
            </van-button>
          </template>

          <van-cell-group inset>
            <van-cell clickable @click="goDetail(item)">
              <template #title>
                <div class="card-title">{{ item.title }}</div>
              </template>
              <template #label>
                <div class="card-meta">
                  <span>{{ item.author || '匿名' }}</span>
                  <span>
                    {{ formatTime(item.viewTime || item.publishTime || item.publish_time) }}
                  </span>
                  <span>浏览 {{ item.views || 0 }}</span>
                </div>
              </template>
              <template #right-icon>
                <img v-if="item.image" :src="item.image" class="thumb" />
              </template>
            </van-cell>
          </van-cell-group>

          <template #right>
            <van-button
              square
              type="danger"
              @click="onDelete(item)"
            >
              删除
            </van-button>
          </template>
        </van-swipe-cell>
      </van-list>
    </van-pull-refresh>

    <van-empty v-if="!listLoading && list.length === 0" description="暂无浏览记录" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import { useHistoryStore } from '../stores/history'

const router = useRouter()
const historyStore = useHistoryStore()

const list = computed(() => historyStore.list)
const total = computed(() => historyStore.total)
const listLoading = computed(() => historyStore.listLoading)
const actionLoading = computed(() => historyStore.actionLoading)
const refreshing = computed({
  get: () => historyStore.listRefreshing,
  set: (v) => (historyStore.listRefreshing = v)
})
const finished = computed(() => !historyStore.hasMore && list.value.length > 0)

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
  // 历史记录中如果有 newsId 就用 newsId，否则退化成 id
  router.push({ name: 'NewsDetail', params: { id: item.newsId || item.id } })
}

async function onDelete(item) {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定删除这条浏览记录吗？'
    })
    const historyId = item.history_id || item.id
    await historyStore.remove(historyId)
    showToast('已删除')
  } catch (e) {}
}

async function onClearAll() {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定清空所有浏览历史？'
    })
    await historyStore.clearAll()
    showToast('已清空浏览历史')
  } catch (e) {}
}

async function onLoad() {
  await historyStore.fetchList()
}

async function onRefresh() {
  await historyStore.refreshList()
}

onMounted(() => {
  return historyStore.refreshList()
})
</script>

<style scoped>
.history-page {
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

.card-title {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #969799;
  margin-top: 4px;
}

.thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-left: 10px;
}
</style>
