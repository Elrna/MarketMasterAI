const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendData: (channel, data) => ipcRenderer.send(channel, data),
  receiveData: (channel, func) => {
    ipcRenderer.on(channel, (event, data) => func(data));
  }
});
