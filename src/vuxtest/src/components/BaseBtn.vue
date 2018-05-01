<template>
  <div id="basebtn">
    <div class="index" @click="returnIndex">
      <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1522401130874&di=1bce39a220bba632cce742b374303b46&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F015f8b58b8d31fa801219c77c609e1.png" alt="">
      <p>home</p>
    </div>
    <div class="exit" @click="exitSever">
      <img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1522403054138&di=88678b3862486ec947612c435a19c93f&imgtype=jpg&src=http%3A%2F%2Fimg0.imgtn.bdimg.com%2Fit%2Fu%3D1766748270%2C2876835116%26fm%3D214%26gp%3D0.jpg" alt="">
      <p>exit</p>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'base-btn',
    methods: {
      returnIndex () {
        this.$router.push({path: '/Index'})
      },
      exitSever () {
        this.$router.push({path: '/'})
      }
    }
  }
</script>

<style scoped>
  #basebtn {
    position: fixed;
    width: 100%;
    display: flex;
    flex-direction: row;
    background: rgba(220,220,220,0.9);
    color: white;
    bottom: 0;
    z-index: 999;
  }
  .index,.exit {
    display: flex;
    flex:1;
    flex-direction: column;
    align-items: center;
  }
  img {
    width: 30px;
    height: 30px;
  }
</style>
