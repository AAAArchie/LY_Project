 <template>
  <el-row :gutter="20" style="margin-top:0">
    <el-col :span="24">
      <div class="grid-content   ">
        <el-carousel indicator-position="outside">
          <el-button :plain="true" @click="open">打开消息提示</el-button>
        </el-carousel>
      </div>
    </el-col>
  </el-row>
</template>

<script>

export default {
  methods: {
    Uv() {
      this.$message('这是一条消息提示');
    },
  }
}
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