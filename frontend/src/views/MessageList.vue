<template>
  <div class="message-page">
    <van-nav-bar title="消息通知" left-arrow @click-left="onBack" />

    <van-empty description="暂无消息通知" />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function onBack() {
  if (window.history.length > 1) router.back()
  else router.replace('/my')
}
</script>

<style scoped>
.message-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
}
</style>
