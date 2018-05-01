<template>
  <div id="itemlist">
    <!--<div class="buttons">-->
      <!--<group title="">-->
        <!--<selector placeholder="全部分公司" v-model="value1" title="单位:" :options="plainList1" @on-change="onChange1"></selector>-->
      <!--</group>-->
      <!--<search-->
        <!--@result-click="resultClick"-->
        <!--@on-change="getResult"-->
        <!--:results="results"-->
        <!--v-model="value"-->
        <!--position="absolute"-->
        <!--auto-scroll-to-top top="46px"-->
        <!--@on-focus="onFocus"-->
        <!--@on-cancel="onCancel"-->
        <!--@on-submit="onSubmit"-->
        <!--ref="search"></search>-->
    <!--</div>-->
    <List></List>
  </div>
</template>

<script scope>
  import List from '@/components/List'
  export default {
    name: 'item-list',
    data () {
      return {

      }
    },
    created () {
      this.$store.state.routerName = 'ItemList'
    },
    mouted () {
      this.axiosFn()
    },
    components: {
      List
    },
    methods: {
      onImgError (item, $event) {
        console.log(item, $event)
      },
      onChange1 (val) {
        console.log(val)
      },
      onChange2 (val) {
        console.log(val)
      },
      setFocus () {
        this.$refs.search.setFocus()
      },
      resultClick (item) {
        window.alert('you click the result item: ' + JSON.stringify(item))
      },
      getResult (val) {
        console.log('on-change', val)
        this.results = val ? getResult(this.value) : []
      },
      onSubmit () {
        this.$refs.search.setBlur()
        this.$vux.toast.show({
          type: 'text',
          position: 'top',
          text: 'on submit'
        })
      },
      onFocus () {
        console.log('on focus')
      },
      onCancel () {
        console.log('on cancel')
      },
      axiosFn () {

      }
    }
  }
  function getResult (val) {
    let rs = []
    for (let i = 0; i < 10; i++) {
      rs.push({
        title: `${val}`,
        other: i
      })
    }
    return rs
  }
</script>

<style scoped>
  #itemlist {
    height:100%;
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 10px;
    align-items: center;
  }
  #itemlist .weui-media-box {
    padding: 8px;
    background: white;
    margin-bottom: 3px;
  }
  #itemlist .weui-media-box__bd {
    height: 68px;
  }
  #itemlist .weui-panel__bd .weui-media-box__hd img {
    width: 68px;
    height: 68px;
    min-height: 68px;
  }
  #itemlist .weui-media-box__title {
    font-size: 14px;
    color: #7BA7E0;
    font-weight: bold;
  }
  #itemlist .company_num {
    font-size: 12px;
    color: #A8AAAF;
    font-weight: bold;
  }
  #itemlist .content {
    display: flex;
    justify-content: space-between;
  }
  #itemlist .weui-btn_warn {
    width: 70px;
    font-size: 12px;
    white-space: nowrap;
    padding: 0;
    height: 25px;
    line-height: 25px;
  }
  #itemlist .content .right>div {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  #itemlist .right div span:nth-child(1) {
    padding: 0 5px;
    font-size: 12px;
    color: #A8AAAF;
    font-weight: bold;
  }
  #itemlist .right div span:nth-child(2) {
    font-size: 16px;
    font-weight: bold;
    text-align: right;
  }
  .red {
    color: #EC6A69;
  }
  .green {
    color: #9DD46D;
  }
  #itemlist .buttons {
    display: flex;
    width: 100%;
    flex-direction: row;
    justify-content: space-around;
    padding: 5px 0;
    align-items: center;
  }
  #itemlist .buttons .vux-no-group-title {
    margin-top: 0;
    width: 140px;
    line-height: 30px;
  }
  #itemlist .buttons .weui-cells {
    margin-top: 0;
    font-size: 12px;
    color: #C8C9CC;
    border: 1px solid #A8ABAF;
    border-radius: 10px;
    font-weight: bold;
  }
  #itemlist .buttons .vux-selector.weui-cell_select-after {
    height: 30px;
  }
  #itemlist .buttons .weui-label {
    width: 35px;
  }
  #itemlist .buttons .weui-select {
    width: 90px;
    padding: 0;
    height: 30px;
    line-height: 30px;
    color: #C8C9CC;
    font-weight: bold;
    padding-right: 30px;
  }
  #itemlist .buttons .weui-cell_select .weui-cell__bd:after {
    transform:rotateZ(135deg)
  }

  /*search*/
  #itemlist  {

  }
  #itemlist .buttons .weui-cells {
    border: 0;
  }
</style>
