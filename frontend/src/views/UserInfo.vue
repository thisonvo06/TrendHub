<template>
  <div class="user-info-page">
    <van-nav-bar title="用户信息" left-arrow @click-left="onBack" />

    <!-- 页面进入时加载动画 -->
    <van-loading v-if="loading" class="page-loading" />

    <template v-else-if="userInfo">
      <!-- 顶部头像区 -->
      <div class="profile-card">
        <img class="avatar" :src="userInfo.avatar || defaultAvatar" alt="头像" />
        <div class="names">
          <div class="username">{{ userInfo.username }}</div>
          <div class="nickname" v-if="userInfo.nickname">
            昵称：{{ userInfo.nickname }}
          </div>
        </div>
      </div>

      <!-- 信息条目 -->
      <van-cell-group inset class="info-group">
        <van-cell title="用户 ID" :value="userInfo.id" />
        <van-cell title="用户名" :value="userInfo.username" />
        <van-cell title="昵称" :value="userInfo.nickname || '暂无'" />
        <van-cell title="性别">
          <template #value>
            {{ genderText(userInfo.gender) }}
          </template>
        </van-cell>
        <van-cell title="简介" is-link @click="openEditBio" :value="userInfo.bio || '暂无'" />
        <van-cell title="头像">
          <template #value>
            <van-image
              round
              width="32"
              height="32"
              :src="userInfo.avatar || defaultAvatar"
            />
          </template>
        </van-cell>
      </van-cell-group>

      <!-- 账户操作（修改密码 入口） -->
      <van-cell-group inset class="info-group">
        <van-cell
          title="修改密码"
          is-link
          @click="openChangePassword"
        />
      </van-cell-group>

      <!-- 编辑简介弹窗 -->
      <van-dialog
        v-model:show="showBioDialog"
        title="修改个人简介"
        :before-close="onBioDialogClose"
      >
        <div class="bio-dialog-content">
          <div class="bio-label">个人简介：</div>
          <van-field
            v-model="bioDraft"
            type="textarea"
            autosize
            :maxlength="500"
            show-word-limit
            placeholder="请输入个人简介"
          />
        </div>
        <template #footer>
          <van-button class="dialog-btn" @click="showBioDialog = false">
            取消
          </van-button>
          <van-button
            type="primary"
            class="dialog-btn"
            :loading="bioSaving"
            @click="confirmBio"
          >
            确认
          </van-button>
        </template>
      </van-dialog>

      <!-- 修改密码弹窗 -->
      <van-dialog
        v-model:show="showPwdDialog"
        title="修改密码"
        :before-close="onPwdDialogClose"
      >
        <div class="pwd-dialog-content">
          <van-field
            v-model="pwdForm.oldPassword"
            type="password"
            label="旧密码"
            placeholder="请输入原密码"
            :rules="[{ required: true, message: '请输入原密码' }]"
          />
          <van-field
            v-model="pwdForm.newPassword"
            type="password"
            label="新密码"
            placeholder="请输入新密码（6-20位）"
            :rules="[
              { required: true, message: '请输入新密码' },
              { pattern: /^.{6,20}$/, message: '密码长度需 6-20 位' }
            ]"
          />
          <van-field
            v-model="pwdForm.confirmPassword"
            type="password"
            label="确认新密码"
            placeholder="请再次输入新密码"
            :rules="[{ required: true, message: '请再次输入新密码' }]"
          />
        </div>
        <template #footer>
          <van-button class="dialog-btn" @click="showPwdDialog = false">
            取消
          </van-button>
          <van-button
            type="primary"
            class="dialog-btn"
            :loading="pwdSaving"
            @click="confirmChangePassword"
          >
            确认
          </van-button>
        </template>
      </van-dialog>

      <!-- 调试区（显示接口返回的原始 JSON） -->
      <div class="raw-section">
        <div class="raw-title">接口返回原始数据（GET /api/user/info）</div>
        <pre class="raw-json">{{ formattedJson }}</pre>
      </div>
    </template>

    <div v-else class="empty-tip">未获取到用户信息</div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const defaultAvatar = 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'

const loading = ref(true)
const userInfo = ref(null)

// 编辑简介弹窗状态
const showBioDialog = ref(false)
const bioDraft = ref('')
const bioSaving = ref(false)

// 修改密码弹窗状态
const showPwdDialog = ref(false)
const pwdSaving = ref(false)
const pwdForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

function resetPwdForm() {
  pwdForm.oldPassword = ''
  pwdForm.newPassword = ''
  pwdForm.confirmPassword = ''
}

