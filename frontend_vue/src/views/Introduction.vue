<template>

  <el-row :gutter="0">
    <el-col :span="19" :offset="2">
      <div class="block">
        <el-timeline>

          <el-timeline-item timestamp="2021/10/14" placement="top">
            <el-card>
              <h3 style="line-height:0">目前进展</h3>
              <el-row :gutter="0">
                <el-col :span="24">
                  <div class="grid-content ">
                    <p> 我们在原有识别类别的基础上，新增了回族、羌族、傣族、黎族、壮族、畲族和白族等服饰，目前网站可识别15类传统风格的服饰。
                      <br>与此同时，网站还新增了图像裁剪和个人中心两个功能，前者可有效的提升上传图片的识别准确率，后者则能记录用户的历史上传记录便于用户随时查阅。</p>
                  </div>
                </el-col>
              </el-row>
              <p>2021/08/01——2021/10/13</p>
            </el-card>
          </el-timeline-item>

          <el-timeline-item timestamp="2021/05/26" placement="top">
            <el-card>
              <h3 style="line-height:0">历史进程</h3>
              <el-row :gutter="10">
                <el-col :span="24">
                  <div class="grid-content ">
                    <p>目前，我们的算法可在线识别藏族、苗族、满族、彝族、朝鲜族、亻革家族和蒙古族7类传统服饰，传统服饰的识别效果与速度都达到了不错的指标;
                      <br>我们正在积极扩充识别类别并开展更多的功能测试，以求挖掘到民族服饰更深的价值，为在新时期发展和推广民族服饰文化提供技术支撑。</p>
                  </div>
                </el-col>
              </el-row>
              <p>2020/06/14——2021/05/25</p>
            </el-card>
          </el-timeline-item>

          <el-timeline-item timestamp="2019/09/30" placement="top">
            <el-card>
              <h3 style="line-height:0">前期准备</h3>
              <el-row :gutter="0">
                <el-col :span="24">
                  <div class="grid-content ">
                    <p>我们获取了大量有效数据集，不仅涉及苗族、蒙古族等类常见的传统服饰，还包括朝鲜族、亻革家族等这类罕见的服饰。
                      <br>通过分析这些服饰类别特征设计合适的算法对其进行优化处理和训练。我们期望构建一个图像特征库，数字化保存民族服饰图像特征。</p>
                  </div>
                </el-col>
              </el-row>
              <p>2019/04/15——2019/09/29 </p>
            </el-card>
          </el-timeline-item>

          <el-timeline-item timestamp="2019/04/06" placement="top">
            <el-card>
              <h3 style="line-height:0">启程</h3>
              <el-row :gutter="0">
                <el-col :span="24">
                  <div class="grid-content ">
                    <p>风格独特的传统服饰文化既美化了中国人民的物质生活，又丰富了中华民族的文化艺术宝库，是中华民族文化传承的重要载体之一。
                      <br>目前，能够帮助大众认知和了解传统服饰文化的途径大多局限于博物馆的静态展示。
                      <br>基于此，我们创建了此网站用于在线识别中国传统服饰，为中国传统服饰文化的弘扬和保护贡献一份力量。</p>
                  </div>
                </el-col>
              </el-row>
              <p>2019/04/05</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-col>
  </el-row>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import HelloWorld from '../components/HelloWorld.vue'; // @ is an alias to /src

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
