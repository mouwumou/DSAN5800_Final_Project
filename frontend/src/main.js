import './assets/main.css'

import { createApp } from 'vue'
// import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'
import store from './stores'

import { useLoginUserStore } from '@/stores/loginUser'

const app = createApp(App)

app.use(store)
app.use(router)


const loginUserStore = useLoginUserStore()
loginUserStore.whoAmI()

app.use(ElementPlus)
app.mount('#app')
