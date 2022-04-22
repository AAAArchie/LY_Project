// 整个项目的入口文件
// 引入一个名为createdApp的工厂函数
import {createApp} from 'vue'
import './themes/index.css'
// 引入APP组件，它是所有组件的父组件
import App from './App.vue'
import router from './utils/router'

// @ts-ignore
// 引入elementui组件库
import ElementPlus, {ElIcon} from 'element-plus';
// 引入elementui全部样式
import 'element-plus/lib/theme-chalk/index.css';
// 将app组件放入容器中，创建应用实例对象，用.mount挂载
const app = createApp(App).use(router).use(ElementPlus).use(ElIcon).mount('#app')
