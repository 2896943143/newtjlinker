<template>
  <div class="page-container" >

    <div class="content-container">
    <div style="margin-bottom: 60px; justify-content: center; align-items: center; display: flex; border-radius: 10px;">
      <ImageButton
        url="/some-page"
        imageSrc="/Logos/Icon.png"
        altText="Example Image"
        borderRadius="15px"
        width="75px"
        height="89px"
        @click="router.push('/welcome')"
      />
      <img src='/Logos/Logo.png' style='width: 300px;' alt='Logo'>
    </div>

    <p class="role-label" style="font-size: 24px; margin-right: 00px; margin-top: -40px; margin-bottom: 40px;  font-weight: 600">用户登录</p>

    <div class="input-wrapper" style="margin-bottom: 10px">
      <div class="input-container">
        <el-icon :size="40"><User /></el-icon>
        <el-input
          v-model="input_id"
          :class="{ 'input-error': inputError.id }"
          style="width: 300px; height: 40px; margin-left: 20px;"
          placeholder="请输入用户名"
        />
      </div>
      <div
        v-if="inputError.id"
        class="error-message"
        :class="{ 'error-message-shake': inputError.id }"
      >
        {{ inputError.idMessage }}
      </div>
    </div>

    <div class="input-wrapper">
      <div class="input-container">
        <el-icon :size="40"><Lock /></el-icon>
        <el-input
          v-model="input_password"
          :class="{ 'input-error': inputError.password }"
          style="width: 300px; height: 40px; margin-left: 20px;"
          placeholder="请输入密码"
          type="password"
          show-password
        />
      </div>
      <div
        v-if="inputError.password"
        class="error-message"
        :class="{ 'error-message-shake': inputError.password }"
      >
        {{ inputError.passwordMessage }}
      </div>
    </div>

    <div class='button-container' style="margin-top: -10px">
      <ShadowButton class="fancy-button" width='300px' height='45px' style='margin-left: 60px' @click="handleLogin">
        <p style='font-size: 24px; margin-right: 10px'>登录</p>
      </ShadowButton>



      <div style="display: flex; justify-content: space-between; margin-left: 60px; width: 82%; margin-top: 15px;">
        <WhiteButton width='100px' height='40px' @click="router.push('/find-password')">
          <p style='font-size: 15px; margin-right: 00px'>忘记密码</p>
        </WhiteButton>
        <WhiteButton width='100px' height='40px' @click="router.push('/welcome')">
          <p style='font-size: 15px; margin-right: 00px'>返回主页</p>
        </WhiteButton>
      </div>
    </div> 


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

<script setup >
import { Lock, User } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
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

const input_id = ref('')
const input_password = ref('')
const router = useRouter()
const inputError = ref({
  id: false,
  password: false,
  idMessage: '',
  passwordMessage: '',
});

const handleLogin = async () => {
  // 重置错误状态
  inputError.value = {
    id: false,
    password: false,
    idMessage: '',
    passwordMessage: '',
  };

  let hasError = false;

  if (!input_id.value) {
    // 强制触发抖动效果
    inputError.value.id = false; // 先设置为 false
    inputError.value.idMessage = '用户名不能为空';
    hasError = true;

    // 确保每次都设置为 true，触发抖动
    setTimeout(() => {
      inputError.value.id = true;
    }, 0); // 延迟到下一个事件循环中，确保动画触发
  }

  if (!input_password.value) {
    // 强制触发抖动效果
    inputError.value.password = false; // 先设置为 false
    inputError.value.passwordMessage = '密码不能为空';
    hasError = true;

    // 确保每次都设置为 true，触发抖动
    setTimeout(() => {
      inputError.value.password = true;
    }, 0); // 延迟到下一个事件循环中，确保动画触发
  }

  if (hasError) return;

  const url = 'http://127.0.0.1:8000/api/userlogin/';
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: input_id.value,
        password: input_password.value,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message);
    }

    const data = await response.json();
    if (data.success) {
      localStorage.clear();
      localStorage.setItem('userId', input_id.value);
      localStorage.setItem('isAdmin', 'no');
      router.push('/home');
    } else {
      inputError.value.id = true;
      inputError.value.password = true;
      inputError.value.passwordMessage = '用户名或密码不正确';
    }
  } catch (error) {
    // let message = '登录失败';
    // if (error && typeof error === 'object' && 'message' in error) {
    //   message = error.message;
    // }

    console.error('登录失败:', error);
    inputError.value.id = true;
    inputError.value.password = true;
    inputError.value.passwordMessage = '用户名或密码不正确';
  }
};


// 点击特效逻辑
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
  // "💕😁😊😂🤣❤️😍👌😘🙌👍😎😉🎶💖😜😀😁😃😄😅😆😂🤣😉😊😋😎😍😘🥰😗😙🥲😚☺️🙂🤗🤩🤔🫡🤨😯🤐🫠🤡🥳🥺🥹🧐🧐👻🤖🤖",
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
</script>

<style lang="scss" scoped>
.page-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  // overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.input-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.button-container {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  justify-content: center;
  align-items: center;
}

.input-wrapper {
  position: relative;
  width: 500px;
  margin-bottom: 20px;
}

// :deep(.input-error) .el-input__inner {
//   border-color: red;
//   box-shadow: 0 0 3px rgba(255, 0, 0, 0.8);
// }

:deep(.input-error) .el-input__wrapper {
  border: 1px solid red !important;
  box-shadow: 0 0 6px 2px rgba(255, 0, 0, 0.3);
  border-radius: 6px;
}

.error-message {
  position: absolute;
  top: 70%;
  left: 130px;
  color: red;
  font-size: 12px;
}

.error-message-shake {
  animation: shake 0.3s ease-in-out;
}

@keyframes shake {
  0% { transform: translateX(0); }
  20% { transform: translateX(-5px); }
  40% { transform: translateX(5px); }
  60% { transform: translateX(-5px); }
  80% { transform: translateX(5px); }
  100% { transform: translateX(0); }
}

.box {
  position: fixed; /* 保证背景图片始终固定 */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  cursor: pointer;
  background: none;
  overflow: hidden;
  z-index: -1;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: url('/public/Logos/background.jpg') no-repeat center center;
    background-size: cover;
    background-position: center;
    opacity: 0.7;
    filter: blur(2px);
    z-index: -1;
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



// .content-container {
//   position: relative;
//   width: 100%;
//   height: 100%;
//   display: flex;
//   flex-direction: column;
//   justify-content: center;
//   align-items: center;
//   z-index: 1; /* 确保内容在背景板上面 */
//   margin-left: 25%;  /* 将内容向右偏移，达到 3/4 位置 */
// }

.content-container {
  position: absolute;  /* 绝对定位 */
  left: 55%;  /* 向右偏移 25%，这样内容会从 3/4 位置开始 */
  width: 40%;  /* 使内容容器占据页面的 75% */
  height: 75%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1; /* 确保内容在背景板上面 */

  /* 添加深灰色透明圆角矩形框 */
  border: 2px solid rgba(50, 50, 50, 0.7); /* 深灰色边框，透明度为0.7 */
  border-radius: 10px; /* 圆角 */
  padding: 20px; /* 适当的内边距，确保内容不与边框重叠 */
  background-color: rgba(0, 0, 0, 0.7); /* 深灰色透明背景 */
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

</style>