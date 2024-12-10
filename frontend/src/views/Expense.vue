<template>
    <SidebarTemplate>
    <div class="expense-page" style="padding: 20px;">
      <h2>My Expense History</h2>
      <div class="filter-bar" style="margin-bottom: 20px; display:flex; gap:10px;">
        <el-input
          placeholder="Filter by category"
          v-model="category"
          style="width: 200px;"
          clearable
        ></el-input>
        <el-button type="primary" @click="filterByCategory">Filter by category</el-button>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          start-placeholder="start date"
          end-placeholder="end date"
          format="yyyy-MM-dd"
          value-format="yyyy-MM-dd"
        ></el-date-picker>
        <el-button type="primary" @click="filterByDateRange">Filter by Date</el-button>
        <el-button @click="loadAllExpenses">Reset</el-button>
      </div>
  
      <el-table :data="expenses" style="width: 100%">
        <!-- <el-table-column prop="id" label="ID" width="50"/> -->
        <el-table-column prop="category" label="Category" width="150"/>
        <el-table-column prop="amount" label="Amount" width="100"/>
        <el-table-column prop="expense_date" label="Date" width="150"/>
        <el-table-column prop="merchant" label="Merchant" width="150"/>
        <el-table-column prop="description" label="Description"/>
      </el-table>
  
      <div v-if="loading" style="text-align:center;margin-top:20px;">
        <el-loading text="Loading..." />
      </div>
      <div v-else-if="errorMessage" style="color:red;text-align:center;margin-top:20px;">
        {{ errorMessage }}
      </div>
    </div>
</SidebarTemplate>
  </template>
  

  <script setup>
  import { ref, onMounted } from 'vue'
  import { ElMessage } from 'element-plus'
  import { getAllExpenses, filterExpenseByCategory, filterExpenseByDateRange } from '@/services/expenseService'
  import {dateFormat} from '@/components/public/utils'
  
  import SidebarTemplate from "../components/public/SidebarTemplate.vue";
  const expenses = ref([])
  const loading = ref(false)
  const errorMessage = ref('')
  const category = ref('')
  const dateRange = ref([])
  
  async function loadAllExpenses() {
    loading.value = true
    errorMessage.value = ''
    try {
      const data = await getAllExpenses()
      expenses.value = data
    } catch(err) {
      errorMessage.value = 'Failed to load expense history'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
  
  async function filterByCategory() {
    if (!category.value) {
      ElMessage.warning('Please input category keyword first')
      return
    }
    loading.value = true
    errorMessage.value = ''
    try {
      const data = await filterExpenseByCategory(category.value)
      expenses.value = data
    } catch(err) {
      errorMessage.value = 'Failed to filter by category'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
  
  async function filterByDateRange() {
    if (!dateRange.value || dateRange.value.length !== 2) {
      ElMessage.warning('Please select start and end date')
      return
    }
    const [start_date, end_date] = dateRange.value
    loading.value = true
    errorMessage.value = ''
    try {
      const data = await filterExpenseByDateRange(start_date, end_date)
      expenses.value = data
    } catch(err) {
      errorMessage.value = 'Failed to filter by date range'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadAllExpenses()
  })
  </script>
  
  <style scoped>
  .expense-page {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
  }
  </style>
  