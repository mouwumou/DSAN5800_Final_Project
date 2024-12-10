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
            <span>Chat</span>
            <el-button icon="el-icon-close" circle @click="toggleChatWindow" class="close-btn"></el-button>
          </div>
          <div class="chat-widget-content">
            <!-- 聊天记录区域 -->
            <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="message.type + '-message'">
              {{ message.text }}
            </div>
            <div v-if="loadingAgentResponse" class="chat-message agent-message">
              Thinking...
            </div>
          </div>
          <div class="chat-widget-input">
            <el-input
              type="textarea"
              v-model="inputValue"
              placeholder="Please enter ..."
              @keyup.enter="sendMessage"
            ></el-input>
            <el-button type="primary" @click="sendMessage">Send</el-button>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { ElMessage } from 'element-plus'
  import { ChatRound } from '@element-plus/icons-vue'
  import { sendQueryToAgent } from '@/services/agentService' // 请根据实际路径修改
  
  const isOpen = ref(false)
  const inputValue = ref('')
  const messages = ref([
    { text: 'Hi, I am a personal financial manager, how can I help you?', type: 'agent' }
  ])
  const loadingAgentResponse = ref(false)
  
  function toggleChatWindow() {
    isOpen.value = !isOpen.value
  }
  
  async function sendMessage() {
    if (!inputValue.value.trim()) {
      ElMessage.warning('Please enter your query')
      return
    }
    // 用户消息加入对话中
    const userMessage = { text: inputValue.value, type: 'user' }
    messages.value.push(userMessage)
    const query = inputValue.value
    inputValue.value = ''
  
    // 向后端发送请求
    try {
      loadingAgentResponse.value = true
      const resp = await sendQueryToAgent(query)
      // resp为后端返回的响应数据，根据你的后端返回结构对以下逻辑做适当修改
      console.log(resp)
      const agentResponseText = (Array.isArray(resp.response) && resp.response[0] && resp.response[0].output)
      ? resp.response[0].output
      : 'I am sorry, I am not able to help you with that.'
      messages.value.push({ text: agentResponseText, type: 'agent' })
    } catch (err) {
      console.error(err)
      messages.value.push({ text: 'I am sorry, there is a newwork error.', type: 'agent' })
    } finally {
      loadingAgentResponse.value = false
    }
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
    margin-left: auto;
  }
  
  .agent-message {
    background: #fff;
    color: #333;
  }
  
  .chat-widget-input {
    padding: 10px;
    background: #fff;
    border-top: 1px solid #ddd;
    display:flex;
    gap:10px;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity .3s;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  </style>
  