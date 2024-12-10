<template>
    <div style="padding: 20px;">
      <h2>Expense Summary</h2>
      <el-button type="primary" @click="loadData" style="margin-bottom: 20px;">Reload Data</el-button>
      
      <div v-if="loading" style="text-align:center;">正在加载数据...</div>
      <div v-else-if="errorMessage" style="color:red;text-align:center;">{{ errorMessage }}</div>
      <div v-else style="width: 600px; height: 400px; margin: 0 auto;">
        <v-chart :option="chartOption" style="width: 100%; height: 100%;"></v-chart>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import axios from 'axios'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { BarChart } from 'echarts/charts'
  import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
  import { useLoginUserStore } from '@/stores/loginUser' // 如果需要根据登录状态判断
  import { ElButton } from 'element-plus'
  import VChart from 'vue-echarts'
  
  // 注册组件
  use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, LegendComponent])
  
  const loading = ref(false)
  const errorMessage = ref('')
  const expenseData = ref([])
  
  // 从 localStorage 获取 token
  function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: {
        authorization: `Bearer ${token}`
      }
    };
  }
  
  async function loadData() {
    loading.value = true
    errorMessage.value = ''
    try {
      const resp = await axios.get('/api/expense/expense_summary', getAuthHeaders())
      expenseData.value = resp.data
    } catch(err) {
      console.error(err)
      errorMessage.value = '加载汇总数据失败'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadData()
  })
  
  const categories = computed(() => expenseData.value.map(item => item.category__name || '未分类'))
  const data = computed(() => expenseData.value.map(item => item.total_spending || 0))
  
  const chartOption = computed(() => ({
    title: {
      text: '各分类消费总额'
    },
    tooltip: {
      trigger: 'axis',
      formatter: params => {
        // params是一个数组，显示x轴对应的数据的tooltip信息，这里只会有一个系列
        const info = params[0]
        return `${info.marker}${info.name}: ${info.value}`
      }
    },
    xAxis: {
      type: 'category',
      data: categories.value
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '总消费',
        type: 'bar',
        data: data.value,
        barWidth: '50%',
        itemStyle: {
          color: '#409eff'
        }
      }
    ]
  }))
  
  </script>
  
  <style scoped>
  </style>
  