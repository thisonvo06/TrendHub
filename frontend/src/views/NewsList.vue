<template>
  <div>
    <van-nav-bar :title="title" left-arrow @click-left="onClickLeft" />
    
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <van-cell
          v-for="item in list"
          :key="item.id"
          clickable
          @click="goDetail(item)"
        >
          <template #title>
            <div class="news-title">{{ item.title }}</div>
          </template>
          <template #label>
            <div class="news-meta">
              <span>{{ item.author }}</span>
              <span>{{ formatTime(item.publish_time) }}</span>
              <span>浏览 {{ item.views }}</span>
            </div>
          </template>
          <template #right-icon>
            <img v-if="item.image" :src="item.image" class="news-image" />
          </template>
        </van-cell>
      </van-list>
    </van-pull-refresh>
    
    <van-empty v-if="!loading && list.length === 0" description="暂无新闻" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const categoryId = computed(() => Number(route.params.categoryId))
const title = ref('新闻列表')
const list = ref([])
const page = ref(1)
const pageSize = 10
const total = ref(0)
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)

function formatTime(time) {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')} ${String(date.getHours()).padStart(2,'0')}:${String(date.getMinutes()).padStart(2,'0')}`
}

async function fetchData(isRefresh = false) {
  try {
    const res = await axios.get('/api/news/list', {
      params: {
        categoryId: categoryId.value,
        page: page.value,
        pageSize
      }
    })
    if (res.data.code === 200) {
      const data = res.data.data
      if (isRefresh) {
        list.value = data.list
      } else {
        list.value.push(...data.list)
      }
      total.value = data.total
      if (!data.hasMore) {
        finished.value = true
      }
    } else {
      showToast(res.data.message || '加载失败')
    }
  } catch (err) {
    showToast('加载失败，请检查后端')
    console.error(err)
  }
}

async function onLoad() {
  if (refreshing.value) {
    page.value = 1
    finished.value = false
  }
  await fetchData(refreshing.value)
  loading.value = false
  refreshing.value = false
}

async function onRefresh() {
  loading.value = true
  page.value = 1
  finished.value = false
  list.value = []
  await fetchData(true)
  loading.value = false
  refreshing.value = false
}

function onClickLeft() {
  router.back()
}

function goDetail(item) {
  router.push({
    name: 'NewsDetail',
    params: { id: item.id }
  })
}

onMounted(async () => {
  // 先获取分类名称作为标题
  try {
    const res = await axios.get('/api/news/categories')
    if (res.data.code === 200) {
      const cat = res.data.data.find(c => c.id === categoryId.value)
      if (cat) title.value = cat.name
    }
  } catch (e) {}
  // 加载第一页
  loading.value = true
  await fetchData(true)
  loading.value = false
})
</script>

<style scoped>
.news-title {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.news-meta {
  font-size: 12px;
  color: #969799;
  display: flex;
  gap: 10px;
}
.news-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}
</style>
