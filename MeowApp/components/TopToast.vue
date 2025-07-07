<template>
  <view v-if="visible" :class="['toast', type]">
    {{ message }}
  </view>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const type = ref('success') // success or error

function showToast(msg, toastType = 'success', duration = 2000) {
  message.value = msg
  type.value = toastType
  visible.value = true
  setTimeout(() => {
    visible.value = false
  }, duration)
}

// 暴露方法
defineExpose({ showToast })
</script>

<style scoped>
.toast {
  position: fixed;
  top: 10rpx;               /* 紧贴屏幕顶部 */
  left: 0;
  width: 100%;
  padding: 20rpx;        
  font-size: 28rpx;
  text-align: center;
  z-index: 9999;
  color: #fff;
}
.success {
  background-color: #4caf50; /* 绿色 */
}
.error {
  background-color: #f44336; /* 红色 */
}
</style>