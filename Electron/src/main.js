const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');

function createWindow() {
  // 新しいウィンドウを作成する
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // セキュリティを考慮した設定
      contextIsolation: true, // セキュリティを考慮した設定
      nodeIntegration: false, // セキュリティを考慮した設定

    }
  });

  // index.htmlをロードする
  mainWindow.loadFile('index.html');
  mainWindow.maximize();

  // DevToolsを開く
  //mainWindow.webContents.openDevTools();
}

ipcMain.on('request-csv-data', (event) => {
  const csvFilePath = path.join('D:/MarketMasterAI/Def/BTCUSDT_5T.csv');
  const results = [];
  
  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      event.reply('csv-data-response', results);
    });
  console.log('Read csv completed.');
});

app.whenReady().then(() => {
  createWindow();
});

app.on('window-all-closed', function () {
  // macOS以外では、ユーザーがCmd + Qで明示的に終了するまでアプリをアクティブに保つ
  if (process.platform !== 'darwin') app.quit();
});
