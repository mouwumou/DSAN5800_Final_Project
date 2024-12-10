<template>
  <div class="info-card">
    <div class="info-head">
      <div class="info-title">
        {{ title }}
      </div>
      <div v-if="more.url != ''" class="info-more">
        <router-link :to="{ name: more.url, params: more.params }"
          >更多>></router-link
        >
      </div>
    </div>

    <el-divider></el-divider>
    <div class="info-container"><slot></slot></div>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String, default: "最新公告" },
    more: {
      url: { type: String, default: "" },
      params: { type: Object, default: ()=> {} },
      default:()=> ({ url: "", params: ()=> {} }),
    },
  },
};
</script>

<style scoped>
.info-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-radius: 8px;
}

.info-head {
  display: flex;
  justify-content: space-between;
}

.info-title {
  font-size: 22px;
}

.info-more {
  font-size: 14px;
  align-self: center;
  cursor: pointer;
}

.info-more a {
  color: #909399;
  text-decoration: none;
}
</style>