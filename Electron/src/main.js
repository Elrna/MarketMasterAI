const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');
const axios = require('axios');

const jPaths = "D:/MarketMasterAI/Def/Path.json";
var filePaths = [];

app.whenReady().then(() => {

  filePaths = loadFilePathJson();
  createWindow();

});

ipcMain.on('sBTCUSDT-current-price', async (event) => {
  var [currentPrice, previousPrice] = await Promise.all([

    getPriceData('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'),
    getPriceData(`https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&startTime=${Date.now() - 86400000}&endTime=${Date.now()}`)

  ]);

  currentPrice = currentPrice.price;
  previousPrice = previousPrice[0][1];

  event.reply('rBTCUSDT-current-price',{
    currentPrice: currentPrice,
    previousPrice: previousPrice,
  });
});

ipcMain.on('sETHUSDT-current-price', async (event) => {
  var [currentPrice, previousPrice] = await Promise.all([

    getPriceData('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'),
    getPriceData(`https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&startTime=${Date.now() - 86400000}&endTime=${Date.now()}`)

  ]);

  currentPrice = currentPrice.price;
  previousPrice = previousPrice[0][1];

  event.reply('rETHUSDT-current-price',{
    currentPrice: currentPrice,
    previousPrice: previousPrice,
  });
});

ipcMain.on('sXRPUSDT-current-price', async (event) => {
  var [currentPrice, previousPrice] = await Promise.all([

    getPriceData('https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT'),
    getPriceData(`https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1d&startTime=${Date.now() - 86400000}&endTime=${Date.now()}`)

  ]);

  currentPrice = currentPrice.price;
  previousPrice = previousPrice[0][1];

  event.reply('rXRPUSDT-current-price',{
    currentPrice: currentPrice,
    previousPrice: previousPrice,
  });
});

ipcMain.on('sSOLUSDT-current-price', async (event) => {
  var [currentPrice, previousPrice] = await Promise.all([

    getPriceData('https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT'),
    getPriceData(`https://api.binance.com/api/v3/klines?symbol=SOLUSDT&interval=1d&startTime=${Date.now() - 86400000}&endTime=${Date.now()}`)

  ]);

  currentPrice = currentPrice.price;
  previousPrice = previousPrice[0][1];

  event.reply('rSOLUSDT-current-price',{
    currentPrice: currentPrice,
    previousPrice: previousPrice,
  });
});

ipcMain.on('request-indicators-data', (event) => {
  
  const filePath = filePaths.json_paths['Technical'];

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading indicators file:', err);
      event.reply('response-indicators-data', { error: 'ファイル読み込みエラー' });
    } else {
      event.reply('response-indicators-data', JSON.parse(data));
    }
  });
});

ipcMain.on('request-path-list', (event) => {
  event.reply('path-list', filePaths);
});


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});


function loadFilePathJson(){
  try{

    const data = fs.readFileSync(jPaths, 'utf8');
    return JSON.parse(data);

  }catch(error){
    console.error('Error reading indicators file:', error);
    return null;
  }
}

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

async function getPriceData(url) {
  try {
  
    const response = await axios.get(url);

    console.log('価格の取得に成功:', response.data);
    return response.data;
  
  } catch (error) {

    console.error('価格の取得に失敗:', error);

  }
}


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