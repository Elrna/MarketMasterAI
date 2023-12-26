const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');
const { spawn } = require('child_process');


let subprocess;

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
  mainWindow.webContents.openDevTools();
}

ipcMain.on('request-csv-data', (event) => {
  const csvFilePath = path.join('D:/MarketMasterAI/Def/BTCUSDT_5T.csv');
  const results = [];

  const jst = new Date().toLocaleString({ timeZone: 'Asia/Tokyo' });
  const jstFate = new Date(jst);
  const formatJST = formatDate(jstFate);



  let targetData = null;

  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on('data', (data) => {
      results.push(data);
    })
    .on('end', () => {
      
      let lastData = results[results.length -1];
      let targetData;
      
      results.forEach((data) => {
        if(data.timestamp &&  data.timestamp.startsWith(formatJST)){
          targetData = data;
        }
      });
      /*
      if(results.timestamp.startsWith(formatJST)){
        targetData = data;
        console.log('targetData: ', targetData);
      }
      */
      event.reply('csv-data-response', {
        lastClose: results ? lastData : 'No data found',
        targetData: targetData ? targetData : 'No data found'
      });
    })
    .on('error', (err) => {
      console.log('CSV読み込みエラー: ', err);
      event.reply('csv-data-error', 'CSV読み込みエラー');
    });

});

app.whenReady().then(() => {
  //runExe('D:/MarketMasterAI/bin/getPrice_BTCUSDT_ochlv.exe');
  createWindow();
});

app.on('window-all-closed', function () {
  // macOS以外では、ユーザーがCmd + Qで明示的に終了するまでアプリをアクティブに保つ
  if (process.platform !== 'darwin') {
    app.quit();
  }
});


// アプリケーションがアクティブになったとき（macOSのみ）
app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

function runExe(filePath){
    // 非同期処理で子プロセスを起動
    const child = spawn(filePath);
    console.log('exe prosecc start.');

    child.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });
  
    child.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
  
    child.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  
    child.on('error', (err) => {
      console.error('Failed to start subprocess.', err);
    });
}

function runExeSync(filePath){
  const result = spawn(filePath, {encoding: 'utf-8'});

  if(result.stdout){
    console.log('stdout: ', result.stdout);
  }

  if(result.stderr){
    console.log('stderr: ', result.stderr);
  }

  if(result.error){
    console.log('error: ', result.error);
  }

  return result.status;

}

// フォーマットを'YYYY/MM/DD HH:MM'形式に変換する関数
function formatDate(date) {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');

  return `${year}/${month}/${day} ${hours}:${minutes}`;
}