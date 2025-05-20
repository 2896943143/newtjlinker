<!--<template>-->
<!--  <div class="page-wrapper" style="&#45;&#45;bg-image: url(../../public/Logos/background.jpg)">-->
<!--    <div class="app-container">-->
<!--      &lt;!&ndash; 左侧聊天列表 &ndash;&gt;-->
<!--      <aside class="sidebar">-->
<!--        <h3 class="sidebar-title">聊天列表</h3>-->
<!--        <ul class="chat-list">-->
<!--          <li-->
<!--            v-for="chat in chats"-->
<!--            :key="chat.id"-->
<!--            :class="['chat-item', { active: chat.id === selectedChat.id } ]"-->
<!--            @click="selectChat(chat)"-->
<!--          >-->
<!--            <div class="avatar">{{ chat.name.charAt(0) }}</div>-->
<!--            <div class="chat-info">-->
<!--              <div class="chat-name">{{ chat.name }}</div>-->
<!--              <div class="chat-last">{{ chat.lastMessage }}</div>-->
<!--            </div>-->
<!--          </li>-->
<!--        </ul>-->
<!--        &lt;!&ndash; 设置按钮 &ndash;&gt;-->
<!--        <div class="sidebar-footer">-->
<!--          <button class="settings-btn" @click="toggleSettings">⚙️ 设置</button>-->
<!--        </div>-->
<!--      </aside>-->

<!--      &lt;!&ndash; 右侧聊天主区域 &ndash;&gt;-->
<!--      <section class="chat-container" :style="backgroundStyle">-->
<!--        <header class="chat-header">-->
<!--          <h2 class="chat-title">{{ selectedChat.name }}</h2>-->
<!--        </header>-->

<!--        &lt;!&ndash; 聊天设置面板 &ndash;&gt;-->
<!--        <div v-if="showSettings" class="settings-panel">-->
<!--          <h3>聊天设置</h3>-->
<!--          <div class="setting-item">-->
<!--            <label>更换背景：</label>-->
<!--            <input type="file" ref="bgInput" @change="onBackgroundChange" accept="image/*" />-->
<!--          </div>-->
<!--          <button class="close-settings" @click="toggleSettings">关闭</button>-->
<!--        </div>-->

<!--        <div class="chat-messages" ref="messagesEnd">-->
<!--          <transition-group name="message-list" tag="div">-->
<!--            <div-->
<!--              v-for="(msg, index) in messages"-->
<!--              :key="msg.id || index"-->
<!--              class="message"-->
<!--              :class="msg.from === 'me' ? 'me' : 'them'"-->
<!--            >-->
<!--              <img-->
<!--                class="message-avatar"-->
<!--                :src="msg.from === 'me' ? myAvatar : otherAvatar"-->
<!--                alt="avatar"-->
<!--              />-->
<!--              <div class="message-content">-->
<!--                <span class="message-text">{{ msg.text }}</span>-->
<!--                <span class="message-date">{{ formatDate(msg.date) }}</span>-->
<!--              </div>-->
<!--            </div>-->
<!--          </transition-group>-->
<!--        </div>-->
<!--        <div class="chat-input">-->
<!--          <div class="icon-row">-->
<!--            &lt;!&ndash; 文件发送图标，触发隐藏 input &ndash;&gt;-->
<!--            <label class="icon-btn file-btn">-->
<!--              📁-->
<!--              <input type="file" ref="fileInput" @change="sendFile" hidden />-->
<!--            </label>-->
<!--            &lt;!&ndash; 更换背景 &ndash;&gt;-->
<!--            <label class="icon-btn bg-btn" title="更换背景">-->
<!--              🖼️-->
<!--              <input type="file" ref="bgInput" @change="onBackgroundChange" accept="image/*" hidden />-->
<!--            </label>-->
<!--            <button class="icon-btn emoji-btn" @click="toggleEmojiPanel">😊</button>-->
<!--          </div>-->
<!--          <div v-if="showEmoji" class="emoji-panel">-->
<!--            <span-->
<!--              v-for="e in emojiList"-->
<!--              :key="e"-->
<!--              class="emoji-item"-->
<!--              @click="addEmoji(e)"-->
<!--            >{{ e }}</span>-->
<!--          </div>-->
<!--          <div class="input-row">-->
<!--            <input-->
<!--              v-model="newMessage"-->
<!--              @keyup.enter="sendMessage"-->
<!--              class="text-input"-->
<!--              placeholder="请输入消息..."-->
<!--            />-->
<!--            <button class="send-btn" @click="sendMessage">发送</button>-->
<!--          </div>-->
<!--        </div>-->
<!--      </section>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script setup>-->
<!--import { ref, onMounted, nextTick } from 'vue'-->

