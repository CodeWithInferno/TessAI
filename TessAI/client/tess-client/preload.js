// // preload.js
// const { contextBridge, ipcRenderer } = require("electron")

// // Expose protected methods that allow the renderer process to use
// // the ipcRenderer without exposing the entire object
// contextBridge.exposeInMainWorld("electronAPI", {
//   sendChat: (message) => {
//     console.log("preload.js: Sending message to main process:", message)
//     return ipcRenderer.invoke("chat-message", message)
//   },
// })

const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  sendChat: (message) => ipcRenderer.invoke('chat-message', message),
  sendAction: (action) => ipcRenderer.invoke('tess-action', action)
})
