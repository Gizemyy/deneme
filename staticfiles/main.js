
console.log('helloooo')

const socket = io('http://127.0.0.1:8000/')


socket.on('welcome', msg=>{
    console.log(msg)
})