<template>
  <div class="sidebar">
    <el-menu
      :default-active="activePage"
      class="el-menu-vertical-demo"
      @select="handleSelect"
      background-color="#aaa"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span>Home</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-document"></i>
        <span>My Expense</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-notebook-1"></i>
        <span>Chat History</span>
      </el-menu-item>

      <el-sub-menu index="4" v-if="loginUser?.is_superuser">
        <template #title>
          <el-icon><location /></el-icon>
          <span>Manage Menu</span>
        </template>
        <el-menu-item index="4-1">Tools Management</el-menu-item>
        <el-menu-item index="4-2">User Management</el-menu-item>
      </el-sub-menu>

      <div style="height: 1200px"></div>
    </el-menu>
  </div>
</template>

<script setup>
import { ref, onMounted, watchEffect } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLoginUserStore } from '@/stores/loginUser'
import { ElIcon } from 'element-plus'
import { Location } from '@element-plus/icons-vue' 
// 如果使用的icon与此处不同，请根据实际图标名称修改引入

const router = useRouter()
const route = useRoute()
const loginUserStore = useLoginUserStore()
const loginUser = loginUserStore.data

// 路径与菜单索引对应关系
const routeMap = {
  "/": "1",
  "/expense": "2",
  "/simulation-list": "3",
  "/student-manage": "4-1",
  "/exam-manage": "4-2",
  "/testbank-manage": "4-3",
  "/home-announcement-manage": "4-4",
  "/icon-title-manage": "4-5",
}

// 菜单索引与路由名称对应关系
const routerMap = {
  1: "Home",
  2: "Expense",
  3: "SimulationList",
  "4-1": "ToolManage",
  "4-2": "UserManage",
}

const activePage = ref("1")

onMounted(() => {
  activePage.value = routeMap[route.path] || "1"
})

// 当路由变更时更新activePage
watchEffect(() => {
  activePage.value = routeMap[route.path] || "1"
})

function handleSelect(key) {
  // 如果当前路径对应的key和选择的key不同，则跳转
  const currentKey = routeMap[route.path]
  if (currentKey !== key) {
    // 根据选中的key跳转相应的路由
    if (routerMap[key]) {
      router.push({ name: routerMap[key] })
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: absolute;
  width: 240px;
}
</style>
