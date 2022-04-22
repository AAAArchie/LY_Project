<template>
  <div style="min-height: 1000px">
    <el-card style="margin-bottom: 40px">
      <el-row>
        <el-button @click="f显示旅行历史对话框">旅行历史</el-button>
      </el-row>
    </el-card>
    <el-row style="margin-bottom: 40px">

      <el-col :span="5">
        <el-image :src="girl" style="height: 600px" fit="cover"></el-image>
      </el-col>

      <el-col :span="5" :offset="1">
        <el-card style=" margin-bottom: 40px">
          <el-button @click="f上传图片(1)" style="width: 100%" :disabled="v上传完成状态.v左侧头像已完成">
            <el-image style="height: 160px" :src="data.headUrl1">
              <template #error>请点击以上传头像</template>
            </el-image>
          </el-button>
        </el-card>
        <el-card :header="data.nation1">
          <el-image style="height: 320px" :src="data.clothesUrl1">
            <template #error>图片未上传</template>
          </el-image>
          <el-button type="Default" @click="f上传图片(3)" style="width: 100%" :disabled="v上传完成状态.v左侧服饰完成">
            上传图像
          </el-button>
        </el-card>
      </el-col>

      <el-col :span="5" :offset="2">
        <el-card style=" margin-bottom: 40px">
          <el-button style="width: 100%" @click="f上传图片(2)" :disabled="v上传完成状态.v右侧头像已完成">
            <el-image style="height: 160px" :src="data.headUrl2">
              <template #error>请点击以上传头像</template>
            </el-image>
          </el-button>
        </el-card>
        <el-card :header="data.nation2">
          <el-image style="height: 320px" :src="data.clothesUrl2">
            <template #error> 图片未上传</template>
          </el-image>
          <el-button type="Default" @click="f上传图片(4)" style="width: 100%" :disabled="v上传完成状态.v右侧服饰已完成">
            上传图像
          </el-button>
        </el-card>
      </el-col>


      <el-col :span="5">
        <el-image :src="boy" style="height: 600px" fit="cover"></el-image>
      </el-col>

    </el-row>

    <el-row>
      <el-col :span="12" :offset="6">
        <el-button style="width: 100%;" @click="state.v显示地点选择对话框=true">选择旅行地点</el-button>
      </el-col>
    </el-row>

    <el-dialog modal v-model="state.v显示地点选择对话框" title="选择旅行地点">
      <el-row>
        <el-col :span="8" v-for="i in v背景图片数据">
          <el-button @click="f选择背景(i.name)">
            <el-image :src="i.url" style="padding: 20px">
              <template #error>{{ i.name }}</template>
            </el-image>
          </el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <el-dialog modal v-model="state.v显示旅行历史对话框" title="旅行历史">
      <el-row>
        <el-col :span="8" v-for="i in v旅行历史数据.data">
          <el-image :src="i.url" style="padding: 20px;height: 160px" fit="contain">
            <template #error>您尚未进行此次旅行</template>
          </el-image>
        </el-col>
      </el-row>
    </el-dialog>


  </div>
</template>


<script lang="ts">
import {computed, reactive, watchEffect} from "vue";
import {ElIcon} from "element-plus";
import constant from "../utils/constants";
import Axios from "axios";
import clients from "../utils/clients";

import boy from '../assets/images/boy.png'
import girl from '../assets/images/girl.png'
import router from "../utils/router";

