<template>
  <button class="start-button">
    <slot />
  </button>
</template>
  
<script setup lang='ts'>
import { defineProps } from "vue";

interface ButtonProps {
  width: string;
  height: string;
}

defineProps<ButtonProps>();
</script>
  
<style scoped>
.start-button {
  height: v-bind(height);
  width: v-bind(width);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  color: black;
  font-weight: bold;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.start-button:hover {
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
  transform: scale(1.05); /* 鼠标悬停时按钮稍微放大 */
  background-color: #f0f0f0; /* 悬停时按钮背景色稍微改变 */
}

.start-button:active {
  transform: scale(0.95); /* 点击时按钮稍微缩小 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 点击时阴影效果减少 */
  background-color: #e0e0e0; /* 点击时背景色更暗 */
}
</style>