<!--// 聊天列表示例数据-->
<!--const chats = ref([-->
<!--  { id: 1, name: 'Alice', lastMessage: '你好！' },-->
<!--  { id: 2, name: '开发群', lastMessage: '请检查代码。' },-->
<!--  { id: 3, name: 'Bob', lastMessage: '下午一起吃饭？' },-->
<!--])-->
<!--const selectedChat = ref(chats.value[0])-->

<!--// 头像路径，替换为实际路径-->
<!--const myAvatar = '/path/to/my-avatar.png'-->
<!--const otherAvatar = '/path/to/other-avatar.png'-->

<!--// 消息列表与输入-->
<!--const messages = ref([])-->
<!--const newMessage = ref('')-->
<!--const showEmoji = ref(false)-->
<!--const showSettings = ref(false)-->

<!--// Emoji 列表-->
<!--const emojiList = ['😀','😂','😍','😎','😭','👍','🙏','🎉']-->

<!--// 背景图-->
<!--const backgroundStyle = ref({})-->
<!--const bgInput = ref(null)-->
<!--const fileInput = ref(null)-->

<!--// 选择聊天-->
<!--function selectChat(chat) {-->
<!--  selectedChat.value = chat-->
<!--  loadMessages()-->
<!--}-->

<!--// 发送消息-->
<!--function sendMessage() {-->
<!--  const text = newMessage.value.trim()-->
<!--  if (!text) return-->
<!--  const message = { id: Date.now(), text, date: new Date().toISOString(), from: 'me' }-->
<!--  messages.value.push(message)-->
<!--  newMessage.value = ''-->
<!--  scrollToBottom()-->
<!--}-->

<!--// 发送文件-->
<!--function sendFile(e) {-->
<!--  const file = e.target.files[0]-->
<!--  if (!file) return-->
<!--  const reader = new FileReader()-->
<!--  reader.onload = () => {-->
<!--    const message = {-->
<!--      id: Date.now(),-->
<!--      text: `[文件] ${file.name}`,-->
<!--      date: new Date().toISOString(),-->
<!--      from: 'me',-->
<!--      fileData: reader.result,-->
<!--      fileName: file.name-->
<!--    }-->
<!--    messages.value.push(message)-->
<!--    scrollToBottom()-->
<!--  }-->
<!--  reader.readAsDataURL(file)-->
<!--  // 重置 input-->
<!--  e.target.value = ''-->
<!--}-->

<!--function onBackgroundChange(e) {-->
<!--  const file = e.target.files[0]-->
<!--  if (!file) return-->
<!--  const reader = new FileReader()-->
<!--  reader.onload = () => {-->
<!--    backgroundStyle.value = {-->
<!--      backgroundImage: `url(${reader.result})`,-->
<!--      backgroundSize: 'cover',-->
<!--      backgroundPosition: 'center',-->
<!--      backgroundRepeat: 'no-repeat'-->
<!--    }-->
<!--  }-->
<!--  reader.readAsDataURL(file)-->
<!--  e.target.value = ''-->
<!--}-->

