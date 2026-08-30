<template>
  <div class="settings-page">
    <van-nav-bar title="设置" left-arrow @click-left="onBack" />

    <van-cell-group inset class="group">
      <van-cell title="个人资料" is-link @click="router.push('/user/info')" />
      <van-cell title="修改密码" is-link @click="router.push('/user/info')">
        <template #value>
          <span class="tip">进入用户信息页修改</span>
        </template>
      </van-cell>
    </van-cell-group>

    <van-cell-group inset class="group" title="通用">
      <van-cell title="清除缓存" is-link value="0.0MB" @click="onClearCache" />
    </van-cell-group>

    <van-cell-group inset class="group" title="关于">
      <van-cell title="版本号" value="v1.0.0" />
      <van-cell title="技术栈" value="FastAPI + Vue 3 + Vant" />
    </van-cell-group>

    <div class="footer">
      <van-button block type="danger" plain @click="onLogout" v-if="userStore.token">
        退出登录
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { showConfirmDialog, showToast } from 'vant'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

function onBack() {
  if (window.history.length > 1) router.back()
  else router.replace('/my')
}

function onClearCache() {
  showToast('缓存已清理')
}

async function onLogout() {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定退出登录吗？'
    })
    userStore.logout()
    showToast('已退出登录')
    router.replace('/my')
  } catch (e) {}
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 60px;
}

.group {
  margin-top: 12px;
}

.tip {
  color: #969799;
  font-size: 13px;
}

.footer {
  margin-top: 40px;
  padding: 0 16px;
}
</style>
