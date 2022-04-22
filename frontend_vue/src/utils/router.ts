import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router'
import Home from '../views/Home.vue'
// import Upload from "../views/SimpleRecognition.vue";
// import Introduction from "../views/Introduction.vue";
import Recognition from "../views/CropRecognition.vue";
import ImageMerge from "../views/ImageMerge.vue";
import UserCenter from "../views/UserCenter.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import List from "../views/List.vue";
// import Modify from "../views/Modify.vue";
// import Gather from "../views/Gather.vue";


const routes: Array<RouteRecordRaw> = [
    {path: '/', name: 'Home', component: Home},
    // {path: '/upload', name: 'Upload', component: Upload},
    {path: '/list', name: 'List', component: List},
    // {path: '/introduction', name: 'Introduction', component: Introduction},
    {path: '/recognition', name: 'Recognition', component: Recognition},
    {path: '/image-merge', name: 'ImageMerge', component: ImageMerge},
    {path: '/image-merge/:id', name: 'ImageMergeDetail', component: ImageMerge, props: true},
    {path: '/login', name: 'Login', component: Login},
    {path: '/register', name: 'Register', component: Register},
    {path: '/userCenter', name: 'UserCenter', component: UserCenter},
    // {path: '/gather', name: 'Gather', component: Gather},
    // {path: '/modify', name: 'Modify', component: Modify},
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router
