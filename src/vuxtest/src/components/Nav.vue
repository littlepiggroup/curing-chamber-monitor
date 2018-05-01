<template>
  <div id="nav">
    <button-tab>
      <button-tab-item @on-item-click="select('Overview')" selected><img class="icon" src="src/assets/images/overView.png" alt="">概览</button-tab-item>
      <button-tab-item @on-item-click="select('ItemList')"><img class="icon" src="src/assets/images/listMenu.png" alt="">项目列表</button-tab-item>
      <button-tab-item @on-item-click="select('AppRating')"><img class="icon" src="src/assets/images/appRank.png" alt="">应用评比</button-tab-item>
      <button-tab-item @on-item-click="select('Collect')"><img class="icon" src="src/assets/images/collect.png" alt="">收藏</button-tab-item>
    </button-tab>
  </div>
</template>

<script>
  export default {
    name: 'navs',
    data: function () {
      return ({

      })
    },
    methods: {
      select (url) {
        this.$store.state.router_Parent = url
        this.$store.state.routerName = url
        this.$router.push({path: '/' + url})
        switch (url) {
          case 'Overview':
            this.$store.state.navIndex = 0
            break
          case 'ItemList':
            this.$store.state.navIndex = 1
            break
          case 'AppRating':
            this.$store.state.navIndex = 2
            break
          case 'Collect':
            this.$store.state.navIndex = 3
            break
        }
      }
    }
  }
</script>

<style scoped>
  /*标签button-tab会被转换成div且class名为vux-button-group*/
  /*标签button-tab-item会被转换成a且class名为vux-button-group，selected属性会给标签添加.vux-button-group-current类名*/
  #nav {
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid lightgray;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    background: #fff;
    overflow: hidden;
  }
  .vux-button-group {
    display: flex;
    flex-direction: row;
    flex: 1;
  }
  a {
    color: white;
    background: #fff;
  }
  .vux-button-tab-item {
    padding: 10px 0;
  }
  .vux-button-group > a.vux-button-tab-item {
    border-radius: 0;
    width: 25%;
  }
  .vux-button-group > a.vux-button-tab-item:after {
    border: 0;
  }
  .icon {
    vertical-align: middle;
    margin: -4px 4px 0 0;
  }
</style>
