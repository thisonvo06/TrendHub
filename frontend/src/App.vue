<template>
  <div class="app-wrapper">
    <!-- 路由页面（留出底部 tabbar 高度） -->
    <div class="page-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <!-- 底部 Tabbar：首页（分类）/ 我的 -->
    <van-tabbar v-model="active" route>
      <van-tabbar-item to="/" icon="apps-o">分类</van-tabbar-item>
      <van-tabbar-item to="/my" icon="user-o">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const active = ref(0)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-size: 16px;
  background-color: #f7f8fa;
  color: #333;
  height: 100%;
  width: 100%;
}

#app {
  max-width: 750px;
  margin: 0 auto;
  min-height: 100%;
  background-color: #fff;
}

/* 移动端适配 */
@media screen and (max-width: 750px) {
  html {
    font-size: calc(100vw / 750 * 16);
  }
}
</style>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background-color, #f7f8fa);
}

.page-content {
  flex: 1;
  /* 底部 Tabbar 高度 + 安全区，防止内容被 tabbar 遮住 */
  padding-bottom: calc(50px + var(--safe-area-inset-bottom, 0px));
}

/* 页面切换淡入淡出 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

