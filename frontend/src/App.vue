<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { computed } from 'vue'
import { useLoginUserStore } from '@/stores/loginUser'
import ChatWidget from '@/components/ChatWidget.vue'

const loginUserStore = useLoginUserStore()
const isLoggedIn = computed(() => !!loginUserStore.data)
</script>

<template>
  <div id="app">
    <Header :logo="logo" :title="title"/>
    <div id="body">
      <router-view></router-view>
    </div>
    <!-- 只有当用户已登录时才显示ChatWidget -->
    <ChatWidget v-if="isLoggedIn" />
  </div>
</template>

<style scoped>
body {
  margin: 0;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

#body {
  margin: 0 auto;
}
</style>
