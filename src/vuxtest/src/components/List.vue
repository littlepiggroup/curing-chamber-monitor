<template>
  <div id="list">
    <div v-show="$store.state.routerName != 'Collect'" class="title">项目列表</div>
    <div class="weui-panel__bd" v-for="(v,index) in this.$store.state.listData">
      <a href="javascript:void(0)" @click="showDetail" class="weui-media-box weui-media-box_appmsg">
        <div class="weui-media-box__hd" @click.stop ="inputClick($event,index)">
          <img :src="'http://127.0.0.1:8000/'+v.image_url" alt="" class="weui-media-box__thumb" :id="'img'+index">
          <form id='form'>
            <input :id="'whole'+index" type="file" style="display: none;" accept="image/*" name="file" @change="previewImg(index, v.project_id)" >
          </form>
        </div>
        <div class="weui-media-box__bd">
          <div class="collect">
            <h4 class="weui-media-box__title">{{v.project_name}}</h4>
            <p class="collect_word" @click.stop="collect">收藏</p>
          </div>
          <p class="company_name">{{v.company_name}}</p>
          <div class="stateBtn">
            <div :class="v.temperature_alert_count?'alert':''" class="warn">
              温度
            </div>
            <div :class="v.humidity_alert_count?'alert':''" class="warn">
              湿度
            </div>
            <div :class="v.video_alert_count?'alert':''" class="warn">
              视频
            </div>
            <div :class="v.sample_alert_count?'alert':''" class="warn">
              试件
            </div>
          </div>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'list',
    data: () => {
      return ({

      })
    },
    created () {
      switch (this.$store.state.routerName) {
        case 'Overview':
          // console.log(123456)
          // this.$http.get('/api/project_phase_report').then((res) => {
          //   this.$store.state.listData = res.data.results
          // }).catch((error) => {
          //   console.log(error)
          // })
          break
        case 'ItemList':
          // console.log(2222222222)
          // this.$http.get('/api/projects').then((res) => {
          //   this.$store.state.listData = res.data.results
          // }).catch((error) => {
          //   console.log(error)
          // })
          break
      }
    },
    methods: {
      showDetail () {
        this.$router.push({path: '/Details'});
        this.$store.state.routerName = 'Details'
      },
      inputClick (e, index) {
        document.getElementById('whole' + index).click()
        // $('#whole' + index).click()
      },
      previewImg (index, id) {
        console.log(id)
        var _this = this;
        var file = $('#whole' + index)[0].files[0]
        var reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = function () {
          document.getElementById('img' + index).src = this.result
          var formData = new FormData($('#form')[0])
          formData.append('project_id', id)
          $.ajax({
            type: 'post',
            url: '/api/upload_project_cover',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
              console.log(data)
            }
          })
          // _this.$http.post('http://47.98.188.88:8000/api/upload_project_cover',{ formData },{ contentType: false },{ processData: false }).then((res) => {
          //   console.log(res)
          // }).catch((error) => {
          //   console.log(error)
          // })
        }
      },
      collect (index) {
        // if(!this.$store.state.listData[index].isCollect){
        //   this.$store.state.listData[index].isCollect = true
        // }else {
        //   this.$store.state.listData[index].isCollect = false
        // }
      }
    },
    computed: {

    }
  }
</script>

<style scoped>
  #list {
    width: 100%;
    background: #fff;
  }
  .title {
    height: 40px;
    padding: 0 12px;
    border-top: 1px solid #fff;
    line-height: 42px;
  }
  .title:before {
    content: '';
    display: inline-block;
    width: 2px;
    box-shadow: 0 0 1px #2175BB;
    height: 14px;
    background: #2175BB;
    vertical-align: middle;
    margin: -3px 6.5px 0 0;
  }
  #list .weui-media-box {
    height: 90px;
    padding: 12px;
    border-top: 1px solid #DDD;
    box-sizing: border-box;
  }
  .weui-media-box__hd {
    width: 66px;
    height: 66px;
  }
  #list .weui-media-box__bd {
    height: 66px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }
  #list .weui-panel__bd .weui-media-box__hd img {
    width: 66px;
    height: 66px;
  }
  #list .collect {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    line-height: 15px;
  }
  .collect_word {
    padding-left: 10px;
    font-size: 14px;
    color: #2175BA;
    white-space: nowrap;
  }
  #list .weui-media-box__title {
    font-size: 15px;
    color: #333333;
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
  #list .company_name {
    font-size: 13px;
    color: #444444;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
  #list .stateBtn {
    display: flex;
    flex-direction: row;
  }
  .warn {
    float: left;
    width: 45px;
    height: 20px;
    line-height: 20px;
    border-radius: 4px;
    background: #e8e9eb;
    color: #1F2022;
    margin-right: 10px;
    font-size: 12px;
    text-align: center;
    position: relative;
  }
  .alert {
    background: #F66061;
    color: white
  }
  .alert:after {
    content: '12';
    text-align: center;
    line-height: 15.5px;
    font-weight: bold;
    color: #fff;
    font-size: 12px;
    display: block;
    width: 15.5px;
    height: 15.5px;
    border-radius: 50%;
    background: #F76060;
    position: absolute;
    top: -8px;
    right: -8px;
  }
</style>
