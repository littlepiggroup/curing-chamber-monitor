<template>
  <div id="apprating">
    <div class="ranking">
      <div class="company_name">{{ $store.state.company_name }}</div>
      <div class="statement" @click="createBB"><i class="iconfont icon-baobiao"></i>生成报表</div>
      <div class="sort" @click="reversefn">
        <img class="reverse" src="src/assets/images/reverse.png" alt="">
        <img class="order" src="src/assets/images/order.png" alt="">
      </div>
    </div>
    <div class="weui-panel__bd">
      <a href="#!/component/cell" class="weui-media-box weui-media-box_appmsg" v-for="(v,index) in $store.state.sortList">
        <div class="weui-media-box__hd">
          <img v-if="index<3" class="medal" :src="'src/assets/images/'+(index+1)+'.png'" alt="">
          <span v-else class="ranking_num">{{index+1}}</span>
        </div>
        <div class="weui-media-box__bd">
          <h4 class="weui-media-box__title">新华医院儿科综合楼项目</h4>
          <p class="weui-media-box__desc">{{v.company_name}}</p>
        </div>
        <div class="score">
          <span class="name">分数</span>
          <span class="number">{{v.score}}</span>
        </div>
      </a>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'app-rating',
    data () {
      return ({

      })
    },
    created () {
      this.$store.state.routerName = 'AppRating'
    },
    components: {

    },
    methods: {
      reversefn () {
        this.$store.state.sort = !this.$store.state.sort
        if(!$('.sort').hasClass('reverse_sort')) {
          $('.sort').addClass('reverse_sort')
        }else {
          $('.sort').removeClass('reverse_sort')
        }
      },
      createBB () {
        this.$http.post('/api/excel_report',{}).then((res) => {
          console.log(res.data.report_url)
          window.location.href = 'http://127.0.0.1:8000/' + res.data.report_url
        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
</script>

<style scoped>
  #apprating {
    display: flex;
    flex-direction: column;
  }
  #apprating .ranking {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    font-size: 14px;
    color: #333333;
    height: 50px;
    line-height: 40px;
    border-top: 0.5px solid #fff;
    padding: 0 12px;
    align-items: center;
  }
  .company_name:before {
    content: '';
    display: inline-block;
    width: 2px;
    height: 14px;
    background: #2175BB;
    box-shadow: 0 0 1px #2175BB;
    vertical-align: middle;
    margin-right: 5px;
    margin-top: -2px;
  }
  .sort {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 5px;
  }
  .order {
    margin-top: 3px;
  }
  #apprating .weui-panel__bd {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
  #apprating .weui-media-box {
    padding: 10px 0;
    border-top: 0.5px solid #DDD;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    color: black!important;
  }
  #apprating .weui-media-box:nth-last-child(1) {
    border-bottom: 0.5px solid #DDD;
  }
  #apprating .weui-media-box__hd {
    height: 30px;
    width: 30px;
    margin: 0 10px 0 10px;
    text-align: center;
    line-height: 30px;
  }
  #apprating .weui-media-box__hd .iconfont {
    font-size: 18px;
  }
  #apprating .medal {
    width: 20px;
  }
  #apprating .weui-media-box {
    color: #989BA1;
    background: #fff;
    margin-bottom: 4px;
  }
  #apprating h4 {
    font-size: 12px;
    font-weight: bold;
    color: black;
  }
  #apprating .weui-media-box__desc {
    color: black;
    font-size: 12px;
  }
  #apprating .score {
    width: 80px;
    display: flex;
    align-items: center;
  }
  #apprating .score .name{
    font-size: 12px;
    color: black;
    font-weight: bold;
    margin-right: 10px;
  }
  #apprating .score .number {
    color: #7CC63C;
    font-weight: bold;
  }
  .reverse_sort {
    transform: rotateZ(180deg);
  }
  .statement {
    background: cornflowerblue;
    color: #fff;
    display: flex;
    width: 100px;
    height: 30px;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-left: 140px;
  }
  .icon-baobiao {
    font-size: 20px;
  }
</style>
