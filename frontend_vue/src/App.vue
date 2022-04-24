<template>
  <!--vue3中的模板结构可以没有根标签-->
  <div id="app">
    <el-container>
      <el-col :xs="40" :sm="24" >
        <el-header>
          <el-menu :default-active="$route.path" class="el-menu-vertical-demo" mode="horizontal" router>
         <!--    <el-menu-item index="/Introduction"><i class="el-icon-user-solid"></i><span
                class="hidden-sm-and-down">项目介绍</span>
            </el-menu-item>-->

          <el-menu-item index="/"><i class="el-icon-house"></i><span class="hidden-sm-and-down">主页</span>
            </el-menu-item>
          <!--<el-menu-item  index="/Gather" class="hidden-sm-and-down"><i class="el-icon-edit"></i><span class="hidden-sm-and-down">收集图片</span></el-menu-item>-->
          <!--  <el-menu-item index="/Upload"> <i class="el-icon-camera-solid"></i><span class="hidden-sm-and-down">快速识别</span>
            </el-menu-item>-->
            <el-menu-item index="/Recognition">
              <i class="el-icon-crop"></i><span class="hidden-sm-and-down">服饰识别</span>
            </el-menu-item>
            <el-menu-item index="/image-merge" v-if="authState.isLogin">
              <i class="el-icon-crop"></i><span class="hidden-sm-and-down">风景照合成</span>
            </el-menu-item>
            <el-menu-item index="/List" v-if="authState.isLogin">
              <i class="el-icon-tickets"></i><span class="hidden-sm-and-down">历史记录</span>
            </el-menu-item>
            <el-menu-item index="/UserCenter" v-if="authState.isLogin">
              <i class="el-icon-user"></i><span class="hidden-sm-and-down">{{ authState.userName }}</span>
            </el-menu-item>
            <el-menu-item index="/Login" v-if="!authState.isLogin">登录</el-menu-item>
            <el-menu-item index="/Register" v-if="!authState.isLogin">注册</el-menu-item>
            <el-menu-item @click="f登出" v-if="authState.isLogin">退出登录</el-menu-item>
            <el-menu-item index="/Uv">
              <el-button :plain="true" @click="Uv">访客量</el-button></el-menu-item>
          </el-menu>
        </el-header>
      </el-col>

      <!--Main-->
      <el-main :xs="24">
        <router-view></router-view>
      </el-main>
      <!--Footer-->
      <el-footer>
       <!-- <el-affix position="bottom" :offset="0">
          <div id="footer">
            <span>www.minzufs.cn  Powered by 桂ICP备19009776号</span>
          </div>
        </el-affix>-->
      </el-footer>

    </el-container>
  </div>

</template>

<script lang="ts">
// 这里这个defineComponent可以理解为是vue3的一个格式文本，就必须这么写就完事儿了
import {computed, defineComponent} from "vue";
import 'element-plus/lib/theme-chalk/display.css';
import router from "./utils/router";
import clients from "./utils/clients";


export default defineComponent({
  name: 'Home',
  setup() {
    const authState = computed(() => clients.auth.vueMonitor() && {
      isLogin: clients.auth.isLoggedIn,
      fullName: clients.auth.token?.fullName,
      userName: clients.auth.token?.userName,
    })
    const f登出 = async () => {
      await clients.auth.logout()
      await router.push({'name': 'Home'})
    }
    // 返回对象（数据，方法等）渲染界面
    return {authState, f登出}
  }
});

</script>


<style>


#footer {

  left: 0;
  bottom: 0;
  height: 50px;
  width: 100%;
  background: whitesmoke;
  text-align: center;
  font-weight: bold;
}
</style>