<!--// 加载历史消息-->
<!--function loadMessages() {-->
<!--  messages.value = [-->
<!--    { id: 0, text: `欢迎进入与${selectedChat.value.name}的聊天！`, date: new Date(Date.now() - 600000).toISOString(), from: 'them' },-->
<!--  ]-->
<!--  scrollToBottom()-->
<!--}-->

<!--// 格式化日期-->
<!--function formatDate(iso) {-->
<!--  return new Date(iso).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })-->
<!--}-->

<!--// 滚动到底部-->
<!--function scrollToBottom() {-->
<!--  nextTick(() => {-->
<!--    const el = messagesEnd.value-->
<!--    if (el) el.scrollTop = el.scrollHeight-->
<!--  })-->
<!--}-->

<!--// 切换 Emoji 面板-->
<!--function toggleEmojiPanel() {-->
<!--  showEmoji.value = !showEmoji.value-->
<!--}-->

<!--// 切换设置面板-->
<!--function toggleSettings() {-->
<!--  showSettings.value = !showSettings.value-->
<!--}-->

<!--// 添加 Emoji-->
<!--function addEmoji(e) {-->
<!--  newMessage.value += e-->
<!--}-->

<!--const messagesEnd = ref(null)-->

<!--// 初始化-->
<!--onMounted(() => loadMessages())-->
<!--</script>-->

<!--<style scoped>-->
<!--.page-wrapper {-->
<!--  /* 继承或重新定义背景变量 */-->
<!--  &#45;&#45;bg-image: none;-->
<!--  display: flex;-->
<!--  justify-content: center;  /* 水平居中 */-->
<!--  align-items: center;      /* 垂直居中 */-->

<!--  /* 使用变量 */-->
<!--  background-image: var(&#45;&#45;bg-image);-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  background-repeat: no-repeat;-->

<!--  /* 保证铺满 */-->
<!--  width: 100%;-->
<!--  height: 100%;-->
<!--}-->

<!--.app-container {-->
<!--   width: 1500px;-->
<!--  height: 1000px;-->

<!--  display: flex;-->
<!--  font-family: "Helvetica Neue", Arial, sans-serif;-->
<!--  position: relative;-->
<!--  background: white; /* 或者半透明背景，看需求 */-->

<!--  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.05);-->
<!--}-->

