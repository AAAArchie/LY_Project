<template>
  <div>
    <el-divider content-position="center"><h1>登录账号</h1></el-divider>
    <el-row>
      <el-col :span="6" :offset="9">
        <el-form>
          <el-form-item label="账号">
            <el-input v-model="formData.username" placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="formData.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button style="width: 100%;" @click="f登录">登录</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>

</template>

<script lang="ts">
import {defineComponent, reactive} from 'vue';
import router from "../utils/router";
import {ElMessage} from 'element-plus'
import clients from "../utils/clients";
import variables from "../utils/variables";


export default defineComponent({
  name: 'Login',
  setup() {
    const formData = reactive({username: '', password: ''})

    async function f登录() {
      if (await clients.auth.login(formData.username, formData.password)) {
        ElMessage.success({type: "success", message: '欢迎登陆本站！', center: true})
        variables.token = clients.auth.token?.value || ''
        variables.username = clients.auth.token?.userName || 'Anonymous'
        variables.userId = clients.auth.token?.userId || -1
        await router.back()
      } else {
        ElMessage.error({type: "error", message: '登陆失败', center: true})
      }
    }

    return {f登录, formData}
  }
});
</script>


<style scoped>
</style>
