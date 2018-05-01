<template>
  <div id="detail">
    <div class="bg">
      <div class="mask">
        <img class="logo" src="src/assets/images/logo.png" alt="">
        <div class="word">
          <h1>上海市轨道指挥交通大楼</h1>
          <div class="c_name">第X工程公司</div>
        </div>
        <div class="show">
          <div class="monitoring video"><i class="iconfont icon-shipin"></i>视频监控</div>
          <div class="monitoring temperature"><i class="iconfont icon-iconset0480"></i>温度26℃</div>
          <div class="monitoring humidity"><i class="iconfont icon-shidu"></i>湿度25%</div>
          <div class="monitoring test_piece"><i class="iconfont icon-ceshi"></i>试件监控</div>
        </div>
      </div>
    </div>
    <div id="main"></div>
    <div class="alertList">
      <div v-transfer-dom>
        <confirm v-model="show" title="处理描述" @on-cancel="onCancel" @on-confirm="onConfirm">
          <p style="text-align:center;">Are you sure</p>
        </confirm>
      </div>
      <Table :data="tableData" :columns="tableColumns" border class="kkk"></Table>
      <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
          <Page :total="100" :current="1" @on-change="changePage"></Page>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  require('iview/src/styles/index.less')
  import {Confirm, TransferDomDirective as TransferDom } from 'vux'
  import { Table, Tag, Page } from 'iview'
  const echarts = require('echarts/lib/echarts')
  export default {
    name: 'detail',
    directives: {
      TransferDom
    },
    components: {
      Confirm,
      Table,
      Tag,
      Page
    },
    data: function () {
      return ({
        date: [],
        data1: [],
        data2: [],
        show: false,
        tableData: this.mockTableData(),
        tableColumns: [
          {
            title: '报警类型',
            key: 'alert'
          },
          {
            title: '报警描述',
            key: 'description'
          },
          {
            title: '时间',
            key: 'time',
            render: (h, params) => {
              return h('div',{
                style: {
                  width: '100%',
                  padding: '0px!important'
                }
              }, this.formatDate(this.tableData[params.index].time));
            }
          },
          {
            title: '处理',
            key: 'status',
            render: (h, params) => {
              const _this = this;
              const row = params.row;
              const color = row.status === 1 ? 'blue' : row.status === 2 ? 'green' : 'red';
              const text = row.status === 1 ? '处理中' : row.status === 2 ? '已处理' : '未处理';
              return h(Tag, {
                props: {
                  type: 'dot',
                  color: color
                },
                style: {
                  display: 'flex',
                  flexDirection: 'row',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '100%',
                  border: '0px!important',
                  padding: '0px'
                },
                nativeOn: {
                  click: function () {
                    _this.show = true
                  }
                }
              }, text);
            }
          }]
      })
    },
    created () {
      this.$store.state.routerName = 'Details'
      this.$http.get('/api/project_sensor_data_series?project_id=1&sensor_id=1&time_range=last_week').then((res) => {
        var data = res.data.results
        for(var i = 0; i < data.length; i++){
          this.date.push(data[i].collect_time.split('T').join(' '))
          this.data1.push(data[i].temperature)
          this.data2.push(data[i].humidity)
          this.drawLine()
        }
      }).catch((error) => {
        console.log(error)
      })
    },
    mounted () {

    },
    methods: {
      mockTableData () {
        let data = [];
        for (let i = 0; i < 10; i++) {
          data.push({
            alert: '试件报警',
            status: Math.floor(Math.random () * 3 + 1),
            description: '描述',
            time: new Date()
          })
        }
        return data;
      },
      formatDate (date) {
        const y = date.getFullYear();
        let m = date.getMonth() + 1;
        m = m < 10 ? '0' + m : m;
        let d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        return y + '-' + m + '-' + d;
      },
      changePage () {
        // The simulated data is changed directly here, and the actual usage scenario should fetch the data from the server
        this.tableData = this.mockTableData();
      },
      showPlugin () {
        console.log(111)
        this.show = true
      },
      onCancel () {
        console.log('取消')
      },
      onConfirm () {
        console.log('确认')
      },
      drawLine () {
        var myChart = echarts.init(document.getElementById('main'))
        var option = {
          title: {
            left: 'left',
            text: '数据图表',
            textStyle: {
              color: '#575757',
              fontWeight: 100,
              fontSize: 16
            }
          },
          legend: {
            orient: 'horizontal',
            right: 10
          },
          // dataZoom: [{
          //   type: 'slider',
          //   start: 0,
          //   end: 10,
          //   bottom: -10
          // }],
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            axisLine: {
              lineStyle: {
                // color: '#EB6D6C',
                // width: 2,
                // onZero: false
              }
            },
            axisLabel: {
              formatter: function (value, index) {
                return value.split(' ')[0] + '\n' + value.split(' ')[1]
              },
              color: '#A8AAAF'
            },
            data: this.date
          },
          yAxis: [{
            type: 'value',
            name: '温度',
            // min: 18,
            // max: 22,
            axisLabel: {
              formatter: '{value}℃'
            }
          }, {
            type: 'value',
            name: '湿度',
            // min: 0.9,
            // max: 1,
            splitNumber: 2,
            axisLabel: {
              rotate: -45,
              formatter: function (value) {
                return value + '%'
              }
            }
          }],
          series: [{
            type: 'line',
            name: '温度',
            symbol: 'circle',
            showSymbol: false,
            lineStyle: {
              color: '#C23531'
            },
            // areaStyle: {
            //   color: '#D2E9B9'
            // },
            data: this.data1
          }, {
            type: 'line',
            name: '湿度',
            symbol: 'circle',
            showSymbol: false,
            yAxisIndex: 1,
            lineStyle: {
              color: '#539FFF'
            },
            data: this.data2
          }]
        }
        myChart.setOption(option)
      }
    }

  }
</script>

<style scoped>
  #detail {
    margin-top: -6px;
  }
  #detail .bg{
    display: flex;
    flex-direction: column;
    height: 182px;
    background: url("../assets/images/block2.jpg") 0/100% 100% no-repeat;
    box-sizing: border-box;
  }
  .mask {
    height: 182px;
    background: linear-gradient(to top, rgba(0,0,0,0.5),rgba(255,255,255,0.1));
  }
  .logo {
    width: 32.5px;
    margin: 25px 0 0 20px;
  }
  .word {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  h1 {
    font-size: 24px;
    color: #fff;
    font-weight: 200;
  }
  .c_name {
    width: 160px;
    font-size: 18px;
    color: #fff;
    text-align: center;
    font-weight: 600;
    border-top: 1px solid #fff;
  }
  .show {
    display: flex;
    flex-direction: row;
    margin-top: 20px;
  }
  .monitoring {
    width: 25%;
    color: #fff;
    border-right: 1px solid #fff;
    text-align: center;
  }
  .monitoring:nth-last-child(1) {
    border: 0;
  }
  .iconfont {
    margin-right: 3px;
  }
  #main {
    display: flex;
    height: calc(100vh - 220px);
    align-items: center;
    justify-content: center;
  }
  .aaa {
    margin-top: 80px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  table th {
    font-weight: 100;
  }
  table tr {
    text-align: center;
  }
  table td {
    height: 30px;
  }
  .icon-weichuligaojing {
    color: red;
    font-size: 20px;
  }
</style>
<style>

</style>
