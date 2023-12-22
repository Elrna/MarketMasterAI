const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendData: (channel) => {
    ipcRenderer.send(channel);
  },
  receiveData: (channel, func) => {
    ipcRenderer.on(channel, (_, data) => func(data));
  }
});
