import Vue from 'vue'
import App from './App'
import components from './component.js'
import router from './router'
import Vuex from 'Vuex'
import Axios from 'axios'
window.$ = require('jquery')
import echarts from 'echarts'
Vue.use(Vuex)
require('vux/src/styles/weui/weui.less')
for (let i in components) {
  Vue.component(i, components[i])
}
var store = new Vuex.Store({
  state:{
    router_Parent: '',
    routerName: 'Overview',
    navIndex: 0,
    timeSelect: '24小时',
    company_id: '',
    listData: [],
    pieData: [{alertItem: [{name: '温度报告', value: null, itemStyle: {color: '#EBD160'}, selected: true}, {name: '湿度报告', value: null, itemStyle: {color: '#58DFE2'}, selected: true}, {name: '试件报告', value: null, itemStyle: {color: '#1ADF8F'}, selected: true}, {name: '视频报告', value: null, itemStyle: {color: '#F66061'}, selected: true}], alertAll: null}],
    company_name: '全部公司',
    project_id: null,
    sort: true,
    sortList: []
  },
  getters:{

  },
  mutations:{

  },
  actions:{

  }
})
Vue.prototype.$http = Axios
// 默认依赖在
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app-box')
