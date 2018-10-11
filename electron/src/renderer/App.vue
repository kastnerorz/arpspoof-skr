<template>
  <div id="app">
    <el-menu :default-active="$route.path" class="el-menu-demo" mode="horizontal" router>
      <el-menu-item index="/" route="/">Poison</el-menu-item>
      <el-menu-item index="/mon" route="/mon">Monitor</el-menu-item>
      <el-menu-item index="/packet_capture" route="/packet_capture">Packet Capture</el-menu-item>
    </el-menu>
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'arp-electron'
  }
</script>

<style>
  /* CSS */
</style>
