<template>
    <div class="container">
      <div id="announcement-container">
          <!-- <Announcement /> -->
      </div>
  
      <div id="exam-in-progress-container">
        <InfoCard :title="'My Expense Summary'">
            <ExpenseChart />
        </InfoCard>
      </div>
    </div>
  </template>
  
  <script>
  import InfoCard from "./public/InfoCard.vue";
  import ExpenseChart from "./Home/ExpenseChart.vue";
  export default {
    components: {
      InfoCard,
      ExpenseChart,
    //   Announcement,
    //   ExamContainer,
    },
  };
  </script>
  
  <style scoped>
  #announcement-container {
    margin-bottom: 30px;
  }
  
  #exam-in-progress-container {
    margin-bottom: 30px;
  }
  </style>