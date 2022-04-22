<template>
  <div class="content">
    <el-card class="box-card">
      <el-col :span="24">
        <div class="grid-content">
          <p>
            <b>识别说明：</b>您可以点击下方高级识别按钮，随后选择您要识别的图片，通过对图片进行裁剪，选择识别区域，系统会对图片进行处理，最终将结果反馈给您。
            图片分辨率过大会影响识别的效率，希望您提供分辨率较低的图片，其识别的时间大概在10秒左右，请您耐心等待。
          </p>
        </div>
      </el-col>
    </el-card>

    <el-row class="handle" type="flex" :gutter="25" v-loading="loading" :data="tableData">
      <el-col :span="8" :xs="24" class="handleImageCol">
        <el-row>
          <el-button
              @click="cropImageAndPredict"
              class="handleBtn"
              align="center"
              :style="{'background-color': '#CAE1FF'}">开始识别
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
          <!--裁剪图片的对话框-->
          <el-dialog
              title="裁剪图片"
              v-model="data.showCropDialog"
              width="80%">
            <vue-picture-cropper
                :boxStyle="{width: '80%', height: '80%', backgroundColor: '#f8f8f8', margin: 'auto'}"
                :img="data.cropImageUrl"
                :options="{
              viewMode: 1,
              dragMode: 'crop',
            }"/>
            <template #footer>
            <span class="dialog-footer">
              <el-button @click="data.showCropDialog = false">取 消</el-button>
              <el-button type="primary" @click="imageCropped">确 定</el-button>
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
import {computed, reactive,} from "vue";
import Axios from "axios";
import VuePictureCropper, {cropper} from 'vue-picture-cropper'
import variables from "../utils/variables";
import {ElLoading} from 'element-plus'; // 不能在左边放键值对，简写成如左


export default {
  name: 'Upload',
  components: {VuePictureCropper},
  setup() {
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

    const data = reactive({
      result: {
        id: '',
        nation1: '',
        time: '',
        nation2: '',
        nation3: "",
        upload_images: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
      },

      showCropDialog: false,
      cropImageUrl: '',

      dialogFormVisible: false,
      deleteConfirmDialogVisible: false,
      selectedImage: '',
      form: {
        assess: '',
      },

    })
    const tableData = computed(() => {
      return [
        {title: '最有可能服饰类别：', name: data.result.nation},
        {title: '第二可能服饰类别：', name: data.result.accuracy},
        {title: '第三可能服饰类别：', name: data.result.b},
        {title: '耗时：', name: data.result.time},
      ]
    })


    // 开始上传，打开选择文件窗口
    async function cropImageAndPredict() {
      const button = document.createElement('input')
      button.type = 'file'
      button.click()

      await new Promise(resolve => {
        button.onchange = resolve
      })

      const file = button.files[0]
      const arrayBuffer = await file.arrayBuffer()
      const blob = new Blob([arrayBuffer])
      data.cropImageUrl = URL.createObjectURL(blob)
      data.showCropDialog = true

    }

    async function imageCropped() {
      data.showCropDialog = false
      const blob = cropper.getBlob()
      showLoading();
      const url = constant.apiUrl + 'images/'
      const form = new FormData()
      const new_name = new Date().getTime()
      // 这里应该改一下用IP地址替代
      form.append('upload_images', blob, new_name + 'cropped.png')
      // token为空则增加
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
        'Content-Type': 'multipart/form-data',
      } : {
        'Content-Type': 'multipart/form-data',
      }
      const response = await Axios.post(url, form, {
        headers,
      })
      const result = response.data
      data.result.id = result.id
      data.result.nation1 = result.nation1 + "服饰"
      data.result.nation2 = result.nation2 + "服饰"
      data.result.nation3 = result.nation3 + "服饰"
      data.result.time = result.time_consuming
      data.result.upload_images = result.upload_images
      hideLoading();
    }


    function User_assess(image) {
      data.form.assess = image.assess
      data.selectedImage = image
      data.dialogFormVisible = true
    }

    async function formFinished() {
      const assess = data.form.assess
      const url = `${constant.apiUrl}images/${data.selectedImage.id}/user-assess?assess=${assess}`
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
        'Content-Type': 'multipart/form-data',
      } : {
        'Content-Type': 'multipart/form-data',
      }
      // 第二个参数为发送的header数据
      await Axios.get(url, {
        headers
      })
      data.dialogFormVisible = false
    }


    return {data, tableData, cropImageAndPredict, imageCropped, User_assess, formFinished}
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
