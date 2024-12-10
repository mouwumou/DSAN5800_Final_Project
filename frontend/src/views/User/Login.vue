<template>
  <Center>
    <el-form
      :model="ruleForm"
      status-icon
      :rules="rules"
      ref="ruleFormRef"
      label-width="100px"
      class="demo-ruleForm form-content formbody"
      @keyup.enter.native="submitForm('ruleFormRef')"
    >
      <el-form-item label="Username" prop="username">
        <el-input v-model="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input
          type="password"
          v-model="ruleForm.password"
          autocomplete="off"
        ></el-input>
      </el-form-item>

      <el-form-item :error="errorMsg">
        <el-button type="primary" @click="submitForm('ruleFormRef')">Submit</el-button>
        <el-button @click="resetForm('ruleFormRef')">Clear</el-button>
      </el-form-item>
    </el-form>
  </Center>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import Center from "../../components/public/Center.vue";
import { useLoginUserStore } from '@/stores/loginUser'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'

const router = useRouter()
const loginUserStore = useLoginUserStore()

// 表单验证函数
const checkUserName = (rule, value, callback) => {
  if (!value) {
    return callback(new Error("Username is required"));
  } else {
    callback();
  }
};
const validatePass = (rule, value, callback) => {
  if (value === "") {
    callback(new Error("Please input the password"));
  } else {
    callback();
  }
};

// 表单数据与规则
const ruleForm = reactive({
  username: "",
  password: "",
});
const errorMsg = ref("");
const rules = {
  username: [{ validator: checkUserName, trigger: "blur" }],
  password: [{ validator: validatePass, trigger: "blur" }],
};

// 表单引用
const ruleFormRef = ref(null);

// 页面加载时检查登陆状态，如已登陆则跳转首页
onMounted(() => {
  if (loginUserStore.data !== null) {
    router.push({ name: "Home" });
  }
});

function submitForm(formRefName) {
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {
      const payload = {
        username: ruleForm.username,
        password: ruleForm.password,
      };
      const result = await loginUserStore.login(payload);
      if (result) {
        // 登陆成功
        router.push({ name: "Home" });
      } else {
        errorMsg.value = "Username or password is incorrect";
      }
    } else {
      console.log("error submit!!");
      return false;
    }
  });
}

// 监测errorMsg变化，弹出错误提示
// watch(errorMsg, (newVal) => {
//   if (newVal) {
//     this.$message.error(newVal);
//   }
// });

function resetForm(formRefName) {
  ruleFormRef.value.resetFields();
}
</script>

<style scoped>
.form-content {
  width: 350px;
}
.formbody {
  min-width: 300px;
}
</style>
