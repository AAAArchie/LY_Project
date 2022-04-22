<template>

  <div id="signup">
    <el-divider content-position="center"><h1>注册账号</h1></el-divider>
    <el-row>
      <el-col :span="6" :offset="9">
        <el-form>
          <el-form-item label="账号">
            <el-input v-model="signupName" placeholder="请输入账号"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="signupPwd" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button style="width: 100%;" @click="signup">注册</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>

</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import Axios from "axios";
import constants from "../utils/constants";
import router from "../utils/router";
import {ElMessage} from "element-plus";

export default defineComponent({
  name: 'Register',
  setup() {
    const signupName = ref('')
    const signupPwd = ref('')

    async function signup(e: any) {
      const url = constants.apiUrl + 'user/'
      const response = await Axios.post(url, {
        'username': signupName.value,
        'password': signupPwd.value,
      })
      // login(response.data)

      ElMessage({
        message: '注册成功，请登入！',
        center: true
      });
      await router.push({name: 'Login'})
    }

    return {signupName, signupPwd, signup}
  }
});
</script>


<style scoped>

</style>