<!--.app-container::before {-->
<!--  content: "";-->
<!--  position: absolute;-->
<!--  top: 0; left: 0; right: 0; bottom: 0;-->
<!--  background-image: var(&#45;&#45;bg-image);-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  opacity: 0.08;-->
<!--  z-index: -1;-->
<!--}-->

<!--/* Sidebar 样式 */-->
<!--.sidebar {-->
<!--  width: 240px;-->
<!--  background: linear-gradient(180deg, #4e54c8, #8f94fb);-->
<!--  color: #fff;-->
<!--  padding: 16px;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  justify-content: space-between;-->
<!--  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);-->
<!--  backdrop-filter: blur(4px);-->
<!--}-->

<!--.sidebar-title {-->
<!--  margin: 0 0 12px;-->
<!--  font-size: 16px;-->
<!--  text-align: center;-->
<!--}-->

<!--.chat-list {-->
<!--  list-style: none;-->
<!--  padding: 0;-->
<!--  margin: 0;-->
<!--  flex: 1;-->
<!--  overflow-y: auto;-->
<!--}-->

<!--.chat-item {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  padding: 8px;-->
<!--  border-radius: 8px;-->
<!--  margin-bottom: 6px;-->
<!--  cursor: pointer;-->
<!--  transition: background 0.3s;-->
<!--}-->

<!--.chat-item:hover,-->
<!--.chat-item.active {-->
<!--  background: rgba(255, 255, 255, 0.2);-->
<!--}-->

<!--.avatar {-->
<!--  width: 36px;-->
<!--  height: 36px;-->
<!--  border-radius: 50%;-->
<!--  background: #fff;-->
<!--  color: #4e54c8;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  margin-right: 10px;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.chat-info {-->
<!--  flex: 1;-->
<!--}-->

<!--.chat-name {-->
<!--  font-size: 14px;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.chat-last {-->
<!--  font-size: 12px;-->
<!--  opacity: 0.8;-->
<!--}-->

<!--.sidebar-footer {-->
<!--  padding-top: 12px;-->
<!--  border-top: 1px solid rgba(255,255,255,0.3);-->
<!--  text-align: center;-->
<!--}-->

<!--.settings-btn {-->
<!--  border: none;-->
<!--  background: transparent;-->
<!--  color: #fff;-->
<!--  font-size: 16px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--/* Chat 主区 */-->
<!--.chat-container {-->
<!--  flex: 1;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  position: relative;-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  background-repeat: no-repeat;-->
<!--  border-radius: 8px;-->
<!--  overflow: hidden;-->
<!--  box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.05);-->
<!--  border-left: 1px solid rgba(0, 0, 0, 0.05);-->
<!--}-->

<!--.chat-header {-->
<!--  padding: 12px;-->
<!--  background: rgba(255, 255, 255, 0.8);-->
<!--  border-bottom: 1px solid #ddd;-->
<!--  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);-->
<!--}-->

<!--.chat-title {-->
<!--  margin: 0;-->
<!--  font-size: 18px;-->
<!--  color: #333;-->
<!--}-->

<!--.settings-panel {-->
<!--  position: absolute;-->
<!--  top: 50px;-->
<!--  right: 20px;-->
<!--  width: 250px;-->
<!--  background: rgba(255,255,255,0.95);-->
<!--  border-radius: 8px;-->
<!--  padding: 16px;-->
<!--  box-shadow: 0 4px 12px rgba(0,0,0,0.15);-->
<!--  z-index: 10;-->
<!--}-->

<!--.settings-panel h3 {-->
<!--  margin: 0 0 12px;-->
<!--  font-size: 16px;-->
<!--}-->

<!--.setting-item {-->
<!--  margin-bottom: 12px;-->
<!--  font-size: 14px;-->
<!--}-->

<!--.close-settings {-->
<!--  border: none;-->
<!--  background: #4e54c8;-->
<!--  color: #fff;-->
<!--  padding: 6px 12px;-->
<!--  border-radius: 4px;-->
<!--  cursor: pointer;-->
<!--}-->

<!--.chat-messages {-->
<!--  flex: 1;-->
<!--  overflow-y: auto;-->
<!--  padding: 16px;-->
<!--  background: rgba(255, 255, 255, 0.7);-->
<!--}-->

<!--.message {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  margin-bottom: 10px;-->
<!--  max-width: 60%;-->
<!--}-->

<!--.message-list-enter-active, .message-list-leave-active {-->
<!--  transition: all 0.3s ease;-->
<!--}-->
<!--.message-list-enter-from, .message-list-leave-to {-->
<!--  opacity: 0;-->
<!--  transform: translateY(10px);-->
<!--}-->

<!--.message.them {-->
<!--  flex-direction: row;-->
<!--}-->

<!--.message.me {-->
<!--  flex-direction: row-reverse;-->
<!--  margin-left: auto;-->
<!--}-->

<!--.message-avatar {-->
<!--  width: 32px;-->
<!--  height: 32px;-->
<!--  border-radius: 50%;-->
<!--}-->

<!--.message-content {-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--  margin: 0 8px;-->
<!--}-->

<!--.message-text {-->
<!--  padding: 8px 12px;-->
<!--  border-radius: 16px;-->
<!--  background: #fff;-->
<!--  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);-->
<!--}-->

<!--.message.me .message-text {-->
<!--  background: #dcf8c6;-->
<!--}-->

<!--.message-date {-->
<!--  font-size: 10px;-->
<!--  margin-top: 4px;-->
<!--  color: #999;-->
<!--  align-self: flex-end;-->
<!--}-->

