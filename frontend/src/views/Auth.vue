<template>
  <Center>
    <h1>登陆验证中....</h1>
    <el-button @click="stuckMethod">回到登录界面</el-button>
  </Center>
</template>

<script setup>
import Center from "../components/public/Center.vue";
import { useLoginUserStore } from "@/stores/loginUser";
import { useRoute, useRouter } from 'vue-router'
import { watch } from 'vue'

const loginUserStore = useLoginUserStore()
const route = useRoute()
const router = useRouter()

function handleLogin() {
  if (loginUserStore.isLoading) {
    return;
  }
  if (loginUserStore.data) {
    if (route.query.returnUrl) {
      router.push(route.query.returnUrl);
    } else {
      router.push({ name: "Home" });
    }
  } else {
    router.push({ name: "Login" });
  }
}

function stuckMethod() {
  loginUserStore.loginOut();
  router.push({ name: "Login" });
}

// watch data 和 isLoading 的变化，并立即执行
watch(
  () => loginUserStore.data,
  () => {
    handleLogin();
  },
  { immediate: true }
);

watch(
  () => loginUserStore.isLoading,
  () => {
    handleLogin();
  },
  { immediate: true }
);
</script>

<style scoped>
h1 {
  font-size: 2em;
}
span {
  text-align: center;
  margin: auto
}
</style>
