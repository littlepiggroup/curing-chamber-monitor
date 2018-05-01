<template>
    <div id="companyList">
      <group title="公司列表">
        <cell :title="i.GSGC"  is-link v-for="(i,index) in companys" :key="index" @click.native="showPrj">
          <div class="badge-value">
            <span class="vertical-middle"></span>
            <badge :text="i.PrjNum"></badge>
          </div>
        </cell>
      </group>
    </div>
</template>

<script>
  const axios = require('axios')
  export default {
    name: 'company-list',
    data: function () {
      return ({
        companys: [
          {
            GSGC: '市政工程公司',
            PrjNum: 5
          },
          {
            GSGC: '市政工程公司',
            PrjNum: 5
          }]
      })
    },
    mounted () {
      // axios.get('/api/building_companies')
      //   .then(function(response){
      //     console.log(response);
      //   })
      //   .catch(function(err){
      //     console.log(err);
      //   });
    },
    methods: {
      showPrj () {
        this.$router.push({path: '/List'})
      }
    }
  }
</script>

<style>
  #companyList .weui-cells__title {
    color: black;
    font-size: 16px;
    font-weight: bold;
  }
  #companyList .weui-cells {
    background: #EEEEEE;
  }
  .weui-cell {
    border: 1px solid lightgray;
    margin-bottom: 10px;
    box-shadow: 0 1px 1px gray;
    background: white;
  }
  .vux-label{
    color: darkslategray;
  }
  .badge-value .vux-badge {
    background: #0bdb44;
  }
  .badge-value {
    display: inline-block!important;
  }
  .vertical-middle {
    vertical-align: middle;
  }
</style>
