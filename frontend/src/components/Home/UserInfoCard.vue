<template>
  <div class="user-info-card">
    <div class="user-info-card-left">
      <div id="username" v-if="loginUserStore.data?.is_superuser">
        Admin User: {{ loginUserStore.data.username }}
      </div>
      <div id="username" v-else>{{ loginUserStore.data?.profile?.name }}</div>
    </div>
    <!-- <div class="user-info-card-right" v-if="!loginUserStore.data?.is_superuser">
      <div>身份证：{{ loginUserStore.data?.profile?.id_number }}</div>
      <div>考号：{{ loginUserStore.data?.username }}</div>
      <div>所属单位：{{ loginUserStore.data?.profile?.department?.name }}</div>
    </div> -->
    <div class="bottom-ui">
      <el-button
        class="change-password-button"
        @click="dialogFormVisible = true"
        plain
      >
        Change Password
      </el-button>
      <el-button class="change-password-button" plain @click="handleLoginOut">
        Quit Login
      </el-button>
    </div>

    <el-dialog
      title="Change Password"
      :width="'35%'"
      v-model="dialogFormVisible"
    >
      <el-form :model="form" :rules="rules" ref="changePasswordFormRef">
        <el-form-item
          label="Current Password"
          :label-width="formLabelWidth"
          prop="password"
        >
          <el-input v-model="form.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="New Password" :label-width="formLabelWidth" prop="npwd">
          <el-input v-model="form.npwd" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item
          label="Confirm New Password"
          :label-width="formLabelWidth"
          prop="npwd2"
        >
          <el-input v-model="form.npwd2" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetForm">Cancel</el-button>
        <el-button type="primary" @click="change_password">Confirm</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useLoginUserStore } from '@/stores/loginUser'
import { changePassword } from '@/services/userService'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const loginUserStore = useLoginUserStore()

const dialogFormVisible = ref(false)
const formLabelWidth = '120px'

const form = reactive({
  password: '',
  npwd: '',
  npwd2: '',
})

// 定义验证规则函数需要闭包访问 form
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } else if (value.length < 8 || value.length > 20) {
    callback(new Error('长度在 8 到 20 个字符'))
  } else if (value === form.password) {
    callback(new Error('旧密码不能与新密码一样'))
  } else {
    callback()
  }
}

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入新密码'))
  } else if (value !== form.npwd) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules = {
  password: [
    { required: true, message: '请输入原密码', trigger: 'change' },
  ],
  npwd: [{ validator: validatePass, trigger: 'blur' }],
  npwd2: [{ validator: validatePass2, trigger: 'blur' }],
}

const changePasswordFormRef = ref(null)

async function change_password() {
  changePasswordFormRef.value.validate(async (valid) => {
    if (valid) {
      const resp = await changePassword(form)
      if (resp.status == 202) {
        // 修改成功
        ElMessageBox.alert('修改成功！', '提示', {
          confirmButtonText: '确定',
          callback: () => {
            router.go(0)
          },
        })
      } else if (resp.status == 204) {
        ElMessageBox.alert('原密码错误', '提示', {
          confirmButtonText: '确定',
        })
      }
    } else {
      console.log('error submit!!')
      return false
    }
  })
}

function resetForm() {
  changePasswordFormRef.value.resetFields()
  dialogFormVisible.value = false
}

function handleLoginOut() {
  loginUserStore.loginOut()
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.user-info-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.user-info-card-left {
  flex-grow: 1;
  margin-bottom: 5px;
}

.user-info-card-right {
  flex-grow: 2;
  font-size: 16px;
  margin-bottom: 15px;
}

#username {
  text-align: center;
  font-size: 20px;
}

.bottom-ui button {
  width: 100%;
  margin: 0 0 10px 0;
}
</style>
