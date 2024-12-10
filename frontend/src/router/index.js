import { createRouter, createWebHistory } from 'vue-router'
import config from './config.js'
import { useLoginUserStore } from '../stores/loginUser.js'

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: config
})

router.beforeEach((to, from, next) => {
  const loginUserStore = useLoginUserStore()

  if (!to.meta.director) {
    // 判断登陆状态
    if (loginUserStore.isLoading) {
      next({
        name: "Auth",
        query: { returnUrl: to.fullPath }
      })
    } else if (loginUserStore.data) {
      // 已登陆用户
      next();
    } else {
      // 未登陆
      next({ name: "Login" });
    }
  } else {
    next();
  }
})

export default router
