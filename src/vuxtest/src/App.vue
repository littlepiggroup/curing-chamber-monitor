<template>
  <div id="app">
    <x-header class="head" :left-options="{preventGoBack: true}" @on-click-back="back" :right-options="{showMore: true}" @on-click-more="showPerson">四建养护室智慧监测系统</x-header>
    <div class="top" v-show="!(($store.state.routerName == 'Details') || ($store.state.routerName == 'PersonData'))">
      <img class="system_bg" src="src/assets/images/bg.png" alt="">
      <Nav :class="this.$store.state.routerName != 'Collect'?'':'bottomRadius'"></Nav>
      <Screen v-show="this.$store.state.routerName == 'Overview' || this.$store.state.routerName == 'ItemList' || this.$store.state.routerName == 'AppRating'"></Screen>
    </div>
    <div class="scrollArea">
      <keep-alive>
        <router-view class="router"></router-view>
      </keep-alive>
    </div>
  </div>
</template>
<script>
  import Nav from '@/components/Nav'
  import Screen from '@/components/Screen'
export default {
  name: 'app',
  data: function () {
    return ({

    })
  },
  mounted () {

  },
  components: {
    Nav,
    Screen
  },
  methods: {
    back () {
      this.$store.state.routerName = this.$store.state.router_Parent
      $('.vux-button-group a').removeClass('vux-button-group-current')
      $('.vux-button-group a').eq(this.$store.state.navIndex).addClass('vux-button-group-current')
      this.$router.push({path: '/' + this.$store.state.router_Parent})
    },
    showPerson () {
      this.$store.state.routerName = 'PersonData'
      this.$router.push({path: '/' + this.$store.state.routerName})
    }
  },
  computed: {

  }
}
</script>
<style>
*{
  margin: 0;
  padding: 0;
  -webkit-text-size-adjust:none;
}
#app {
  height: 100vh;
  font-family: PingFangSC-Regular, sans-serif;
  display: flex;
  flex-direction: column;
}
.top {
  display: flex;
  flex-direction: column;
}
.scrollArea {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.system_bg {
  width: 100%;
  background: red;
  margin-bottom: -12px;
}
.vux-header {
  background: #3B3B3B!important;
}
.vux-header .vux-header-left .left-arrow:before {
  border-color: #fff!important;
}
.vux-header .vux-header-left .vux-header-back {
  font-size: 17px;
  color: #fff;
}
.vux-header .vux-header-right .vux-header-more:after {
  content: url("assets/images/person.png")!important;
}
#app .vux-header-title {
  font-size: 17px;
}
.router {
  margin-top: 6px;
  width: 100%;
  overflow: hidden;
  overflow-y: scroll;
}
.bottomRadius {
  /*border-bottom-right-radius: 10px;*/
  /*border-bottom-left-radius: 10px;*/
  border-radius: 10px;
  box-shadow: 0 9px 9px rgba(0,0,0,0.16);
}
</style>