<!--.chat-input {-->
<!--  padding: 8px;-->
<!--  background: rgba(255, 255, 255, 0.9);-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.icon-row {-->
<!--  display: flex;-->
<!--  margin-bottom: 6px;-->
<!--}-->

<!--.icon-btn {-->
<!--  border: none;-->
<!--  background: transparent;-->
<!--  font-size: 22px;-->
<!--  cursor: pointer;-->
<!--  margin-right: 12px;-->
<!--}-->

<!--.emoji-panel {-->
<!--  display: flex;-->
<!--  flex-wrap: wrap;-->
<!--  background: #fff;-->
<!--  padding: 8px;-->
<!--  border-radius: 6px;-->
<!--  box-shadow: 0 2px 6px rgba(0,0,0,0.1);-->
<!--  margin-bottom: 6px;-->
<!--}-->

<!--.emoji-item {-->
<!--  font-size: 20px;-->
<!--  padding: 4px;-->
<!--  cursor: pointer;-->
<!--  margin: 2px;-->
<!--}-->

<!--.input-row {-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--}-->

<!--.text-input {-->
<!--  flex: 1;-->
<!--  padding: 8px 12px;-->
<!--  border: 1px solid #ccc;-->
<!--  border-radius: 20px;-->
<!--  margin-right: 8px;-->
<!--  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);-->
<!--}-->

<!--.send-btn {-->
<!--  padding: 8px 16px;-->
<!--  border: none;-->
<!--  background: #4e54c8;-->
<!--  color: #fff;-->
<!--  border-radius: 20px;-->
<!--  font-weight: bold;-->
<!--  cursor: pointer;-->
<!--  transition: background 0.3s;-->
<!--}-->

<!--.send-btn:hover {-->
<!--  background: #3b3fc1;-->
<!--}-->

<!--/* 移动端适配 */-->
<!--@media (max-width: 768px) {-->
<!--  .sidebar {-->
<!--    width: 100%;-->
<!--    height: auto;-->
<!--    position: fixed;-->
<!--    bottom: 0;-->
<!--    left: 0;-->
<!--    right: 0;-->
<!--    z-index: 999;-->
<!--  }-->

<!--  .chat-container {-->
<!--    margin-bottom: 120px; /* 为移动端底部聊天栏留出空间 */-->
<!--  }-->
<!--}-->

