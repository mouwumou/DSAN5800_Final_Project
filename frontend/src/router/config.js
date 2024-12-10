// config.js
export default [
    {
      path: "/",
      name: "Home",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      path: "/expense",
      name: "Expense",
      component: () => import("@/views/Expense.vue"),
    },
    {
      path: "/login",
      name: "Login",
      component: () => import("@/views/User/Login.vue"),
      meta: {
        director: true,
      },
    },
    {
      path: "/auth",
      name: "Auth",
      component: () => import("@/views/Auth.vue"),
      meta: {
        director: true,
      },
    },
  ];
  