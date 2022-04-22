<template>
    <div>
    <el-divider content-position="center"><h1>登录账号</h1></el-divider>
    <el-row>
      <el-col :span="6" :offset="9">
        <el-form>
          <el-form-item label="新密码">
            <el-input v-model="data.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button style="width: 100%;" @click="updatePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {reactive} from "vue";
import constant from "../utils/constants";
import Axios from "axios";
import {ElMessage} from "element-plus";
import variables from "../utils/variables";


export default {
  name: 'UserCenter',
  setup() {
    const data = reactive({
      password: '',
    })

    async function updatePassword() {
      const url = `${constant.apiUrl}user/${variables.userId}/`
      const headers = {Authorization: `JWT ${variables.token}`}
      try {
        const response = await Axios.patch(url, {
          'password': data.password,
        }, {
          headers
        })
        ElMessage('密码已修改')
      } catch (e) {
        ElMessage('密码修改失败')
      }
    }

    return {data, updatePassword}
  },
}
</script>

<style scoped>
</style>
