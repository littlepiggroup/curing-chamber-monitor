<template>
    <div id="screen">
      <div class="name">{{changeWord}}</div>
      <div class="selector">
        <!--<search placeholder="搜索项目名" :autoFixed="false" on-change=""></search>-->
        <select @change="choose1" class="unit" name="单位">
          <option value ="" disabled selected>单位</option>
          <option v-for="i in unitList" :value="i.key">{{ i.value }}</option>
        </select>
        <!--<popup-picker  title="显示值" :data="['我不会影响遮罩层'.split('')]" v-model="value6"></popup-picker>-->
        <select v-show="$store.state.routerName == 'Overview' || $store.state.routerName == 'AppRating'" @change="choose2"  class="time" name="时间">
          <option value ="" disabled selected>时间</option>
          <option v-for="i in timeList" :value="i.key">{{ i.value }}</option>
        </select>
        <select v-show="$store.state.routerName == 'Details'" @change="choose3"  class="sensor" name="传感器">
          <option value ="" disabled selected>传感器</option>
          <option v-for="i in sensorList" :value="i.key">{{ i.value }}</option>
        </select>
      </div>
    </div>
</template>

<script>
  const echarts = require('echarts/lib/echarts')
  export default {
    name: 'screen',
    data: function () {
      return ({
        unitList: [],
        timeList: [{key: 'last_day', value: '过去一天'}, {key: 'last_week', value: '过去一周'}, {key: 'last_month', value: '过去一月'}],
        sensorList: [1, 2],
        left_word: '筛选',
        unit: null,
        time: null,
        sensor_id: null
      })
    },
    created () {
      //公司select列表渲染
      this.$http.get('/api/building_companies').then((res) => {
        var data = res.data.results
        for (var i = 0; i < data.length; i++) {
          this.unitList.push({key:data[i].id, value: data[i].name})
        }
      }).catch((error) => {
        console.log(error)
      })
      //传感器select列表
      // this.$http.get('').then((res) => {
      //   var data = res.data.results
      //   sensorList = data
      // }).catch((error) => {
      //   console.log(error)
      // })
    },
    mounted () {

    },
    computed: {
      changeWord () {
        switch (this.$store.state.routerName) {
          case 'Overview':
            $('select').val('')
            this.left_word = '筛选'
            this.$http.get('/api/project_phase_report').then((res) => {
              this.$store.state.listData = res.data.results
            }).catch((error) => {
              console.log(error)
            })
            break
          case 'ItemList':
            $('select').val('')
            this.left_word = '筛选'
            this.$http.get('/api/projects').then((res) => {
              this.$store.state.listData = res.data.results
            }).catch((error) => {
              console.log(error)
            })
            break
          case 'AppRating':
            $('select').val('')
            this.left_word = '本系统应用排行榜'
            this.$http.get('/api/project_score_report?company_id=1&orderby_score_asc=true&time_range=last_month').then((res) => {
              this.$store.state.sortList = res.data.results
            }).catch((error) => {
              console.log(error)
            })
            break
        }
        return this.left_word
      }
    },
    methods: {
      choose1 () {
        this.unit = $('.unit').val()
        this.time = $('.time').val()
        this.$store.state.company_name = $('.unit').find('option:selected').text()
        var url, url2, url3
        switch (this.$store.state.routerName) {
          case 'Overview':
            if (!this.time) {
              //还没选择时间的时候返回的报警项目数据请求地址
              url = '/api/project_phase_report?company_id=' + this.unit
            }else {
              //已经选择时间的时候返回的报警项目数据请求地址
              url = '/api/project_phase_report?company_id=' + this.unit + '&time_range=' + this.time
            }
            this.$http.get(url).then((res) => {
              var data = res.data.results
              var video_alert_count = 0,
                  humidity_alert_count = 0,
                  sample_alert_count = 0,
                  temperature_alert_count = 0,
                  alertAll = 0
              for (var i = 0; i < data.length; i++) {
                video_alert_count += data[i].video_alert_count
                humidity_alert_count += data[i].humidity_alert_count
                sample_alert_count += data[i].sample_alert_count
                temperature_alert_count += data[i].temperature_alert_count
              }
              alertAll += video_alert_count + humidity_alert_count + sample_alert_count + temperature_alert_count
              this.$store.state.pieData[0].alertItem[0].value = temperature_alert_count ? temperature_alert_count : null
              this.$store.state.pieData[0].alertItem[1].value = humidity_alert_count ? humidity_alert_count : null
              this.$store.state.pieData[0].alertItem[2].value = sample_alert_count ? sample_alert_count : null
              this.$store.state.pieData[0].alertItem[3].value = video_alert_count ? video_alert_count : null
              this.$store.state.pieData[0].alertAll = alertAll
              this.drawLine()
              this.$store.state.listData = data
            }).catch((error) => {
              console.log(error)
            })
            break
          case 'ItemList':
            url2 = '/api/projects?company=' + this.unit
            this.$http.get(url2).then((res) => {
              this.$store.state.listData = res.data.results
            }).catch((error) => {
              console.log(error)
            })
            break
          case 'AppRating':
            if (!this.time) {
              url3 = '/api/project_score_report?company_id=' + this.unit +'&time-range=last_month&orderby_score_asc=' + this.$store.state.sort
            }else {
              url3 = '/api/project_score_report?company_id=' + this.unit +'&time-range=' + this.time + '&orderby_score_asc=' + this.$store.state.sort
            }
            this.$http.get(url3).then((res) => {
              this.$store.state.sortLIst = res.data.results
            }).catch((error) => {
              console.log(error)
            })
        }
      },
      choose2 () {
        this.unit = $('.unit').val()
        this.time = $('.time').val()
        this.$store.state.listTitle = $('.time').find('option:selected').text()
        var url, url3
        if (!this.unit) {
          url = '/api/project_phase_report?time_range=' + this.time
        }else {
          url = '/api/project_phase_report?company_id=' + this.unit + '&time_range=' + this.time
        }
        // $('.time').css('width', $('.time option:selected').text().length * 20 + 'px')
        switch (this.$store.state.routerName) {
          case 'Overview':
            this.$http.get(url).then((res) => {
              var data = res.data.results
              var video_alert_count = 0,
                humidity_alert_count = 0,
                sample_alert_count = 0,
                temperature_alert_count = 0,
                alertAll = 0
              for (var i = 0; i < data.length; i++) {
                video_alert_count += data[i].video_alert_count
                humidity_alert_count += data[i].humidity_alert_count
                sample_alert_count += data[i].sample_alert_count
                temperature_alert_count += data[i].temperature_alert_count
              }
              alertAll += video_alert_count + humidity_alert_count + sample_alert_count + temperature_alert_count
              this.$store.state.pieData[0].alertItem[0].value = temperature_alert_count ? temperature_alert_count : null
              this.$store.state.pieData[0].alertItem[1].value = humidity_alert_count ? humidity_alert_count : null
              this.$store.state.pieData[0].alertItem[2].value = sample_alert_count ? sample_alert_count : null
              this.$store.state.pieData[0].alertItem[3].value = video_alert_count ? video_alert_count : null
              this.$store.state.pieData[0].alertAll = alertAll
              this.drawLine()
              this.$store.state.listData = data
            }).catch((error) => {
              console.log(error)
            })
            break
          case 'AppRating':
            if (!this.unit) {
              url3 = '/api/project_score_report?company_id=1&time-range=' + this.time + '&orderby_score_asc=' + this.$store.state.sort
            }else {
              url3 = '/api/project_score_report?company_id=' + this.unit +'&time-range=' + this.time + '&orderby_score_asc=' + this.$store.state.sort
            }
            this.$http.get(url3).then((res) => {
              this.$store.state.sortLIst = res.data.results
            }).catch((error) => {
              console.log(error)
            })
        }
      },
      choose3 () {
        this.time = $('.time').val()
        this.sensor_id = $('.sensor').val()
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
    }

  }
</script>

<style scoped>
  #screen {
    display: flex;
    flex-direction: row;
    padding: 5px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.16);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    justify-content: space-between;
    background: #fff;
  }
  .name {
    font-size: 15px;
    font-weight: bold;
    color: #808080;
    padding: 5px 10px;
    white-space: nowrap;
  }
  .name:before {
    content: '';
    display: inline-block;
    width: 2px;
    box-shadow: 0 0 1px #2175BB;
    height: 14px;
    background: #2175BB;
    vertical-align: middle;
    margin: -2px 6px 0 0;
  }
  /*selector*/
  .selector {
    display: flex;
    flex-direction: row;
    min-width: 150px;
    justify-content: space-around;
  }
  select {
    width: 50px;
    border: 0;
    background: #fff;
    font-weight: bold;
    color: #8F8F8F;
  }
</style>
<style>
  .weui-search-bar__cancel-btn {
    font-size: 14px;
  }
  .weui-search-bar {
    padding: 0;
  }
  .weui-search-bar:before {
    border: 0;
  }
  .weui-search-bar:after {
    border: 0;
  }
</style>
