<template>
  <SidebarTemplate>
    <el-row>
    <el-col :span="18">
      <HomeBody />
    </el-col>
    <el-col :span="5" :offset="1">
      <UserInfoCard />
    </el-col></el-row>
  </SidebarTemplate>
</template>

<script>
import SidebarTemplate from "../components/public/SidebarTemplate.vue";
import HomeBody from "../components/HomeBody.vue";
import UserInfoCard from "../components/Home/UserInfoCard.vue";
export default {
  components: {
    SidebarTemplate,
    HomeBody,
    UserInfoCard,
  },
};
</script>

<style scoped>
</style>