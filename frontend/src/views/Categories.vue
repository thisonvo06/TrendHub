<template>
  <div>
    <van-nav-bar title="全部分类" left-arrow @click-left="onClickLeft" />
    <div class="category">
      <van-grid :column-num="3" :border="false">
        <van-grid-item
          v-for="item in categories"
          :key="item.id"
          :text="item.name"
          @click="onSelect(item)"
        />
      </van-grid>
      <div v-if="loading" class="loading">加载中...</div>
      <van-empty v-else-if="categories.length === 0" description="暂无分类数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import axios from 'axios'

const router = useRouter()
const categories = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('/api/news/categories')
    if (res.data.code === 200) {
      categories.value = res.data.data
    } else {
      showToast(res.data.message || '加载失败')
    }
  } catch (err) {
    showToast('网络错误，请检查后端是否启动')
    console.error(err)
  } finally {
    loading.value = false
  }
})

function onClickLeft() {
  // 首页无返回，提示即可
  showToast('已在首页')
}

function onSelect(item) {
  // 跳转到新闻列表页
  router.push({
    name: 'NewsList',
    params: { categoryId: item.id }
  })
}
</script>

<style scoped>
.category {
  padding: 10px;
}
.loading {
  text-align: center;
  padding: 40px;
  color: #969799;
}
</style>
