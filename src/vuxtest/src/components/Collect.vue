<template>
    <div>
      <list></list>
    </div>
</template>

<script>
  import List from '@/components/List'
  export default {
    name: 'collect',
    components: {
      List
    },
    created () {
      this.$store.state.routerName = 'Collect'
    }
  }
</script>

<style scoped>

</style>
