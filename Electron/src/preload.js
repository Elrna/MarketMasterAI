<<<<<<< HEAD
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendData: (channel) => {
    ipcRenderer.send(channel);
  },
  receiveData: (channel, func) => {
    ipcRenderer.on(channel, (_, data) => func(data));
  }
});
=======
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendData: (channel) => {
    ipcRenderer.send(channel);
  },
  receiveData: (channel, func) => {
    ipcRenderer.on(channel, (_, data) => func(data));
  }
});
>>>>>>> 7c0f11edcfe2c5065551d8214761ecb4cc2be555
