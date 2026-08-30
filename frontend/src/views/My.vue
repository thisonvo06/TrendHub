<template>
  <div class="my-page">
    <!-- 顶部导航栏 -->
    <van-nav-bar title="我的" />

    <!-- 用户信息卡片（蓝色部分，点击查询用户信息） -->
    <div class="user-card" @click="handleCardClick">
      <img
        class="avatar"
        :src="userStore.userInfo?.avatar || defaultAvatar"
        alt="avatar"
      />
      <div class="user-info">
        <div class="username">
          {{ userStore.userInfo?.nickname || userStore.userInfo?.username || '未登录' }}
        </div>
        <div class="bio">
          {{ userStore.userInfo?.bio || '这个人很懒，什么都没留下' }}
        </div>
      </div>
      <van-icon name="arrow" class="arrow-icon" />
    </div>

    <!-- 未登录遮罩：点击用户卡片弹出登录/注册弹窗 -->
    <van-popup
      v-model:show="showAuth"
      position="bottom"
      round
      :style="{ height: '60%' }"
    >
      <van-tabs v-model:active="authTab" sticky>
        <van-tab title="登录">
          <van-form class="auth-form" @submit="onLogin">
            <van-field
              v-model="loginForm.username"
              label="用户名"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请输入用户名' }]"
            />
            <van-field
              v-model="loginForm.password"
              type="password"
              label="密码"
              placeholder="请输入密码"
              :rules="[{ required: true, message: '请输入密码' }]"
            />
            <div class="form-actions">
              <van-button type="primary" native-type="submit" :loading="loading">
                登录
              </van-button>
            </div>
          </van-form>
        </van-tab>
        <van-tab title="注册">
          <van-form class="auth-form" @submit="onRegister">
            <van-field
              v-model="registerForm.username"
              label="用户名"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请输入用户名' }]"
            />
            <van-field
              v-model="registerForm.password"
              type="password"
              label="密码"
              placeholder="请输入密码（6-20位）"
              :rules="[
                { required: true, message: '请输入密码' },
                { min: 6, max: 20, message: '密码长度为6-20位' }
              ]"
            />
            <div class="form-actions">
              <van-button type="primary" native-type="submit" :loading="loading">
                注册并登录
              </van-button>
            </div>
          </van-form>
        </van-tab>
      </van-tabs>
    </van-popup>

    <!-- 功能菜单 -->
    <van-cell-group inset class="menu-group">
      <van-cell title="我的收藏" is-link icon="star-o" @click="router.push('/favorite/list')" />
      <van-cell title="浏览历史" is-link icon="clock-o" @click="router.push('/history/list')" />
      <van-cell title="消息通知" is-link icon="bell-o" @click="router.push('/message/list')" />
      <van-cell title="设置" is-link icon="setting-o" @click="router.push('/settings')" />
    </van-cell-group>

    <van-cell-group inset class="menu-group" v-if="userStore.token">
      <van-cell title="退出登录" center>
        <template #title>
          <span class="logout-text" @click="onLogout">退出登录</span>
        </template>
      </van-cell>
    </van-cell-group>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()

const defaultAvatar = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const showAuth = ref(false)
const authTab = ref(0)
const loading = ref(false)

const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', password: '' })

// 点击蓝色用户卡片：没登录弹登录框；已登录则跳转至"用户信息详情"页
// 详情页 onMounted 中调用 GET /api/user/info
function handleCardClick() {
  if (!userStore.token) {
    showAuth.value = true
    return
  }
  router.push('/user/info')
}

async function onLogin() {
  loading.value = true
  try {
    await userStore.doLogin({ ...loginForm })
    showToast('登录成功')
    showAuth.value = false
  } catch (e) {
    // 错误已在 request 拦截器处理
  } finally {
    loading.value = false
  }
}

async function onRegister() {
  loading.value = true
  try {
    await userStore.doRegister({ ...registerForm })
    showToast('注册成功')
    showAuth.value = false
  } catch (e) {
    // 错误已在 request 拦截器处理
  } finally {
    loading.value = false
  }
}

async function onLogout() {
  try {
    await showConfirmDialog({
      title: '提示',
      message: '确定退出登录吗？'
    })
    userStore.logout()
    showToast('已退出登录')
  } catch (e) {
    // 取消
  }
}
</script>

<style scoped>
.my-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 24px;
}

/* 蓝色用户卡片 */
.user-card {
  display: flex;
  align-items: center;
  margin: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #1989fa 0%, #50a9ff 100%);
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(25, 137, 250, 0.25);
  position: relative;
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.4);
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  margin-left: 16px;
  overflow: hidden;
}

.username {
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bio {
  margin-top: 6px;
  font-size: 13px;
  opacity: 0.85;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.arrow-icon {
  font-size: 16px;
  opacity: 0.85;
  margin-left: 8px;
}

/* 菜单 */
.menu-group {
  margin-top: 16px;
}

.logout-text {
  color: #ee0a24;
  display: block;
  width: 100%;
  text-align: center;
}

.auth-form {
  padding: 16px 0;
}

.form-actions {
  padding: 16px;
}
</style>
