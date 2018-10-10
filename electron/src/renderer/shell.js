
const exec = require('child_process').exec

export function getAllHost (ipAddr) {
  let res = []
  return new Promise(resolve => {
    let nmapCmd = 'nmap -sP ' + ipAddr + '/24'
    exec(nmapCmd, function (err, stdout, stderr) {
      if (err) {
        console.log('nmap error: ' + stderr)
      } else {
        let arpCmd = 'arp -l -a | grep -v none'
        exec(arpCmd, function (err, stdout, stderr) {
          if (err) {
            console.log('arp error: ' + stderr)
          } else {
            let rows = stdout.split('\n')
            for (let i = 1, len = rows.length; i < len; i++) {
              let cols = rows[i].split(' ')
              cols = cols.filter(col => col !== '')
              if (cols[0] !== ' ') {
                res.push({
                  'host': cols[0],
                  'mac': cols[1]
                })
                resolve(res)
              }
            }
          }
        })
      }
    })
  })
}

const fs = require('fs')
const readline = require('readline')
const Stream = require('stream')

function streamFile (filename) {
  var instream = fs.createReadStream(filename)
  var outstream = new Stream()
  return readline.createInterface(instream, outstream)
}
export function getLogs () {
  let logs = []
  return new Promise(resolve => {
    let rl = streamFile('/Users/kastner/Projects/arpspoof-skr/monitor.log')
    rl.on('line', line => {
      let req = line.split(' ')
      logs.push({
        'type': req[0],
        'src': req[1],
        'dst': req[2]
      })
    })
    resolve(logs)
  })
}
