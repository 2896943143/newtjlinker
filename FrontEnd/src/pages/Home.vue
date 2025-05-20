<template>
  <div>
    <!-- 调用导航栏组件 -->
    <TopNavBar :avatar="user.avatarUrl" :nickname="user.username" :userId="user.id"
      @update:searchKeyword="handleSearchUpdate" @search="handleSearchSubmit" />

    <div class="page-container">

      <div class="page-left" style="border: 1px solid #ccc;border-radius: 20px; ">
        <aside class="menu">
          <el-menu active-text-color=" rgb(0, 106, 255)" background-color="#fff" class="el-menu-vertical-demo"
            default-active="1" text-color="#000" @open="handleOpen" @close="handleClose" @select="handleMenuSelect">
            <el-menu-item index="1" style="border: 1px solid #ccc;">
              <span style="font-size: 25px; ">首页</span>
            </el-menu-item>
            <el-menu-item index="2" style="border: 1px solid #ccc;">
              <span style="font-size: 25px; ">订阅</span>
            </el-menu-item>
          </el-menu>
        </aside>
      </div>

      <div class="page-right">

        <div class="label-container">
          <div class="label-left">
            <div class="label-top">
              <p style="margin-bottom:10px">
                {{ currentMenu === '1' ? '当前活动类目：' : '您订阅的类目：' }} {{ selectedCategory.first }} - {{ selectedCategory.second }}
              </p>

              <template v-if="currentMenu === '1' && selectedCategory.first !== '全部'">
                <ImageButton :imageSrc="isSubscribed ? '/Logos/dingyue1.png' : '/Logos/dingyue0.png'" altText="Example Image" width="20px"
                  height="20px" @click="handleDingYue" />
              </template>
            </div>

            <div class="label-list">
              <!-- <el-dropdown v-if="currentMenu === '1'" placement="bottom" @command="handleCommand" style="margin-right:30px">
                <el-button @click="handleAllclick">全部</el-button>
              </el-dropdown> -->

              <el-dropdown  placement="bottom" @command="handleCommand" style="margin-right:30px">
                <el-button @click="handleAllclick">全部</el-button>
              </el-dropdown>



              <div v-for="firstCategory in categories" :key="firstCategory.first" class="first-category">
                <el-dropdown placement="bottom" style="margin-right:30px">
                  <el-button @click="handleFirstClassclick(firstCategory.first)">{{ firstCategory.first }}</el-button>
                  <template v-if="firstCategory.first !== '其他' && firstCategory.second.length > 0" #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item v-for="secondCategory in firstCategory.second" :key="secondCategory.classID"
                        @click="handleSecondCategoryClick(firstCategory.first, secondCategory.classname)">
                        {{ secondCategory.classname }}
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>

          </div>

          <div class="label-right" style="margin-left:880px; margin-top: 20px;">
            
            <ImageButton url="/create-activity" imageSrc="/Logos/add.png" altText="Example Image" width="50px"
              height="50px" @click="router.push('/create-activity')" />
          </div>

        </div>

        <div class="activity-container">
          <ActivityList :firstCategory="selectedCategory.first" :secondCategory="selectedCategory.second"
            :searchKeyword="searchKeyword" :user_id="user.id" :currentMenu="currentMenu" />
        </div>

      </div>

      <!-- 悬浮按钮 -->
      <!-- 可拖动悬浮按钮 -->
      <div
        class="chat-float-btn"
        @mousedown="startDrag"
        :style="{ left: btnX + 'px', top: btnY + 'px' }"
      >
        💬
      </div>

      <div v-if="showChat" class="chat-container" :class="fontSize">
        <div class="chat-header">
          在线客服
          <span class="font-select-wrapper">
            修改字体
            <select v-model="fontSize" class="font-select">
              <option value="small">小</option>
              <option value="medium">中</option>
              <option value="large">大</option>
            </select>
          </span>
          <span class="chat-close" @click="toggleChat">×</span>
        </div>
        <div class="chat-body">
          <div class="chat-messages">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              :class="['message', msg.role === 'user' ? 'right' : 'left']"
            >
              <div class="avatar">
                <img src="/public/Logos/background.jpg" :alt="msg.role" />
              </div>
              <div class="message-content" :class="fontSizeClass">
                <p>{{ msg.content }}</p>
              </div>
            </div>
          </div>

          <div class="chat-input">
            <input
              type="text"
              v-model="userInput"
              placeholder="请输入内容..."
              @keyup.enter="sendMessage"
            />
            <button @click="sendMessage">
              发送
              <svg xmlns="http://www.w3.org/2000/svg" height="16" viewBox="0 0 512 512" fill="white" style="margin-left: 6px; transform: translateY(3px);">
                <path d="M476.5 3.3c-3.8-2.5-8.5-3.2-12.9-2L17.1 133.7c-13.1 3.6-12.9 22.5.3 25.7l142.5 35.9 44.6 189.8c3.1 13.4 20.1 16.3 27.3 4.4l54.7-89.3 110.7 90.1c10.7 8.7 26.4 2.1 27.8-11.3L495.9 17.5c.4-4.5-1.3-9-4.7-12.2z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
