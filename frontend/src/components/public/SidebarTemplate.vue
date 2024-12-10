<template>
  <div class="body">
    <el-row>
      <Sidebar @pageSelect="pageSelect" />
      <div class="home-container">
        <el-col :span="21" :offset="1">
          <slot></slot>
        </el-col>
      </div>
    </el-row>
  </div>
</template>

<script>
import Sidebar from "./Sidebar.vue";
export default {
  components: {
    Sidebar,
  },
  data() {
    return {
    };
  },
  methods: {
    pageSelect(key) {
      this.page = key;
    },
  },
};
</script>

<style scoped>
.body {
  margin: 0px;
}

.home-container {
  margin-top: 20px;
  margin-left: 240px;
}
</style>