<template>
    <div>
      <!-- 悬浮按钮 -->
      <div class="chat-widget-floating-button" @click="toggleChatWindow">
        <el-icon>
          <chat-round />
        </el-icon>
      </div>
  
      <!-- 对话窗口 -->
      <transition name="fade">
        <div class="chat-widget-window" v-if="isOpen">
          <div class="chat-widget-header">
            <span>客服对话</span>
            <el-button icon="el-icon-close" circle @click="toggleChatWindow" class="close-btn"></el-button>
          </div>
          <div class="chat-widget-content">
            <!-- 聊天记录区域 -->
            <div v-for="(msg, index) in messages" :key="index" class="chat-message" :class="msg.sender === 'user' ? 'user-message' : 'agent-message'">
              <!-- 文本消息 -->
              <div v-if="msg.type === 'text'">{{ msg.content }}</div>
              <!-- 图片消息 -->
              <div v-else-if="msg.type === 'image'">
                <img :src="msg.content" alt="图片" style="max-width: 150px; border-radius:4px;" />
              </div>
            </div>
          </div>
          <div class="chat-widget-input">
            <el-input
              type="textarea"
              v-model="inputValue"
              placeholder="输入你的问题..."
              class="chat-input"
              @keyup.enter="sendMessage"
            ></el-input>
            <div class="input-actions">
              <el-upload
                class="upload-btn"
                action="/api/upload-image"
                :headers="getAuthHeaders()"
                :show-file-list="false"
                name="file"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
              >
                <el-button type="text" icon="el-icon-picture" />
              </el-upload>
              <el-button type="primary" @click="sendMessage">发送</el-button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { ChatRound } from '@element-plus/icons-vue'
  
  const isOpen = ref(false)
  const inputValue = ref('')
  const messages = reactive([
    { sender: 'agent', type: 'text', content: '您好，请问有什么能帮助您的吗？' },
    { sender: 'user', type: 'text', content: '我想了解一下关于您服务的更多信息。' },
  ])
  
  function toggleChatWindow() {
    isOpen.value = !isOpen.value
  }
  
  // 模拟获取token的函数。实际项目中请根据你的逻辑实现
  function getToken() {
    return localStorage.getItem('token')
  }
  
  function getAuthHeaders() {
    const token = getToken()
    return {
      authorization: `Bearer ${token}`
    }
  }
  
  function sendMessage() {
    const content = inputValue.value.trim()
    if (!content) {
      ElMessage.warning('请输入要发送的内容')
      return
    }
    // 将用户消息加入messages
    messages.push({ sender: 'user', type: 'text', content: content })
    inputValue.value = ''
  
    // 此处可以调用后端接口传递用户消息，并将返回的回复加入messages
    // 这里先省略后端逻辑，只展示UI效果
    setTimeout(() => {
      messages.push({ sender: 'agent', type: 'text', content: '好的，我正在处理你的请求...' })
    }, 1000)
  }
  
  function handleUploadSuccess(response, file) {
    // 假设后端返回的response中包含图片的访问地址，如 response.fileUrl
    // 根据你的实际接口响应修改此处逻辑
    if (response && response.fileUrl) {
      // 将用户上传的图片消息加入messages
      messages.push({ sender: 'user', type: 'image', content: response.fileUrl })
      // 此处同样可以向后端发送此图片消息，并根据回复做相应处理
      setTimeout(() => {
        messages.push({ sender: 'agent', type: 'text', content: '我已收到您的图片。' })
      }, 1000)
    } else {
      ElMessage.error('图片上传失败，服务器未返回有效地址')
    }
  }
  
  function handleUploadError(err, file) {
    ElMessage.error('图片上传失败')
    console.error('Upload error:', err)
  }
  </script>
  
  <style scoped>
  .chat-widget-floating-button {
    position: fixed;
    right: 20px;
    bottom: 20px;
    background-color: #409eff;
    border-radius: 50%;
    padding: 15px;
    color: #fff;
    cursor: pointer;
    box-shadow: 0 2px 12px rgba(0,0,0,.1);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color .3s;
  }
  .chat-widget-floating-button:hover {
    background-color: #66b1ff;
  }
  
  .chat-widget-window {
    position: fixed;
    right: 20px;
    bottom: 80px;
    width: 300px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,.1);
    display: flex;
    flex-direction: column;
    height: 400px;
    overflow: hidden;
  }
  
  .chat-widget-header {
    background: #409eff;
    color: #fff;
    padding: 10px;
    display:flex;
    align-items:center;
    justify-content: space-between;
  }
  
  .chat-widget-header .close-btn {
    color: #fff;
  }
  
  .chat-widget-content {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    background: #f0f0f0;
    display: flex;
    flex-direction: column;
  }
  
  .chat-message {
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 10px;
    max-width: 80%;
    word-wrap: break-word;
  }
  .user-message {
    background: #409eff;
    color: #fff;
    align-self: flex-end;
  }
  .agent-message {
    background: #fff;
    color: #333;
    align-self: flex-start;
  }
  
  .chat-widget-input {
    padding: 10px;
    background: #fff;
    border-top: 1px solid #ddd;
    display:flex;
    align-items: flex-start;
    gap:10px;
  }
  
  .chat-input {
    flex:1;
  }
  
  .input-actions {
    display:flex;
    flex-direction: column;
    gap:5px;
  }
  
  .upload-btn {
    padding:0;
    margin:0;
    line-height: 1;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity .3s;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  </style>
  