<template>
  <div id="persondata">
    <div class="bg">
      <div class="headerPic"></div>
    </div>
    <div class="name">
      <div class="login_name">
        <p>登录名:</p>
        <p>15000852554</p>
      </div>
      <div class="real_name">
        <p>真实姓名:</p>
        <p>邱嘉</p>
      </div>
    </div>
    <div class="tel">
      <p>电话:</p>
      <p>15000852554</p>
    </div>
    <div class="department">
      <p>所属部门:</p>
      <p>筑众科技</p>
    </div>
    <div class="exit">退出登录</div>
  </div>
</template>

<script>
  export default {
    name: 'person-data',
    data: function () {
      return ({

      })
    }
  }
</script>

<style scoped>
#persondata {
  display: flex;
  flex-direction: column;
  flex: 1;
  background: #EAEAEA;
  margin-top: -4px;
}
  .bg {
    height: 180px;
    background: url("../assets/images/block3.jpg") 0/100% no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .headerPic {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    border: 2px solid #fff;
    background: url("../assets/images/block3.jpg") center/200% no-repeat;
  }
  .login_name, .real_name, .tel, .department, .exit {
    font-size: 14px;
    font-weight: 600;
    display: flex;
    flex-direction: row;
    background: #fff;
    padding: 10px 15px;
    justify-content: space-between;
  }
  #persondata p:nth-of-type(even) {
    color: #888888;
    font-weight: normal;
  }
  .exit {
    display: flex;
    justify-content: center;
    color: #D7545A;
    letter-spacing: 1px;
    font-size: 15px;
  }
  .name, .tel, .department, .exit {
    margin-top: 12px;
  }
</style>
