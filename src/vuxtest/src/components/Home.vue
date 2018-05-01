<template>
    <div id="home">
      <h1>四建养护室智慧监测系统</h1>
      <x-button type="primary" link="/Index" class="login">登录</x-button>
    </div>
</template>

<script>
  export default {
    name: 'home'
  }
</script>

<style scoped>
  #home {
    height: 100vh;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background: skyblue;
  }
  h1 {
    margin: 0;
    font-size: 20px;
    color: white;
    padding-top: 200px;
  }
  #home .login {
    width: 50%;
    margin-top: 50px;
  }
</style>
