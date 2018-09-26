<template>
  <div id="wrapper">
    <div class="block">
      <button @click="getInfo">查看ARP缓存</button>
      <div v-for="item in list" :key="item.index">
        <p>{{ item.ip }}</p>
      </div>
    </div>
    <div style="width:100%">
      <div class="block" style="width:20%">
        <button @click="attack">攻击&欺骗</button>
        <div style="margin-top:20px;">
          <div class="choose">
            <p class="item-width">IP:</p>
            <input class="input" placeholder="请输入要攻击的ip" v-model="ip"/> 
          </div>
          <div class="choose">
            <p class="item-width">Gateway</p>
            <input class="input" placeholder="请输入网关" v-model="door">
          </div>
          <div class="choose">
            <p class="item-width">Frequency</p>
            <input class="input" placeholder="请输入频率" v-model="frequency"/> 
          </div>
          <div class="choose">
            <p class="item-width">interface</p>
            <input class="input" placeholder="请输入interface" v-model="interface"/>
          </div>
          <div class="choose">
            <p class="item-width">count</p>
            <input class="input" placeholder="请输入count" v-model="count"/>
          </div>
          <div class="choose">
            <p class="item-width">Block network</p>
            <input type="checkbox" style="margin-right:40px" v-model="network"/>
          </div>
        </div>
      </div>
      <div style="width:80%">
        
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'landing-page',
    data () {
      return {
        list: [],
        ip: '',
        door: '',
        count: '',
        frequency: '',
        interface: '',
        network: false
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
    padding-bottom: 30px;
  }

  .choose {
    padding-bottom: 20px;
  }

  .input {
    font: 16px arial,sans-serif;
    line-height: 34px;
    height: 30px !important;
    width: 140px;
    margin-right: 20px;
  }

  .item-width {
    width: 100px;
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
