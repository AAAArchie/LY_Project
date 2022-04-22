<template>
  <el-row :gutter="20" style="margin-top:0">
    <el-col :span="24">
      <div class="grid-content   ">
        <el-carousel indicator-position="outside">
          <el-image
              style="width: 100%; height: 100%"
              :src="HomeImage" alt="empty"></el-image>
        </el-carousel>
      </div>
    </el-col>
  </el-row>

  <el-row style="margin-top:20px">
    <el-col :span="5" :offset="1" :xs="0">
      <div class="grid-content ">
        <h2>可识别服饰类别</h2>
        <el-divider></el-divider>
        <div class="block">
          <el-timeline style="margin-left:10px">
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">苗族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">彝族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">亻革家族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">朝鲜族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">蒙古族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">汉族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">回族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">壮族</p>
            </el-timeline-item>
          </el-timeline>
        </div>


        <el-col :span="0" :offset="10" style="margin-top:-417px">
          <el-timeline>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">藏族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">羌族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">傣族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">白族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">满族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">畲族</p>
            </el-timeline-item>
            <el-timeline-item timestamp="" placement="top">
              <p style="margin-top:-13px">黎族</p>
            </el-timeline-item>
          </el-timeline>
        </el-col>

      </div>
    </el-col>

    <el-col :span="14" :offset="3" :xs="{span: 12, offset: 0}">
      <h2>操作说明：</h2>
      <el-divider></el-divider>
      <ol style="line-height:2;">
        <li>如果您想快速识别图片，点击上方快速识别按钮，系统会对您选择的图片进行识别；</li>
        <li>如果您对快速识别的结果不满意，您可以尝试高级识别，系统会对您选择的图片进行识别；</li>
        <li>如果您满意识别结果，您可以选择注册，系统会将历史记录果保存；</li>
        <li>如果您对识别的结果不满意，您可以提出您的建议，我们将会认真参考；</li>
        <li>如果您想更多的了解本项目，您可以联系我们 minzfs@163.com；</li>
        <li>后续功能还在更新中。</li>
      </ol>

    </el-col>
  </el-row>


</template>

<script lang="ts">
import {defineComponent} from 'vue';
import HelloWorld from '../components/HelloWorld.vue'; // @ is an alias to /src
import HomeImage from '../assets/images/MOSAIC3.png'

export default defineComponent({
  name: 'Home',
  components: {
    HelloWorld,
  },
  data() {
    return {
      currentDate: new Date(),
      src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      homeSrc: '',
      processSrc: '',
      memberSrc: '',
      HomeImage,
    };
  },

});
</script>


<style>
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}
</style>
