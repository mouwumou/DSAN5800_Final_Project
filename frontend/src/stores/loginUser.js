// useLoginUserStore.js
import { defineStore } from 'pinia'
import { login, logOut, whoAmI } from '@/services/userService'

export const useLoginUserStore = defineStore('loginUser', {
  state: () => ({
    data: null,
    isLoading: false,
  }),
  actions: {
    async login(payload) {
      this.isLoading = true;
      const resp = await login(payload);
      let result = false;
      if (resp.status === 200) {
        const token = resp.data.access;
        if (token) {
          localStorage.setItem("token", token);
        }
        const resp2 = await whoAmI();
        if (resp2) {
          this.data = resp2.data;
        }
        result = true;
      }
      this.isLoading = false;
      return result;
    },
    async whoAmI() {
      this.isLoading = true;
      const resp = await whoAmI();
      if (resp) {
        this.data = resp.data;
      }
      this.isLoading = false;
    },
    loginOut() {
      logOut();
      this.data = null;
    }
  }
})
