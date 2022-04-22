<template>
  <div class="content">
    <el-card class="box-card">
      <el-col :span="24">
        <div class="grid-content">
          <p>
            <b>快速识别说明：</b>您可以点击下方开始快速识别按钮，随后选择您要识别的图片，经过系统处理后，最终将结果反馈给您。
            图片分辨率过大会影响识别的效率，希望您提供分辨率较低的图片，其识别的时间大概在10秒左右，请您耐心等待。
            如果您对快速识别的结果不满意，您可以尝试高级识别。
          </p>
        </div>
      </el-col>
    </el-card>

    <el-row class="handle" type="flex" :gutter="25" v-loading="loading" :data="tableData">
      <el-col :span="8" :xs="24" class="handleImageCol">
        <el-row>
          <el-button
              type="file"
              @click="upload"
              class="handleBtn"
              align="center"
              :style="{'background-color': '#CAE1FF'}">开始快速识别
          </el-button>
        </el-row>
        <el-row>
          <el-empty
              class="handleImage"
              prop="src"
              description="暂无图片"
              :image="data.result.upload_images"
          ></el-empty>
        </el-row>
      </el-col>

      <el-col :span="9" :xs="24" :offset="2">
        <el-row class="inter">
          <div class="grid-content bg-purple">
            <el-table :data="tableData" class="interTable">
              <el-table-column prop="title" label="识别结果" width="230"></el-table-column>
              <el-table-column prop="name" width="230"></el-table-column>
            </el-table>
          </div>

          <el-col :span="4" :xs="8">
            <el-button
                class="button"
                type="text"
                v-if="data.result.id"
                @click="User_assess(data.result)"
            >识别有误？
            </el-button>
          </el-col>

          <!--用于修改民族的对话框-->
          <el-dialog title="您的建议" v-model="data.dialogFormVisible">
            <el-form :model="data.form">
              <el-form-item label="我们将会认真参考您的建议：" :xs="12">
                <el-input v-model="data.form.assess" autocomplete="off" :xs="12"></el-input>
              </el-form-item>
            </el-form>
            <template #footer>
              <span class="dialog-footer">
                <el-button @click="data.dialogFormVisible = false" :xs="6">取 消</el-button>
                <el-button type="primary" @click="formFinished" :xs="6">确 定</el-button>
              </span>
            </template>
          </el-dialog>
        </el-row>
      </el-col>
    </el-row>
  </div>

</template>


<script>
import constant from "../utils/constants";
import {computed, reactive} from "vue";
import Axios from "axios";
import variables from "../utils/variables";
import {ElLoading} from 'element-plus';


export default {
  name: 'Upload',
  setup() { // 组合式函数定义

// elementUI的函数
    // 加载图片中
    let loadingCount = 0;
    let loading;
    const startLoading = () => {
      loading = ElLoading.service({
        lock: true,
        text: '识别中，请稍后，由于网络问题图片加载可能有延缓...',
        background: 'rgba(0, 0, 0, 0.7)'
      });
    };

    const endLoading = () => {
      loading.close();
    };

    const showLoading = () => {
      if (loadingCount === 0) {
        startLoading();
      }
      loadingCount += 1;
    };

    const hideLoading = () => {
      if (loadingCount <= 0) {
        return;
      }
      loadingCount -= 1;
      if (loadingCount === 0) {
        endLoading();
      }
    };

    // 常量声明
    // 直接把一般数据或对象等直接当作data对象，通过reactive直接赋值解决————封装的意思，比ref来解决一般数据类型好多了
    // ref、reactive 都是vue3的函数
    // let 声明的变量只在 let 命令所在的代码块内有效。——es6语法
    // const 声明一个只读的常量，一旦声明，常量的值就不能改变。——es6语法
    const data = reactive({
      // 对象
      result: {
        id: '',
        nation1: '',
        nation2: '',
        nation3: '',
        time: '',
        upload_images: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
      },
      // dialogFormVisible 弹窗显示的bool值
      dialogFormVisible: false,
      deleteConfirmDialogVisible: false,
      selectedImage: '',
      form: {
        assess: '',
      },
    })
    const tableData = computed(() => {
      return [
        {title: '最有可能服饰类别：', name: data.result.nation1},
        {title: '第二可能服饰类别：', name: data.result.nation2},
        {title: '第三可能服饰类别：', name: data.result.nation3},
        {title: '耗时：', name: data.result.time},
      ]
    })

// 函数编写
    // 开始上传，打开选择文件窗口
    async function upload() {
      const button = document.createElement('input')
      button.type = 'file'
      button.click()
      // 由于事件和回调函数无法满足开发者的需求，需要异步编程方案 Promise
      await new Promise(resolve => {
        //当用户改变input输入框内容时执行一段Javascript代码，onchange，有on就是代表只要改变就执行函数，HTML 元素改变
        button.onchange = resolve
      })
      showLoading();
      const url = constant.apiUrl + 'images/'
      const file = button.files[0]
      console.log(file)


      // 创建表单数据 FormData()是一个对象（WebAPI）
      const form = new FormData()
      form.append('upload_images', file)
      // token的创建
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
        'Content-Type': 'multipart/form-data',
      } : {
        'Content-Type': 'multipart/form-data',
      }
      // 定义url跟表单数据结合上token,await，代码暂停，等待axios执行完毕
      const response = await Axios.post(url, form, {
        headers
      })

      const result = response.data
      data.result.id = result.id
      data.result.nation1 = result.nation1
      data.result.nation2 = result.nation2 + "服饰"
      data.result.nation3 = result.nation3 + "服饰"
      data.result.time = result.time_consuming
      data.result.upload_images = result.upload_images
      hideLoading();
    }

    // data.result当初参数image的值，传入用户建议中
    function User_assess(image) {
      data.form.assess = image.assess
      data.selectedImage = image
      data.dialogFormVisible = true
    }

    // 表单提交，将用户建议data.form.assess赋值给常量assess，将url，headers，等转化成jwt的token并通过Axios传输到后端
    async function formFinished() {
      const assess = data.form.assess
      // es6中采用${XXX}来在字符串中插入变量
      const url = `${constant.apiUrl}images/${data.selectedImage.id}/user-assess?assess=${assess}`
      // 登录的token有没有，有则返回包含token的，否则相反
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
        'Content-Type': 'multipart/form-data',
      } : {
        'Content-Type': 'multipart/form-data',
      }
      alert(headers)
      await Axios.get(url, {
        headers
      })
      // 传输完成后将弹窗显示关闭
      data.dialogFormVisible = false
    }

    return {data, tableData, upload, User_assess, formFinished}  // 这里返回的任何内容都可以用于组件的其余部分
  },
}
</script>


<style scoped>
.content {
  max-width: 1200px;
  margin: 0 auto;
}

.handle {
  margin-top: 24px;
}

.handleImageCol {
  max-width: 500px;
}

.handleBtn {
  width: 100%;
  /* 设置按钮高度 */
}

.handleImage {
  padding-top: 0;
}

.handleImage :deep(.el-empty__image) {
  width: 100%;
}

.inter {
  margin-top: 43px;
}

.interTable::before {
  content: none;
}

.el-row {
  margin-bottom: 20px;
}

.el-row :last-child {
  margin-bottom: 0;
}

.bg-purple {
  background: #d3dce6;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