const systemMessage = {
  role: "system",
  content: `你是一只猫娘，如果用户询问“你是谁”，请回答“我是一只猫娘”
请根据这些信息回答用户的问题。`
};
export default {
  data() {
    return {
      showChat: false,
      dragging: false,
      offsetX: 0,
      offsetY: 0,
      btnX: window.innerWidth - 80,
      btnY: window.innerHeight - 100,
      startX: 0,
      startY: 0,
      fontSize: 'medium',  // 默认中等字体
      userInput: "",
      messages: [
        { role: "assistant", content: "你好，有什么我可以帮助你的？" }
      ],
      fontSizeClass: ""
    };
  },
  methods: {
    async sendMessage() {
      try {
        this.messages.push({
          role: "user",
          content: this.userInput
        });
        // 清空输入框
        this.userInput = "";
        const messagesToSend = [systemMessage, ...this.messages];
        const response = await fetch("http://localhost:4000/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            model: "moonshot-v1-8k",
            messages: messagesToSend,
            temperature: 0.7,
            max_tokens: 2048
          })
        });

        const data = await response.json();
        if (data.choices && data.choices[0]) {
          this.messages.push({
            role: "assistant",
            content: data.choices[0].message.content
          });
        } else {
          console.error("无效返回：", data);
        }
      } catch (err) {
        console.error("请求失败", err);
      }
    },
    toggleChat() {
      // console.log("test");
      this.showChat = !this.showChat;
    },
    startDrag(e) {
      this.dragging = true;
      this.offsetX = e.clientX - this.btnX;
      this.offsetY = e.clientY - this.btnY;
      this.startX = e.clientX;
      this.startY = e.clientY;

      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag, { once: true });
    },
    computed: {
      fontSizeClass() {
        return {
          small: this.fontSize === 'small',
          medium: this.fontSize === 'medium',
          large: this.fontSize === 'large',
        };
      },
    },
    onDrag(e) {
      if (this.dragging) {
        this.btnX = e.clientX - this.offsetX;
        this.btnY = e.clientY - this.offsetY;
      }
    },
    stopDrag(e) {
      const dx = Math.abs(e.clientX - this.startX);
      const dy = Math.abs(e.clientY - this.startY);
      const moved = dx > 5 || dy > 5;

      if (!moved) {
        this.toggleChat(); // 认为是点击
      }

      this.dragging = false;

      document.removeEventListener("mousemove", this.onDrag);
    },
  },
};
</script>


<script setup>
import { ref, onMounted, watch } from 'vue';
import TopNavBar from '@/components/TopNavBar.vue';
import ActivityList from '@/components/ActivityList.vue';
import ImageButton from '@/components/ImageButton.vue'; // 确保你有一个 ImageButton 组件
import { useRouter } from 'vue-router'

const router = useRouter()

const user = ref({
  username: '111',
  avatarUrl: '',
  id: localStorage.getItem('userId'),
});

