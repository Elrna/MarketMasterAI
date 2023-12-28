const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');
const { spawn } = require('child_process');
const axios = require('axios');
const { request } = require('http');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    }
  });

  mainWindow.loadFile('index.html');
  mainWindow.maximize();

}

// BTCUSDTの現在価格を取得する関数
async function getCurrentPrice() {
  try {
    var response = await axios.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
    return response.data.price;
  } catch (error) {
    console.error('価格の取得に失敗:', error);
  }
}

// BTCUSDTの24時間前の価格を取得する関数
async function getPreviousPrice() {
  try {
    var endTime = Date.now();
    var startTime = endTime - 86400000;

    var response = await axios.get(`https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime=${startTime}&endTime=${endTime}`);
    var previousDayData = response.data[0];
    return previousDayData[1];
  } catch (error) {
    console.error('前日価格の取得に失敗:', error);
  }
}

ipcMain.on('request-current-price', async (event) => {
  var currentPrice = await getCurrentPrice();
  var previousPrice = await getPreviousPrice();
  var change = 0;

  if (currentPrice && previousPrice) {
    change = ((currentPrice - previousPrice) / previousPrice) * 100;
  }

  console.log('currentPrice: ', currentPrice);
  console.log('previousPrice: ', previousPrice);
  console.log('before raito: ', change);


  event.reply('current-price',{
    currentPrice: currentPrice,
    previousPrice: previousPrice,
    beforeRaito: change
  });
});

ipcMain.on('request-csv-data', (event) => {
  const csvFilePath = path.join('D:/MarketMasterAI/Def/BTCUSDT_5T.csv');
  const results = [];

  const jst = new Date().toLocaleString({ timeZone: 'Asia/Tokyo' });
  const jstFate = new Date(jst);
  const formatJST = formatDate(jstFate);

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

ipcMain.on('request-indicators-data', (event) => {
  const filePath = path.join('D:/MarketMasterAI/bin/Technical.json');
  
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading indicators file:', err);
      event.reply('response-indicators-data', { error: 'ファイル読み込みエラー' });
    } else {
      event.reply('response-indicators-data', JSON.parse(data));
    }
  });
});

app.whenReady().then(() => {
  //runExe('D:/MarketMasterAI/bin/getPrice_BTCUSDT_ochlv.exe');
  createWindow();
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
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