function openChangePassword() {
  resetPwdForm()
  showPwdDialog.value = true
}

function onPwdDialogClose(action, done) {
  done()
}

async function confirmChangePassword() {
  // 前端基本校验
  if (!pwdForm.oldPassword) {
    showToast('请输入原密码')
    return
  }
  if (!pwdForm.newPassword || pwdForm.newPassword.length < 6 || pwdForm.newPassword.length > 20) {
    showToast('新密码 6-20 位')
    return
  }
  if (pwdForm.newPassword !== pwdForm.confirmPassword) {
    showToast('两次输入的新密码不一致')
    return
  }
  if (pwdForm.newPassword === pwdForm.oldPassword) {
    showToast('新密码不能与旧密码相同')
    return
  }
  pwdSaving.value = true
  try {
    // 按 API 文档规范使用 camelCase 字段名
    await userStore.changePassword({
      oldPassword: pwdForm.oldPassword,
      newPassword: pwdForm.newPassword
    })
    showToast('修改密码成功')
    showPwdDialog.value = false
  } catch (e) {
    // 拦截器已处理通用错误；旧密码不通过也会报错
  } finally {
    pwdSaving.value = false
  }
}

function openEditBio() {
  bioDraft.value = userInfo.value?.bio || ''
  showBioDialog.value = true
}

// Dialog 关闭前的处理（确认/取消）
function onBioDialogClose(action, done) {
  // action: 'confirm' | 'cancel'
  done()
}

async function confirmBio() {
  bioSaving.value = true
  try {
    // 调用 PUT /api/user/update 更新简介
    await userStore.updateUserInfo({ bio: bioDraft.value })
    // 本地更新 userInfo 展示
    userInfo.value = { ...userInfo.value, bio: bioDraft.value }
    showToast('简介已更新')
    showBioDialog.value = false
  } catch (e) {
    // request 拦截器已处理错误提示
  } finally {
    bioSaving.value = false
  }
}

function genderText(g) {
  if (!g || g === 'unknown') return '未知'
  if (g === 'male') return '男'
  if (g === 'female') return '女'
  return g
}

const formattedJson = computed(() =>
  JSON.stringify(userInfo.value, null, 2)
)

function onBack() {
  // 回到上一页（/my）
  if (window.history.length > 1) {
    router.back()
  } else {
    router.replace('/my')
  }
}

onMounted(async () => {
  // 没 token 直接回 /my
  if (!userStore.token) {
    showToast('请先登录')
    router.replace('/my')
    return
  }
  loading.value = true
  try {
    // 调用后端 GET /api/user/info
    await userStore.fetchUserInfo()
    userInfo.value = { ...userStore.userInfo }
  } catch (e) {
    // request 拦截器已经 toast 过，401 会清 token 回 /my
    if (!userStore.token) {
      router.replace('/my')
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.user-info-page {
  min-height: 100vh;
  background-color: var(--background-color, #f7f8fa);
  padding-bottom: 24px;
}

.page-loading {
  display: block;
  margin: 80px auto 0;
}

.profile-card {
  display: flex;
  align-items: center;
  margin: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #1989fa 0%, #50a9ff 100%);
  border-radius: 12px;
  color: #fff;
  box-shadow: 0 4px 12px rgba(25, 137, 250, 0.25);
}

.avatar {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.4);
  flex-shrink: 0;
}

.names {
  margin-left: 16px;
  flex: 1;
  overflow: hidden;
}

.username {
  font-size: 20px;
  font-weight: 600;
}

.nickname {
  margin-top: 6px;
  font-size: 13px;
  opacity: 0.85;
}

.info-group {
  margin-top: 8px;
}

.empty-tip {
  text-align: center;
  color: #999;
  padding: 60px 0;
}

.raw-section {
  margin: 16px;
  padding: 12px 14px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.raw-title {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.raw-json {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  font-family: Consolas, Monaco, 'Courier New', monospace;
  color: #333;
  background: #f7f8fa;
  padding: 10px 12px;
  border-radius: 6px;
  white-space: pre-wrap;
  word-break: break-all;
}

/* 编辑简介弹窗样式 */
.bio-dialog-content {
  padding: 16px 16px 0;
}

.bio-label {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 500;
}

/* 修改密码弹窗样式 */
.pwd-dialog-content {
  padding: 16px 16px 0;
}

.dialog-btn {
  width: 40%;
  margin: 0 4%;
}
</style>