<!--.sidebar,-->
<!--.chat-container,-->
<!--.settings-panel,-->
<!--.chat-input,-->
<!--.message-text {-->
<!--  /* 增加统一阴影 */-->
<!--  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.icon-btn {-->
<!--  position: relative;-->
<!--  font-size: 24px;-->
<!--  /* 增大点击区域 */-->
<!--  width: 40px;-->
<!--  height: 40px;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  border-radius: 50%;-->
<!--}-->

<!--.file-btn input,-->
<!--.emoji-btn {-->
<!--  cursor: pointer;-->
<!--}-->
<!--</style>-->

<template>
  <div class="page-wrapper" style="--bg-image: url(../../public/Logos/background.jpg)">
    <div class="app-container">
      <!-- 左侧聊天列表 -->
      <aside class="sidebar">
        <h3 class="sidebar-title">聊天列表</h3>
        <ul class="chat-list">
          <li
            v-for="chat in chats"
            :key="chat.id"
            :class="['chat-item', { active: chat.id === selectedChat?.id } ]"
            @click="selectChat(chat)"
          >
            <div class="avatar">{{ chat.name.charAt(0) }}</div>
            <div class="chat-info">
              <div class="chat-name">{{ chat.name }}</div>
              <div class="chat-last">{{ chat.message }}</div>
            </div>
          </li>
        </ul>
        <!-- 设置按钮 -->
        <div class="sidebar-footer">
          <button class="settings-btn" @click="toggleSettings">⚙️ 设置</button>
        </div>
      </aside>

      <!-- 右侧聊天主区域 -->
      <section class="chat-container" :style="backgroundStyle">
        <header class="chat-header">
          <h2 class="chat-title">{{ selectedChat?.name || '聊天界面' }}</h2>
        </header>

        <!-- 聊天设置面板 -->
        <div v-if="showSettings" class="settings-panel">
          <h3>聊天设置</h3>
          <div class="setting-item">
            <label>更换背景：</label>
            <input type="file" ref="bgInput" @change="onBackgroundChange" accept="image/*" />
          </div>
          <button class="close-settings" @click="toggleSettings">关闭</button>
        </div>

        <div class="chat-messages" ref="messagesEnd">
          <transition-group name="message-list" tag="div">
            <div
              v-for="(msg, index) in messages"
              :key="msg.id || index"
              class="message"
              :class="msg.from === user.id ? 'me' : 'them'"
            >
              <!-- 头像 -->
              <img
                class="message-avatar"
                :src="`http://127.0.0.1:8000${msg.avatar_url}`"
                alt="avatar"
              />

              <div class="message-body">
                <!-- 在气泡上方显示用户名 -->
                <div class="message-user">
                  {{ msg.name }}
                </div>
                <div class="message-content">
                  <span class="message-text">{{ msg.message }}</span>
                  <span class="message-date">{{ formatDate(msg.time) }}</span>
                </div>
              </div>
            </div>
          </transition-group>
        </div>

        <div class="chat-input">
          <div class="icon-row">
            <!-- 文件发送图标，触发隐藏 input -->
            <label class="icon-btn file-btn">
              📁
              <input type="file" ref="fileInput" @change="sendFile" hidden />
            </label>
            <!-- 更换背景 -->
            <label class="icon-btn bg-btn" title="更换背景">
              🖼️
              <input type="file" ref="bgInput" @change="onBackgroundChange" accept="image/*" hidden />
            </label>
            <button class="icon-btn emoji-btn" @click="toggleEmojiPanel">😊</button>
          </div>
          <div v-if="showEmoji" class="emoji-panel">
            <span
              v-for="e in emojiList"
              :key="e"
              class="emoji-item"
              @click="addEmoji(e)"
            >{{ e }}</span>
          </div>
          <div class="input-row">
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              class="text-input"
              placeholder="请输入消息..."
            />
            <button class="send-btn" @click="sendMessage">发送</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
const user = ref({
  username: '111',
  avatarUrl: '',
  id: localStorage.getItem('userId'),
});

// 聊天列表与当前选中
const chats = ref([])
const selectedChat = ref(null)

// 消息列表与输入
const messages = ref([])
const newMessage = ref('')
const showEmoji = ref(false)
const showSettings = ref(false)
const emojiList = ['😀','😂','😍','😎','😭','👍','🙏','🎉']

// 背景图
const backgroundStyle = ref({})
const bgInput = ref(null)
const fileInput = ref(null)
const messagesEnd = ref(null)

let ws = null

// 格式化日期
function formatDate(iso) {
  return new Date(iso).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    const el = messagesEnd.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

function toggleSettings() {
  showSettings.value = !showSettings.value
}

// 获取聊天列表
async function fetchChats() {
   try {
    const url = `http://127.0.0.1:8000/api/new_get_chat_list/?userId=${user.value.id}`
    const res = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    const data = await res.json()
    chats.value = data
    if (chats.value.length) {
      selectChat(chats.value[0])
    }
  } catch (e) {
    console.error('加载聊天列表失败', e)
  }
  console.log(chats.value)
}

// 选择聊天，加载历史消息
async function selectChat(chat) {
  selectedChat.value = chat
  await loadMessages(chat.id)
}

// 加载历史消息
async function loadMessages(chatId) {
  try {
     if (selectedChat.value.type===0) {
       const res = await fetch(`http://127.0.0.1:8000/api/load_message_person/?userId=${user.value.id}&otherId=${chatId}`)
       const data = await res.json()
       messages.value = data
       scrollToBottom()
     }
     else{
       const res = await fetch(`http://127.0.0.1:8000/api/load_message_group/?roomId=${chatId}`)
       const data = await res.json()
       messages.value = data
       scrollToBottom()
     }
  } catch (e) {
    console.error('加载消息失败', e)
    messages.value = []
  }
}

// 发送消息
async function sendMessage() {
  const text = newMessage.value.trim()
  if (!text || !selectedChat.value) return
  try {
    if (selectedChat.value.type===0) {
      const res = await fetch(`http://127.0.0.1:8000/api/send_message_person/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text, sendUserId: user.value.id, receiveUserId: selectedChat.value.id})
      })
      const saved = await res.json()
      messages.value.push(saved)
      const chat = chats.value.find(c => c.id === selectedChat.value.id)
      chat.message = text
      newMessage.value = ''
      scrollToBottom()
    }
    else {
       const res = await fetch(`http://127.0.0.1:8000/api/send_message_group/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({roomId:selectedChat.value.id, userID:user.value.id, message:text})
      })
      const saved = await res.json()
      messages.value.push(saved)
      const chat = chats.value.find(c => c.id === selectedChat.value.id)
      chat.message = text
      newMessage.value = ''
      scrollToBottom()
    }
  } catch (e) {
    console.error('发送消息失败', e)
  }
}

// 发送文件
function sendFile(e) {
  const file = e.target.files[0]
  if (!file || !selectedChat.value) return
  const reader = new FileReader()
  reader.onload = async () => {
    try {
      const res = await fetch(`/api/chats/${selectedChat.value.id}/files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileName: file.name, fileData: reader.result })
      })
      const saved = await res.json()
      messages.value.push(saved)
      selectedChat.value.lastMessage = `[文件] ${file.name}`
      scrollToBottom()
    } catch (err) {
      console.error('发送文件失败', err)
    }
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

// 更换背景
function onBackgroundChange(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    backgroundStyle.value = {
      backgroundImage: `url(${reader.result})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat'
    }
  }
  reader.readAsDataURL(file)
  e.target.value = ''
}

// Emoji 操作
function toggleEmojiPanel() {
  showEmoji.value = !showEmoji.value
}
function addEmoji(e) {
  newMessage.value += e
}

// 初始化 WebSocket
function initWebSocket() {
  ws = new WebSocket('ws://localhost:8000/api/ws/')
  ws.onmessage = (event) => {
    const { message, from1, to1, avatar_url, time1, name,chatid} = JSON.parse(event.data)
    if (to1 === user.value.id) {
      const chat = chats.value.find(c => c.id === chatid)
      if (chat) chat.message = message
      else {
        chats.value.push({'id': from1, 'message':null, 'name': name, 'type': 0})
        const chatnow = chats.value.find(c => c.id === chatid)
        chatnow.message=message
      }
      if (selectedChat.value && selectedChat.value.id === chatid) {
        messages.value.push({ from: from1, message: message, time: time1, avatar_url: avatar_url ,name:name})
        scrollToBottom()
      }
    }
  }
  ws.onclose = () => console.warn('WebSocket 已断开')
  ws.onerror = (err) => console.error('WebSocket 发生错误', err)
}
async function postDone(){
  const person=localStorage.getItem("another_person")
  if (person) {
    const chat = chats.value.find(c => c.id === person)
    console.log('组件挂载时变量值:', person)
    console.log('组件挂载时变量值:',chats.value)
    if(chat === undefined){
      const userId = person; // 替换为你要查询的用户ID
      const url = `http://127.0.0.1:8000/api/users/info?id=${userId}`; // 将userId放在URL查询字符串中

      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        chats.value.push({'id': person, 'message':null, 'name': data.Name, 'type': 0})
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    }
    const chatNow = chats.value.find(c => c.id === person)
    selectChat(chatNow)
  }
  localStorage.removeItem("another_person");
}

onMounted(() => {
  fetchChats()
    .then(() => initWebSocket())
    .then(() => postDone())
})

onBeforeUnmount(() => {
  if (ws) ws.close()
})
</script>
<style scoped>
.message-body {
  display: flex;
  flex-direction: column;
}
.message-user {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
  padding-left: 8px;
}
.page-wrapper {
  /* 继承或重新定义背景变量 */
  --bg-image: none;
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;      /* 垂直居中 */

  /* 使用变量 */
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  /* 保证铺满 */
  width: 100%;
  height: 100%;
}

.app-container {
   width: 1500px;
  height: 1000px;

  display: flex;
  font-family: "Helvetica Neue", Arial, sans-serif;
  position: relative;
  background: white; /* 或者半透明背景，看需求 */

  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.05);
}

.app-container::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: var(--bg-image);
  background-size: cover;
  background-position: center;
  opacity: 0.08;
  z-index: -1;
}