export default {
  name: 'ImageMerge',
  components: {ElIcon},
  props: {
    id: {type: String, required: false}
  },
  setup: function (props: { id?: string }) {
    const v已经创建过对象 = computed(() => props.id !== undefined)

    const data = reactive({
      nation1: '请上传图片', nation2: '请上传图片', clothesUrl1: '', clothesUrl2: '',
      clothesId1: -1, clothesId2: -1, headUrl1: '', headUrl2: '',
    } as {
      nation1: string, nation2: string, clothesUrl1: string, clothesUrl2: string,
      clothesId1: number, clothesId2: number, headUrl1: string, headUrl2: string,
    })

    const state = reactive({
      v显示地点选择对话框: false,
      v显示合成结果对话框: false,
      v显示旅行历史对话框: false,
    })

    const v背景图片数据 = [...Array(7).keys()].slice(1).map(i => ({
      name: `bg${i}`, url: `${constant.host}media/background-image/bg${i}.png`
    }))

    watchEffect(async () => {
      if (!v已经创建过对象.value) return
      const response = await clients.v图片合成过程.retrieve(props.id as string)
      if (response.person_1_head_image.length) data.headUrl1 = response.person_1_head_image
      if (response.person_2_head_image.length) data.headUrl2 = response.person_2_head_image

      if (response.person_1_identification > 0) {
        data.clothesUrl1 = response.person_1_identification_detail.upload_images
        data.clothesId1 = response.person_1_identification
        data.nation1 = response.person_1_identification_detail.nation1
      }
      if (response.person_2_identification > 0) {
        data.clothesUrl2 = response.person_2_identification_detail.upload_images
        data.clothesId2 = response.person_2_identification
        data.nation2 = response.person_2_identification_detail.nation1
      }
    })

    const v上传完成状态 = reactive({
      vImage1Finished左侧头像已完成: computed(() => data.headUrl1.length > 0),
      vImage2Finished右侧头像已完成: computed(() => {
        return data.headUrl2.length > 0
      }),
      vImage3Finished左侧服饰已完成: computed(() => data.clothesUrl1.length > 0),
      vImage4Finished右侧服饰已完成: computed(() => data.clothesUrl2.length > 0),
    })

    const f跳转到登录页面 = async () => await router.push({name: 'Login'})

    /**
     * 将一张图片上传到服务器
     * @param type 1,2,3,4 表示4个上传的位置，分别为左上，右上，左下，右下
     */
    const f上传图片 = async (type: 1 | 2 | 3 | 4) => {
      // 如果没有登录，则跳转到登录页面
      if (!clients.auth.isLoggedIn) {
        await f跳转到登录页面()
        return
      }

      const v详情接口的路径 = v已经创建过对象.value ? `${constant.apiUrl}merged-images/${props.id}/` : `${constant.apiUrl}merged-images/`
      const v图像字段名 = {1: 'person_1_head_image', 2: 'person_2_head_image', 3: 'upload_images', 4: 'upload_images'}[type]
      const v图像上传路径 = {1: v详情接口的路径, 2: v详情接口的路径, 3: `${constant.apiUrl}images/`, 4: `${constant.apiUrl}images/`,}[type]

      const inputButton = document.createElement('input')
      inputButton.type = 'file'
      inputButton.click()

      // 由于事件和回调函数无法满足开发者的需求，需要异步编程方案 Promise
      // 将回调函数的方案优化为 Promise 方案
      //当用户改变input输入框内容时执行一段Javascript代码，onchange，有on就是代表只要改变就执行函数，HTML 元素改变
      await new Promise(resolve => inputButton.onchange = resolve)
      const file = inputButton.files && inputButton.files[0]
      if (!file) return

      // 创建表单数据 FormData()是一个对象（WebAPI）
      const v表单 = new FormData()
      v表单.append(v图像字段名, file)
      const headers = {
        ...{'Content-Type': 'multipart/form-data'},
        ...clients.auth.isLoggedIn ? {Authorization: 'JWT ' + clients.auth.token?.value} : undefined
      }

      // 对于四种图片分别使用不同的方案进行上传
      let v图片合成过程数据
      switch (type) {
        case 1:
        case 2: {
          const response = v已经创建过对象.value ? await Axios.patch(v图像上传路径, v表单, {headers}) : await Axios.post(v图像上传路径, v表单, {headers})
          const result = response.data
          if (type === 1) {
            data.headUrl1 = result.person_1_head_image
          } else {
            data.headUrl2 = result.person_2_head_image
          }
          v图片合成过程数据 = result
          break
        }
        case  3: {
          data.nation1 = '图片上传并处理中'
          const response = await Axios.post(v图像上传路径, v表单, {headers})
          const result = response.data
          data.clothesId1 = result.id
          data.clothesUrl1 = result.upload_images
          data.nation1 = result.nation1
          if (v已经创建过对象.value) {
            v图片合成过程数据 = await clients.v图片合成过程.patch(props.id as string, {person_1_identification: result.id as number})
          } else {
            v图片合成过程数据 = await clients.v图片合成过程.post({person_1_identification: result.id as number})
          }
          break
        }
        case 4: {
          data.nation2 = '图片上传并处理中'
          const response = await Axios.post(v图像上传路径, v表单, {headers})
          const result = response.data
          data.clothesId2 = result.id
          data.clothesUrl2 = result.upload_images
          data.nation2 = result.nation1
          if (v已经创建过对象.value) {
            v图片合成过程数据 = await clients.v图片合成过程.patch(props.id as string, {
              person_2_identification: result.id as number
            })
          } else {
            v图片合成过程数据 = await clients.v图片合成过程.post({
              person_2_identification: result.id as number
            })
          }
          break
        }
        default:
          throw "This should never be reached"
      }
      if (v图片合成过程数据.id > 0 && !v已经创建过对象.value)
        await router.push({name: 'ImageMergeDetail', params: {'id': v图片合成过程数据?.id.toString()}})
    }

    const f选择背景 = async (bgName: string) => {
      await clients.v图片合成过程.patch(props.id as string, {background_name: bgName})
      state.v显示地点选择对话框 = false
      state.v显示合成结果对话框 = true
      const response = await clients.v图片合成过程.action('merge', props.id as string)
      v旅行结果数据.url = response.result_image
    }

    const v旅行结果数据 = reactive({
      url: '',
    })

    const f显示旅行历史对话框 = async () => {
      if (!clients.auth.isLoggedIn) await f跳转到登录页面()
      state.v显示旅行历史对话框 = true
      const value = await clients.v图片合成过程.list({
        endpoint: `${constant.apiUrl}merged-images/travelled/`
      })
      let backgroundImages = [...Array(7).keys()].slice(1).map(i => ({
        name: `bg${i}`, url: '',
      }))
      v旅行历史数据.data = backgroundImages.map(i => ({
        name: i.name, url: value.results.find(j => j.background_name === i.name)?.result_image || ''
      }))
    }

    const v旅行历史数据 = reactive({
      data: [{name: 'bg1', url: ''}]
    })

    return {data: data, f上传图片, boy, girl, v上传完成状态, state, v背景图片数据, f选择背景, v旅行结果数据, f显示旅行历史对话框, v旅行历史数据}
  },
}


</script>
<style scoped></style>
