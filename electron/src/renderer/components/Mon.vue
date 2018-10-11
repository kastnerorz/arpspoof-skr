<template>
  <div>
    <el-container>
        <el-aside width="200px">
          <el-row type="flex" justify="center">
            <el-col :span="18">
              <el-form label-position="top">
                <el-form-item label="Subnet">
                  <el-input v-model="subnet"></el-input>
                </el-form-item>
                <el-form-item >
                  <el-button @click="initMonitor">Init Monitor</el-button>
                </el-form-item>
                <el-form-item >
                  <el-button @click="startMonitor">Start Monitor</el-button>
                </el-form-item>
                <el-form-item >
                  <el-button @click="setColor">Start Monitor</el-button>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
          
        </el-aside>
        <el-main>
          <div class="card-wrapper">
            <el-row :gutter="4">
              <el-col :span="6" v-for="host in hosts" :key="host.mac" style="margin-bottom:10px;">
                <el-card class="card" :style="{ backgroundColor: changeColor(host.status) }" >
                  <div>Host: {{ host.host }}</div>
                  <div>Mac: {{ host.mac }}</div>
                </el-card>
              </el-col>
            </el-row>
              
          </div>
        </el-main>
      </el-container>
  </div>
</template>

<script>
import * as shell from '../shell'
export default {
  name: 'monitor',
  data () {
    return {
      subnet: '',
      exitMonitor: false,
      hosts: [],
      logs: []
    }
  },
  methods: {
    async initMonitor () {
      this.hosts = []
      this.exitMonitor = false
      if (this.subnet === '') {
        this.$message.error('Subnet should not be blank!')
        return
      }
      let res = await shell.getAllHost(this.subnet)
      for (let i = 0, len = res.length; i < len; i++) {
        this.hosts.push({
          'status': 0,
          'host': res[i].host,
          'mac': res[i].mac
        })
      }
      this.logs = await shell.getLogs()

      // while (!this.exitMonitor) {
      //   let rl = shell.streamFile('201308.log')
      //   rl.on('line', function (line) {
      //     let req = line.split(' ')
      //     this.setColor(req[1], req[0])
      //   })
      // }
    },
    startMonitor () {
      while (true) {
        this.$set(this.hosts[Math.ceil(Math.random() * 100)], 'status', Math.ceil(Math.random() * 2))
      }
    },

    sleep (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    changeColor (status) {
      console.log('change')
      console.log(status)
      if (status === 0) {
        return '#fff'
      } else if (status === 1) {
        return '#67C23A'
      } else if (status === 2) {
        return '#F56C6C'
      }
    },
    async setColor (ip, type) {
      let index = 0
      for (let i = 0, len = this.hosts.length; i < len; i++) {
        console.log(1, this.hosts[i].host, ip)
        if (this.hosts[i].host === ip) {
          console.log(1, this.hosts[i].ip, ip)
          index = i
          this.$set(this.hosts[i], 'status', type)
        }
      }
      await this.sleep(2000)
      this.$set(this.hosts[index], 'status', 0)
    }
  }
}
</script>

<style scoped>
.card-wrapper {
  display: flex;
  flex-direction: row
}
</style>


