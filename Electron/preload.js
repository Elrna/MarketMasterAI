const { contextBridge, ipcRenderer } = require('electron');
const fs = require('fs');

contextBridge.exposeInMainWorld(
    "electronAPI", {
        readJsonFile: (filePath, callback) => ipcRenderer.invoke('read-json-file', filePath).then(callback)
    }
);

async function readJsonFile(filePath) {
    try {
        return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    } catch (err) {
        console.error('Failed to read or parse JSON file', err);
        throw err;
    }
}

// contextBridgeを使用してレンダラープロセスに公開
contextBridge.exposeInMainWorld('electronAPI', {
    readJsonFile: readJsonFile
});