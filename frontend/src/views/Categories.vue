<template>
  <div class="categories-page">
    <van-nav-bar title="全部分类" left-arrow @click-left="onClickLeft" />
    <div class="category">
      <van-loading v-if="loading" class="page-loading" />
      <van-grid v-else :column-num="3" :border="false">
        <van-grid-item
          v-for="item in categories"
          :key="item.id"
          :text="item.name"
          icon="newspaper-o"
          @click="onSelect(item)"
        />
      </van-grid>
      <van-empty v-if="!loading && categories.length === 0" description="暂无分类数据" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { useNewsStore } from '../stores/news'

const router = useRouter()
const newsStore = useNewsStore()

const loading = computed(() => newsStore.categories.length === 0)

const categories = computed(() => newsStore.categories)

onMounted(async () => {
  try {
    await newsStore.fetchCategories({ skip: 0, limit: 100 })
  } catch (err) {
    showToast('加载失败，请稍后重试')
    console.error(err)
  }
})

function onClickLeft() {
  // 首页无返回
  showToast('已在首页')
}

function onSelect(item) {
  newsStore.setCurrentCategory(item.id, item.name)
  router.push({
    name: 'NewsList',
    params: { categoryId: item.id }
  })
}
</script>

<style scoped>
.categories-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 60px;
}

.category {
  padding: 16px;
}

.page-loading {
  display: block;
  margin: 80px auto 0;
}
</style>
