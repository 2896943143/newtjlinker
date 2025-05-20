<template>
  <div class="page-container no-scroll">
    
    <div class="content-container">
      <div style="margin-bottom: 120px; margin-top: -50px; justify-content: center; align-items: center; display: flex;">
      <!-- <div style="margin-bottom: 80px; justify-content: center; align-items: center; display: flex;"> -->
        <img src="/Logos/Icon.png" style="width: 150px; border-radius: 30px;" alt="Icon">
        <img src="/Logos/Logo.png" style="width: 600px;" alt="Logo">
      </div>

      <div class="drop-down">
        <p class="role-label" style="font-size: 24px; margin-right: 00px; font-weight: 600">请选择登录角色</p>
        <el-select v-model="value" placeholder="身份" size="large" class="select-box" @change="handleSelectChange">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>

      <p v-if="showError" class="error-message">* 请选择登录角色</p>


      <div class="button-container">
        <ShadowButton class="fancy-button" width="221px" height="60px" style="margin-left: 50px" @click="login">
          <p>登录</p>
        </ShadowButton>
        <ShadowButton class="fancy-button" width="221px" height="60px" style="margin-left: 50px" @click="handleRegister">
          <p>注册</p>
        </ShadowButton>
      </div>

      <el-dialog 
        :model-value="dialogVisible" 
        title="提示" 
        @close="dialogVisible = false"
        aria-live="assertive"
        aria-labelledby="dialog-title"
      >
        <span>管理员账号不能注册</span>
      </el-dialog>


      <div ref="container" class="box" @click="handleRandom">
        <span
          :key="childKey"
          ref="child"
          :style="{ color: colorRandom(), left: childLeft, top: childTop }"
          class="minbox"
        >
          {{ msg }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ShadowButton from "@/components/ShadowButton.vue";
import { onMounted, onBeforeUnmount } from "vue";

onMounted(() => {
  // 禁用页面滚动
  document.body.style.overflow = 'hidden'; 
  document.documentElement.style.overflow = 'hidden'; // 确保 HTML 也不滚动
  window.scrollTo(0, 0);
});

onBeforeUnmount(() => {
  // 恢复页面滚动
  document.body.style.overflow = ''; 
  document.documentElement.style.overflow = ''; // 恢复 HTML 滚动
});

const router = useRouter();

// 第一个模板的逻辑
const container = ref(null);
const child = ref(null);
const childKey = ref(0);

const colorRandom = () => {
  let color;
  do {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    color = `rgb(${r},${g},${b})`;
  } while (color === "rgb(250,235,215)");
  return color;
};

const textArr = [
  "😒",
  "💕😁😊😂🤣❤️😍👌😘🙌👍😎😉🎶💖😜😀😁😃😄😅😆😂🤣😉😊😋😎😍😘🥰😗😙🥲😚☺️🙂🤗🤩🤔🫡🤨😯🤐🫠🤡🥳🥺🥹🧐🧐👻🤖🤖",
  "💕",
  "😁",
  "😊",
  "😂",
  "🤣",
  "❤️",
  "😍",
  "👌",
  "😘",
  "🙌",
  "👍",
  "😎",
  "😉",
  "🎶",
  "💖",
  "😜",
  "😀",
  "😁",
  "😃",
  "😄",
  "😅",
  "😆",
  "😂",
  "🤣",
  "😉",
  "😊",
  "😋",
  "😎",
  "😍",
  "😘",
  "🥰",
  "😗",
  "😙",
  "🥲",
  "😚",
  "🙂",
  "🤗",
  "🤩",
  "🤔",
  "🫡",
  "🤨",
  "😯",
  "🤐",
  "🫠",
  "🤡",
  "🥳",
  "🥺",
  "🥹",
  "🧐",
  "👻",
  "🤖",
 
];

const randomInd = () => {
  return Math.floor(Math.random() * textArr.length);
};

const msg = ref(null);
const childLeft = ref(0);
const childTop = ref(0);

const handleRandom = (e) => {
  childLeft.value = e.clientX + "px";
  childTop.value = e.clientY + "px";
  msg.value = textArr[randomInd()];
  childKey.value++;
};

// 第二个模板的逻辑
const dialogVisible = ref(false);
const value = ref("");

const options = [
  {
    value: "user",
    label: "用户",
  },
  {
    value: "manager",
    label: "管理员",
  },
];
const showError = ref(false);

// 处理角色选择的变化
const handleSelectChange = () => {
  if (value.value) {
    showError.value = false; // 当选择了角色时，隐藏错误提示
  }
};

const login = () => {
  if (value.value === 'user') {
    router.push('/login/user');
  } else if (value.value === 'manager') {
    router.push('/login/manager');
  } else {
    showError.value = true;

    // 重新触发动画
    const errorEl = document.querySelector('.error-message');
    if (errorEl) {
      errorEl.classList.remove('shake');
      void errorEl.offsetWidth; // 强制重绘
      errorEl.classList.add('shake');
    }
  }
};

const handleRegister = () => {
  if (value.value === "user") {
    router.push("/register");
  } else if (value.value === "manager") {
    dialogVisible.value = true;
  } else {
    router.push("/register");
  }
};

</script>
<style lang="scss" scoped>

.no-scroll {
  overflow: hidden !important; /* 禁用滚动条 */
}

.page-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  // overflow: hidden;
}