/* Sidebar 样式 */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #4e54c8, #8f94fb);
  color: #fff;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(4px);
}

.sidebar-title {
  margin: 0 0 12px;
  font-size: 16px;
  text-align: center;
}

.chat-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
  overflow-y: auto;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 8px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.chat-item:hover,
.chat-item.active {
  background: rgba(255, 255, 255, 0.2);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #fff;
  color: #4e54c8;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  font-weight: bold;
}

.chat-info {
  flex: 1;
}

.chat-name {
  font-size: 14px;
  font-weight: bold;
}

.chat-last {
  font-size: 12px;
  opacity: 0.8;
}

.sidebar-footer {
  padding-top: 12px;
  border-top: 1px solid rgba(255,255,255,0.3);
  text-align: center;
}

.settings-btn {
  border: none;
  background: transparent;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

/* Chat 主区 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.05);
  border-left: 1px solid rgba(0, 0, 0, 0.05);
}

.chat-header {
  padding: 12px;
  background: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid #ddd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.chat-title {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.settings-panel {
  position: absolute;
  top: 50px;
  right: 20px;
  width: 250px;
  background: rgba(255,255,255,0.95);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 10;
}

.settings-panel h3 {
  margin: 0 0 12px;
  font-size: 16px;
}

.setting-item {
  margin-bottom: 12px;
  font-size: 14px;
}

.close-settings {
  border: none;
  background: #4e54c8;
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: rgba(255, 255, 255, 0.7);
}

.message {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  max-width: 60%;
}

.message-list-enter-active, .message-list-leave-active {
  transition: all 0.3s ease;
}
.message-list-enter-from, .message-list-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.message.them {
  flex-direction: row;
}

.message.me {
  flex-direction: row-reverse;
  margin-left: auto;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.message-content {
  display: flex;
  flex-direction: column;
  margin: 0 8px;
}

.message-text {
  padding: 8px 12px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.message.me .message-text {
  background: #dcf8c6;
}

.message-date {
  font-size: 10px;
  margin-top: 4px;
  color: #999;
  align-self: flex-end;
}

.chat-input {
  padding: 8px;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
}

.icon-row {
  display: flex;
  margin-bottom: 6px;
}

.icon-btn {
  border: none;
  background: transparent;
  font-size: 22px;
  cursor: pointer;
  margin-right: 12px;
}

.emoji-panel {
  display: flex;
  flex-wrap: wrap;
  background: #fff;
  padding: 8px;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  margin-bottom: 6px;
}

.emoji-item {
  font-size: 20px;
  padding: 4px;
  cursor: pointer;
  margin: 2px;
}

.input-row {
  display: flex;
  align-items: center;
}

.text-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 20px;
  margin-right: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.send-btn {
  padding: 8px 16px;
  border: none;
  background: #4e54c8;
  color: #fff;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.send-btn:hover {
  background: #3b3fc1;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 999;
  }

  .chat-container {
    margin-bottom: 120px; /* 为移动端底部聊天栏留出空间 */
  }
}

.sidebar,
.chat-container,
.settings-panel,
.chat-input,
.message-text {
  /* 增加统一阴影 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.icon-btn {
  position: relative;
  font-size: 24px;
  /* 增大点击区域 */
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.file-btn input,
.emoji-btn {
  cursor: pointer;
}
</style>
