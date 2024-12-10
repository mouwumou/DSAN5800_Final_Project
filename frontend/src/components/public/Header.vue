<template>
  <div id="header">
    <el-row type="flex" class="row-bg" justify="center">
      <el-col :span="22">
        <el-row justify="space-between" type="flex" algin="middle">
          <div class="logo-container">
            <img id="logo" alt="Vue logo" :src="logo" />
            <span>{{title}}</span>
          </div>

          <div v-if="isLogging">loading...</div>
          <div v-else-if="loginUser" class="nav-user-info">
            <!-- <div class="nav-announcement">公告</div> -->
            <el-dropdown>
              <span class="el-dropdown-link">
                <span v-if="loginUser.profile">{{ loginUser.profile.name }}</span>
                <span>{{ loginUser.username }}</span>
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item v-if="isAdmin" divided
                  >管理中心</el-dropdown-item
                >
                <el-dropdown-item divided><div @click="handleLoginOut">退出登录</div></el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
          <div v-else><el-button @click="direct_to_login">登录</el-button></div>

          <!-- <el-menu
            mode="horizontal"
            style="border-bottom: 0px; line-height: 60px"
          >
            <el-menu-item index="1">处理中心</el-menu-item>
            <el-menu-item index="2">处理中心</el-menu-item>
            <el-menu-item index="3">处理中心</el-menu-item>
            <div v-if="isLogin" class="nav-user-info">
              <el-avatar :size="50" :src="circleUrl"></el-avatar>
            </div>
            <div v-else><el-button>登录</el-button></div>
          </el-menu> -->
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      isAdmin: false,
      circleUrl:
        "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
    };
  },
  props:{
    logo: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState("loginUser", {
      loginUser: "data",
      isLogging: "isLoading",
    }),
  },
  methods: {
    direct_to_login() {
      // 如果用户登录
      // 执行一些操作
      // 跳转到登录页面
      this.$router.push({ name: "Login" });
    },
    handleLoginOut() {
      console.log("logout")
      this.$store.dispatch("loginUser/loginOut");
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style scoped>
#header {
  height: 74px;
  border-bottom: 1px solid #dcdfe6;
}

.row-bg {
  align-items: center;
  height: 100%;
}
.logo-container {
  margin: auto 0;
}

#logo {
  max-height: 46px;
  margin: auto 0;
  vertical-align: middle;
}

.nav-announcement {
  display: block;
  padding: 0 20px;
  cursor: pointer;
  position: relative;
  transition: border-color 0.3s, background-color 0.3s, color 0.3s;
  color: #909399;

  border-radius: 10px;
  margin-right: 10px;
  float: left;
  line-height: 56px;
}

.nav-announcement:hover {
  outline: none;
  color: #303133;
}
.nav-announcement .active {
  color: #303133;
}
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
  display: flex;
  align-items: center;
    margin-top: 10px;
}

.el-dropdown-link span {
  color: #606266;
  font-size: 18px;
}

.el-icon-arrow-down {
  font-size: 22px;
}
</style>