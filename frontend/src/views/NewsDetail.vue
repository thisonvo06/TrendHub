<template>
  <div>
    <van-nav-bar title="新闻详情" left-arrow @click-left="onClickLeft" />
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="detail" class="detail">
      <h1 class="title">{{ detail.title }}</h1>
      <div class="meta">
        <span>{{ detail.author }}</span>
        <span>{{ detail.publishTime }}</span>
        <span>浏览 {{ detail.views }}</span>
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
            <span class="views">{{ news.views }} 浏览</span>
          </template>
        </van-cell>
      </div>
    </div>
    
    <van-empty v-else description="新闻不存在" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const detail = ref(null)
const loading = ref(true)

async function fetchDetail() {
  try {
    const res = await axios.get('/api/news/detail', {
      params: { id: route.params.id }
    })
    if (res.data.code === 200) {
      detail.value = res.data.data
    } else {
      showToast(res.data.message || '加载失败')
    }
  } catch (err) {
    showToast('加载失败，请检查后端')
    console.error(err)
  } finally {
    loading.value = false
  }
}

function onClickLeft() {
  router.back()
}

function goDetail(news) {
  router.push({
    name: 'NewsDetail',
    params: { id: news.id }
  })
}

onMounted(fetchDetail)
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 40px;
  color: #969799;
}
.detail {
  padding: 16px;
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
