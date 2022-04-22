<template>
  <div class="about">
    <h1>往日识别图片</h1>
  </div>
  <el-space wrap>
    <div>
      <el-row type="flex" :gutter="20">·
        <el-col :span="4" :xs="8" v-for="image in data.images" :key="image.id">
          <div class="grid-content bg-purple">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="image.upload_images" class="image">
              <div style="padding: 14px;">
                <span v-if="image.modified_nation">{{ image.modified_nation }}</span>
                <span v-else>{{ image.nation }}</span>

                <div class="bottom">
                  <el-button class="button" type="text" @click="modifyNation(image)">修改</el-button>
                  <el-button type="text" @click="openConfirmDeleteDialog(image)">删除</el-button>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </el-space>

  <!--用于修改民族的对话框-->
  <el-dialog title="修正民族" v-model="data.dialogFormVisible">
    <el-form :model="data.form">
      <el-form-item label="修正后的民族" :xs="12">
        <el-input v-model="data.form.newName" autocomplete="off" :xs="12"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
    <span class="dialog-footer">
      <el-button @click="data.dialogFormVisible=false" :xs="6">取 消</el-button>
      <el-button type="primary" @click="formFinished" :xs="6">确 定</el-button>
    </span>
    </template>
  </el-dialog>

  <!--用于确认删除的对话框-->

  <el-dialog title="提示" v-model="data.deleteConfirmDialogVisible " width="30%">
    <span>确认删除？</span>
    <template #footer>
    <span class="dialog-footer">
      <el-button @click="data.deleteConfirmDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="deleteConfirmed">确 定</el-button>
    </span>
    </template>
  </el-dialog>

</template>


<script lang="ts">
import {defineComponent, reactive} from 'vue';
import Axios from "axios";
import constant from "../utils/constants";
import variables from "../utils/variables"; // @ is an alias to /src

export default defineComponent({
  setup() {
    const stubImageData = {
      id: 1, nation: '',
      modified_nation: '',
      upload_images: '',
    }
    const data = reactive({
      images: [stubImageData],
      dialogFormVisible: false,
      deleteConfirmDialogVisible: false,
      selectedImage: stubImageData,
      form: {
        newName: '',
      },
    });

    async function loadAllImages() {
      const url = constant.apiUrl + 'images/'
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
      } : {}
      const response = await Axios.get(url, {
        headers
      })
      data.images = response.data
    }

    loadAllImages()

    function modifyNation(image: any) {
      data.dialogFormVisible = true
      data.form.newName = image.nation
      data.selectedImage = image
    }

    async function formFinished() {
      const newName = data.form.newName
      const url = `${constant.apiUrl}images/${data.selectedImage.id}/change-nation?name=${newName}`
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
      } : {}
      await Axios.get(url, {
        headers
      })
      await loadAllImages()
      data.dialogFormVisible = false
    }


    async function openConfirmDeleteDialog(image: any) {
      data.selectedImage = image
      data.deleteConfirmDialogVisible = true;
    }

    async function deleteConfirmed() {  // 打包请求，转化为jwt的token，通过Axios传输到后台删除
      const url = `${constant.apiUrl}images/${data.selectedImage.id}`
      const headers = variables.token !== '' ? {
        Authorization: 'JWT ' + variables.token,
      } : {}
      await Axios.delete(url, {
        headers
      })
      await loadAllImages()
      data.deleteConfirmDialogVisible = false
    }

    return {data, modifyNation, formFinished, openConfirmDeleteDialog, deleteConfirmed}
  }
});
</script>


<style>
.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  width: 100%;
  min-height: auto;
}

.image {
  width: 100%;
  display: block;
}
</style>