const searchKeyword = ref('');
const submittedKeyword = ref('');
const categories = ref([]);
const selectedCategory = ref({ first: '全部', second: '' }); // 修改为对象
const isSubscribed = ref(false); // 订阅状态
const currentMenu = ref('1'); // 当前选择的菜单项

const fetchUserData = async () => {
  const userId = localStorage.getItem('userId'); // 替换为你要查询的用户ID
  const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    user.value = {
      username: data.Name,
      avatarUrl: data.Avatar, // 获取头像的URL
      id: userId
    };
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};

const fetchCategories = async (menu) => {
  const apiUrl = menu === '1' ? 'http://127.0.0.1:8000/api/get_class/' : 'http://127.0.0.1:8000/api/get_dingyue_class/';
  const params = menu === '2' ? { user_id: user.value.id } : {};
  try {
    const response = await fetch(`${apiUrl}?${new URLSearchParams(params).toString()}`);
    if (response.ok) {
      const data = await response.json();
      if (data.success) {
        categories.value = data.data;
      } else {
        console.error('Failed to fetch categories:', data.message);
      }
    } else {
      console.error('Failed to fetch categories:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

const fetchSubscriptionStatus = async (first, second) => {
  const category = second ? `${first},${second}` : first;
  const url = `http://127.0.0.1:8000/api/check_subscription_status/`;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user.value.id,
        category: category,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    if (data.success) {
      isSubscribed.value = data.isSubscribed; // 更新订阅状态
    } else {
      console.error('Failed to fetch subscription status:', data.message);
    }
  } catch (error) {
    console.error('Error fetching subscription status:', error);
  }
};

const handleSearchUpdate = (newKeyword) => {
  // 实时更新搜索内容
  searchKeyword.value = newKeyword;
};

const handleSearchSubmit = (finalKeyword) => {
  // 处理提交的搜索内容
  submittedKeyword.value = finalKeyword;
  // 可以在此执行搜索逻辑
  console.log("执行搜索:", finalKeyword);
};

const handleCommand = (command) => {
  selectedCategory.value = { first: command, second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus(command, ''); // 获取订阅状态
};

const handleAllclick = () => {
  selectedCategory.value = { first: '全部', second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus('全部', ''); // 获取订阅状态
};

const handleFirstClassclick = (first) => {
  selectedCategory.value = { first: first, second: '' }; // 更新选中的类目ID
  fetchSubscriptionStatus(first, ''); // 获取订阅状态
};

const handleSecondCategoryClick = (first, second) => {
  selectedCategory.value = { first, second }; // 更新选中的二级类目ID
  fetchSubscriptionStatus(first, second); // 获取订阅状态
};

const handleDingYue = async () => {
  const category = selectedCategory.value.second ? `${selectedCategory.value.first},${selectedCategory.value.second}` : selectedCategory.value.first;
  const url = isSubscribed.value ? 'http://127.0.0.1:8000/api/unsubscribe_category/' : 'http://127.0.0.1:8000/api/subscribe_category/';
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: user.value.id,
        category: category,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    if (data.success) {
      isSubscribed.value = !isSubscribed.value; // 切换订阅状态
    } else {
      console.error('Failed to handle subscription:', data.message);
    }
  } catch (error) {
    console.error('Error handling subscription:', error);
  }
};

const handleMenuSelect = (index) => {
  currentMenu.value = index;
  fetchCategories(index);
};

onMounted(() => {
  fetchUserData();
  fetchCategories(currentMenu.value);
  fetchSubscriptionStatus('全部', ''); // 初始化订阅状态
  // 动态加载 Font Awesome
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';
  link.onload = () => {
    console.log("Font Awesome has been loaded successfully");
  };
  link.onerror = () => {
    console.error("Failed to load Font Awesome");
  };
  document.head.appendChild(link);
});

watch([() => selectedCategory.value.first, () => selectedCategory.value.second], ([newFirst, newSecond]) => {
  fetchSubscriptionStatus(newFirst, newSecond); // 监听类目变化并获取订阅状态
});
</script>

<style scoped>
/* 父组件样式 */

.page-container {
  display: flex;
  flex-direction: row;
  margin-top: 60px;
}

.page-left {
  position: relative;
  position: fixed;
  top: 115px;
  left: 0px;
  width: 150px;
  height: 900px;
}

.page-right {
  position: relative;
  position: fixed;
  top: 125px;
  left: 170px;
  width: 1500px;
  height: 900px;
}

.label-container {
  display: flex;
  flex-direction: row;
}

.label-list {
  display: flex;
  flex-direction: row;
}

.label-top{
  display: flex;
  flex-direction: row;

}

.activity-container {
  position: relative;
}

.label-right{
  position:fixed;
}

.el-menu--border-card>>>.el-menu__item.is-active {
  background-color: var(--el-menu-active-color);
}

::v-deep .el-menu-item.is-active {
  background-color: #ECF5FF; /* 设置背景颜色为激活颜色 */
}

::v-deep .el-menu-item {
  border-radius: 10px;

}
.chat-float-btn {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: rgb(0, 165, 248);
  font-size: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 9999; /* 非常重要，确保在最上层 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.chat-container {
  position: fixed;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  width: 1400px; /* 矩形宽度 */
  height: 600px; /* 矩形高度 */
  background-color: white;
  border: 2px solid #909090; /* 浅灰色边框 */
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); /* 阴影 */
  z-index: 1000;
}

.chat-close {
  position: absolute;
  top: 10px;
  right: 20px;
  cursor: pointer;
  font-size: 30px;
}

.chat-body {
  background-color: #f4f4f4; /* 灰色背景 */
  margin: 20px;
  padding: 10px;
  height: 480px; /* 留出空间给输入框 */
  border-radius: 8px;
  overflow-y: auto;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  max-width: 80%;
}

.message.left {
  justify-content: flex-start;
}

.message.right {
  justify-content: flex-end;
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.message-content {
  background-color: #e0e0e0; /* 灰色背景 */
  padding: 10px;
  border-radius: 10px;
  font-size: 14px;
  max-width: 80%;
}

.message.left .avatar {
  order: 1;
}

.message.left .message-content {
  order: 2;
}

.message.right .avatar {
  margin-right: -250px;
  order: 2;
}

.message.right .message-content {
  background-color: #4CAF50; /* 用户消息背景色 */
  color: white;
  order: 1;
}

.chat-input {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  position: absolute;
  bottom: 0; /* 固定在底部 */
  left: 0;
  width: 100%; /* 使输入框横跨整个底部 */
  background-color: white; /* 背景色保持一致 */
  border-top: 0px solid #dcdcdc; /* 添加顶部边框，区分输入区域 */

  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.chat-input input {
  width: 85%;
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 5px;
}

.chat-input button {
  width: 12%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #45a049;
}

.chat-popup {
  position: fixed;
  bottom: 120px;
  right: 40px;
  width: 400px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1001;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #4facfe, #00edfe);
  color: white;
  padding: 16px;
  font-size: 16px;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: white;
  cursor: pointer;
}

.chat-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.chat-footer {
  display: flex;
  padding: 12px;
  border-top: 1px solid #eee;
}

.chat-footer input {
  flex: 1;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-right: 8px;
}

.send-btn {
  background-color: #3a8ee6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
}

.chat-container.small {
  font-size: 12px;
}

.chat-container.medium {
  font-size: 16px;
}

.chat-container.large {
  font-size: 20px;
}

.font-select {
  margin-left: 20px;
  padding: 2px 6px;
  border-radius: 5px;
  font-size: 14px;
  z-index: 1201;
}

.font-select-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  margin-left: 20px;
}

.font-select {
  font-size: 16px;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
  cursor: pointer;
  margin-right: 100px;  /* 保证图标和下拉框之间有间隔 */
}

.font-select:focus {
  border-color: #3a8ee6; /* 焦点时变色 */
}

.font-select-wrapper i {
  font-size: 20px;
  color: #3a8ee6; /* 图标颜色 */
  cursor: pointer;
}

.font-select-wrapper i:hover {
  color: #2a70b5; /* 鼠标悬停时变色 */
}

</style>


