<template>
  <div id="wrapper">
    <div class="block">
      <button @click="getInfo">进行扫描</button>
      <div v-for="item in list" :key="item.index">
        <p>{{ item.ip }}</p>
      </div>
    </div>
    <div class="block">
      <button @click="attack">攻击&欺骗</button>
      <p class="item-width">要攻击的IP:</p><input class="item-width" placeholder="请输入要攻击的ip"/>  
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'landing-page',
    data () {
      return {
        list: []
      }
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      getInfo () {
        axios.get('https://www.easy-mock.com/mock/5baadd26cff4974b9da470ce/getip').then((res) => {
          console.log(res.data)
          this.list = res.data
        }).catch((err) => {
          console.log(err)
        })
      },
      attack () {
        console.log('attack')
      }
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body { font-family: 'Source Sans Pro', sans-serif; }

  #wrapper {
    background:
      radial-gradient(
        ellipse at top left,
        rgba(255, 255, 255, 1) 40%,
        rgba(229, 229, 229, .9) 100%
      );
    height: 100vh;
    padding: 40px 40px;
    width: 100vw;
  }

  .block {
    padding-bottom: 20px;
  }

  .item-width {
    width: 140px;
    float: left;
  }
  button {
    font-size: .8em;
    cursor: pointer;
    outline: none;
    padding: 0.75em 2em;
    border-radius: 2em;
    display: inline-block;
    color: #fff;
    background-color: #4fc08d;
    transition: all 0.15s ease;
    box-sizing: border-box;
    border: 1px solid #4fc08d;
  }

  button.alt {
    color: #42b983;
    background-color: transparent;
  }
</style>
