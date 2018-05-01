<template>
    <div id="wrap">
      <x-header class="head" :right-options="{showMore: true}" @on-click-more="showMenus = true">四建养护室智慧监测系统</x-header>
      <div class="top" v-show="isOverview">
        <div class="company">
          <img class="logo" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1522750451&di=0ca1481aafbfbbdbd1631bd62983bac2&imgtype=jpg&er=1&src=http%3A%2F%2Fzhuangshi.buildjob.net%2Fmem_logo%2F20138%2F1377653626524.gif" alt="">
          <span class="companyName">上海建工四建集团有限公司</span>
        </div>
        <h1>养护室智慧监测系统</h1>
      </div>
      <Nav @choosename="isIndex"></Nav>
      <router-view></router-view>
    </div>
</template>
<script>
  import Nav from '@/components/Nav'
  export default {
    name: 'index',
    data: function () {
      return ({
        isOverview: true
      })
    },
    components: {
      Nav
    },
    methods: {
      isIndex (val) {
        if (val == 'Overview') {
          this.isOverview = true
        } else {
          this.isOverview = false
        }
      }
    }
  }
</script>

<style>
  #wrap {
    height: 100%;
  }
  #wrap .vux-header .vux-header-title {
    font-size: 14px;
  }
  #wrap .vux-header .vux-header-right .vux-header-more:after {
    content: "\EA01";
    font-size: 16px;
    font-family: weui;
  }
  .top {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #5A92D9;
  }
  .top .company {
    display: flex;
    flex-direction: row;
    align-items: flex-end;
  }
  .top .companyName {
    font-size: 14px;
    line-height: 14px;
    margin-top: 40px;
    color: white;
    font-weight: bold;
  }
  .logo {
    width: 30px;
    height: 30px;
  }
  h1 {
    font-size: 20px;
    font-weight:600;
    letter-spacing: 1px;
    color: white;
    margin-top: 15px;
  }
</style>