.box {
  position: fixed;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  cursor: pointer;
  // background-color: rgb(33, 151, 255);
  // background: linear-gradient(to right, #008cff, #66ccff);
  background: url('/public/Logos/background.jpg') no-repeat center center;
  background-size: cover;
  background-position: center;
  opacity: 0.7;
  filter: blur(1px);
  overflow: hidden;
  z-index: -2; /* 确保背景板在内容下面 */

  /* 白色矩形框 */
  &::before {
    content: '';
    position: absolute;
    top: 51%;  /* 将矩形框垂直居中 */
    left: 50%; /* 将矩形框水平居中 */
    transform: translate(-50%, -50%); /* 通过translate进行偏移，确保居中 */
    width: 55%; /* 宽度为80%，可以根据需要调整 */
    height: 68%; /* 高度为50%，可以根据需要调整 */
    background-color: white;
    z-index: -1; /* 将矩形框置于内容下方 */
    border-radius: 50px; /* 可选，给矩形框添加圆角 */
    opacity: 0.8; /* 设置透明度，提升背景层次 */
  }

  .minbox {
    width: fit-content;
    position: absolute;
    animation: moveAndFadeout 1s ease-in-out forwards;
  }

  @keyframes moveAndFadeout {
    0% {
      transform: translate(0, 0) scale(1) rotate(0deg);
      opacity: 1;
    }
    100% {
      transform: translate(20px, -80px) rotate(180deg) scale(2);
      opacity: 0;
    }
  }
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 8px;
  text-align: center;
}

.shake {
  animation: shake 0.3s;
}

@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  50% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
}

.content-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1; /* 确保内容在背景板上面 */
  overflow: hidden;
}

.drop-down {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 20px;  /* 增加间距，改善元素之间的布局 */
}

.label-text {
  font-size: 24px;
  color: #333;  /* 使用深色字体，增加可读性 */
  margin-right: 20px;  /* 保持合适的间距 */
}

.select-box {
  width: 100px;  /* 调整下拉框的宽度 */
  font-size: 18px;  /* 调整字体大小，保持一致 */
  // font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: #0080ff;  /* 设置背景色，增加视觉层次感 */
  border-radius: 8px;  /* 圆角边框 */
  border: 0px solid #ccc;  /* 边框颜色 */
}

.select-box .el-select__dropdown {
  border-radius: 8px;  /* 下拉框边框圆角 */
  background-color: #fff;  /* 下拉框背景色 */
}

.select-box .el-option {
  font-size: 16px;  /* 下拉选项字体大小 */
}

.button-container {
  display: flex;
  margin-top: 60px;
  justify-content: center;
  align-items: center;
}

.fancy-button {
  --btn-bg: #4facfe;
  --btn-shadow: 0 6px 15px rgba(0, 132, 255, 0.3);
  // --btn-hover-bg: linear-gradient(135deg, #00c6ff, #0072ff);
  --btn-hover-bg: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
  color: white;
  background: var(--btn-bg);
  border: none;
  border-radius: 12px;
  box-shadow: var(--btn-shadow);
  transition: all 0.3s ease;
  cursor: pointer;
}

.fancy-button:hover {
  background: var(--btn-hover-bg);
  box-shadow: 0 8px 20px rgba(0, 115, 230, 0.4);
  transform: translateY(-2px);
}

.fancy-button:active {
  transform: scale(0.98);
  box-shadow: 0 4px 12px rgba(0, 115, 230, 0.2);
}

.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.1); /* 半透明白色背景 */
  backdrop-filter: blur(10px);         /* 背景模糊 */
  -webkit-backdrop-filter: blur(10px); /* 兼容 Safari */
  border-radius: 20px;                 /* 圆角 */
  border: 1px solid rgba(255, 255, 255, 0.3); /* 半透明白色边框 */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); /* 柔和阴影 */
  padding: 30px;
}
</style>