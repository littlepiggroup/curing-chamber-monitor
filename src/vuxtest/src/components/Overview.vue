<template>
  <div id="overview">
    <div id="main" style="width: 400px;height:400px;">------没有报警项目</div>
    <List></List>
  </div>
</template>
<!--group会被转换成一个大div。1、如果title有值的话会在内部生成两个小div，一个小div类名weui-cells__title，内容就是title的值，一个小div类名weui-cells，这个小div有一个before伪类，作用是生成一条底线
2、如果title没有值的话，会转换成一个大div，在里面生成一个小div,类名为weui-cells vux-no-group-title，伪类同上-->
<!--selector会被转换成div，类名为vux-selector weui-cell weui-cell_select weui-cell_select-after，15px左padding-->
<script>
  // 基于准备好的dom，初始化echarts实例
  import List from '@/components/List'
  const echarts = require('echarts/lib/echarts')
  export default {
    name: '',
    data () {
      return {
        // pieData: [{alertItem: [{name: '温度报告', value: null, itemStyle: {color: '#EBD160'}, selected: true}, {name: '湿度报告', value: null, itemStyle: {color: '#58DFE2'}, selected: true}, {name: '试件报告', value: null, itemStyle: {color: '#1ADF8F'}, selected: true}, {name: '视频报告', value: null, itemStyle: {color: '#F66061'}, selected: true}], alertAll: 0}]
      }
    },
    created () {
      this.$http.get('/api/company_phase_report').then((res) => {
        var data = res.data.results[0]
        console.log(data)
        this.$store.state.pieData[0].alertItem[0].value = data.temperature_alert_count ? data.temperature_alert_count : null
        this.$store.state.pieData[0].alertItem[1].value = data.humidity_alert_count ? data.humidity_alert_count : null
        this.$store.state.pieData[0].alertItem[2].value = data.sample_alert_count ? data.sample_alert_count : null
        this.$store.state.pieData[0].alertItem[3].value = data.video_alert_count ? data.video_alert_count : null
        this.$store.state.pieData[0].alertAll = data.temperature_alert_count + data.humidity_alert_count + data.sample_alert_count + data.video_alert_count
        this.drawLine()
      }).catch((error) => {
        console.log(error)
      })
    },
    mounted () {
      // this.drawLine()
    },
    components: {
      List
    },
    methods: {
      onChange1 (val) {
        console.log(val)
      },
      onChange2 (val) {
        console.log(val)
      },
      drawLine () {
        let myChart = echarts.init(document.getElementById('main'))
        var option = {
          tooltip: {
            trigger: 'item',
            formatter: "{a}<br/>{b}: {c}"
          },
          legend: {
            type: 'plain',
            orient: 'vertical',
            bottom: 20,
            height: 50,
            align: 'left',
            itemWidth: 16,
            itemHeight: 16,
            textStyle: {
              color: '#5C5C5C',
              fontSize: 14
            },
            data: [
              {name: '温度报告', icon: 'roundRect'},
              {name: '湿度报告', icon: 'roundRect'},
              {name: '试件报告', icon: 'roundRect'},
              {name: '视频报告', icon: 'roundRect'}]
          },
          series: [
            {
              name: '报警数',
              type: 'pie',
              radius: ['35%', '55%'],
              center: ['50%', '35%'],
              selectedOffset: 5,
              label: {
                formatter: '{b}: {c}'
              },
              labelLine: {
                length: 0.5
              },
              data: this.$store.state.pieData[0].alertItem,
              itemStyle: {
                emphasis: {
                  shadowBlur: 5,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }, {
              name: '',
              type: 'pie',
              silent: true,
              label: {
                normal: {
                  formatter: '{one|{b}} \n {two|{c}件}',
                  position: 'center',
                  z: 999,
                  emphasis: {
                    show: true,
                    textStyle: {
                      color: 'black',
                      fontSize: '20'
                    }
                  },
                  rich: {
                    one: {
                      color: '#333333',
                      fontSize: 15
                    },
                    two: {
                      color: '#333333',
                      fontSize: 28,
                      lineHeight: 35
                    }
                  }
                }
              },
              avoidLabelOverlap: false,
              radius: ['35%', '45%'],
              center: ['50%', '35%'],
              selectedOffset: 5,
              data: [{name: '24小时报警项目数', value: this.$store.state.pieData[0].alertAll, itemStyle: {color: 'rgba(255,255,255,0.5)'}, selected: true}]
            }
          ]
        }
        myChart.setOption(option);
      }
    },
    computed: {

    }
  }
</script>

<style scope>
  #overview {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #f5f5f5;
  }
  #main {

  }
</style>
